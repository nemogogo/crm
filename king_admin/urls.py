"""perfectcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import url
from king_admin import views

urlpatterns = [
    path(r'', views.index1,name='table_index'),
    # url(r'^(\w+)/(\w+)/$', views.display_table_obj,name='table_objs'),
    url(r'^(\w+)/(\w+)/$', views.display_table_obj,name="table_objs"),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change,name='table_obj_change'),
    url(r'^(\w+)/(\w+)/add/$', views.table_obj_add,name='table_obj_add'),
    url(r'^(\w+)/(\w+)/(\d+)/change/obj_delete/$', views.obj_delete,name='obj_delete'),
    # url(r'^(\w+)/(\w+)/obj_delete1/$', views.obj_delete1, name='obj_delete1'),
    #
    # url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change,name="table_obj_change"),
    # url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change,name="table_obj_change"),
    # path('customers/', views.customer_list,name='customer_list'),

]
