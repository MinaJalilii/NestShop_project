from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from core.views import *
from django.urls import reverse, resolve
from model_bakery import baker
from core.models import *

""" 
def setUp(self):
        self.client = Client()
        self.url = reverse('') 
"""


class TestHomeView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_view_GET(self):
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')


class TestProductListView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('home:product-list')

    def test_GET_request(self):
        user = User.objects.create_user(username='mina', email='mina@email.com', password='mina-password')
        image = SimpleUploadedFile(name='author-2.png',
                                   content=open('media/profile_pictures/author-2.png', 'rb').read(),
                                   content_type='image/png')
        vendor = baker.make(Vendor, user=user, image=image)
        category = baker.make(Category, image=image)
        product1 = baker.make(Product, price=10.24, old_price=5.32, vendor=vendor, category=category, user=user,
                              image=image,
                              product_status='published')
        product2 = baker.make(Product, price=10.24, old_price=5.32, vendor=vendor, category=category, user=user,
                              image=image,
                              product_status='published')
        product3 = baker.make(Product, price=10.24, old_price=5.32, vendor=vendor, category=category, user=user,
                              image=image, product_status='draft')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/product-list.html')
        self.assertIn(product1, response.context['products'])
        self.assertIn(product2, response.context['products'])
        self.assertNotIn(product3, response.context['products'])


class TestCategoryListView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('home:category-list')

    def test_GET_request(self):
        image = SimpleUploadedFile(name='author-2.png',
                                   content=open('media/profile_pictures/author-2.png', 'rb').read(),
                                   content_type='image/png')
        category1 = baker.make(Category, image=image)
        category2 = baker.make(Category, image=image)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/category-list.html')
        self.assertIn('categories', response.context)
        self.assertIn(category1, response.context['categories'])
        self.assertIn(category2, response.context['categories'])


class TestCategoryProductListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home:category_product_list', args=('cata2g783b43c',))

    def test_GET_request(self):
        user = User.objects.create_user(username='mina', email='mina@email.com', password='mina-password')
        image = SimpleUploadedFile(name='author-2.png',
                                   content=open('media/profile_pictures/author-2.png', 'rb').read(),
                                   content_type='image/png')
        category = baker.make(Category, image=image, cid='cata2g783b43c')
        vendor = baker.make(Vendor, user=user, image=image)
        product1 = baker.make(Product, price=10.24, old_price=5.32, vendor=vendor, category=category, user=user,
                              image=image,
                              product_status='published')
        product2 = baker.make(Product, price=10.24, old_price=5.32, vendor=vendor, category=category, user=user,
                              image=image,
                              product_status='published')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/category-product-list.html')
        self.assertIn('category', response.context)
        self.assertIn('products', response.context)
        self.assertIn(product1, response.context['products'])
        self.assertIn(product2, response.context['products'])
        self.assertEqual(response.context['category'], category)


class TestVendorListView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('home:vendor-list')

    def test_GET_request(self):
        user = User.objects.create_user(username='mina', email='mina@email.com', password='mina-password')
        image = SimpleUploadedFile(name='author-2.png',
                                   content=open('media/profile_pictures/author-2.png', 'rb').read(),
                                   content_type='image/png')
        vendor1 = baker.make(Vendor, user=user, image=image, cover_image=image)
        vendor2 = baker.make(Vendor, user=user, image=image, cover_image=image)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/vendors-list.html')
        self.assertIn('vendors', response.context)
        self.assertIn(vendor1, response.context['vendors'])
        self.assertIn(vendor2, response.context['vendors'])


class TestVendorDetailView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('home:vendor-detail', args=('ven2af4g433e4',))
        self.user = User.objects.create_user(username='test-user', email='test@email.com', password='test-password')
        self.image = SimpleUploadedFile(name='author-2.png',
                                        content=open('media/profile_pictures/author-2.png', 'rb').read(),
                                        content_type='image/png')
        self.cover_image = SimpleUploadedFile(name='author-2.png',
                                              content=open('media/profile_pictures/author-2.png', 'rb').read(),
                                              content_type='image/png')
        self.vendor = baker.make(Vendor, user=self.user, image=self.image, cover_image=self.cover_image,
                                 vid='ven2af4g433e4')

    def test_GET_request(self):
        product1 = baker.make(Product, price=10.24, old_price=5.32, vendor=self.vendor, user=self.user,
                              image=self.image,
                              product_status='published')
        product2 = baker.make(Product, price=10.24, old_price=5.32, vendor=self.vendor, user=self.user,
                              image=self.image,
                              product_status='published')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/vendor-details.html')
        self.assertIn('vendor', response.context)
        self.assertEqual(self.vendor, response.context['vendor'])
        self.assertIn('products', response.context)
        self.assertIn(product1, response.context['products'])
        self.assertIn(product2, response.context['products'])

    def test_vendor_not_found(self):
        url = reverse('home:vendor-detail', args=('non-existing-vid',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_no_published_products(self):
        response = self.client.get(self.url)
        Product.objects.filter(vendor=self.vendor, product_status='published').delete()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [])


class TestRatingToWidthFunction(TestCase):

    def test_valid_ratings(self):
        self.assertEqual(rating_to_width(1), 20)
        self.assertEqual(rating_to_width(2), 40)
        self.assertEqual(rating_to_width(3), 60)
        self.assertEqual(rating_to_width(4), 80)
        self.assertEqual(rating_to_width(5), 100)

    def test_decimal_rating(self):
        self.assertEqual(rating_to_width(3.5), 70)
        self.assertEqual(rating_to_width(4.7), 100)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            rating_to_width("3.5")
        with self.assertRaises(TypeError):
            rating_to_width([3.5])
        with self.assertRaises(ValueError):
            rating_to_width(0)
        with self.assertRaises(ValueError):
            rating_to_width(6)


class TestProductDetailView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("home:product-detail", args=('pid-for-a-product',))
        self.user = User.objects.create_user(username='test-user', email='test@email.com', password='test-password')
        self.image = SimpleUploadedFile(name='author-2.png',
                                        content=open('media/profile_pictures/author-2.png', 'rb').read(),
                                        content_type='image/png')
        self.vendor = baker.make(Vendor, user=self.user, image=self.image)
        self.category = baker.make(Category, image=self.image)
        self.product = baker.make(Product, pid='pid-for-a-product', user=self.user, image=self.image,
                                  vendor=self.vendor, category=self.category,
                                  price=10.25, old_price=5.45)

    def test_valid_product_detail_view_with_existing_product(self):
        response = self.client.get(self.url)
        context = response.context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/product-detail.html')
        self.assertIn('product', context)
        self.assertIn('product_images', context)
        self.assertIn('related_products', context)
        self.assertIn('products', context)
        self.assertIn('reviews', context)
        self.assertIn('make_review', context)
        self.assertIn('review_form', context)
        self.assertIn('avg_rating', context)
        self.assertIn('rating_width', context)
        self.assertIn('rating_percentages', context)
        self.assertEqual(self.product, context['product'])

    def test_invalid_product_detail_view_with_nonexistent_product(self):
        invalid_url = self.url = reverse("home:product-detail", args=('invalid-pid-product',))
        response = self.client.get(invalid_url)
        context = response.context
        self.assertEqual(response.status_code, 404)
        self.assertNotIn('product', context)
