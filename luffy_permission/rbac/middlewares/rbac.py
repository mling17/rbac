import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_url = request.path_info
        for url in settings.VALID_URL_LIST:
            if re.match(url, current_url):
                return
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

        # 如果权限列表是空的，就让其重新登陆
        if not permission_dict:
            return HttpResponse('还没有登陆，请重新登陆')
        # 进行权限验证
        flag = False
        url_record = [
            {'title': '首页', 'url': '#'}
        ]
        for item in permission_dict.values():
            reg = '^%s$' % item["url"]
            if re.match(reg, current_url):
                flag = True
                # 获取用户访问当前url的id，如果是非菜单权限就是pid，菜单权限就是pid为空，则取id值
                request.current_selected_permission_id = item['pid'] or item['id']
                if not item['pid']:
                    url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
                else:
                    url_record.extend([{'title': item['p_title'], 'url': item['p_url']}])
                    url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])

                request.breadcrumb = url_record
                break
        if not flag:
            return HttpResponse('您没有权限访问次页面')
