from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfil


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfilForm(forms.ModelForm):

    class Meta:
        model = UserProfil
        fields = (
            'curso',
            'n_matriculas',
            'facebook',
            'instagram',
            'twitter',
            'profil_image',
        )
class SendUserReport(forms.Form):
    report = forms.CharField( widget=forms.Textarea(attrs={
                                        "rows": 6,
                                        "cols": 60,
                                        }))
