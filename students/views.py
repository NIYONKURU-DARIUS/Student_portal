import time
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Max, Min, Count
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Student
from .forms import StudentForm
from .graph_utils import generate_all_student_graphs
from .decorators import instructor_required


# --- AUTHENTICATION VIEWS ---

def login_view(request):
    """
    Handles user authentication for both Instructors and Students.
    Redirects authenticated users to the student directory or intended URL.
    """
    if request.user.is_authenticated:
        return redirect('student_list')

    redirect_to = request.POST.get('next') or request.GET.get('next') or 'student_list'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(redirect_to)
    else:
        form = AuthenticationForm(request)

    return render(request, 'students/login.html', {
        'form': form,
        'next': redirect_to,
    })


def logout_view(request):
    """Logs out the current user and returns to the login page."""
    logout(request)
    return redirect('login')


# --- APPLICATION VIEWS ---

# 1. READ (List all students) - Accessible by all authenticated users (Students & Instructors)
@login_required
def student_list(request):
    students = Student.objects.all()
    
    # Optional search / filter query
    query = request.GET.get('q', '').strip()
    course_filter = request.GET.get('course', '').strip()

    if query:
        students = students.filter(first_name__icontains=query) | students.filter(last_name__icontains=query) | students.filter(email__icontains=query)
    if course_filter:
        students = students.filter(course=course_filter)

    # Compute high-level metrics for dashboard cards
    total_count = Student.objects.count()
    stats = Student.objects.aggregate(
        avg_grade=Avg('grade'),
        avg_study_hours=Avg('study_hours_per_week'),
        top_grade=Max('grade')
    )
    
    courses = Student.COURSE_CHOICES

    context = {
        'students': students,
        'total_count': total_count,
        'avg_grade': round(stats['avg_grade'], 1) if stats['avg_grade'] else 0,
        'avg_study_hours': round(stats['avg_study_hours'], 1) if stats['avg_study_hours'] else 0,
        'top_grade': round(stats['top_grade'], 1) if stats['top_grade'] else 0,
        'courses': courses,
        'selected_course': course_filter,
        'query': query,
    }
    return render(request, 'students/student_list.html', context)


# 2. CREATE (Register a new student) - Restricted to Instructors and Admins
@instructor_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Register'})


# 3. UPDATE (Edit existing student record) - Restricted to Instructors and Admins
@instructor_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Update'})


# 4. DELETE (Remove student record) - Restricted to Instructors and Admins
@instructor_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


# 5. ANALYTICS & QUICKGRAPHS DASHBOARD - Accessible by Students & Instructors
@login_required
def analytics_dashboard(request):
    students = Student.objects.all()
    graphs_data = None
    
    if students.exists():
        # Generate graphs using quickgraph-darius12
        graphs_data = generate_all_student_graphs()

    # Pass cache-busting timestamp so browser reloads newly generated graphs
    cache_buster = int(time.time())

    context = {
        'total_students': students.count(),
        'graphs_data': graphs_data,
        'cache_buster': cache_buster,
        'avg_grade': students.aggregate(avg=Avg('grade'))['avg'],
        'avg_hours': students.aggregate(avg=Avg('study_hours_per_week'))['avg'],
    }
    return render(request, 'students/analytics.html', context)


# Helper: Load Sample Demo Data - Restricted to Instructors and Admins
@instructor_required
def seed_sample_data(request):
    """Seed initial student records to showcase quickgraphs immediately."""
    if Student.objects.count() == 0:
        samples = [
            ("Alice", "Uwase", "alice.uwase@example.com", "Computer Science", 88.5, 20.0),
            ("Bernard", "Mugisha", "bernard.m@example.com", "Software Engineering", 79.0, 16.5),
            ("Clarisse", "Ingabire", "clarisse.i@example.com", "Data Science", 92.0, 24.0),
            ("David", "Kamanzi", "david.k@example.com", "Cybersecurity", 68.5, 12.0),
            ("Eric", "Habimana", "eric.h@example.com", "Information Technology", 74.0, 14.0),
            ("Fiona", "Iradukunda", "fiona.i@example.com", "Computer Science", 95.0, 26.0),
            ("Gasana", "Patrick", "gasana.p@example.com", "Software Engineering", 82.5, 18.0),
            ("Honorine", "Mutoni", "honorine.m@example.com", "Data Science", 86.0, 21.0),
        ]
        for fn, ln, em, crs, grd, hrs in samples:
            Student.objects.create(
                first_name=fn,
                last_name=ln,
                email=em,
                course=crs,
                grade=grd,
                study_hours_per_week=hrs
            )
    return redirect('student_list')
