from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from rbac import models
from rbac.forms.role import RoleModelForm


def role_list(request):
    if request.method == 'GET':
        roles = models.Role.objects.all()
        return render(request, 'rbac/role_list.html', {'roles': roles})


def role_add(request):
    if request.method == 'GET':
        form = RoleModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/change.html', {'form': form})


def role_edit(request, pk):
    obj = models.Role.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('没有此角色')
    if request.method == 'GET':
        form = RoleModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = RoleModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/role_list.html', {'form': form})


def role_del(request, pk):
    origin_url = reverse('rbac:role_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    models.Role.objects.filter(id=pk).delete()
    return redirect(origin_url)
