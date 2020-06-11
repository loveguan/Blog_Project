from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=32, verbose_name='用户名', unique=True)
    pwd = models.CharField(max_length=32, verbose_name='密码')
    roles = models.ManyToManyField(to='Role')
    ver_name = models.CharField(max_length=32, verbose_name='使用人')

    def __str__(self):
        return self.name


class Role(models.Model):
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(to="Permission")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '用户列表'


class Permission(models.Model):
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=128)
    action = models.CharField(max_length=32, default="")
    group = models.ForeignKey(to="PermissionGroup", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PermissionGroup(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title
