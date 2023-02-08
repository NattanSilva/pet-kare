from rest_framework import serializers

from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer

from .models import PetChoices


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.DecimalField(max_digits=8, decimal_places=2)
    sex = serializers.ChoiceField(
        choices=PetChoices.choices,
        default=PetChoices.DEFAULT,
    )

    group = GroupSerializer()
    traits = TraitSerializer(many=True, read_only=True)