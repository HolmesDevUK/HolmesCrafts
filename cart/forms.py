from django import forms

class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "quantity-input"})
    )
    chosen_image = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"id": "chosen_image"})
    )

