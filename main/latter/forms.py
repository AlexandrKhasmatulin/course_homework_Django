from django import forms

from main.latter.models import SmsLetter


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():  # стилизация (нужно в каждый класс)
            field.widget.attrs['class'] = 'form-control'


class SmsLetterForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = SmsLetter
        fields = ("title", "client", "send_time", "frequency", "status")
    # def clean_name(self):
    #     name = self.cleaned_data["name"]
    #     forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
    #
    #     for word in forbidden_words:
    #         if word in name.lower():  # запрещенные слова
    #             raise forms.ValidationError("Название продукта содержит запрещенное слово.")
    #
    #     return name


class SubjectForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = SmsLetter
        fields = "__all__"


class EmailLatter(forms.Form):
    email = forms.EmailField()