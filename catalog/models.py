from django.db import models
import os
import uuid
from datetime import datetime

def upload_to(instance, filename):
    
    app_name = instance._meta.app_label
    folder_name = instance.__class__.__name__.lower()
    
    
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    
    date_path = datetime.now().strftime("%Y/%m/%d")
    
    return os.path.join(app_name, folder_name, date_path, filename)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Size(models.Model):

    ORIENTATION = (
        ("portrait", "Portrait"),
        ("landscape", "Landscape")
    )

    name = models.CharField(max_length=20)
    orientation = models.CharField(max_length=10, choices=ORIENTATION)

    def __str__(self):
        return f"{self.name} - {self.orientation}"
    
class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PriceGroup(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_type} - ({self.size}) - £{self.price}"
    
class Product(models.Model):
    name = models.CharField(max_length=100, default="")
    price_group = models.ForeignKey(PriceGroup, on_delete=models.PROTECT, related_name="products")
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    code = models.CharField(max_length=20, null=True, unique=True)
    is_featured = models.BooleanField(default=False)
    in_store = models.BooleanField(default=True)
    has_variants = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)
    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        ordering = ["order"]

    @property
    def price(self):
        return self.price_group.price

    @property
    def size(self):
        return self.price_group.size   
    



class Notebook(Product):
    theme = models.CharField(max_length=100)
    page_img = models.CharField(max_length=100)
    front_img = models.CharField(max_length=100)


class NotebookImg(models.Model):
    notebook = models.OneToOneField(Notebook, on_delete=models.CASCADE, related_name="images")
    open_cover = models.ImageField(upload_to=upload_to)
    front_cover = models.ImageField(upload_to=upload_to)
    inside_front = models.ImageField(upload_to=upload_to)
    inside_back = models.ImageField(upload_to=upload_to)
    middle = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return f"{self.notebook} images"
    
    class Meta:
        verbose_name_plural = "Notebook images"

class CardType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Card(Product):
    card_type = models.ForeignKey(CardType, on_delete=models.PROTECT, related_name="cards")

class CardInsert(models.Model):
    card_type = models.ForeignKey(CardType, on_delete=models.PROTECT, related_name="card_inserts")
    message = models.CharField(max_length=100)
    picture = models.CharField(max_length=100)
    img = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return f"{self.card_type} - {self.picture}"
    

    
class CardImg(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE, related_name="images")
    wide_img = models.ImageField(upload_to=upload_to, null=True, blank=True)
    tall_img = models.ImageField(upload_to=upload_to, null=True, blank=True)
    small_img = models.ImageField(upload_to=upload_to, null=True, blank=True)
    inside_img = models.ForeignKey(CardInsert, on_delete=models.SET_NULL, related_name="images", null=True, blank=True)

    def __str__(self):
        return f"{self.card} images"
    
    class Meta:
        verbose_name_plural = "Card images"

class CardVariant(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="variants")
    variant_name = models.CharField(max_length=100)
    variant_img = models.ImageField(upload_to=upload_to)
    order = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return f"{self.card} ({self.variant_name})"

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Card variants"

