from django.test import TestCase
from .models import Project, Bugs, Comments
from django.contrib.auth.models import User


class TestTracker(TestCase):
    
    def setUp(self) -> None:
        
        # Create users
        user1 = User.objects.create(
            email='john@gmail.com',
            username='john',
            password='password'
        )
        
        user2 = User.objects.create(
            email='doe@gmail.com', 
            username='doe', 
            password='password'
        )

        # Create projects
        p1 = Project.objects.create(
            name='Test Project 1',
            description='Test Description',
        )
        p1.user.set([user1])
        
        p2 = Project.objects.create(
            name='Test Project 2',
            description='Test Description 2',
        )

        p2.user.set([user1, user2])
        
        # Create bugs
        b1 = Bugs.objects.create(
            title='Test Bug 1',
            description='Test Bug Description',
            project = p1,
            created_by = user2
        )
        b1.assignees.set([user1])
        
        b2 = Bugs.objects.create(
            title='Test Bug 2',
            description='Test Bug Description 2',
            project = p2,
            created_by = user1
        )
        b2.assignees.set([user1, user2])

        # create comments
        c1 = Comments.objects.create(
            author = user1,
            comment = 'Test comment 1',
            bug = b1
        )
        
        c2 = Comments.objects.create(
            author = user2,
            comment = 'Test comment 2',
            bug = b2
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
