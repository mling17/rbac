from django import forms
from rbac import models
from rbac.forms.base import BootstrapModelForm


class RoleModelForm(BootstrapModelForm):
    class Meta:
        model = models.Role
        fields = ['title']

