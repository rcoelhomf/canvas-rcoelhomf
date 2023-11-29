from django.urls import path
from .views import CourseView, CourseDetailView, ContentView, ContentDetailView, StudentsView

urlpatterns = [
    path('courses/', CourseView.as_view()),
    path('courses/<course_id>/', CourseDetailView.as_view()),
    path('courses/<course_id>/contents/', ContentView.as_view()),
    path('courses/<course_id>/contents/<content_id>/', ContentDetailView.as_view()),
    path('courses/<course_id>/students/', StudentsView.as_view()),
]
