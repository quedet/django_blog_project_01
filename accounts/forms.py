from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User

from accounts.models import Profile

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username (e.g. cillian)'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password (e.g. *********)'}))
    
class UserPasswordResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address (e.g. xyz@gmail.com)'}))

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username (e.g. cillian)'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address (e.g. xyz@gmail.com)'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a password (e.g **********)'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'repeat your password (e.g *******)'}))
    
class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'}), required=False)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}), required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your date of birth'}), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter something about your'}), required=False)
    
    class Meta:
        model = Profile
        fields = ('cover_image', 'profile_image', 'date_of_birth', 'bio')