#!/usr/bin/env python

# encoding: utf-8

'''

@author: JOJ

@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.

@contact: zhouguanjie@qq.com

@software: JOJ

@file: stark.py

@time: 2019-12-06 8:10

@desc:

'''

from django.conf.urls import url, re_path

from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from stark.utils.page import Pagination


class ShowList(object):
    def __init__(self, config, data_list, request):
        self.config = config
        self.data_list = data_list
        self.request = request
        # 分页
        data_count = self.data_list.count()
        current_page = int(self.request.GET.get('page', 1))
        base_path = self.request.path
        params = self.request.GET
        per_page_num = 1
        pager_count = 11
        self.pagination = Pagination(current_page, data_count, base_path, params, per_page_num, pager_count, )
        # 分页后的数据
        self.page_data = self.data_list[self.pagination.start:self.pagination.end]
        # action批量初始化，字段
        self.actions = self.config.new_actions()

    def get_header(self):
        head_list = []
        print('header', self.config.new_list_play())

        for field in self.config.new_list_play():
            if callable(field):
                val = field(self, header=True)
                head_list.append(val)
            else:
                if field == "__str__":
                    head_list.append(self.config.model._meta.model_name.upper())
                else:
                    val = self.config.model._meta.get_field(field).verbose_name

                    head_list.append(val)
        print(head_list)
        return head_list

    def get_body(self):
        # 表单

        new_data_list = []
        for obj in self.page_data:

            temp = []
            for field in self.config.new_list_play():
                if callable(field):
                    val = field(self.config, obj)
                else:
                    val = getattr(obj, field)
                    # 在连接表里边，在字段做超链接
                    if field in self.config.list_display_links:
                        model_name = self.config.model._meta.model_name
                        app_label = self.config.model._meta.app_label
                        _url = reverse("%s_%s_change" % (app_label, model_name), args=(obj.pk,))
                        val = mark_safe("<a href='%s'>%s</a>" % (_url, val))
                temp.append(val)
            new_data_list.append(temp)
            '''
                  [
                      [1,"alex",12],
                      [1,"alex",12],
                      [1,"alex",12],
                      [1,"alex",12],

                           ]

                  '''
        print(new_data_list)
        return new_data_list

    def get_action_list(self):
        """action批量初始化，架构数据"""
        temp = []
        for action in self.actions:
            temp.append(
                {
                    'name': action.__name__,
                    'desc': action.short_description
                }
            )
        print(temp)
        return temp


class ModelStark(object):
    # 表单现实的字段
    list_display = ["__str__"]

    # 表单做的超连接
    list_display_links = []
    # 查询过滤的字段
    search_fields = []
    # 批量动作
    actions = []
    # modeform构建
    modelform_class = None

    # 初始化
    def __init__(self, model, site):
        self.model = model
        self.site = site

    # 批量删除函数
    def patch_delete(self, request, queryset):
        queryset.delete()

    patch_delete.short_description = "Delete selected"

    # 增加新定义的
    def new_actions(self):
        temp = []
        temp.extend(self.actions)
        temp.append(ModelStark.patch_delete)
        return temp

    # url反向解析
    def get_change_url(self, obj):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        _url = reverse("%s_%s_change" % (app_label, model_name), args=(obj.pk,))
        return _url

    def get_delete_url(self, obj):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        _url = reverse("%s_%s_delete" % (app_label, model_name), args=(obj.pk,))
        return _url

    def get_add_url(self):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        _url = reverse("%s_%s_add" % (app_label, model_name))
        return _url

    def get_list_url(self):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        _url = reverse("%s_%s_list" % (app_label, model_name))
        return _url

    # 执行的函数
    def edit(self, obj=None, header=False):

        if header:
            return '编辑'
        _url = self.get_change_url(obj)
        print("_url", _url)
        return mark_safe("<a href='%s'>编辑</a>" % _url)

    def deletes(self, obj=None, header=False):

        if header:
            return '操作'
        _url = self.get_delete_url(obj)
        print('_url', _url)
        return mark_safe("<a href='%s'>删除</a>" % _url)

    def check_box(self, obj=None, header=False):

        if header:
            return '选择'
        return mark_safe("<input id='choice' type='checkbox'>")

    # modeform构建，如果没有就用的默认的

    def get_modelform_class(self):
        if not self.modelform_class:
            from django.forms import ModelForm
            from django.forms import widgets as wid
            class ModelFormDemo(ModelForm):
                class Meta:
                    model = self.model
                    print(self.model)
                    fields = "__all__"

            return ModelFormDemo
        else:
            return self.modelform_class

    # action view
    # 添加
    def add_view(self, request):
        ModelFormDemo = self.get_modelform_class()
        if request.method == "POST":
            form = ModelFormDemo(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            return render(request, 'add_view.html', locals())
        form = ModelFormDemo()
        return render(request, 'add_view.html', locals())

    # 删除
    def delete_view(self, request, id):
        url = self.get_list_url()
        if request.method == "POST":
            self.model.objects.filter(pk=id).delete()
            return redirect(url)
        return render(request, 'delete_view.html', locals())

    # 修改
    def change_view(self, request, id):

        ModelFormDemo = self.get_modelform_class()
        edit_obj = self.model.objects.filter(pk=id).first()
        if request.method == "POST":
            form = ModelFormDemo(request.POST, instance=edit_obj)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            return render(request, 'add_view.html', locals())
        form = ModelFormDemo(instance=edit_obj)
        # print(form)
        return render(request, 'add_view.html', locals())

    # 获取组合新的展示的列表，字段加函数（增加checkbox，修改，删除，每个都有）
    def new_list_play(self):
        temp = []
        # 选择框
        temp.append(ModelStark.check_box)
        temp.extend(self.list_display)
        # 编辑,如果有字段在list_display_links里边,将编辑字段隐藏
        if not self.list_display_links:
            temp.append(ModelStark.edit)
        # 删除
        temp.append(ModelStark.deletes)
        return temp

    def get_search_condition(self, request):
        # 模糊查询
        key_word = request.GET.get('q')
        self.key_word = key_word
        print(key_word)
        from django.db.models import Q
        search_connection = Q()
        if key_word:
            search_connection.connector = 'or'
            for search_field in self.search_fields:
                search_connection.children.append((search_field + "__contains", key_word))
        return search_connection

    # 展示list
    def list_view(self, request):
        # 批量操作
        if request.method == 'POST':
            print('-----------------')
            print('post', request.POST)
            action = request.POST.get('action')
            if action:
                selected_pk = request.POST.getlist('selected_pk')
                # 反射查询
                action_func = getattr(self, action)
                print(selected_pk)
                queryset = self.model.objects.filter(pk__in=selected_pk)
                print('==========')
                print(queryset)
                ret = action_func(request, queryset)
        # 获取search Q 对象
        search_connection = self.get_search_condition(request)
        data_list = self.model.objects.all().filter(search_connection)
        # 构建一个对象showlist，表头，表单，在html直接调用对象获取表头和表单
        show_list = ShowList(self, data_list, request)
        # 增加按钮的url
        add_url = self.get_add_url()
        models_name = self.model._meta.model_name.upper()
        return render(request, "list_view.html", locals())
        # return HttpResponse('list')

    def get_urls_2(self):
        temp = []
        # 获取model名
        model_name = self.model._meta.model_name
        # 获取app名
        app_label = self.model._meta.app_label
        temp.append(re_path(r"^add/", self.add_view, name="%s_%s_add" % (app_label, model_name)))
        temp.append(re_path(r"^(\d+)/delete/", self.delete_view, name="%s_%s_delete" % (app_label, model_name)))
        temp.append(re_path(r"^(\d+)/change/", self.change_view, name="%s_%s_change" % (app_label, model_name)))
        temp.append(re_path(r"^$", self.list_view, name="%s_%s_list" % (app_label, model_name)))

        return temp

    @property
    def urls_2(self):
        print(self.model)
        return self.get_urls_2(), None, None


class StarkSite(object):
    def __init__(self):
        self._registry = {}

    def rigister(self, model, stark_class=None):
        if not stark_class:
            stark_class = ModelStark
        self._registry[model] = stark_class(model, self)
        print(self)
        print(self._registry)

    def get_url(self):

        temp = []
        for model, stark_class_obj in self._registry.items():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            # 分发增删改查
            temp.append(re_path(r"^%s/%s/" % (app_label, model_name), stark_class_obj.urls_2))
            '''
                     url(r"^app01/userinfo/",UserConfig(Userinfo).urls_2),
                     url(r"^app01/book/",ModelStark(Book).urls_2), 


                     '''
        print(temp)
        return temp

    @property
    def urls(self):
        return self.get_url(), None, None


site = StarkSite()
