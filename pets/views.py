# import ipdb
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Request, Response, status

from groups.models import Group
from traits.models import Trait

from .models import Pet
from .serializers import PetSerializer
from .utils import (trait_includes, verify_group_existence,
                    verify_trait_existence)


class PetView(APIView, PageNumberPagination):
    def get(self, req: Request) -> Response:
        pets = Pet.objects.all()
        trait_name_param = req.query_params.get("trait", None)

        if trait_name_param:
            trait = get_object_or_404(Trait, name=trait_name_param)
            pets_filtred = Pet.objects.filter(traits=trait).all()
            result_page = self.paginate_queryset(pets_filtred, req)
            serializer = PetSerializer(result_page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            result_page = self.paginate_queryset(pets, req)
            serializer = PetSerializer(result_page, many=True)
            return self.get_paginated_response(serializer.data)

    def post(self, req: Request) -> Response:
        serializer = PetSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group")
        traits_data = serializer.validated_data.pop("traits", None)
        pet_data = serializer.validated_data

        current_group = verify_group_existence(
            group_data["scientific_name"],
            group_data
        )

        created_pet = Pet.objects.create(**pet_data, group=current_group)

        if traits_data:
            for item in traits_data:
                current_trait = verify_trait_existence(item["name"], item)
                created_pet.traits.add(current_trait)

        serialized_result = PetSerializer(created_pet)
        # ipdb.set_trace()
        return Response(
            serialized_result.data,
            status.HTTP_201_CREATED
        )


class PetDetailView(APIView):
    def get(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, req: Request, pet_id) -> Response:
        pet = get_object_or_404(Pet, id=int(pet_id))
        serializer = PetSerializer(data=req.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Separar os dados
        group_data = serializer.validated_data.pop("group", None)
        traits_data = serializer.validated_data.pop("traits", None)
        pet_data = serializer.validated_data

        for key, value in pet_data.items():
            setattr(pet, key, value)
        pet.save()

        if group_data:
            current_group = verify_group_existence(
                group_name=group_data["scientific_name"],
                new_group=group_data
            )
            pet.group = current_group
            pet.save()

        if traits_data:
            pet.traits.clear()
            for item in traits_data:
                current_trait = verify_trait_existence(
                    trait_name=item["name"],
                    new_trait=item
                )
                pet.traits.add(current_trait)
                pet.save()

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
