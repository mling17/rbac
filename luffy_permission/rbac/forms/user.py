from django import forms
from django.core.exceptions import ValidationError
from rbac import models
from rbac.forms.base import BootstrapModelForm


class UserModelForm(BootstrapModelForm):
    confirm_pwd = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', 'password', 'confirm_pwd']

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirm_pwd(self):
        confirm_pwd = self.cleaned_data['confirm_pwd']
        pwd = self.cleaned_data['password']
        if confirm_pwd == pwd:
            return confirm_pwd
        raise ValidationError('两次密码输入不一致')


class UserEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.UserInfo
        exclude = ['password', 'roles']

    def __init__(self, *args, **kwargs):
        super(UserEditModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ResetPwdModelform(BootstrapModelForm):
    confirm_pwd = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_pwd']

    def __init__(self, *args, **kwargs):
        super(ResetPwdModelform, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirm_pwd(self):
        confirm_pwd = self.cleaned_data['confirm_pwd']
        pwd = self.cleaned_data['password']
        if confirm_pwd == pwd:
            return confirm_pwd
        raise ValidationError('两次密码输入不一致')
