from django.urls import include, path
from rest_framework import routers

from .views import (UserViewSet)

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('users', UserViewSet)

auth_urlpatterns = [
    path('token/', APIGetToken.as_view(), name='get_token'),
    path('signup/', APISignup.as_view(), name='signup'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns)),
    path('v1/', include(router.urls)),
]