from django import forms
from django.contrib.auth.models import User
from .models import Usuario, TipoUsuario

class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    tipo_usuario = forms.ModelChoiceField(queryset=TipoUsuario.objects.all(), required=True)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2")
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            tipo = self.cleaned_data['tipo_usuario']
            usuario = Usuario(usuario=user, tipo_usuario=tipo)
            usuario.save()
        return user
