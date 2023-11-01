"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user(self):
        """Test creating user successful"""
        email = "test@example.com"
        password = 'pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_normilize(self):
        """Test creating user successful and normilized"""
        emails_list = [
            ["ASDAS@EXAMPLE.com", "ASDAS@example.com"],
            ["asd1WW@EXAMPlE.com", "asd1WW@example.com"],
        ]
        for email, target in emails_list:
            user = get_user_model().objects.create_user(
                email=email,
                password='qwerty',
            )
            self.assertEqual(user.email, target)

    def test_create_superuser(self):
        """Test creating superuser"""
        user = get_user_model().objects.create_superuser(
            'test@exxample.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
