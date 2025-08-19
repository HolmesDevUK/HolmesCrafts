from django.db import models


class Navbar(models.Model):
    page_name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    is_card = models.BooleanField()
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.page_name

    class Meta:
        verbose_name_plural = "Navbar pages"   