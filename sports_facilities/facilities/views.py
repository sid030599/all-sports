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
    GymIdValidationSerializer,
    GymPhotoSerializer,
    GymDetailSerializer,
    GymFeatureSerializer,
    GymRatingReviewSerializer,
    GymSubscriptionPlanSerializer,
    
)
from facilities.filters import GymFilter


class GymListView(APIView):
    """
    Gym create view
    """

    serializer_class = GymSerializer
    filter_class = GymFilter
    queryset = Gym.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=str,
                description="name of the gym",
            ),
            OpenApiParameter(
                "address",
                type=str,
                description="city of the gym",
            ),
        ]
    )
    def get(self, request):
        
        gym_queryset = self.filter_class(
            self.request.GET, queryset=self.queryset
        ).qs
        serializer = self.serializer_class(gym_queryset, many=True)
        return Response(serializer.data)


class GymDetailView(APIView):
    """
    Gym Detail View
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GymDetailSerializer
    validation_serializer = GymIdValidationSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "gym_id",
                type=float,
                description="id for fetching the gym details",
            ),
        ]
    )
    def get(self, request):
        validation_serializer = self.validation_serializer(data=request.query_params)
        validation_serializer.is_valid(raise_exception=True)
        gym_id = validation_serializer.validated_data.get("gym_id")
        gym = Gym.objects.filter(id=gym_id).first()
        serializer = self.serializer_class(gym)
        return Response(serializer.data)
    
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        parameters=[
            OpenApiParameter(
                "gym_id",
                type=float,
                description="id for updating the gym details",
            ),
        ]
    )
    def put(self, request, pk):
        gym_id = request.query_params.get("gym_id")
        gym = get_object_or_404(Gym, pk=gym_id)
        serializer = self.serializer_class(gym, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        gym = get_object_or_404(Gym, pk=pk)
        gym.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GymPhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    validation_serializer = GymIdValidationSerializer
    serializer_class = GymPhotoSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "gym_id",
                type=float,
                description="id for fetching the gym details",
            ),
        ]
    )
    def get(self, request):
        validation_serializer = self.validation_serializer(data=request.query_params)
        validation_serializer.is_valid(raise_exception=True)
        gym_id = validation_serializer.validated_data.get("gym_id")
        gym_photos = GymPhoto.objects.filter(gym_id=gym_id)
        serializer = self.serializer_class(gym_photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'gym': {'type': 'integer'},
                    'photo': {'type': 'string', 'format': 'binary'},
                    'video': {'type': 'string', 'format': 'binary'},
                    'description': {'type': 'string'},
                },
                'required': ['gym', 'photo'],
            }
        },
        responses=GymPhotoSerializer,
    )
    def post(self, request):
        # Use a single serializer to handle validation and creation
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
        serializer = self.serializer_class(data=data, context={'request': request})
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
        serializer = self.serializer_class(data=data, context={'request': request})
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
        serializer = self.serializer_class(data=request.data, context={'request': request})
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
        serializer = self.serializer_class(data=data, context={'request': request})

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
        serializer = self.serializer_class(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
