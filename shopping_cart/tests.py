from store.models import Product
from .models import CartItem, Order, OrderItem
from store.models import Category
from PIL import Image
import io
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

class ShoppingCartTests(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client()

        image = Image.new('RGB', (600, 400), color='blue')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)

        # Create SimpleUploadedFile object
        self.uploaded_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )

        # Create a category for testing
        self.category = Category.objects.create(
            name="Test Category",
            image=self.uploaded_image,
            sort_order=1
        )

        self.product = Product.objects.create(
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
        self.session = self.client.session
        self.session.save()

    def test_add_to_cart(self):
        # Refresh session to ensure it's saved
        self.session = self.client.session

        # Use POST method to add product to the cart
        response = self.client.post(reverse('add_to_cart', args=[self.product.id, 1]))
        self.assertEqual(response.status_code, 302)


        # Verify that the cart item was added
        cart_items = CartItem.objects.filter(session_key=self.session.session_key)
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items[0].quantity, 1)

        response = self.client.post(reverse('add_to_cart', args=[self.product.id, 2]))
        self.assertEqual(response.status_code, 302)
        cart_items = CartItem.objects.filter(session_key=self.session.session_key)
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items[0].quantity, 3)

        # Adding a non-existent product
        response = self.client.post(reverse('add_to_cart', args=[999, 1]))
        self.assertEqual(response.status_code, 404)

        # Adding a product with zero quantity
        response = self.client.post(reverse('add_to_cart', args=[self.product.id, 0]))
        self.assertEqual(response.status_code, 302)
        cart_items = CartItem.objects.filter(session_key=self.session.session_key)
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items[0].quantity, 3)  # Quantity should remain unchanged

    def test_del_from_cart(self):
        # Refresh session to ensure it's saved
        self.session = self.client.session

        CartItem.objects.create(product=self.product, session_key=self.session.session_key, quantity=1)
        response = self.client.get(reverse('del_from_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        cart_items = CartItem.objects.filter(session_key=self.session.session_key)
        self.assertEqual(cart_items.count(), 0)

        # Deleting a product not in the cart
        response = self.client.post(reverse('del_from_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

        # Deleting a product when cart is empty
        response = self.client.post(reverse('del_from_cart', args=[999]))
        self.assertEqual(response.status_code, 404)
    #
    def test_change_quantity(self):
        # Refresh session to ensure it's saved
        self.session = self.client.session

        CartItem.objects.create(product=self.product, session_key=self.session.session_key, quantity=1)
        response = self.client.get(reverse('change_quantity', args=[self.product.id, 5]))
        self.assertEqual(response.status_code, 200)
        cart_items = CartItem.objects.filter(session_key=self.session.session_key)
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items[0].quantity, 5)

        # Changing quantity to zero (should be handled)
        response = self.client.post(reverse('change_quantity', args=[self.product.id, 0]))
        self.assertEqual(response.status_code, 200)
        cart_items = CartItem.objects.filter(session_key=self.session.session_key)
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items[0].quantity, 5)  # Quantity should remain unchanged

        # Changing quantity of a non-existent product
        response = self.client.post(reverse('change_quantity', args=[999, 5]))
        self.assertEqual(response.status_code, 404)

    def test_create_order(self):
        # Refresh session to ensure it's saved
        self.session = self.client.session

        CartItem.objects.create(product=self.product, session_key=self.session.session_key, quantity=1)
        response = self.client.get(reverse('create_order', args=['Doe', 'John', 'john@example.com', 'City', 'Address', '12345']))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.all()
        self.assertEqual(orders.count(), 1)
        order_items = OrderItem.objects.filter(order=orders[0])
        self.assertEqual(order_items.count(), 1)
        self.assertEqual(order_items[0].quantity, 1)

    def test_cart_view(self):
        # Refresh session to ensure it's saved
        self.session = self.client.session

        CartItem.objects.create(product=self.product, session_key=self.session.session_key, quantity=1)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping_cart/cart.html')
        self.assertContains(response, 'Test Product')

        # Viewing empty cart
        CartItem.objects.filter(session_key=self.session.session_key).delete()
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping_cart/cart.html')
        self.assertNotContains(response, 'Test Product')
