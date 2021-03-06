#!/usr/bin/env python

# encoding: utf-8

'''

@author: JOJ

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: zhouguanjie@qq.com

@software: JOJ

@file: stark.py

@time: 2019-12-06 8:09

@desc:

'''
from stark.service.stark import site, ModelStark

from .models import *
from django.forms import ModelForm
from django.forms import widgets as wid


class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

        labels = {
            "title": "书籍名称",
            "price": "价格",
            "authors": "作者",
            "publishDate": "出版日期",
        }


class AuthorModelForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


class BookConfig(ModelStark):

    # 自定义函数，实现自己想实现的东西
    def title(self, obj=None, header=False):
        if header:
            return '书籍名称'
        else:

            return  obj.title

    # 展示的字段
    list_display = ['nid', title, "price", "publish", "authors", "publishDate"]
    # 展示字段设置链接
    list_display_links = ["price"]
    # 搜索字段
    search_fields = ['title', 'price']
    modelform_class = BookModelForm
    # 过滤字段使用
    list_filter = ['authors', 'publish', 'title']

    # 批量修改数据
    def patch_init(self, request, queryset):
        queryset.update(price=100)

    patch_init.short_description = '批量初始化'

    actions = [patch_init]



class AuthorConfig(ModelStark):
    list_display = ['name', 'age']
    # 使用默认的modelform，注释掉自己写的
    # modelform_class = AuthorModelForm


site.rigister(Book, BookConfig)
site.rigister(Publish)
site.rigister(Author, AuthorConfig)
site.rigister(AuthorDetail)
