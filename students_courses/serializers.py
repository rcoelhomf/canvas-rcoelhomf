from rest_framework import serializers
from .models import StudentCourse


class AccountPutSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)

    class Meta:
        model = StudentCourse
        fields = ['id', 'student_id', 'student_username', 'student_email', 'status']
        read_only_fields = ['student_username']
