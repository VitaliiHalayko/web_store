from django.test import TestCase
from django.urls import reverse
from .models import Category
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


class CategoriesViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create an image in memory
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)

        # Create SimpleUploadedFile object
        uploaded_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )

        # Create sample categories for testing
        Category.objects.create(
            name='Category 1',
            image=uploaded_image,
            desc='Description 1',
            is_visible=True,
            sort_order=1
        )
        Category.objects.create(
            name='Category 2',
            image=uploaded_image,
            desc='Description 2',
            is_visible=True,
            sort_order=2
        )

    def test_categories_page_status_code(self):
        """
        Test if the categories page returns a 200 status code.
        """
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)

    def test_categories_page_template(self):
        """
        Test if the categories page uses the correct template.
        """
        response = self.client.get(reverse('categories'))
        self.assertTemplateUsed(response, 'categories/categories.html')

    def test_categories_page_content(self):
        """
        Test if the categories page contains the expected categories.
        """
        response = self.client.get(reverse('categories'))
        self.assertContains(response, 'Category 1')
        self.assertContains(response, 'Category 2')
        self.assertContains(response, 'Description 1')
        self.assertContains(response, 'Description 2')

        # Check if context contains the correct categories
        categories = response.context['categories']
        self.assertEqual(len(categories), 2)

        # Verify that the categories have the expected names
        category_names = [category.name for category in categories]
        self.assertIn('Category 1', category_names)
        self.assertIn('Category 2', category_names)

    def test_category_properties(self):
        """
        Test if the category properties are correctly set.
        """
        category = Category.objects.get(name='Category 1')
        self.assertEqual(category.desc, 'Description 1')
        self.assertTrue(category.is_visible)
        self.assertEqual(category.sort_order, 1)