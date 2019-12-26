from django.template import Library
from django.conf import settings
from collections import OrderedDict
from django.http import QueryDict
from django.urls import reverse
from rbac.service import urls

register = Library()


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    """
    动态显示一级菜单
    :param request:
    :return:
    """
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    key_list = sorted(menu_dict)
    ordered_dict = OrderedDict()
    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'
        for per in val['children']:
            if per['id'] == request.current_selected_permission_id:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val
    return {'menu_dict': ordered_dict}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    """
    导航条
    :param request:
    :return:
    """
    return {'breadcrumb': request.breadcrumb}


@register.filter()
def has_permission(request, name):
    """
    判断是否有权限
    :param request:
    :param name:
    :return:
    """
    if name in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True


@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    # basic_url = reverse(name, args=args, kwargs=kwargs)
    # if not request.GET:
    #     return basic_url
    # query_dict = QueryDict(mutable=True)
    # query_dict['_filter'] = request.GET.urlencode()  # 获取url中携带的参数mid=1&age=2
    # return "%s?%s" % (basic_url, query_dict.urlencode())
    return urls.memory_url(request, name, *args, **kwargs)
