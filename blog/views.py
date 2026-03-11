from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Blog
from .serializers import AdminBlogSerializer, BlogListSerializer, BlogDetailSerializer


# Admin API
class AdminBlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = AdminBlogSerializer
    permission_classes = [AllowAny]   # testing ke liye
    # production me IsAdminUser use karo:
    # permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {'request': self.request}


# User blog list API
class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}


# User single blog detail API
class BlogDetailAPIView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_serializer_context(self):
        return {'request': self.request}
