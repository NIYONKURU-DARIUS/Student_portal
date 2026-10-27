import os
from collections import defaultdict
from django.conf import settings
from django.db.models import Avg, Count
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend safe for Django web servers

import quickgraph
from quickgraph import graphs
from .models import Student


def generate_all_student_graphs():
    """
    Generates all 4 graph types using the quickgraph-darius12 package:
      1. Pie Graph: Distribution of students by course
      2. Bar Graph: Average student grade by course
      3. Scatter Graph: Study hours per week vs. Grade
      4. Line Graph: Grade progression across registered students
    Saves them to MEDIA_ROOT/graphs and returns their media URLs.
    """
    students = list(Student.objects.all().order_by('id'))
    if not students:
        return None

    # Ensure output directory exists
    graphs_dir = os.path.join(settings.MEDIA_ROOT, 'graphs')
    os.makedirs(graphs_dir, exist_ok=True)

    file_paths = {
        'pie': os.path.join(graphs_dir, 'students_course_pie.png'),
        'bar': os.path.join(graphs_dir, 'students_grade_bar.png'),
        'scatter': os.path.join(graphs_dir, 'students_study_scatter.png'),
        'line': os.path.join(graphs_dir, 'students_trend_line.png'),
    }

    # 1. PIE GRAPH: Course Distribution
    course_counts = defaultdict(int)
    for s in students:
        course_counts[s.course] += 1
    
    pie_labels = list(course_counts.keys())
    pie_values = list(course_counts.values())
    if pie_labels and pie_values:
        graphs.pie_graph(
            labels=pie_labels,
            values=pie_values,
            title="Student Enrollment Distribution by Course",
            save=file_paths['pie'],
            show=False,
        )

    # 2. BAR GRAPH: Average Grade by Course
    course_grades = defaultdict(list)
    for s in students:
        course_grades[s.course].append(float(s.grade))
    
    bar_labels = list(course_grades.keys())
    bar_values = [round(sum(vals) / len(vals), 1) for vals in course_grades.values()]
    if bar_labels and bar_values:
        graphs.bar_graph(
            labels=bar_labels,
            values=bar_values,
            title="Average Grade (%) by Course",
            xlabel="Course / Department",
            ylabel="Average Score (%)",
            save=file_paths['bar'],
            show=False,
        )

    # 3. SCATTER GRAPH: Study Hours vs Grade
    scatter_x = [float(s.study_hours_per_week) for s in students]
    scatter_y = [float(s.grade) for s in students]
    if scatter_x and scatter_y:
        graphs.scatter_graph(
            x=scatter_x,
            y=scatter_y,
            title="Correlation: Study Hours per Week vs. Grade",
            xlabel="Weekly Study Hours (hrs)",
            ylabel="Grade / Score (%)",
            save=file_paths['scatter'],
            show=False,
        )

    # 4. LINE GRAPH: Performance Trend
    line_x = [f"#{s.id} {s.first_name}" for s in students]
    line_y = [float(s.grade) for s in students]
    if line_x and line_y:
        graphs.line_graph(
            x=line_x,
            y=line_y,
            title="Academic Performance Progression Across Students",
            xlabel="Student Record",
            ylabel="Grade (%)",
            save=file_paths['line'],
            show=False,
        )

    return {
        'pie_url': f"{settings.MEDIA_URL}graphs/students_course_pie.png",
        'bar_url': f"{settings.MEDIA_URL}graphs/students_grade_bar.png",
        'scatter_url': f"{settings.MEDIA_URL}graphs/students_study_scatter.png",
        'line_url': f"{settings.MEDIA_URL}graphs/students_trend_line.png",
    }
