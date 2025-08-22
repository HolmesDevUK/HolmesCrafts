from .models import Card, Notebook

def get_featured():

    return {
        "notebooks": Notebook.objects.filter(is_featured=True),
        "birthday_cards": Card.objects.filter(card_type__name="birthday", is_featured=True),
        "wedding_cards": Card.objects.filter(card_type__name="wedding", is_featured=True),
        "seasonal_cards": Card.objects.filter(card_type__name="seasonal", is_featured=True),
        "special_cards": Card.objects.filter(card_type__name="special", is_featured=True),
        "other_cards": Card.objects.filter(card_type__name="other", is_featured=True),
    }