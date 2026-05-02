from django.db import models
from common.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name