from django import forms
from django.forms.models import BaseInlineFormSet


class RecipeInLineFormSet(BaseInlineFormSet):
    """Форма рецепта для админки"""

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        has_ingredient = any(
            cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data
        )
        if not has_ingredient:
            raise forms.ValidationError('Требуется добавить ингредиент.')
