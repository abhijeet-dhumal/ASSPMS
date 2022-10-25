from time import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from services.forms import UserRecordForm
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView,ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.utils import timezone

from services.models import (
    Appointment,
    AppointmentSlot,
    Notification,
    UserRecord
)

from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView,DeleteView

from django.urls import reverse_lazy
# FE views
class NotificationListView(ListView):
    model = Notification
    template_name = 'services/notifications.html'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Notification.objects.filter(user=request.user).all()

class UserRecordsListView(ListView):
    model = UserRecord
    template_name = 'services/user_record_list.html'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return UserRecord.objects.filter(user=request.user).all()


class UserRecordsCreateView(CreateView):
    model = UserRecord
    template_name = 'services/user_records.html'
    permission_classes = (IsAuthenticated,)
    fields="__all__"

class UserRecordFormView(FormView):
    model = UserRecord
    template_name = 'services/user_records.html'
    success_url = reverse_lazy('user_records') 
    form_class=UserRecordForm

    def form_valid(self, form):
        record = form.save(commit=False)
        record.save()
        data = form.cleaned_data
        UserRecord.objects.update_or_create(entry_time=data['entry_time'],
        exit_time=data['exit_time'],
        status=data['status'],
        license_plate_text=data['license_plate_text'],
        parking_slot_details=data['parking_slot_details']
        ) 
        return redirect('user_records')

from PIL import Image
import base64
from io import BytesIO
from urllib.request import urlopen
from services.code.prediction import license_plate_text_detection
def UserRecordUpdate(request,pk):
    instance = get_object_or_404(UserRecord, id=pk)
    recordform=UserRecordForm(request.POST or None, instance=instance)

    if recordform.is_valid():
        recordform.save()
        instance.updated_at=timezone.now()
        # print(instance.updated_at)
        # img = open('','rb')
        img_url=instance.vehicle_image.url
        text=str(img_url)[1:]
        print(text)
        texts=list()
        for template in license_plate_text_detection(text):
            texts.append(template['prediction'][0]['ocr_text'])
        instance.license_plate_text=texts[0]
        print(f'Found texts in this image are : {texts}')
        instance.save()
        return redirect('user_records')
    
    context={'recordform':recordform,'record':instance}
    return render(request,"services/user_record_update.html",context)


def UserRecordDelete(request,pk):
    userdetails=UserRecord.objects.get(id=pk)
    if request.method == 'POST':
        userdetails.delete()
        return redirect('user_records')
    return render(request,'services/delete.html', {'object': userdetails})
