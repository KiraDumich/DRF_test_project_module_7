from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CoursePaginator, LessonPaginator
from materials.permissions import Owner, Staff
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~Staff,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (Staff | Owner,)
        elif self.action == "destroy":
            self.permission_classes = (~Staff | Owner,)
        return [permission() for permission in self.permission_classes]

    # def get_queryset(self):
    #     if not self.request.user.is_staff:
    #         return Course.objects.filter(owner=self.request.user)
    #     elif self.request.user.is_staff:
    #         return Course.objects.all()

    # def get_serializer_class(self):
    #     if self.action == "retrieve":
    #         return CourseDetailSerializer
    #     return CourseSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~Staff, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (Owner,)
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, Staff | Owner,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, Staff | Owner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, Owner | ~Staff,)


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        sub_item = Subscription.objects.all().filter(user=user).filter(course=course)

        if sub_item.exists():
            sub_item.delete()
            message = 'Подписка отключена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка включена'
        return Response({"message": message})
