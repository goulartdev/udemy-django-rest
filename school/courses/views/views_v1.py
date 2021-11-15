from django.shortcuts import get_object_or_404
from rest_framework import generics

from ..models import Course, Review
from ..serializers import CourseSerializer, ReviewSerializer


class CoursesApiView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseApiView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "slug"
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class ReviewsApiView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        course_slug = self.kwargs.get("slug")

        if course_slug:
            queryset = queryset.filter(course__slug=course_slug)

        return queryset


class ReviewApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object(self):
        kwargs = {
            "pk": self.kwargs.get("pk"),
        }

        course_slug = self.kwargs.get("slug")

        if course_slug:
            kwargs["course__slug"] = course_slug

        return get_object_or_404(self.get_queryset(), **kwargs)
