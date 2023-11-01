from .models import Author
from rest_framework import serializers


class AuthorListSerializer(serializers.ModelSerializer):
    """serializer for recipes"""

    class Meta:
        model = Author
        fields = ['id', 'name']
        read_only_fields = ['id']
