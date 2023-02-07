from django.db import models


class PetChoices(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    DEFAULT = "Not Informed"


class Pet(models.Model):
    name =  models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    sex = models.CharField(
        max_length=20,
        choices=PetChoices.choices,
        default=PetChoices.DEFAULT
    )

    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.PROTECT,
        null=False,
        related_name="pets" 
    )

    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="traits"
    )

    def __repr__(self) -> str:
        return f"<Pet ({self.id}) - {self.name}>"