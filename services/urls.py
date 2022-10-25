from django.urls import path, re_path
from services.fe_views import *
from services import fe_views
from services.views import (
    AppointmentAPIView,
    AppointmentSlotAPIView,
    NotificationAPIView,
    UserRecordAPIView
)

urlpatterns = [
    # FE endpoints
    path('user_records',UserRecordsListView.as_view(), name='user_records'),
    path('user_record_create',UserRecordsCreateView.as_view(), name='user_record_create'),
    path('user_record_update/<int:pk>/',fe_views.UserRecordUpdate, name='user_record_update'),
    path('user_record_delete/<int:pk>/',fe_views.UserRecordDelete, name='user_record_delete'),

    path('user_notifications', NotificationListView.as_view(),
         name='user_notifications'),

    # API endpoints 
    path('parking_appointments', AppointmentAPIView.as_view(
        {'get': 'list', 'post': 'create'}), name='appointments'),
    path('parking_appointments/<int:pk>', AppointmentAPIView.as_view(
        {'get': 'retrieve', 'patch': 'partial_update'}), name='appointment'),
    path('parking_appointment_slots', AppointmentSlotAPIView.as_view(),
         name='appointment_slots'),
    path('notifications', NotificationAPIView.as_view(),
         name='notifications')
]
