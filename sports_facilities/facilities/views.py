from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Gym, GymPhoto
from .serializers import GymSerializer, GymPhotoSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser


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


class GymPhotoUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # To handle file uploads
    serializer_class = GymPhotoSerializer
    
    def post(self, request, gym_id):
        try:
            gym = Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            return Response(
                {"error": "Gym not found"}, status=status.HTTP_404_NOT_FOUND
            )

        photo = request.FILES.get("photo")
        if not photo:
            return Response(
                {"error": "No photo provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        gym_photo = GymPhoto.objects.create(gym=gym, photo=photo)
        serializer = GymPhotoSerializer(gym_photo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


from django.db import connection
from django.db.models.expressions import RawSQL
from drf_spectacular.utils import extend_schema, OpenApiParameter

class GymsWithinRadiusView(APIView):
    permission_classes = [IsAuthenticated]

    
    @extend_schema(
        parameters=[
            OpenApiParameter('lat', type=float, description='Latitude of the location from which the radius is calculated'),
            OpenApiParameter('lon', type=float, description='Longitude of the location from which the radius is calculated'),
            OpenApiParameter('distance', type=float, description='distance'),
        ]
    )
    def get(self, request):
        lat = float(request.query_params.get('lat'))
        lon = float(request.query_params.get('lon'))
        distance = request.query_params.get('distance')

        if not lat or not lon:
            return Response({"error": "Latitude and longitude must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            distance_formula = """
                6371 * acos(
                    cos(radians(%s)) * cos(radians(latitude)) *
                    cos(radians(longitude) - radians(%s)) +
                    sin(radians(%s)) * sin(radians(latitude))
                )
            """

            gyms = Gym.objects.annotate(
                distance=RawSQL(distance_formula, (lat, lon, lat))
            ).filter(distance__lte=distance).order_by('distance')
            
            if not gyms.exists():
                return Response({"message": "No gyms found within 1 km radius"}, status=status.HTTP_404_NOT_FOUND)

            serializer = GymSerializer(gyms, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

