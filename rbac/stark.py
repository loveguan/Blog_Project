from stark.service.stark import site, ModelStark

from .models import *
from django.forms import ModelForm


class UserConfig(ModelStark):
    # 展示的字段
    list_display = ['name', 'pwd', 'ver_name','roles']
    # list_display_links = ['name']


class RoleConfig(ModelStark):
    # 展示的字段
    list_display = ['title', 'permissions']
    list_display_links = ['title']


class PermissionConfig(ModelStark):
    # 展示的字段
    list_display = ['id','title', 'url',]


site.rigister(User, UserConfig)
site.rigister(Role, RoleConfig)
site.rigister(Permission, PermissionConfig)
site.rigister(PermissionGroup)
