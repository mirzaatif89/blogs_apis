from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminBlogViewSet, BlogListAPIView, BlogDetailAPIView

router = DefaultRouter()
router.register(r'admin/blogs', AdminBlogViewSet, basename='admin-blogs')

urlpatterns = [
    path('', include(router.urls)),

    # User APIs
    path('blogs/', BlogListAPIView.as_view(), name='blog-list'),
    path('blogs/<slug:slug>/', BlogDetailAPIView.as_view(), name='blog-detail'),
    
]
