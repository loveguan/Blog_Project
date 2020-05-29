import time
from django.urls import reverse
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class TimeItMiddleware(MiddlewareMixin):
    def process_request(self, request):
        self.start_time = time.time()
        return

    def process_view(self, request, func, *args, **kwargs):
        if request.path != reverse('index'):
            return None

        start = time.time()
        reponse = func(request)
        costed = time.time() - start
        print('process view: {:.2f}s'.format(costed))
        return reponse

    def process_exception(self, request, exception):
        pass

    def process_templete_response(self, request, reponse):
        return reponse

    def process_response(self, request, response):
        costed = time.time() - self.start_time
        print('request to response cose:{:.2f}s'.format(costed))
        return response
