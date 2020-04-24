from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Your Full Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Your Email"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Your Message"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if "gmail.com" in email or "iit" in email or 'nit' in email:
            return email
        raise forms.ValidationError("Use Valid Email!")
