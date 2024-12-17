from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Gym, Member
from .serializers import GymSerializer, MemberSerializer
from django.shortcuts import get_object_or_404


# Gym List & Create View (for authenticated users)
class GymListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GymSerializer
    
    def get(self, request):
        gyms = Gym.objects.all()
        serializer = GymSerializer(gyms, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Automatically associate the gym with the logged-in owner (user)
        request.data["owner"] = (
            request.user.id
        )  # Set the owner field to the logged-in user
        serializer = GymSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Gym Detail View (for authenticated owners and admins)
class GymDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GymSerializer

    def get(self, request, pk):
        gym = get_object_or_404(Gym, pk=pk)
        serializer = GymSerializer(gym)
        return Response(serializer.data)

    def put(self, request, pk):
        gym = get_object_or_404(Gym, pk=pk)
        serializer = GymSerializer(gym, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        gym = get_object_or_404(Gym, pk=pk)
        gym.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)