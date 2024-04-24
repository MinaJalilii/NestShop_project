from django.test import TestCase
from core.views import *
from django.urls import resolve, reverse


class TestUrls(TestCase):
    def test_home(self):
        url = reverse('home:home')
        self.assertEqual(resolve(url).func, home_view)

    def test_product_list(self):
        url = reverse('home:product-list')
        self.assertEqual(resolve(url).func, product_list_view)

    def test_product_detail(self):
        url = reverse('home:product-detail', args=('prd3gf475g523',))
        self.assertEqual(resolve(url).func, product_detail_view)

    def test_compare(self):
        url = reverse('home:compare')
        self.assertEqual(resolve(url).func, compare_products_view)

    def test_add_to_compare(self):
        url = reverse('home:add-to-compare')
        self.assertEqual(resolve(url).func, add_to_compare)

    def test_delete_from_compare(self):
        url = reverse('home:delete-from-compare')
        self.assertEqual(resolve(url).func, delete_product_from_compare)

    def test_category_list(self):
        url = reverse('home:category-list')
        self.assertEqual(resolve(url).func, category_list_view)

    def test_category_product_list(self):
        url = reverse('home:category_product_list', args=('cata2g783b43c',))
        self.assertEqual(resolve(url).func, category_product_list_view)

    def test_vendor_list(self):
        url = reverse('home:vendor-list')
        self.assertEqual(resolve(url).func, vendor_list_view)

    def test_vendor_detail(self):
        url = reverse('home:vendor-detail', args=('ven1af4g433e4',))
        self.assertEqual(resolve(url).func, vendor_detail_view)

    def test_tag_list(self):
        url = reverse('home:tag-list', args=('milk',))
        self.assertEqual(resolve(url).func, tag_list)

    def test_add_review_ajax(self):
        url = reverse('home:ajax_add_review', args=(15,))
        self.assertEqual(resolve(url).func, ajax_add_review)

    def test_search(self):
        url = reverse('home:search')
        self.assertEqual(resolve(url).func, search_view)

    def test_vendor_search(self):
        url = reverse('home:vendor-search')
        self.assertEqual(resolve(url).func, vendor_search_view)

    def test_filter_products(self):
        url = reverse('home:filter-product')
        self.assertEqual(resolve(url).func, filter_product)

    def test_add_to_cart(self):
        url = reverse('home:add-to-cart')
        self.assertEqual(resolve(url).func, add_to_cart_view)

    def test_cart_view(self):
        url = reverse('home:cart')
        self.assertEqual(resolve(url).func, cart_view)

    def test_delete_from_cart(self):
        url = reverse('home:delete-from-cart')
        self.assertEqual(resolve(url).func, delete_product_from_cart)

    def test_update_quantity(self):
        url = reverse('home:update-cart')
        self.assertEqual(resolve(url).func, update_cart)

    def test_checkout(self):
        url = reverse('home:checkout')
        self.assertEqual(resolve(url).func, checkout)

    def test_success_payment(self):
        url = reverse('home:payment-success')
        self.assertEqual(resolve(url).func, paypal_success)

    def test_fail_payment(self):
        url = reverse('home:payment-failed')
        self.assertEqual(resolve(url).func, paypal_fail)

    def test_user_dashboard(self):
        url = reverse('home:dashboard')
        self.assertEqual(resolve(url).func, user_dashboard)

    def test_order_detail(self):
        url = reverse('home:order-detail', args=(12,))
        self.assertEqual(resolve(url).func, order_detail)

    def test_default_address(self):
        url = reverse('home:make-default-address')
        self.assertEqual(resolve(url).func, make_default_address)

    def test_empty_cart(self):
        url = reverse('home:empty-cart')
        self.assertEqual(resolve(url).func, empty_cart)

    def test_add_to_wishlist(self):
        url = reverse('home:add-to-wishlist')
        self.assertEqual(resolve(url).func, add_to_wishlist)

    def test_wishlist(self):
        url = reverse('home:wishlist')
        self.assertEqual(resolve(url).func, wishlist_view)

    def test_remove_from_wishlist(self):
        url = reverse('home:remove-from-wishlist')
        self.assertEqual(resolve(url).func, remove_from_wishlist)

    def test_about_us(self):
        url = reverse('home:about-us')
        self.assertEqual(resolve(url).func, about_us_view)

    def test_blog_list(self):
        url = reverse('home:blog-list')
        self.assertEqual(resolve(url).func, blog_list_view)

    def test_all_deals(self):
        url = reverse('home:all-deals')
        self.assertEqual(resolve(url).func, all_deals_view)

    def test_add_new_review(self):
        url = reverse('home:add-new-review')
        self.assertEqual(resolve(url).func, add_new_review)

    def test_add_reply(self):
        url = reverse('home:add-new-reply')
        self.assertEqual(resolve(url).func, add_new_reply)
