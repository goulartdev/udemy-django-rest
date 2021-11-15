from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework import permissions

from school.decorators.paginate import paginate

from ..models import Course, Review
from ..serializers import CourseSerializer, ReviewSerializer


class CourseViewSet(ModelViewSet):
    # permission_classes = (permissions.DjangoModelPermissions, )
    queryset = Course.objects.all()
    lookup_field = "slug"
    serializer_class = CourseSerializer

    @paginate(ReviewSerializer)
    @action(detail=True, methods=["get"])
    def reviews(self, request, slug):
        return self.get_object().reviews.all()


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
