from .models import Card, Notebook

def get_featured():

    return {
        "notebooks": Notebook.objects.filter(is_featured=True),
        "birthday_cards": Card.objects.filter(card_type="birthday", is_featured=True),
        "wedding_cards": Card.objects.filter(card_type="wedding", is_featured=True),
        "seasonal_cards": Card.objects.filter(card_type="seasonal", is_featured=True),
        "special_cards": Card.objects.filter(card_type="special", is_featured=True),
        "other_cards": Card.objects.filter(card_type="other", is_featured=True),
    }