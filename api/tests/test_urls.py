from django.urls import resolve, reverse
from django.test import TestCase
from api.views import *


class TestUrls(TestCase):
    def test_product_list(self):
        url = reverse('api:product-api')
        self.assertEqual(resolve(url).func.view_class, ProductApiView)

    def test_product_detail(self):
        url = reverse('api:product-detail-api', args=(2,))
        self.assertEqual(resolve(url).func.view_class, ProductDetailApiView)