from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .urls import urlpatterns
from .models import Course
from .serializers import CourseSerializer

headers = { 'Authorization': 'Token ' }

class CourseTest(APITestCase, URLPatternsTestCase):
    urlpatterns = urlpatterns

    def setUp(self) -> None:
        super(CourseTest, self).setUp()
        
        self.course_1 = Course.objects.create(title='test course 1')
        self.course_2 = Course.objects.create(title='test course 2')
        self.course_3 = Course.objects.create(title='test course 3')

        auth = {
            'username': 'test_1', 
            'password': '123#asdE',
        }

        user = User.objects.create_user(**auth)

        refresh = RefreshToken.for_user(user)

        self.token = str(refresh.access_token)


    def test_list_courses(self):
        print('Should be able to list all courses')

        with self.subTest():
            response = self.client.get(reverse('courses'))

            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['results'], serializer.data)

    def test_create_course_not_authenticated(self):
        print('Should not be able to create a course if not authenticated')

        with self.subTest():
            response = self.client.post(reverse('courses'), {
                'title': 'test course 4'
            }, format='json')

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_course_authenticated(self):
        print('Should be able to create a course if authenticated')

        with self.subTest():
            
            title = 'test course 4'

            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

            response = self.client.post(reverse('courses'), {
                'title': title
            }, format='json', )

            course = Course.objects.get(title=title)
            serializer = CourseSerializer(course, many=False)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, serializer.data)


    def test_view_course(self):
        print('Should be able to view a course')

        with self.subTest():
            response = self.client.get(
                reverse('course', kwargs={ 'slug': self.course_1.slug }))
            
            serializer = CourseSerializer(self.course_1, many=False)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)


    def test_edit_course_not_authenticated(self):
        print('Should not be able to edit a course if not authenticated')

        with self.subTest():
            new_title = f'{self.course_1}_edited'

            response = self.client.put(
                reverse('course', kwargs={ 'slug': self.course_1.slug }),
                data={ 'title': new_title }, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  


    def test_edit_course_authenticated(self):
        print('Should be able to edit a course if authenticated')

        with self.subTest():
            new_title = f'{self.course_1}_edited'

            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

            response = self.client.put(
                reverse('course', kwargs={ 'slug': self.course_1.slug }),
                data={ 'title': new_title }, format='json')
            
            course = Course.objects.get(title=new_title)
            serializer = CourseSerializer(course, many=False)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)


    def test_delete_course_not_authenticated(self):
        print('Should not be able to delete a course if not authenticated')

        with self.subTest():
            response = self.client.delete(
                reverse('course', kwargs={ 'slug': self.course_1.slug }))
            
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  


    def test_delete_course_authenticated(self):
        print('Should be able to delete a course if authenticated')

        with self.subTest():
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

            response = self.client.delete(
                reverse('course', kwargs={ 'slug': self.course_1.slug }))

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertRaises(Course.DoesNotExist, Course.objects.get, id=self.course_1.id)