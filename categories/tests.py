from django.test import TestCase
from django.urls import reverse
from .models import Category
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
import os


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

    @classmethod
    def tearDownClass(cls):
        for category in Category.objects.all():
            if category.image and 'test_image' in category.image.name:
                if os.path.isfile(category.image.path):
                    os.remove(category.image.path)
        super().tearDownClass()

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


class CategoryModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create an image in memory
        image = Image.new('RGB', (600, 400), color='blue')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)

        # Create SimpleUploadedFile object
        cls.uploaded_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )

    @classmethod
    def tearDownClass(cls):
        for category in Category.objects.all():
            if category.image and 'test_image' in category.image.name:
                if os.path.isfile(category.image.path):
                    os.remove(category.image.path)
        super().tearDownClass()

    def test_create_category(self):
        """
        Testing the creation of a category object
        """
        category = Category.objects.create(
            name='Test Category',
            image=self.uploaded_image,
            desc='Test Description',
            is_visible=True,
            sort_order=1
        )
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.desc, 'Test Description')
        self.assertTrue(category.is_visible)
        self.assertEqual(category.sort_order, 1)

    def test_image_processing_on_save(self):
        """
        Testing image processing when saving
        """
        category = Category.objects.create(
            name='Test Category',
            image=self.uploaded_image,
            desc='Test Description',
            is_visible=True,
            sort_order=1
        )

        img_path = category.image.path
        img = Image.open(img_path)

        self.assertEqual(img.size, (450, 300))
        self.assertTrue(img.format, 'JPEG')

    def test_image_aspect_ratio(self):
        """
        Test changing the image proportions
        """
        image = Image.new('RGB', (800, 200), color='green')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)

        uploaded_image = SimpleUploadedFile(
            name='test_image_wide.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )

        category = Category.objects.create(
            name='Test Category Wide',
            image=uploaded_image,
            desc='Test Description Wide',
            is_visible=True,
            sort_order=1
        )

        img_path = category.image.path
        img = Image.open(img_path)

        self.assertEqual(img.size, (450, 300))
        self.assertTrue(img.format, 'JPEG')

    def test_image_cleanup(self):
        """
        Test deleting test images after the tests
        """
        category = Category.objects.create(
            name='Test Category Cleanup',
            image=self.uploaded_image,
            desc='Test Description Cleanup',
            is_visible=True,
            sort_order=1
        )

        img_path = category.image.path
        self.assertTrue(os.path.isfile(img_path))

        Category.objects.all().delete()

        self.assertFalse(os.path.isfile(img_path))