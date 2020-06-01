from stark.service.stark import site, ModelStark

from .models import *
from django.forms import ModelForm


class UserConfig(ModelStark):
    # 展示的字段
    list_display = ['name', 'pwd', 'ver_name','roles']


class RoleConfig(ModelStark):
    # 展示的字段
    list_display = ['title', 'permissions']


class PermissionConfig(ModelStark):
    # 展示的字段
    list_display = ['id','title', 'url']


site.rigister(User, UserConfig)
site.rigister(Role, RoleConfig)
site.rigister(Permission, PermissionConfig)
