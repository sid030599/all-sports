from django.db import models
from auth_app.models import CustomUser


class Gym(models.Model):
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="gyms",
        limit_choices_to={"role": "owner"},
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1028, blank=True, null=True)
    address = models.JSONField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    price_range = models.CharField(max_length=50, blank=True, null=True)
    equipment = models.JSONField(blank=True, null=True)
    logo = models.ImageField(upload_to="gym_logos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.FloatField(default=0.0)
    review_count = models.PositiveIntegerField(default=0)

    def update_rating(self):
        """
        Update the average_rating and review_count for the gym.
        """
        ratings = self.ratings_reviews.aggregate(
            avg=models.Avg("rating"), count=models.Count("rating")
        )
        self.average_rating = round(ratings["avg"],2) or 0.0
        self.review_count = ratings["count"] or 0
        self.save()

    def __str__(self):
        return self.name


class GymPhoto(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField(upload_to="gym_photos/")
    video = models.FileField(upload_to="gym_videos/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.gym.name}"


class GymTrainer(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="trainer_profile",
        limit_choices_to={"role": "trainer"},
    )
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="trainers")
    specialization = models.CharField(max_length=255, null=True, blank=True)
    certification = models.TextField(null=True, blank=True)
    years_of_experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Trainer at {self.gym.name}"
    
    class Meta:
        unique_together = ("user", "gym")


class GymFeature(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class GymSubscriptionPlan(models.Model):
    gym = models.ForeignKey(
        Gym, on_delete=models.CASCADE, related_name="subscription_plans"
    )
    plan_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField(GymFeature)
    offers = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.plan_name} - {self.gym.name}"

class GymMember(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="member_profile",
        limit_choices_to={"role": "member"},
    )
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="gym_members")
    subscription_plan = models.CharField(max_length=50)
    subscription_plan_new = models.ForeignKey(GymSubscriptionPlan, on_delete=models.CASCADE, related_name="gym_members", default=1)
    subscription_start_date = models.DateField()
    subscription_end_date = models.DateField()
    subscription_type = models.CharField(
        max_length=50, choices=[("monthly", "Monthly"), ("yearly", "Yearly")]
    )
    goals = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Member at {self.gym.name}"
    
    class Meta:
        unique_together = ("user", "gym")


class GymRatingReview(models.Model):
    gym = models.ForeignKey(
        Gym, on_delete=models.CASCADE, related_name="ratings_reviews"
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="ratings_reviews",
        limit_choices_to={"role": "member"},
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    )
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("gym", "user")

    def __str__(self):
        return f"{self.user.username} - {self.gym.name} ({self.rating} stars)"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the review first
        self.gym.update_rating() 
