from typing import List, Type

from django.db import models
from enumfields import Enum, EnumField


class Tag(models.Model):
    tag_type_enum: Enum
    model: models.Model

    name = models.CharField(max_length=128, unique=True)
    types: models.ManyToManyField
    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField(blank=True)
    synonyms = models.CharField(blank=True, max_length=1024)
    status: EnumField
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_model(self) -> Type[models.Model]:
        pass

    def get_types_formatted(self) -> List[str]:
        return [type_instance.type.value for type_instance in self.types.all()]

    def count(self) -> int:
        count = 0
        for enum_member in self.tag_type_enum:
            lookup_name = f"tags_{enum_member.value}__in"
            count += self.get_model().objects.filter(**{lookup_name: [self]}).count()
        return count

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
