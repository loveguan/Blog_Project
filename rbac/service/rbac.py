import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class ValidPermission(MiddlewareMixin):
    def process_request(self, request):

        # 当前访问路径
        current_path = request.path_info
        print(current_path)
        # 1.白名单
        valid_url_list = ['/login/', '/reg/', '/admin/.*']
        for valid_url in valid_url_list:
            ret = re.match(valid_url, current_path)
            if ret:
                return None
        # 2.检验是否登录
        user_id = request.session.get('user_id', None)
        if not user_id:
            return redirect('/login/')
        # 3.检验权限
        permission_dict = request.session.get('permission_dict', {})
        flag = False
        print('=========================================')
        for item in permission_dict.values():
            print(item)
            print(item["urls"])
            print(item["actions"])
            urls = item["urls"]
            for reg in urls:

                permisson = "^%s$" % reg
                print(permisson)
                ret = re.match(permisson, current_path)
                if ret:
                    flag = True
                    request.actions=item["actions"]
                    return None
            if not flag:
                return HttpResponse("没有访问权限")
            return None
