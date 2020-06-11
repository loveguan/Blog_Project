from django.shortcuts import render, HttpResponse, redirect
from rbac.models import *
from rbac.service.perssions import initial_session


# Create your views here.
def login(request):
    # 获取之前访问的路径。跳转回要访问的路径
    request_param = request.GET.get('path')
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user = User.objects.filter(name=user, pwd=pwd).first()
        if user:
            request.session['user_id'] = user.pk
            request.session['user_name']=user.name
            # request.session.set_expiry(0)
            initial_session(request, user)
            if request_param:
                return redirect(request_param)
            else:
                return HttpResponse('login sucess!!!!')

    return render(request, 'rbac/login.html', locals())


def logout(request):
    request.session.clear()
    return redirect('/login')
