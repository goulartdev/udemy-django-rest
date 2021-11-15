from rest_framework import serializers
from django.db.models import Avg

from .models import Course, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            "email": {
                "write_only": True,
            }
        }
        model = Review
        fields = (
            "id",
            "course",
            "name",
            "email",
            "comment",
            "rating",
            "created_date",
            "updated_date",
            "is_active",
        )


class CourseSerializer(serializers.ModelSerializer):

    # Nested relationship
    # reviews = ReviewSerializer(many=True, read_only=True)

    # Hyperlinked related field
    # reviews = serializers.HyperlinkedRelatedField(
    #     many=True, read_only=True, view_name="review-detail"
    # )

    # primary key related field
    # reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "slug",
            "created_date",
            "updated_date",
            "is_active",
            "average_rating",
            # "reviews",
        )


    def get_average_rating(self, obj):
        return round(obj.reviews.aggregate(Avg('rating')).get('rating__avg') or 0, 2)
