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
    
    path('user_appointment_slots', AppointmentSlotsListView.as_view(),
         name='user_appointment_slots'),
    path('user_appointment_slots_create', AppointmentSlotCreateView.as_view(),
         name='user_appointment_slots_create'),  
    path('user_appointment_slots_update/<int:pk>/',fe_views.AppointmentSlotUpdate, name='user_appointment_slots_update'),
    path('user_appointment_slots_delete/<int:pk>/',fe_views.AppointmentSlotDelete, name='user_appointment_slots_delete'),     

    path('user_appointments', AppointmentListView.as_view(),
         name='user_appointments'),
    path('user_appointments_create', AppointmentCreateView.as_view(),
         name='user_appointments_create'),  
    path('user_appointments_update/<int:pk>/',fe_views.AppointmentUpdate, name='user_appointments_update'),
    path('user_appointments_delete/<int:pk>/',fe_views.AppointmentDelete, name='user_appointments_delete'),     

    # API endpoints 
    path('api/user_records', UserRecordAPIView.as_view(
        {'get': 'list', 'post': 'create'}), name='appointments'),
    path('api/parking_appointments', AppointmentAPIView.as_view(
        {'get': 'list', 'post': 'create'}), name='appointments'),
    path('api/parking_appointments/<int:pk>', AppointmentAPIView.as_view(
        {'get': 'retrieve', 'patch': 'partial_update'}), name='appointment'),
    path('api/parking_appointment_slots', AppointmentSlotAPIView.as_view(),
         name='appointment_slots'),
    path('api/notifications', NotificationAPIView.as_view(),
         name='notifications')
]
