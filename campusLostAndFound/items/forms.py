"""
Forms for the Items app.
Yeh file sab forms define karti hai jo user input handle karti hain.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Item


class UserRegisterForm(UserCreationForm):
    """
    User registration form.
    Django ki UserCreationForm ko extend karke extra fields add kiye hain.
    """
    email = forms.EmailField(
        required=True,
        help_text="Valid email address dein"
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        help_text="Apna first name dein"
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        help_text="Apna last name dein"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap classes add karna sab fields mein
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def clean_email(self):
        """
        Email uniqueness check karna.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class ItemForm(forms.ModelForm):
    """
    Item create/update form.
    Item model ke liye ModelForm hai.
    """
    date_lost_found = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Jis din item gumi ya mili"
    )

    class Meta:
        model = Item
        fields = [
            'title',
            'description',
            'category',
            'status',
            'image',
            'location',
            'date_lost_found',
            'contact_email',
            'contact_phone',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap classes add karna sab fields mein
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'


class ItemSearchForm(forms.Form):
    """
    Item search form.
    Search aur filter functionality ke liye hai.
    """
    query = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search items...'
        })
    )
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + Item.CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + Item.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
