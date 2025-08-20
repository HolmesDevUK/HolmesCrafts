from .models import Card, Notebook

def get_featured():

    return {
        "notebooks": Notebook.objects.filter(is_featured=True),
        "birthday_cards": Card.objects.filter(card_type="Birthday", is_featured=True),
        "wedding_cards": Card.objects.filter(card_type="Wedding", is_featured=True),
        "seasonal_cards": Card.objects.filter(card_type="Seasonal", is_featured=True),
        "special_cards": Card.objects.filter(card_type="Special Occasion", is_featured=True),
        "other_cards": Card.objects.filter(card_type="Other", is_featured=True),
    }