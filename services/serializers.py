from django.shortcuts import get_object_or_404
from rest_framework import serializers
from account.serializers import UserSerializer
from services.models import Appointment, AppointmentSlot, Notification, UserRecord
from account.models import User
from account.utils import Util

class UserRecordSerializer(serializers.ModelSerializer):
    vehicle_image_data = serializers.JSONField(
        write_only=True, required=False, allow_null=True)
    license_plate_image_data = serializers.JSONField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = UserRecord
        fields = "__all__"

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user

        if 'vehicle_image_data' in validated_data:
            vehicle_image_data = validated_data.pop('vehicle_image_data')
            validated_data['vehicle_image'] = Util.base64_to_file(vehicle_image_data)

        if 'license_plate_image_data' in validated_data:
            license_plate_image_data = validated_data.pop('license_plate_image_data')
            validated_data['license_plate_image'] = Util.base64_to_file(license_plate_image_data)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['created_by'] = self.context['request'].user
        
        if 'vehicle_image_data' in validated_data:
            vehicle_image_data = validated_data.pop('vehicle_image_data')
            validated_data['vehicle_image'] = Util.base64_to_file(vehicle_image_data)

        if 'license_plate_image_data' in validated_data:
            license_plate_image_data = validated_data.pop('license_plate_image_data')
            validated_data['license_plate_image'] = Util.base64_to_file(license_plate_image_data)
        
        return super().update(instance, validated_data)


class AppointmentSlotSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = AppointmentSlot
        fields = "__all__"
        extra_kwargs = {
            'is_available': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        user = get_object_or_404(
            User, pk=validated_data.pop('user_id'))
        validated_data['user'] = user
        return super().create(validated_data)


class AppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    slot = AppointmentSlotSerializer(read_only=True)
    slot_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
        extra_kwargs = {
            'amount': {'required': True},
            'is_paid': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['slot'] = get_object_or_404(
            AppointmentSlot, pk=validated_data.pop('slot_id'))
        return super().create(validated_data)

class NotificationSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
