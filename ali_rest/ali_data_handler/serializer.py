from rest_framework import serializers
from .models import CompanySell

class CompanySellSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySell
        fields = [
            'data',
        ]