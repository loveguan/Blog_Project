import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class ValidPermission(MiddlewareMixin):
    def process_request(self, request):

        # 当前访问路径
        current_path = request.path_info
        # 1.白名单
        valid_url_list = ['/login/', '/logout/', '/reg/', '/admin/.*']
        for valid_url in valid_url_list:
            ret = re.match(valid_url, current_path)
            if ret:
                return None
        # 2.检验是否登录
        user_id = request.session.get('user_id', None)
        user_name = request.session.get('user_name', None)
        if not user_id:
            _url = '/login/?path=%s' % (request.path_info)
            return redirect(_url)
        # 3.检验权限,访问一个路径生成在这个url下边所有的权限

        permission_dict = request.session.get('permission_dict', {})
        print('==============')
        print(permission_dict)
        flag = False
        for item in permission_dict.values():
            urls = item["urls"]
            for reg in urls:

                permisson = "^%s$" % reg
                ret = re.match(permisson, current_path)
                if ret:
                    flag = True
                    request.actions = item["actions"]
                    return None
        # 如果是admin用户直接过去
        if user_name == 'admin':
            request.actions=[]
            return None
        if not flag:
            return HttpResponse("没有访问权限")
