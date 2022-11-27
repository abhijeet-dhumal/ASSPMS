from time import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from services.forms import AppointmentForm, AppointmentSlotForm, UserRecordForm
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView,ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse

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
        return Notification.objects.filter(created_by=request.user).all()

from django.shortcuts import render
from django.db.models import Q  # New
class UserRecordsListView(ListView):
    model = UserRecord
    template_name = 'services/user_record_list.html'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        request = self.request
        search_post = request.GET.get('search')
        if search_post:
            posts = UserRecord.objects.filter(Q(created_by__email__icontains=search_post) | Q(licenseplatetext__icontains=search_post) | Q(status__icontains=search_post)).order_by('-created_at')
        else:
            # If not searched, return default posts
            posts = UserRecord.objects.filter(created_by=request.user).order_by('-created_at')
        return posts

class AppointmentSlotsListView(ListView):
    model = AppointmentSlot
    template_name = 'services/appointment_slots.html'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        request = self.request
        search_post = request.GET.get('search')
        if search_post:
            posts = AppointmentSlot.objects.filter(Q(created_by__email__icontains=search_post) | Q(date__icontains=search_post) | Q(is_verified__icontains=search_post)).order_by('-created_at')
        else:
            # If not searched, return default posts
            posts = AppointmentSlot.objects.filter(created_by=request.user).order_by('-created_at')
        return posts


class UserRecordsCreateView(CreateView):
    model = UserRecord
    template_name = 'services/user_records.html'
    permission_classes = (IsAuthenticated,)
    fields="__all__"


from services.code.prediction import license_plate_text_detection
def UserRecordUpdate(request,pk):
    instance = get_object_or_404(UserRecord, id=pk)
    recordform=UserRecordForm(instance=instance)
    if request.method=='POST':
        recordform=UserRecordForm(request.POST, request.FILES, instance=instance)
        if recordform.is_valid():
            recordform.save()
            instance.updated_at=timezone.now()
            if instance.vehicle_image:
                img_url=instance.vehicle_image.url
                text=str(img_url)[1:]
                print(text)
                texts=list()
                for template in license_plate_text_detection(text):
                    texts.append(template['prediction'][0]['ocr_text'])
                instance.licenseplatetext=texts[0]
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

from django.urls import reverse
class AppointmentSlotCreateView(CreateView):
    model = AppointmentSlot
    template_name = 'services/user_records.html'
    form_class= AppointmentSlotForm
    permission_classes = (IsAuthenticated,)

    def get_success_url(self):
        return reverse('user_appointment_slots')

def AppointmentSlotUpdate(request,pk):
    instance = get_object_or_404(AppointmentSlot, id=pk)
    recordform=AppointmentSlotForm(instance=instance)

    if request.method=='POST':
        recordform=AppointmentSlotForm(request.POST,request.FILES,instance=instance)
        if recordform.is_valid():
            recordform.save()
            return redirect('user_appointment_slots')
        else:
            return HttpResponse(request,"Appointment slot already booked or enter valid details !!!")
    
    context={'recordform':recordform,'record':instance}
    return render(request,"services/user_record_update.html",context)


def AppointmentSlotDelete(request,pk):
    userdetails=AppointmentSlot.objects.get(id=pk)
    if request.method == 'POST':
        userdetails.delete()
        return redirect('user_appointment_slots')
    return render(request,'services/delete.html', {'object': userdetails})


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'services/appointments.html'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        request = self.request
        search_post = request.GET.get('search')
        if search_post:
            posts = Appointment.objects.filter(Q(created_by__email__icontains=search_post) | Q(slot__icontains=search_post) | Q(is_paid__icontains=search_post)| Q(amount__icontains=search_post)).order_by('-created_at')
        else:
            # If not searched, return default posts
            posts = Appointment.objects.filter(created_by=request.user).order_by('-created_at')
        return posts
        
class AppointmentCreateView(CreateView):
    model = Appointment
    template_name = 'services/user_records.html'
    form_class= AppointmentForm
    permission_classes = (IsAuthenticated,)

    def get_success_url(self):
        return reverse('user_appointments')


def AppointmentUpdate(request,pk):
    instance = get_object_or_404(Appointment, id=pk)
    recordform=AppointmentForm(instance=instance)

    if request.method=='POST':
        recordform=AppointmentForm(request.POST,request.FILES,instance=instance)
        if recordform.is_valid():
            recordform.save()
            instance.updated_at=timezone.now()
            instance.save()
            return redirect('user_appointments')
        else:
            messages.warning(request,f'Please enter valid details !!! ')
    
    context={'recordform':recordform,'record':instance}
    return render(request,"services/user_record_update.html",context)


def AppointmentDelete(request,pk):
    userdetails=Appointment.objects.get(id=pk)
    if request.method == 'POST':
        userdetails.delete()
        return redirect('user_appointments')
    return render(request,'services/delete.html', {'object': userdetails})
