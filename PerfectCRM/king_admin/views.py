from django.shortcuts import render
from king_admin import king_admin

# Create your views here.

def index(request):
    # print(king_admin.enabled_admins['crm']['customerfollowup'].model )
    return render(request, "king_admin/table_index.html", {'table_list': king_admin.enabled_admins})

def display_table_objs(request, app_name, table_name):
    print("-->", app_name, table_name)

    admin_class = king_admin.enabled_admins[app_name][table_name]
    print(request.GET)

    return render(request, "king_admin/table_objs.html", {'admin_class': admin_class})
