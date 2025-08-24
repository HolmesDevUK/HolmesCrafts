from .models import Card, Notebook

def get_featured():

    return {
        "notebooks": Notebook.objects.filter(is_featured=True).select_related("images"),
        "birthday_cards": Card.objects.filter(card_type__name="Birthday", is_featured=True).select_related("images"),
        "wedding_cards": Card.objects.filter(card_type__name="Wedding & Anniversary", is_featured=True).select_related("images"),
        "seasonal_cards": Card.objects.filter(card_type__name="Seasonal", is_featured=True).select_related("images"),
        "special_cards": Card.objects.filter(card_type__name="Special Occasion", is_featured=True).select_related("images"),
        "other_cards": Card.objects.filter(card_type__name="Other", is_featured=True).select_related("images"),
    }