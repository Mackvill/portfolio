from django import forms
from django.shortcuts import redirect
from .models import Clients, PhotoSessions, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role')

class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['name', 'email', 'phone']

    def save(self, commit=True):
        email = self.cleaned_data['email']
        existing_client = Clients.objects.filter(email=email).first()

        if existing_client:
            # Если клиент с таким email уже существует, обновляем его данные
            existing_client.name = self.cleaned_data['name']
            existing_client.phone = self.cleaned_data['phone']
            if commit:
                existing_client.save()
            return existing_client
        else:
            # Если клиент с таким email не существует, создаем нового
            return super().save(commit=commit)


class PhotoSessionForm(forms.ModelForm):
    class Meta:
        model = PhotoSessions
        fields = ['date', 'duration', 'location', 'notes']

    def save(self, commit=True):
        photo_session = super().save(commit=False)
        if commit:
            photo_session.save()
        return photo_session