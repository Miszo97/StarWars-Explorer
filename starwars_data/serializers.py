from rest_framework import serializers
from starwars_data.models import Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'file_name', 'created_at')