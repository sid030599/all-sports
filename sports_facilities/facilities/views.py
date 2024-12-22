from django.db.models.expressions import RawSQL
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from facilities.models import (
    Gym,
    GymPhoto,
    GymSubscriptionPlan,
    GymFeature,
    GymRatingReview,
    GymMember,
    GymTrainer,
)
from auth_app.serializers import  MemberSerializer, TrainerSerializer
from facilities.serializers import (
    GymSerializer,
    GymPhotoSerializer,
    GymDetailSerializer,
    GymFeatureSerializer,
    GymRatingReviewSerializer,
    GymSubscriptionPlanSerializer,
    
)


class GymListCreateView(APIView):
    """
    Gym create view
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GymSerializer

    def get(self, request):
        gyms = Gym.objects.all()
        serializer = GymSerializer(gyms, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data["owner"] = (
            request.user.id
        )
        serializer = GymSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GymDetailView(APIView):
    """
    Gym Detail View
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GymDetailSerializer

    def get(self, request, pk):
        gym = get_object_or_404(Gym, pk=pk)
        serializer = self.serializer_class(gym)
        return Response(serializer.data)

    def put(self, request, pk):
        gym = get_object_or_404(Gym, pk=pk)
        serializer = self.serializer_class(gym, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        gym = get_object_or_404(Gym, pk=pk)
        gym.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GymPhotoUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
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


class GymsWithinRadiusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "lat",
                type=float,
                description="Latitude of the location from which the radius is calculated",
            ),
            OpenApiParameter(
                "lon",
                type=float,
                description="Longitude of the location from which the radius is calculated",
            ),
            OpenApiParameter("distance", type=float, description="distance"),
        ]
    )
    def get(self, request):
        lat = float(request.query_params.get("lat"))
        lon = float(request.query_params.get("lon"))
        distance = request.query_params.get("distance")

        if not lat or not lon:
            return Response(
                {"error": "Latitude and longitude must be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            distance_formula = """
                6371 * acos(
                    cos(radians(%s)) * cos(radians(latitude)) *
                    cos(radians(longitude) - radians(%s)) +
                    sin(radians(%s)) * sin(radians(latitude))
                )
            """

            gyms = (
                Gym.objects.annotate(distance=RawSQL(distance_formula, (lat, lon, lat)))
                .filter(distance__lte=distance)
                .order_by("distance")
            )

            if not gyms.exists():
                return Response(
                    {"message": "No gyms found within 1 km radius"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = GymSerializer(gyms, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GymSubscriptionPlanView(APIView):
    serializer_class = GymSubscriptionPlanSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "gym_id",
                type=int,
                description="Id of gym for Subscription",
            )
        ]
    )
    def get(self, request):
        subscription_plans = GymSubscriptionPlan.objects.filter(
            gym_id=request.query_params.get("gym_id")
        )
        serializer = GymSubscriptionPlanSerializer(subscription_plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GymRatingReviewView(APIView):
    serializer_class = GymRatingReviewSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "gym_id",
                type=int,
                description="Id of gym for review",
            )
        ]
    )
    def get(self, request):
        reviews = GymRatingReview.objects.filter(
            gym_id=request.query_params.get("gym_id")
        )
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "gym_id",
                type=int,
                description="Id of gym for deletion",
            ),
            OpenApiParameter(
                "review_id",
                type=int,
                description="Id of review for deletion",
            )
        ]
    )
    def delete(self, request):
        try:
            review = GymRatingReview.objects.filter(**request.query_params).first()
            review.delete()
            return Response(
                {"message": "Review deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except GymRatingReview.DoesNotExist:
            return Response(
                {"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )


class GymFeatureView(APIView):
    serializer_class = GymFeatureSerializer
    
    def get(self, request):
        features = GymFeature.objects.all()
        serializer = GymFeatureSerializer(features, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GymMemberView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer


    @extend_schema(
        parameters=[
            OpenApiParameter(
                "gym_id",
                type=int,
                description="Id of gym for member retrieval",
            )
        ]
    )
    def get(self, request):
        """
        Retrieve all members of a gym.
        """
        gym_id = request.query_params.get("gym_id")
        if not gym_id:
            return Response(
                {"error": "Gym ID must be provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        gym_members = Gym.objects.filter(id=gym_id).values_list("gym_members", flat=True)
        member = GymMember.objects.filter(id__in=gym_members)
        serializer = self.serializer_class(member, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Add a new gym member to a specific gym.
        """
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GymTrainerView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrainerSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "gym_id",
                type=int,
                description="Id of gym for trainer retrieval",
            )
        ]
    )
    def get(self, request):
        """
        Retrieve all trainers of a gym.
        """
        gym_id = request.query_params.get("gym_id")
        if not gym_id:
            return Response(
                {"error": "Gym ID must be provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        gym_trainers = Gym.objects.filter(id=gym_id).values_list("trainers", flat=True)
        trainer = GymTrainer.objects.filter(id__in=gym_trainers)
        serializer = self.serializer_class(trainer, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Add a new gym trainer to a specific gym.
        """
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)