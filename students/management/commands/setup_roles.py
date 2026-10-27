from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from students.models import Student


class Command(BaseCommand):
    help = "Initializes authorization groups (Instructor, Student), permissions, and demo test accounts."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Setting up groups and permissions..."))

        # 1. Retrieve Student model content type
        content_type = ContentType.objects.get_for_model(Student)
        student_perms = Permission.objects.filter(content_type=content_type)

        # 2. Setup "Instructor" Group (Full CRUD permissions)
        instructor_group, created = Group.objects.get_or_create(name='Instructor')
        for perm in student_perms:
            instructor_group.permissions.add(perm)
        self.stdout.write(self.style.SUCCESS(f"  [OK] Group '{instructor_group.name}' configured with full Student permissions."))

        # 3. Setup "Student" Group (Read-only view permission)
        student_group, created = Group.objects.get_or_create(name='Student')
        view_perm = student_perms.filter(codename='view_student').first()
        if view_perm:
            student_group.permissions.add(view_perm)
        self.stdout.write(self.style.SUCCESS(f"  [OK] Group '{student_group.name}' configured with read-only permissions."))

        # 4. Create Demo Test Accounts
        # A. Instructor User
        instructor_user, created = User.objects.get_or_create(
            username='instructor1',
            defaults={'email': 'instructor1@example.com', 'first_name': 'Prof.', 'last_name': 'Hategekimana'}
        )
        instructor_user.set_password('instructor123')
        instructor_user.is_staff = True
        instructor_user.save()
        instructor_user.groups.set([instructor_group])
        self.stdout.write(self.style.SUCCESS("  [OK] User 'instructor1' created (Password: instructor123, Role: Instructor)"))

        # B. Student User
        student_user, created = User.objects.get_or_create(
            username='student1',
            defaults={'email': 'student1@example.com', 'first_name': 'Jean', 'last_name': 'Claude'}
        )
        student_user.set_password('student123')
        student_user.is_staff = False
        student_user.save()
        student_user.groups.set([student_group])
        self.stdout.write(self.style.SUCCESS("  [OK] User 'student1' created (Password: student123, Role: Student)"))

        # C. Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'first_name': 'Super', 'last_name': 'Admin'}
        )
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS("  [OK] Superuser 'admin' created (Password: admin123, Role: Admin)"))

        self.stdout.write(self.style.SUCCESS("\nSetup complete! You can now test role-based access."))
