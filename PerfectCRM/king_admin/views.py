from django.shortcuts import render
from king_admin import king_admin
from king_admin.utils import table_filter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
    # print(king_admin.enabled_admins['crm']['customerfollowup'].model )
    return render(request, "king_admin/table_index.html", {'table_list': king_admin.enabled_admins})

def display_table_objs(request, app_name, table_name):
    print("-->", app_name, table_name)

    admin_class = king_admin.enabled_admins[app_name][table_name]
    print(request.GET)
    object_list, filter_conditions = table_filter(request, admin_class)

    paginator = Paginator(object_list, admin_class.list_per_page)
    try:
        query_sets = paginator.page('page')
    except PageNotAnInteger:
        query_sets = paginator.page(1)
    except EmptyPage:
        query_sets = paginator.page(paginator.num_pages)

    return render(request, "king_admin/table_objs.html", {'admin_class': admin_class,
                                                          'query_sets': query_sets,
                                                          'filter_conditions': filter_conditions,})
