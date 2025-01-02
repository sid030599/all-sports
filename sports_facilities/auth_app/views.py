from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema, OpenApiParameter


from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from auth_app.openApi.utils import AuthOpenApiRequest

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT tokens.
    Extends the default behavior of TokenObtainPairView.
    """

    @extend_schema(
        methods=["POST"],
        request={
            "application/json": {
                "type": "object",
                "properties": AuthOpenApiRequest.Token.value,
            },
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view for refreshing JWT tokens.
    Extends the default behavior of TokenRefreshView.
    """

    @extend_schema(
        methods=["POST"],
        request={
            "application/json": {
                "type": "object",
                "properties": AuthOpenApiRequest.Token.value,
            },
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class UserListAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "role",
                type=str,
                description="Filter users by role",
            ),
        ]
    )
    def get(self, request):
        role = request.query_params.get("role")
        if role:
            users = CustomUser.objects.filter(role=role)
        else:
            users = CustomUser.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")
        
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
