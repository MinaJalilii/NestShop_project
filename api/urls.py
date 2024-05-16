from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import *
from rest_framework import routers

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet, basename='categories')

# urlpatterns = router.urls
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('test/', test_end_point, name='test'),
    path('', get_routes),
]
