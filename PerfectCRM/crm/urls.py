from django.conf.urls import url
from crm import views

urlpatterns = [
    url(r'^$', views.index, name="sales_index"),
    url(r'^customers/$', views.index, name="customer_list"),
    # url(r'^customers/$', views.index, name="customer_list"),
]
