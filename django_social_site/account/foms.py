from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
  password = forms.CharField(label='password', widget=forms.PasswordInput)
  password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ['username', 'first_name', 'email']

  def clean_password2(self):
    cd = self.cleaned_data
    if cd['password'] != cd['password2']:
      raise forms.ValidationError("Passwords dont match")
    return cd['password2']
  
  def clean_email(self):
    # email 기반 가입시 동일 email을 가진 사용자가 있는지 검증
    data = self.cleaned_data['email']
    if User.objects.filter(email=data).exists():
      raise forms.ValidationError("Email already in use.")
    return data

class UserEditForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email']
  def clean_email(self):
    data = self.cleaned_data['email']
    # 나를 제외한 다른 사람이 해당 email을 쓰고 있으면 그것으로 바꾸지 못한다.
    qs = User.objects.exclude(id=self.instance.id).filter(email=data)
    if qs.exists():
      raise forms.ValidationError("Email already in use")
    return data

class ProfileEditForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['date_of_birth', 'photo']



