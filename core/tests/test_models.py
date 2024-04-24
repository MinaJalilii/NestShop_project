from django.test import TestCase
from core.models import *
from model_bakery import baker


class TestCategoryModel(TestCase):
    def test_category_image(self):
        image_url = '/media/profile_pictures/author-2.png'
        category = Category(image=image_url)
        image_html = category.category_image()
        self.assertIn(image_url, image_html)
        self.assertIn('width="50"', image_html)
        self.assertIn('height="50"', image_html)

    def test_model_str(self):
        category = baker.make(Category, title='drinks')
        self.assertEqual(str(category), 'drinks')


class TestVendorModel(TestCase):
    def test_model_str(self):
        vendor = baker.make(Vendor, title='mina')
        self.assertEqual(str(vendor), 'mina')

    def test_vendor_image(self):
        image_url = '/media/profile_pictures/author-2.png'
        vendor = Vendor(image=image_url)
        image_html = vendor.vendor_image()
        self.assertIn(image_url, image_html)
        self.assertIn('width="50"', image_html)
        self.assertIn('height="50"', image_html)


class TestProductModel(TestCase):

    def test_model_str(self):
        product = baker.make(Product, title='papaya')
        self.assertEqual(str(product), 'papaya')

    def test_product_image(self):
        image_url = '/media/profile_pictures/author-2.png'
        product = Product(image=image_url)
        image_html = product.product_image()
        self.assertIn(image_url, image_html)
        self.assertIn('width="50"', image_html)
        self.assertIn('height="50"', image_html)

    def test_get_perecentage(self):
        product = Product(price=10.00, old_price=20.00)
        expected_discount = ((product.old_price - product.price) / product.old_price) * 100
        actual_discount = product.get_percentage()
        self.assertAlmostEqual(actual_discount, expected_discount, delta=0.01)


class TestCartOrderItemsModel(TestCase):

    def test_order_image(self):
        image_url = '/media/profile_pictures/author-2.png'
        cart_order_item = CartOrderItems(image=image_url)
        image_html = cart_order_item.order_image()
        self.assertIn(image_url, image_html)
        self.assertIn('width="50"', image_html)
        self.assertIn('height="50"', image_html)

    def test_order_objects(self):
        user = baker.make(User, username='test_user', email='test@example.com')
        cart_order = baker.make(CartOrder, user=user)
        cart_order_item = baker.make(CartOrderItems, order=cart_order)
        expected_output = f"Order_NO-{cart_order.id}|user:{user.email}"
        actual_output = cart_order_item.order_objects()
        self.assertEqual(actual_output, expected_output)


class TestProductReviewModel(TestCase):

    def test_model_str(self):
        user = baker.make(User, username='mina')
        review = baker.make(ProductReview, user=user, review='hello hello')
        self.assertEqual(str(review), f"{review.user.username}-{review.review[:70]}")

    def test_get_rating(self):
        test_data = [
            (1, 20),
            (2, 42),
            (3, 63),
            (4, 85),
            (5, 100),
        ]
        for rating_value, expected_rating in test_data:
            user = baker.make(User, username='test_user')
            product = baker.make(Product)
            review = baker.make(ProductReview, user=user, product=product, rating=rating_value)
            actual_rating = review.get_rating()
            self.assertEqual(actual_rating, expected_rating, msg=f"Failed for rating {rating_value}")


class TestWishlistModel(TestCase):
    def test_model_str(self):
        product = baker.make(Product, title='banana')
        wishlist = baker.make(Wishlist, product=product)
        self.assertEqual(str(wishlist), 'banana')
