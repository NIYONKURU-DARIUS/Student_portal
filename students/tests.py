from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Student


class StudentAuthAndCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Groups
        self.instructor_group = Group.objects.create(name='Instructor')
        self.student_group = Group.objects.create(name='Student')

        # Create Instructor User
        self.instructor_user = User.objects.create_user(
            username='prof',
            password='password123'
        )
        self.instructor_user.groups.add(self.instructor_group)

        # Create Student User
        self.student_user = User.objects.create_user(
            username='stud',
            password='password123'
        )
        self.student_user.groups.add(self.student_group)

        # Sample student record
        self.student = Student.objects.create(
            first_name="Jean",
            last_name="Bizimana",
            email="jean.bizimana@example.com",
            course="Computer Science",
            grade=85.0,
            study_hours_per_week=18.0
        )

    def test_student_model_creation(self):
        self.assertEqual(str(self.student), "Jean Bizimana")
        self.assertEqual(self.student.status_badge, "badge-success")

    # --- Authorization Tests: Unauthenticated ---
    def test_unauthenticated_redirects_to_login(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    # --- Authorization Tests: Student Role (Read-Only) ---
    def test_student_role_can_view_list_and_analytics(self):
        self.client.login(username='stud', password='password123')

        # Can view directory
        list_response = self.client.get(reverse('student_list'))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "Jean Bizimana")

        # Can view analytics
        analytics_response = self.client.get(reverse('analytics_dashboard'))
        self.assertEqual(analytics_response.status_code, 200)

    def test_student_role_denied_from_creating(self):
        self.client.login(username='stud', password='password123')
        response = self.client.get(reverse('student_create'))
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Access Restricted", status_code=403)

    def test_student_role_denied_from_editing(self):
        self.client.login(username='stud', password='password123')
        response = self.client.get(reverse('student_update', args=[self.student.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Access Restricted", status_code=403)

    def test_student_role_denied_from_deleting(self):
        self.client.login(username='stud', password='password123')
        response = self.client.post(reverse('student_delete', args=[self.student.pk]))
        self.assertEqual(response.status_code, 403)
        # Ensure student was NOT deleted
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())

    # --- Authorization Tests: Instructor Role (Full Access) ---
    def test_instructor_create_view_post(self):
        self.client.login(username='prof', password='password123')
        response = self.client.post(reverse('student_create'), {
            'first_name': 'Aline',
            'last_name': 'Mutesi',
            'email': 'aline.m@example.com',
            'course': 'Data Science',
            'grade': 90.0,
            'study_hours_per_week': 22.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Student.objects.count(), 2)

    def test_instructor_update_view(self):
        self.client.login(username='prof', password='password123')
        response = self.client.post(reverse('student_update', args=[self.student.pk]), {
            'first_name': 'Jean Updated',
            'last_name': 'Bizimana',
            'email': 'jean.bizimana@example.com',
            'course': 'Cybersecurity',
            'grade': 92.0,
            'study_hours_per_week': 20.0
        })
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, "Jean Updated")

    def test_instructor_delete_view_post(self):
        self.client.login(username='prof', password='password123')
        response = self.client.post(reverse('student_delete', args=[self.student.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())
