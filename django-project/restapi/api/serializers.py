from rest_framework import serializers
from .models import users
class userstojson(serializers.ModelSerializer):

    class Meta:
        model=users
        fields="__all__"