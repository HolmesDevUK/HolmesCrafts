from django.db import models

# Create your models here.

class Notebook(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    theme = models.CharField(max_length=100)
    page_img = models.CharField(max_length=100)
    front_img = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    code = models.CharField(max_length=20, null=True, unique=True)

    def __str__(self):
        return f"{self.name} ({self.size})"
    
class NotebookImg(models.Model):
    notebook = models.OneToOneField(Notebook, on_delete=models.CASCADE, related_name="images")
    open_cover = models.ImageField(upload_to="images")
    front_cover = models.ImageField(upload_to="images")
    back_cover = models.ImageField(upload_to="images")
    inside_front = models.ImageField(upload_to="images")
    inside_back = models.ImageField(upload_to="images")
    middle = models.ImageField(upload_to="images")
    zoom_middle = models.ImageField(upload_to="images")

    def __str__(self):
        return f"{self.notebook} images"
    
    class Meta:
        verbose_name_plural = "Notebook images"

class Card(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    in_store = models.BooleanField(default=True)
    has_variants = models.BooleanField(default=False)
    card_type = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True, unique=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class CardImg(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE, related_name="images")
    wide_img = models.ImageField(upload_to="images", null=True, blank=True)
    tall_img = models.ImageField(upload_to="images", null=True, blank=True)
    small_img = models.ImageField(upload_to="images", null=True, blank=True)
    inside_img = models.ImageField(upload_to="images", null=True, blank=True)

    def __str__(self):
        return f"{self.card} images"
    
    class Meta:
        verbose_name_plural = "Card images"

class CardVariant(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="variants")
    variant_name = models.CharField(max_length=100)
    variant_img = models.ImageField(upload_to="images")

    def __str__(self):
        return f"{self.card} ({self.variant_name})"

    class Meta:
        verbose_name_plural = "Card variants"    


class Navbar(models.Model):
    page_name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    is_card = models.BooleanField()
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    def __str__(self):
        return self.page_name

    class Meta:
        verbose_name_plural = "Navbar pages"            
        

