#!/usr/bin/env python
# coding:utf-8
from wsgiref.simple_server import make_server
from jinja2 import Template



def index():
    '''
    # 读取html文件并显示
    f = open('templates/t1.html')
    data = f.read()
    return data
    '''

    f = open('templates/t2.html')
    result = f.read()
    template = Template(result)
    data = template.render(name='john Doe', user_list=['alex', 'eric'])
    return data




def login():
    return 'login'


def routers():
    urlpatterns = (
        ('/index/', index),
        ('/login/', login),
    )

    return urlpatterns


def RunServer(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    url = environ['PATH_INFO']
    urlpatterns = routers()
    func = None
    for item in urlpatterns:
        if item[0] == url:
            func = item[1]
            break
    if func:
        return func()
    else:
        return '404 not found'


if __name__ == '__main__':
    httpd = make_server('', 8000, RunServer)
    print "Serving HTTP on port 8000..."
    httpd.serve_forever()