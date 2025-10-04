import re
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, min_length=5)
    password = forms.CharField(min_length=5)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not re.search(r"[A-Za-z]", password):
            raise forms.ValidationError("Password must contain at least one letter.")
    
        if not re.search(r"[0-9]", password):
            raise forms.ValidationError("Password must contain at least one digit.")
    
        if not re.search(r"[$%*@]", password):
            raise forms.ValidationError("Password must contain at least one special character from $, %, *, @.")
        
        return password

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, min_length=5)
    password = forms.CharField(min_length=5)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not re.search(r"[A-Za-z]", password):
            raise forms.ValidationError("Password must contain at least one letter.")
    
        if not re.search(r"[0-9]", password):
            raise forms.ValidationError("Password must contain at least one digit.")
    
        if not re.search(r"[$%*@]", password):
            raise forms.ValidationError("Password must contain at least one special character from $, %, *, @.")
        
        return password

class GuessForm(forms.Form):
    guess_text = forms.CharField(max_length=5, min_length=5)

    def clean_guess_text(self):
        guess_text = self.cleaned_data['guess_text']

        # guess_text must only contain uppercase letters
        if not (guess_text.isalpha() or guess_text.isupper()):
            raise forms.ValidationError("Guess text must only contain uppercase letters.")
        
        return guess_text

class AdminDayForm(forms.Form):
    date = forms.DateField()

class AdminUserForm(forms.Form):
    username = forms.CharField(max_length=150, min_length=5)