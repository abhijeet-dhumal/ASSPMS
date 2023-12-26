from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView,ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from datetime import datetime, timedelta


from services.models import (
    Appointment,
    AppointmentSlot,
    Notification,
    UserRecord
)
from services.serializers import (
    AppointmentSerializer,
    AppointmentSlotSerializer,
    NotificationSerializer,
    UserRecordSerializer
)
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from commons.utils import Util
# API views

class UserRecordAPIView(ModelViewSet):
    queryset = UserRecord.objects.all()
    serializer_class = UserRecordSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notification_service = UserRecord.objects.filter(
            user=self.request.user).order_by('-created_at')

        if notification_service:
            notificationSerializer = UserRecordSerializer(
                notification_service, many=True)
            return Response(notificationSerializer.data, status=status.HTTP_200_OK)
        return Response({'detail': "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        query = UserRecordSerializer(data=request.data)
        if query.is_valid():
            query.create(query.validated_data)
            return Response(query.data, 201)
        return Response(query.errors, 400)

class NotificationAPIView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notification_service = Notification.objects.filter(
            user=self.request.user).order_by('-datetime')

        if notification_service:
            notificationSerializer = NotificationSerializer(
                notification_service, many=True)
            return Response(notificationSerializer.data, status=status.HTTP_200_OK)
        return Response({'detail': "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        query = NotificationSerializer(data=request.data)
        if query.is_valid():
            query.create(query.validated_data)
            return Response(query.data, 201)
        return Response(query.errors, 400)

class AppointmentSlotAPIView(ListCreateAPIView):
    serializer_class = AppointmentSlotSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        professional_user_id = self.request.query_params.get(
            'professional_user_id')
        appointment_slots = AppointmentSlot.objects.all().filter(professional_user=user)
        if len(appointment_slots) != 0:
            return AppointmentSlot.objects.all().filter(
                professional_user=user, date__gte=datetime.now(), date__lte=datetime.now() + timedelta(days=7))
        else:
            if professional_user_id != None:
                return AppointmentSlot.objects.all().filter(professional_user__id=professional_user_id)
            else:
                return AppointmentSlot.objects.all()


class AppointmentAPIView(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # pagination_class = PageNumberPagination
    # PageNumberPagination.page_size = 10
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == "Simple User":
                return Appointment.objects.filter(user=user).order_by('slot__start_time')
            else:
                return Appointment.objects.filter(
                    slot__professional_user=user, is_accepted=None).order_by('slot__start_time')
        else:
            return Appointment.objects.none()

    def create(self, request):
        user = request.user
        try:
            slot_id = request.data['slot_id']
        except:
            return Response({'slot_id': ['This field required!']}, status=status.HTTP_400_BAD_REQUEST)
        try:
            slot_id = int(slot_id)
        except:
            return Response({'slot_id': ['This field must be an integer!']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = request.data['amount']
        except:
            return Response({'amount': ['This field required!']}, status=status.HTTP_400_BAD_REQUEST)
        try:
            amount = float(amount)
        except:
            return Response({'amount': ['This field must be an integer or decimal number!']}, status=status.HTTP_400_BAD_REQUEST)

        slot = get_object_or_404(AppointmentSlot, pk=slot_id)
        is_available = slot.is_available
        if is_available:
            super().create(request)
            slot.is_available = False
            slot.save()
            return Response({'detail': 'Appointment request sent succesfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Appointment request sent already!'}, status=status.HTTP_409_CONFLICT)
