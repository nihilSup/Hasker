from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class QuestionsAPITests(APITestCase):
    def test_questions(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('question-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search(self):
        url = reverse('question-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trending(self):
        url = reverse('question-trending')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_question_answers(self):
        url = reverse('question-answers', args=(5,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
