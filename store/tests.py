from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Product, Category, Attribute, Value
from PIL import Image
import io
import os


class StoreViewTests(TestCase):
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

        # Create a category for testing
        cls.category = Category.objects.create(
            name="Test Category",
            image=cls.uploaded_image,
            sort_order=1
        )

        # Create a product for testing
        cls.product = Product.objects.create(
            name="Test Product",
            short_description="Test short description",
            description="Test description",
            image=cls.uploaded_image,
            image_on_shop_page=cls.uploaded_image,
            category=cls.category,
            price=100.00,
            price_with_discount=80.00,
            total_orders_count=10,
            total_count_on_warehouse=50,
            is_visible=True
        )

        # Create an attribute for testing
        cls.attribute = Attribute.objects.create(
            name="Color",
            category=cls.category,
            is_show=True
        )

        # Create a value for testing
        cls.value = Value.objects.create(
            attribute=cls.attribute,
            product=cls.product,
            category=cls.category,
            value="Red",
            selected=True
        )

    @classmethod
    def tearDownClass(cls):
        for product in Product.objects.all():
            for image_field in [product.image, product.image_on_shop_page]:
                if image_field and 'test_image' in image_field.name:
                    if os.path.isfile(image_field.path):
                        os.remove(image_field.path)
        for category in Category.objects.all():
            if category.image and 'test_image' in category.image.name:
                if os.path.isfile(category.image.path):
                    os.remove(category.image.path)
        super().tearDownClass()

    def setUp(self):
        self.client = Client()

    def test_popular_items_view(self):
        """
        Test that we can successfully retrieve the most popular items
        """
        response = self.client.get(reverse('popular'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
        self.assertIn('products', response.context)
        self.assertEqual(list(response.context['products']), [self.product])

    def test_new_arrivals_view(self):
        """
        Test that we can successfully retrieve the new items
        """
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
        self.assertIn('products', response.context)
        self.assertEqual(list(response.context['products']), [self.product])

    def test_category_products_view(self):
        """
        Test that we can successfully retrieve correct items
        """
        response = self.client.get(reverse('category_products', args=[self.category.name]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
        self.assertIn('products', response.context)
        self.assertEqual(list(response.context['products']), [self.product])

    def test_category_products_post_view(self):
        """
        Test that we can successfully retrieve correct sorted and filtered items
        """
        post_data = {
            'min_price': '50',
            'max_price': '150',
            'Color': ['Red'],
            'sort_option': 'price_asc'
        }
        response = self.client.post(reverse('category_products', args=[self.category.name]), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
        self.assertIn('products', response.context)
        self.assertEqual(list(response.context['products']), [self.product])

    def test_product_page_view(self):
        """
        Test that we can successfully retrieve correct product page
        """
        response = self.client.get(reverse('product', args=[self.category.name, self.product.name]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product.html')
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], self.product)


class ProductModelTest(TestCase):
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

        # Create a category for testing with the required sort_order field
        cls.category = Category.objects.create(
            name="Test Category",
            image=cls.uploaded_image,
            sort_order=1  # Assuming sort_order is an integer field
        )

    @classmethod
    def tearDownClass(cls):
        for product in Product.objects.all():
            for image_field in [product.image, product.image_on_shop_page]:
                if image_field and 'test_image' in image_field.name:
                    if os.path.isfile(image_field.path):
                        os.remove(image_field.path)
        for category in Category.objects.all():
            if category.image and 'test_image' in category.image.name:
                if os.path.isfile(category.image.path):
                    os.remove(category.image.path)
        super().tearDownClass()

    def test_product_creation(self):
        """
        Testing the creation of a product object
        """
        product = Product.objects.create(
            name="Test Product",
            short_description="Test short description",
            description="Test description",
            image=self.uploaded_image,
            image_on_shop_page=self.uploaded_image,
            category=self.category,
            price=100.00,
            price_with_discount=80.00,
            total_orders_count=10,
            total_count_on_warehouse=50,
            is_visible=True
        )

        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.short_description, "Test short description")
        self.assertEqual(product.description, "Test description")
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.price, 100.00)
        self.assertEqual(product.price_with_discount, 80.00)
        self.assertEqual(product.total_orders_count, 10)
        self.assertEqual(product.total_count_on_warehouse, 50)
        self.assertTrue(product.is_visible)

    def test_image_resizing(self):
        """
        Testing image processing when saving
        """
        product = Product.objects.create(
            name="Test Product with Image",
            short_description="Test short description",
            description="Test description",
            image=self.uploaded_image,
            image_on_shop_page=self.uploaded_image,
            category=self.category,
            price=100.00,
            price_with_discount=80.00,
            total_orders_count=10,
            total_count_on_warehouse=50,
            is_visible=True
        )

        main_image = Image.open(product.image)

        self.assertEqual(main_image.size, (600, 400), "Main image size should be 600x400")

    def test_unique_name_constraint(self):
        """
        Test unique constraint on product name
        """
        Product.objects.create(
            name="Unique Product",
            short_description="Test short description",
            description="Test description",
            image=self.uploaded_image,
            image_on_shop_page=self.uploaded_image,
            category=self.category,
            price=100.00,
            price_with_discount=80.00,
            total_orders_count=10,
            total_count_on_warehouse=50,
            is_visible=True
        )

        with self.assertRaises(Exception):
            Product.objects.create(
                name="Unique Product",
                short_description="Test short description",
                description="Test description",
                image=self.uploaded_image,
                image_on_shop_page=self.uploaded_image,
                category=self.category,
                price=100.00,
                price_with_discount=80.00,
                total_orders_count=10,
                total_count_on_warehouse=50,
                is_visible=True
            )


class AttributeModelTest(TestCase):
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

        # Create a category for testing
        cls.category = Category.objects.create(
            name="Test Category",
            image=cls.uploaded_image,
            sort_order=1
        )

    @classmethod
    def tearDownClass(cls):
        for category in Category.objects.all():
            if category.image and 'test_image' in category.image.name:
                if os.path.isfile(category.image.path):
                    os.remove(category.image.path)
        super().tearDownClass()

    def test_attribute_creation(self):
        """
        Testing the creation of an attribute object
        """
        attribute = Attribute.objects.create(
            name="Color",
            category=self.category,
            is_show=True
        )
        self.assertEqual(attribute.name, "Color")
        self.assertEqual(attribute.category, self.category)
        self.assertTrue(attribute.is_show)

    def test_default_is_show(self):
        """
        Testing the is the is_show default set to True
        """
        attribute = Attribute.objects.create(
            name="Size",
            category=self.category
        )
        self.assertTrue(attribute.is_show)  # Check that is_show defaults to True


class ValueModelTest(TestCase):
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

        # Create a category for testing
        cls.category = Category.objects.create(
            name="Test Category",
            image=cls.uploaded_image,
            sort_order=1
        )

        # Create a product for testing
        cls.product = Product.objects.create(
            name="Test Product",
            short_description="Test short description",
            description="Test description",
            image=cls.uploaded_image,
            image_on_shop_page=cls.uploaded_image,
            category=cls.category,
            price=100.00,
            price_with_discount=80.00,
            total_orders_count=10,
            total_count_on_warehouse=50,
            is_visible=True
        )

        # Create an attribute for testing
        cls.attribute = Attribute.objects.create(
            name="Color",
            category=cls.category,
            is_show=True
        )

    @classmethod
    def tearDownClass(cls):
        for product in Product.objects.all():
            for image_field in [product.image, product.image_on_shop_page]:
                if image_field and 'test_image' in image_field.name:
                    if os.path.isfile(image_field.path):
                        os.remove(image_field.path)
        for category in Category.objects.all():
            if category.image and 'test_image' in category.image.name:
                if os.path.isfile(category.image.path):
                    os.remove(category.image.path)
        super().tearDownClass()

    def test_value_creation(self):
        """
        Testing the creation of a value object
        """
        value = Value.objects.create(
            attribute=self.attribute,
            product=self.product,
            category=self.category,
            value="Red",
            selected=True
        )
        self.assertEqual(value.attribute, self.attribute)
        self.assertEqual(value.product, self.product)
        self.assertEqual(value.category, self.category)
        self.assertEqual(value.value, "Red")
        self.assertTrue(value.selected)

    def test_default_selected(self):
        """
        Testing is the selected default set to False
        """
        value = Value.objects.create(
            attribute=self.attribute,
            product=self.product,
            category=self.category,
            value="Blue"
        )
        self.assertFalse(value.selected)  # Check that selected defaults to False

    def test_delete_category_cascades_to_value(self):
        """
        Testing the values deletion cascades after category is deleted
        """
        value = Value.objects.create(
            attribute=self.attribute,
            product=self.product,
            category=self.category,
            value="Yellow",
            selected=False
        )
        self.category.delete()
        with self.assertRaises(Value.DoesNotExist):
            value.refresh_from_db()

    def test_delete_product_cascades_to_value(self):
        """
        Testing the values deletion cascades after product is deleted
        """
        value = Value.objects.create(
            attribute=self.attribute,
            product=self.product,
            category=self.category,
            value="Black",
            selected=False
        )
        self.product.delete()
        with self.assertRaises(Value.DoesNotExist):
            value.refresh_from_db()

    def test_delete_attribute_cascades_to_value(self):
        """
        Testing the values deletion cascades after attribute is deleted
        """
        value = Value.objects.create(
            attribute=self.attribute,
            product=self.product,
            category=self.category,
            value="White",
            selected=False
        )
        self.attribute.delete()
        with self.assertRaises(Value.DoesNotExist):
            value.refresh_from_db()