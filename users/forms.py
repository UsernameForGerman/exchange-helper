from django import forms

class UserAuthenticationForm(forms.ModelForm):
    class Meta:
        fields = ('username', 'password')

