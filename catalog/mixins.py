from django.db import models

class OrderingMixin(models.Model):
    order = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ["order"]
        abstract = True