"""AutoInfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from Info import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^index$', views.index),
    url(r'^ui-buttons$', views.ui_buttons),
    url(r'^ui-icons', views.ui_icons),
    url(r'^extensions$', views.extensions, name='extensions'),
    url(r'^genieacs$', views.genieacs, name="genieacs"),
    url(r'^genieacs/tasks$', views.genieacs_tasks),
    url(r'^genieacs/yaml$', views.genieacs_yaml, name="genieacs_yaml"),
    url(r'^genieacs/log$', views.genieacs_log, name="genieacs_log"),
    url(r'^genieacs/log/(?P<logfile>.*)$', views.logfile),
    url(r'^file_upload$', views.file_upload, name="file_upload"),
    url(r'file_upload_progress/$', views.get_file_upload_progress, name="file_upload_progress"),
    url(r'delete_cache_key/$', views.delete_cache_key, name="delete_cache_key"),
    url(r'^config_phone', views.config_phone, name="config_phone"),
    url(r'^reboot_phone', views.reboot_phone, name="reboot_phone"),
    url(r'^check_ping', views.check_ping, name="check_ping"),
    url(r'^check_area', views.check_area, name="check_area"),
    url(r'^multishow', views.multishow, name="multishow"),
    url(r'^excel_export$', views.excel_export, name="excel_export"),
    url(r'^download_excel/(?P<filename>.*)$', views.download_excel, name="download_excel"),
    url(r'^wakeup', views.wakeup, name="wakeup"),
    url(r'^pagenumper', views.pagenumper, name="pagenumper"),

    url(r'genieacs/delete$', views.delete),

    url(r'genieacs/test$', views.test),


]

