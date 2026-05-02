from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status

from .serializers import RegisterSerializer


@extend_schema(
    tags=['Authentication'],
    request=RegisterSerializer,
    responses={
        201: RegisterSerializer,
        400: OpenApiResponse(description='Validation error'),
    },
    description='Register a new user with email and password.',
)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def get_success_headers(self, data):
        return {}

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response
