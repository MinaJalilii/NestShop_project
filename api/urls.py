from django.urls import path
from api.views import *

app_name = "api"

urlpatterns = [
    path("api/product", ProductApiView.as_view(), name="product-api"),
    path("api/product/<int:pk>", ProductDetailApiView.as_view(), name="product-detail-api"),
    path("api/product/create", ProductCreateApiView.as_view(), name="product-create-api"),
    path("api/user", UserApiView.as_view(), name="user-api"),
    path("api/user/<int:pk>", UserDetailApiView.as_view(), name="user-detail-api"),
    path("api/user/create", UserCreateApiView.as_view(), name="user-create-api"),
    path("api/user/profile", ProfileApiView.as_view(), name="profile-api"),
    path("api/user/profile/<int:pk>", ProfileDetailApiView.as_view(), name="profile-detail-api"),
    path("api/user/profile/create", ProfileCreateApiView.as_view(), name="profile-create-api"),
]
