from django.utils.deprecation import MiddlewareMixin  # 引入中间件
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
import requests


class Is_login(MiddlewareMixin):
    def process_request(self, request):
        ticket = request.COOKIES.get("sso.jd.com")
        ip = request.META.get("REMOTE_ADDR")
        print('ticket: ', ticket)
        print('ip: ', ip)
        if ticket:
            url = """http://ssa.jd.com/sso/ticket/verifyTicket?ticket={ticket}&url={url}&ip={ip}""".format(
                ticket=ticket, url="neup.jd.com:8000", ip=ip)
            response = requests.get(url)
            # url = "http://ssa.jd.com/sso/ticket/verifyTicket"
            # data = {
            #     'ticket': ticket,
            #     'url': 'neup.jd.com',
            #     'ip': ip,
            # }

            # response = requests.get(url=url, params=data)
            print(url)
            print('response:  ', response.text)
            # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', response.content)
            request.session['username'] = response.text
        else:
            return redirect("http://ssa.jd.com/sso/login?returnUrl=neup.jd.com:8000")

    def process_response(self, request, response):
        return response

    # def process_view(self, request, process_view, view_args, view_kwargs):
    #     print(request.path)
    #     print("One-processView")
    #     # return render(request,"alert/index.html")
    #     # return redirect(request.path)
    #
    # def process_exception(self, request, exception):
    #     print("one-exception")
    #
    # def process_template_response(self, request, response):
    #     print("one-process_template_response")
    #     return response
