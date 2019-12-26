from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from rbac import models
from rbac.forms.user import UserModelForm, UserEditModelForm, ResetPwdModelform


def user_list(request):
    if request.method == 'GET':
        users = models.UserInfo.objects.all()
        return render(request, 'rbac/user_list.html', {'users': users})


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, pk):
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('没有此用户')
    if request.method == 'GET':
        form = UserEditModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = UserEditModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/user_list.html', {'form': form})


def user_del(request, pk):
    origin_url = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    models.UserInfo.objects.filter(id=pk).delete()
    return redirect(origin_url)


def reset_pwd(request, pk):
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('没有此用户')
    if request.method == 'GET':
        form = ResetPwdModelform()
        return render(request, 'rbac/change.html', {'form': form})
    form = ResetPwdModelform(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})
