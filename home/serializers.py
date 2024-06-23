from rest_framework import serializers
from .models import SmileCenter
from .models import Zone
from .models import Service
from .models import CenterType

class SmileCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmileCenter
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'zone']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class CenterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterType
        fields = '__all__'
        extra_kwargs = {
            'center_type_name': {'help_text': 'The name of the center type'},
        }