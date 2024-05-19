from django.test import TestCase
from django.urls import reverse


class AboutViewTests(TestCase):
    def test_about_page_status_code(self):
        """
        Test if the about page returns a 200 status code.
        """
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_template(self):
        """
        Test if the about page uses the correct template.
        """
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'about/about.html')

    def test_about_page_content(self):
        """
        Test if the about page contains specific content.
        """
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'About page')