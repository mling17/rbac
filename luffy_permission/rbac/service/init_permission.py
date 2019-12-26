from django.conf import settings


def init_permission(current_user, request):
    # 初始化用户权限信息并放入session中
    permission_queryset = current_user.roles.filter(permissions__isnull=False).all().values('permissions__id',
                                                                                            'permissions__title',
                                                                                            'permissions__url',
                                                                                            'permissions__name',
                                                                                            'permissions__pid_id',
                                                                                            'permissions__menu_id',
                                                                                            'permissions__menu__title',
                                                                                            'permissions__menu__icon',
                                                                                            'permissions__pid__id',
                                                                                            'permissions__pid__title',
                                                                                            'permissions__pid__url',
                                                                                            ).distinct()

    # permission_list = [item['permissions__url'] for item in permission_queryset]
    permission_dict = {}
    menu_dict = {}
    """
    菜单信息：
    {
        1: {
            'title': '信息管理',
            'icon': 'fa-sliders',
            'children': [
                {'title': '客户列表', 'url': '/customer/list/'}
            ]
        },
        2: {
            'title': '用户管理',
            'icon': 'fa-ship',
            'children': [
                {'title': '账单列表', 'url': '/payment/list/'}
            ]
        }
    }
    """
    for item in permission_queryset:
        # 权限列表
        permission_dict[item['permissions__name']] = {'id': item['permissions__id'],
                                                      'title': item['permissions__title'],
                                                      'url': item['permissions__url'],
                                                      'pid': item['permissions__pid_id'],
                                                      'p_id': item['permissions__pid__id'],
                                                      'p_title': item['permissions__pid__title'],
                                                      'p_url': item['permissions__pid__url']
                                                      }

        # 获取菜单
        menu_id = item['permissions__menu_id']  # 有值说明是二级菜单
        if not menu_id:
            continue
        node = {'id': item['permissions__id'], 'title': item['permissions__title'],
                'url': item['permissions__url']}  # 二级菜单的标题和url
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],  # 一级菜单标题
                'icon': item['permissions__menu__icon'],  # 一级菜单图标
                'children': [node, ]
            }
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
