from stark.service.stark import site, ModelStark

from .models import *
from django.forms import ModelForm
from django.forms import widgets as wid


class StudentModelForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

        labels = {
            "name": "名称",
            "sex": "性别"
        }


class StudentConfig(ModelStark):
    list_display = ["name", "sex", "profession"]
    list_display_links = ["sex"]
    modelform_class = StudentModelForm


site.rigister(Student, StudentConfig)
