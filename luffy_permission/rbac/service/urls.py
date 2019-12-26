from django.urls import reverse
from django.http import QueryDict


def memory_reverse(request, name):
    url = reverse(name)
    origin_params = request.GET.get('_filter')
    if origin_params:
        url = "%s?%s" % (url, origin_params)
    return url


def memory_url(request, name, *args, **kwargs):
    basic_url = reverse(name, args=args, kwargs=kwargs)
    if not request.GET:
        return basic_url
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()  # 获取url中携带的参数mid=1&age=2
    return "%s?%s" % (basic_url, query_dict.urlencode())
