from django.shortcuts import render

# Create your views here.


from django.shortcuts import render,HttpResponse
from .models import Student,Book
from .forms import StudentForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View


def index(request):
    words = 'World!'
    students = Student.get_all()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            student = Student()
            student.name = cleaned_data['name']
            student.sex = cleaned_data['sex']
            student.email = cleaned_data['email']
            student.profession = cleaned_data['profession']
            student.qq = cleaned_data['qq']
            student.phone = cleaned_data['phone']
            student.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = StudentForm()
    print(form)
    print(form.errors)
    context = {
        'students': students,
        'form': form
    }
    return render(request, 'index.html', context=context)


class IndexView(View):
    template_name = 'index.html'

    def get_context(self):
        students = Student.get_all()
        context = {
            'students': students
        }
        return context

    def get(self, request):
        context = self.get_context()
        form = StudentForm()
        context.update({'form': form})
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        context = self.get_context()
        context.update({'form': form})
        return render(request, self.template_name, context=context)
def test_index(request):
    # book_list = []
    # for i in range(500):
    #     book_obj = Book(title="book_%s" % i, price=i * i)
    #     book_list.append(book_obj)
    # Book.objects.bulk_create(book_list)
    base_url=request.path
    current_page=request.GET.get('page',1)
    all_count=Book.objects.all().count()
    params=request.GET
    per_page=10
    max_show=11
    print(request.GET)
    from stark.utils.page import Pagination
    # self, current_page, all_count, base_url, params, per_page_num=8, pager_count=11, ):
    pagination = Pagination(int(current_page), all_count, base_url,params)
    print(pagination.start)
    print(pagination.end)

    book_list = Book.objects.all()[pagination.start:pagination.end]  # 对数据进行切片

    from django.http.request import QueryDict
    # dic = QueryDict(mutable=True)
    # dic["info"] = 123

    # print(type(request.GET))
    # request.GET["info"]=123

    import copy
    params = copy.deepcopy(request.GET)
    params["xxx"] = 123

    return render(request, "index_test.html", locals())



