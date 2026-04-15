from rest_framework import serializers
from .models import County


class CountyListSerializer(serializers.ModelSerializer):

    """Lightweight serializer for listing all counties"""

    class Meta:
        
        model = County
        
        fields = [
            
            'id', 'code', 'name', 'slug', 'region',
            'population', 'latitude', 'longitude'
        ]


class CountyDetailSerializer(serializers.ModelSerializer):

        """Full serializer for single county detail""" 

        class Meta:

            model = County

            fields = '__all__'
