from rest_framework import serializers

class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    serviceType = serializers.CharField(required=False, allow_blank=True)
    availability = serializers.CharField(required=False, allow_blank=True)
    message = serializers.CharField(required=False, allow_blank=True)
