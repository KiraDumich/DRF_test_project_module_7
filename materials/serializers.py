from rest_framework import serializers
from materials.models import Lesson, Course, Subscription
from rest_framework.serializers import SerializerMethodField

from materials.validators import UrlValidator
from users.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='lesson_url')]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    course_lesson_count = SerializerMethodField()
    course_lessons = SerializerMethodField()
    subscription = SerializerMethodField()

    def get_subscription(self, instance):
        user = self.context['request'].user
        return Subscription.objects.all().filter(user=user).filter(course=instance).exists()

    # def get_sub_course(self, course):
    #     sub_set = Subscription.objects.filter(course=course.id)
    #     if sub_set.user == self.request.user:
    #         return "Подписан на обновления курса"
    #     else:
    #         return "Не подписан на обновления курса"

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


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
