from django.shortcuts import render, redirect, HttpResponse
from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm
from django.urls import reverse
from rbac.service.urls import memory_reverse


def menu_list(request):
    if request.method == 'GET':
        menus = models.Menu.objects.all()
        menu_id = request.GET.get('mid')
        second_menu_id = request.GET.get('sid')
        if menu_id:
            second_menus = models.Permission.objects.filter(menu_id=menu_id)
        else:
            second_menus = []
        second_menus_exist = models.Permission.objects.filter(id=second_menu_id).exists()
        if not second_menus_exist:
            second_menu_id = []
        if second_menu_id:
            permissions = models.Permission.objects.filter(pid_id=second_menu_id)
        else:
            permissions = []
        return render(request, 'rbac/menu_list.html',
                      {'menus': menus, 'menu_id': menu_id,
                       'second_menus': second_menus,
                       'second_menu_id': second_menu_id,
                       'permissions': permissions})


def menu_add(request):
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, pk):
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('没有此菜单')
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/menu_list.html', {'form': form})


def menu_del(request, pk):
    origin_url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    models.Menu.objects.filter(id=pk).delete()
    return redirect(origin_url)


def second_menu_add(request, menu_id):
    menu_obj = models.Menu.objects.filter(id=menu_id).first()
    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_obj})
        return render(request, 'rbac/change.html', {'form': form})
    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, pk):
    permission_obj = models.Permission.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = SecondMenuModelForm(instance=permission_obj, data=request.POST)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/menu_list.html', {'form': form})


def second_menu_del(request, pk):
    origin_url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    models.Permission.objects.filter(id=pk).delete()
    return redirect(origin_url)
