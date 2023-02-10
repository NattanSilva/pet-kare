from rest_framework import serializers


class TraitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    trait_name = serializers.CharField(source="name", max_length=20)
    created_at = serializers.DateTimeField(read_only=True)
