from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField, UserCreationForm, AuthenticationForm
from django import forms
from .models import User


class CustomUserChangeForm(UserChangeForm):
  password = ReadOnlyPasswordHashField()
  class Meta:
    model = User
    fields = '__all__' 

class CustomUserCreationForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'
      # if visible.field.help_text:
      #   visible.field.widget.attrs['data-toggle'] = 'popover'
      #   visible.field.widget.attrs['data-container'] = 'body'
      #   visible.field.widget.attrs['title'] = 'Help'
      #   visible.field.widget.attrs['data-content'] = visible.field.help_text
      #   print(visible.field)

    self.fields['password1'].widget.attrs.update({'placeholder':'Enter Password'})        
    self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})

  class Meta:
    model = User
    fields = ('first_name','last_name','email','phone_number')
    widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter email address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone No.'}),
        }


class LoginForm(forms.Form):
  # def __init__(self, *args, **kwargs):
  #   super().__init__(*args, **kwargs)
  #   for visible in self.visible_fields():
  #     visible.field.widget.attrs['class'] = 'form-control'
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'form-control'

  email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder' : 'Enter email address'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Enter Password'}))
