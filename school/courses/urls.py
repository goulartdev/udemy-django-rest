from django.urls import path
from rest_framework.routers import SimpleRouter

from .views.views_v1 import CourseApiView, ReviewApiView, CoursesApiView, ReviewsApiView
from .views.views_v2 import CourseViewSet, ReviewViewSet


router = SimpleRouter()

## API V2
router.register("courses", CourseViewSet)
router.register("reviews", ReviewViewSet)

## API V1
urlpatterns = [
    path("courses/", CoursesApiView.as_view(), name="courses"),
    path("courses/<slug:slug>", CourseApiView.as_view(), name="course"),
    path(
        "courses/<slug:slug>/reviews/", ReviewsApiView.as_view(), name="course_reviews"
    ),
    path(
        "courses/<slug:slug>/reviews/<int:pk>/",
        ReviewApiView.as_view(),
        name="course_review",
    ),
    path("reviews/", ReviewsApiView.as_view(), name="reviews"),
    path("reviews/<int:pk>", ReviewApiView.as_view(), name="review"),
]
