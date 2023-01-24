from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


from home.models import Product, ProductPhoto
from django.contrib.auth.forms import UserCreationForm


class AddProductForm(forms.ModelForm):
    captcha = CaptchaField(label='Капча')

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['photo'].empty_label = 'Фотография не выбрана'
        self.fields['category'].empty_label = 'Категория не выбрана'
        self.fields['price'].initial = 100

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 10})
        }

    def clean_price(self):
        price = self.cleaned_data['price']

        if price < 0:
            ValidationError('Цена не может быть отрицательной')
        elif price == 0:
            ValidationError('Цена не может равняться нулю')

        return price


class AddProductPhotoForm(forms.ModelForm):
    captcha = CaptchaField(label='Капча')

    class Meta:
        model = ProductPhoto
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль ', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Подтверждение пароля ', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
