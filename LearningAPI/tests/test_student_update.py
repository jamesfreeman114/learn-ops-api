from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from LearningAPI.models import NssUser
from rest_framework.test import APIClient
from pytest import fail

class StudentPartialUpdateTests(APITestCase):
    """Tests for PATCH /students/{pk}/"""
    def test_patch_slack_handle_persists_to_database(self):
        user = User.objects.create_user(
            username='teststudent',
            password='testpass123'
        )
        nss_user = NssUser.objects.create(
            user=user,
            slack_handle='@old_handle',
            github_handle='old_github'
        )
        token = Token.objects.create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        """PUT slack_handle should save the new value to the database."""
        response = client.put(
            f"/students/{nss_user.id}",
            {"slack_handle": "@newhandle"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        nss_user.refresh_from_db()
        self.assertEqual(nss_user.slack_handle, "@newhandle")