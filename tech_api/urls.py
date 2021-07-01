"""tech_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from main.views import *

router = DefaultRouter()
router.register('posts', PostsViewSet)
router.register('comments', CommentViewSet)

schem_view = get_schema_view(
    openapi.Info(
        title = 'My API',
        default_version='v1',
        description='My ecommerce API'
    ),
    public=True,
    permission_classes=[AllowAny],
)

# как работает
"""
create -> v1/api/posts/ POST
list -> posts/ GET
retrieve -> posts/id/ GET - один конкртеный пост
updaate -> posts/id/ PUT
partial_update -> posts/id/ PATCH
destroy -> posts/id/DELETE
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/api/categories/', CategoryListView.as_view()),
    path('v1/api/', include(router.urls)),
    path('v1/api/add-image/', PImageView.as_view()),
    path('v1/api/', include('account.urls')),
    path('v1/api/docs/', schem_view.with_ui('swagger'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
