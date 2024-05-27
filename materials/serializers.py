from rest_framework import serializers
from materials.models import Lesson, Course
from rest_framework.serializers import SerializerMethodField

from users.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    course_lesson_count = SerializerMethodField()
    course_lessons = SerializerMethodField()

    def get_course_lessons(self, course):
        lessons_set = Lesson.objects.filter(course=course.id)
        return [(lesson.lesson_name, lesson.lesson_description, lesson.lesson_url, lesson.owner) for lesson in
                lessons_set]

    def get_course_lesson_count(self, course):
        lesson_set = Lesson.objects.filter(course=course.id)
        return lesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'
