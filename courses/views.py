from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import permissions
from .models import Course
from accounts.models import Account
from contents.models import Content
from .serializers import CourseSerializer, PutCourseSerializer
from contents.serializers import ContentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import HavePermission, IsAccountOwner, HaveUserPermission


class CourseView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HavePermission]

    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Course.objects.all()

        userCourses = Account.objects.get(pk=self.request.user.id)
        return userCourses.my_courses


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HavePermission]

    serializer_class = CourseSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'course_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Course.objects.all()

        userCourses = Account.objects.get(pk=self.request.user.id)
        return userCourses.my_courses


class ContentView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HavePermission]

    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_id'])


class ContentDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HaveUserPermission]

    serializer_class = ContentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'content_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Content.objects.all()

        userContents = Content.objects.filter(course__contents=self.kwargs['content_id'])
        return userContents

    def get_object(self):
        if permissions.SAFE_METHODS:
            content = Content.objects.filter(pk=self.kwargs['content_id']).first()
            course = Course.objects.filter(pk=self.kwargs['course_id']).exists()
            if not content:
                raise NotFound({'detail': 'content not found.'})
            if not course:
                raise NotFound({'detail': 'course not found.'})
        return super().get_object()


class StudentsView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = Course.objects.all()
    serializer_class = PutCourseSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'course_id'

    def get_object(self):
        try:
            Account.objects.get(email=self.request.data['students_courses'][0]['student_email'])
            course = Course.objects.get(pk=self.kwargs['course_id'])
            return course
        except Account.DoesNotExist:
            raise ParseError({'detail': f'No active accounts was found: {self.request.data["students_courses"][0]["student_email"]}.'})

    def perform_update(self, serializer):
        user = Account.objects.get(email=self.request.data['students_courses'][0]['student_email'])
        course = Course.objects.get(pk=self.kwargs['course_id'])
        course.students.add(user)
