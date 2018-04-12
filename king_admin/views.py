from django.shortcuts import render,redirect
from king_admin.utils import  table_filter,table_sort,table_search
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.decorators import login_required
# Create your views here.
from king_admin import king_admin,forms
from crm import permissions

@login_required
def index1(request):
    # print(king_admin.enabled_admin['crm']['customer'].model)
    return render(request,'king_admin/table_index.html',{'table_list':king_admin.enabled_admin})

import importlib
@login_required
def display_table_obj(request,app_name,table_name):
    print('display--->',app_name,table_name)

    # model_module=importlib.import_module('%s.models'%app_name)
    # model_obj=getattr(model_module,table_name)
    admin_class=king_admin.enabled_admin[app_name][table_name]
    if request.method=='POST':
        print(request.POST)
        print(request.POST.get('selected_ids'))
        print(request.POST.get('action'))
        print(request.POST.get('selected_obj'))
        selected_o=request.POST.get('selected_obj')
        selected_action=request.POST.get('action')
        selected_ids=request.POST.get('selected_ids')
        if selected_ids and selected_action:
            ids=selected_ids.split(',')
            selected_objs=admin_class.model.objects.filter(id__in=ids)
            # print(selected_objs)
            func = getattr(admin_class, selected_action)
            return func(admin_class, request, selected_objs)
        elif selected_o and selected_action:
            ids = selected_o.strip()
            ids=ids.split(' ')
            selected_objs = admin_class.model.objects.filter(id__in=ids)
            print(selected_objs)
            func = getattr(admin_class, selected_action)
            return func(admin_class, request, selected_objs)

            print('sadfsdfsd')
        else:
            print('------no selected or action')

    object_list, filter_condtions = table_filter(request, admin_class)

    # print('object________',admin_class.model.objects.all())
    object_list=table_search(request,admin_class,object_list)

    object_list,orderby_key=table_sort(request,admin_class,object_list)#排序后的结果
    # print('2', object_list,filter_condtions)
    paginator = Paginator(object_list,admin_class.list_per_page)  # Show 25 contacts per page
    page=request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)

    return render(request,'king_admin/table_objs.html',{'admin_class':admin_class,
                                                        'filter_condtions':filter_condtions,
                                                        'query_sets':query_sets,
                                                        "previous_orderby": request.GET.get("o",''),
                                                        "orderby_key": orderby_key,
                                                        "search_text": request.GET.get('_q', '')
                                                        })
@permissions.check_permission
@login_required
def table_obj_add(request,app_name,table_name):
    admin_class = king_admin.enabled_admin[app_name][table_name]
    admin_class.is_add_form = True
    model_form_class = forms.creat_model_form(request, admin_class)

    if request.method == 'POST':
        obj=request.POST
        obj=model_form_class(obj)
        obj.is_valid()
        if obj.is_valid():
            obj.save()
            print("objsave")
            return redirect(request.path.replace('add/',''))
        else:
            return render(request, 'king_admin/table_obj_add.html',
                          {'obj': obj, 'app_name': app_name, 'table_name': table_name})


    else:
        obj = model_form_class()
        return render(request, 'king_admin/table_obj_add.html', {'obj': obj,'app_name':app_name,'table_name':table_name})
@login_required
def table_obj_change(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admin[app_name][table_name]
    # print(type(admin_class))
    obj1 = admin_class.model.objects.get(id=obj_id)
    model_form_class = forms.creat_model_form(request, admin_class)

    if request.method=='POST':
        obj=request.POST
        obj=model_form_class(obj,instance=obj1)
        if obj.is_valid():
            obj.save()
    else:
        obj = model_form_class(instance=obj1) #为什么调整get和post 的顺序可以让obj有cleandata



    return render(request,'king_admin/table_obj_change.html',{"form_obj":obj,
                                                              "admin_class":admin_class,
                                                              "app_name":app_name,
                                                              "table_name":table_name})

@login_required
def  obj_delete(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admin[app_name][table_name]

    obj = admin_class.model.objects.get(id=obj_id)

    if request.method=='POST':
        print("--------------delete")
        obj.delete()
        print(table_name,obj_id)
        return redirect('/king_admin/{app_name}/{model_name}/'.format(app_name=app_name,model_name=table_name))

    # print(obj,type(obj))
    # print(obj._meta.related_objects)
    ele = '<ul>'
    # for field_obj in obj._meta.related_objects:
    #     inele = ''
    #     print('------------------here we are')
    #     related_table_name = field_obj.name
    #     print('related_table_name', related_table_name)
    #     related_lookup_name = "%s_set" % related_table_name
    #     related_objs = getattr(obj, related_lookup_name).all()
    #     print(getattr(obj, related_lookup_name).all())
    #     if related_objs:
    #         for i in related_objs:
    #             print(related_table_name, i)
    #
    #             inele += '<li>%s%s</li>' % (related_table_name, i)
    #
    #     ele += inele
    #     # print(str(i).strip('<>'))
    # ele += '</ul>'
    # m2m_fields=admin_class.model._meta.local_many_to_many

    return render(request,'king_admin/obj_delete.html',{'app_name':app_name,
                                                        'table_name':table_name,
                                                        'obj':obj,
                                                        'admin_class':admin_class,
                                                        'obj_id':obj.id})

# def obj_delete1(request,app_name,table_name,objs):
#     admin_class = king_admin.enabled_admin[app_name][table_name]
#     print('sdafsdfsad')
#
#     if request.method == 'POST':
#         for obj in objs:
#             print('------>',table_name,obj.id)
#         print("--------------delete------")
#         return redirect('/king_admin/table_objs.html')
#     return render(request, 'king_admin/obj_delete1.html', {'app_name': app_name,
#                                                           'table_name': table_name,
#                                                           'objs': objs,
#                                                           'admin_class': admin_class,})