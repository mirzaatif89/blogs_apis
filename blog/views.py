from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from .models import Blog
from .serializers import (
    AdminBlogSerializer,
    BlogListSerializer,
    BlogDetailSerializer,
    ContactSerializer,
)
from .email_client import EmailDeliveryError, send_email


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


class ContactMessageAPIView(APIView):
    """Accept a contact request and forward its details over email."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        subject = f"New inquiry from {data['full_name']}"
        body = "\n".join([
            f"Full name: {data['full_name']}",
            f"Email: {data['email']}",
            f"Phone number: {data['phone_number']}",
            f"Service: {data['service']}",
            "Message:",
            data['message'],
        ])
        html_body = """
        <html>
          <body>
            <h2>New contact request</h2>
            <table cellpadding="6" cellspacing="0" style="border-collapse:collapse;">
              <tr><td><strong>Full name</strong></td><td>{full_name}</td></tr>
              <tr><td><strong>Email</strong></td><td>{email}</td></tr>
              <tr><td><strong>Phone number</strong></td><td>{phone_number}</td></tr>
              <tr><td><strong>Service</strong></td><td>{service}</td></tr>
            </table>
            <h3>Message</h3>
            <p>{message}</p>
          </body>
        </html>
        """.format(**data)
        recipients = settings.CONTACT_NOTIFICATION_EMAILS

        try:
            send_email(subject=subject, body=body, html_body=html_body, to=recipients)
        except EmailDeliveryError:
            return Response(
                {'detail': 'Unable to send contact notification right now.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({'detail': 'Contact request sent.'}, status=status.HTTP_202_ACCEPTED)
