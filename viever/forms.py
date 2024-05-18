from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Anime
from django.contrib.auth import password_validation
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    password2 = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')

GENRES= (
    ('Повседневность', 'Повседневность'),
    ('Романтика', 'Романтика'),
    ('Драмма', 'Драмма'),
    ('Экшн', 'Экшн'),
    ('Ужасы', 'Ужасы'),
)

class AnimeAdminForm(forms.ModelForm):
    genre = forms.MultipleChoiceField(choices=GENRES)

    class Meta:
        model = Anime
        fields = '__all__'
