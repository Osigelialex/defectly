from django.test import TestCase, Client
from .models import Bugs, Comments
from project.models import Project
from django.contrib.auth.models import User


class TestTracker(TestCase):

    def setUp(self) -> None:

        # Create users
        user1 = User.objects.create_user(
            email='john@gmail.com',
            username='john',
            password='password'
        )

        user2 = User.objects.create_user(
            email='doe@gmail.com',
            username='doe',
            password='password'
        )

        # Create projects
        p1 = Project.objects.create(
            name='Test Project 1',
            description='Test Description',
        )
        p1.user.add(user1)

        p2 = Project.objects.create(
            name='Test Project 2',
            description='Test Description 2',
        )

        p2.user.add(user1)
        p2.user.add(user2)

        # Create bugs
        b1 = Bugs.objects.create(
            title='Test Bug 1',
            description='Test Bug Description',
            project=p1,
            created_by=user2
        )
        b1.assignees.add(user1)

        b2 = Bugs.objects.create(
            title='Test Bug 2',
            description='Test Bug Description 2',
            project=p2,
            created_by=user1
        )
        b2.assignees.add(user1)
        b2.assignees.add(user2)

        # create comments
        c1 = Comments.objects.create(
            author=user1,
            comment='Test comment 1',
            bug=b1
        )

        c2 = Comments.objects.create(
            author=user2,
            comment='Test comment 2',
            bug=b2
        )

    def test_project_created(self):
        """Tests if project is created"""
        count = Project.objects.all().count()
        self.assertEqual(count, 2)

    def test_bug_created(self):
        """Tests if bug is created"""
        count = Bugs.objects.all().count()
        self.assertEqual(count, 2)

    def test_comment_created(self):
        """Tests if a comment is created"""
        count = Bugs.objects.all().count()
        self.assertEqual(count, 2)

    def test_project_assignment(self):
        """Tests if project can be assigned"""
        p1 = Project.objects.get(name="Test Project 1")
        p2 = Project.objects.get(name='Test Project 2')

        u1 = User.objects.get(username='john')
        u2 = User.objects.get(username='doe')

        self.assertEqual(p1.user.count(), 1)
        self.assertEqual(p2.user.count(), 2)
        
        p1.user.add(u2)
        self.assertIn(u2, p1.user.all())

        self.assertIn(u1, p1.user.all())
        self.assertIn(u1, p2.user.all())
        self.assertIn(u1, p2.user.all())

    def test_bug_assignment(self):
        """Tests if bugs can be assigned"""
        b1 = Bugs.objects.get(title="Test Bug 1")
        b2 = Bugs.objects.get(title="Test Bug 2")

        u1 = User.objects.get(username='john')
        u2 = User.objects.get(username='doe')

        self.assertEqual(b1.assignees.count(), 1)
        self.assertEqual(b2.assignees.count(), 2)

        self.assertIn(u1, b1.assignees.all())
        self.assertIn(u1, b2.assignees.all())
        self.assertIn(u2, b2.assignees.all())

    def test_login_page(self):
        """Tests if login page is functional"""
        client = Client()
        logged_in = client.login(username='john', password='password')
        self.assertTrue(logged_in)
        response = client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page(self):
        """Tests if dashboard page is functional"""
        client = Client()
        response = client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

        client.login(username='john', password='password')
        response = client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        
    def test_bugs_page(self):
        """Tests if bugs page is functional"""
        client = Client()
        response = client.get('/bugs/')
        self.assertEqual(response.status_code, 302)
        
        client.login(username='john', password='password')
        response = client.get('/bugs/')
        self.assertEqual(response.status_code, 200)
        
    def test_projects_page(self):
        """Tests if projects page is functional"""
        client = Client()
        response = client.get('/projects/')
        self.assertEqual(response.status_code, 302)
        
        client.login(username='john', password='password')
        response = client.get('/projects/')
        self.assertEqual(response.status_code, 200)
