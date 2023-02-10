from groups.models import Group
from traits.models import Trait


def verify_group_existence(group_name: str, new_group: Group) -> Group:
    try:
        group = Group.objects.get(scientific_name__iexact=group_name)
        return group
    except Group.DoesNotExist:
        created_group = Group.objects.create(**new_group)
        return created_group


def verify_trait_existence(trait_name: str, new_trait: Trait) -> Trait:
    try:
        trait = Trait.objects.get(name__iexact=trait_name)
        return trait
    except Trait.DoesNotExist:
        created_trait = Trait.objects.create(**new_trait)
        return created_trait


def trait_includes(value, lista):
    for item in lista:
        if item["name"] == value:
            return True
    return False
