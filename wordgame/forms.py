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