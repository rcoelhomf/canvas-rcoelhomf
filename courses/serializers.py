from rest_framework import serializers
from students_courses.serializers import AccountPutSerializer
from contents.serializers import ContentSerializer
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'status', 'start_date', 'end_date', 'instructor', 'contents', 'students_courses']
        extra_kwargs = {'students_courses': {'source': 'students'}}


class PutCourseSerializer(serializers.ModelSerializer):
    students_courses = AccountPutSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'students_courses']
        depth = 1
        read_only_fields = ['id', 'name']
