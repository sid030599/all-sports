import django_filters
from facilities.models import Gym


class GymFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    address = django_filters.CharFilter(
        field_name="address__city", lookup_expr="icontains"
    )
    owner = django_filters.CharFilter(
        field_name="owner__username", lookup_expr="icontains"
    )
    standard = django_filters.CharFilter(lookup_expr="icontains")
    min_average_rating = django_filters.NumberFilter(
        field_name="average_rating", lookup_expr="gte"
    )
    review_count = django_filters.NumberFilter(
        field_name="review_count", lookup_expr="gte"
    )

    class Meta:
        model = Gym
        fields = [
            "name",
            "owner",
            "standard",
            "average_rating",
            "address",
            "review_count",
        ]
