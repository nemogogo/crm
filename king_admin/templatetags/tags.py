#__author:zhang_lei
#date:2018/1/27

from django import template
from django.core.exceptions import FieldDoesNotExist
from django.utils.safestring import mark_safe
register=template.Library()
from django.utils.timezone import datetime,timedelta
from king_admin import king_admin,forms

@register.simple_tag
def render_app_name(admin_class):

    return admin_class.model._meta.verbose_name_plural

@register.simple_tag
def get_query_set(admin_class):
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(obj,request,admin_class):

    row_ele=""
    for index,column in enumerate(admin_class.list_display):
        try:
            obj_field=obj._meta.get_field(column)
            if obj_field.choices:
                row_data=getattr(obj,"get_%s_display"%column)()
                # print('rowdata',row_data)
            else:
                row_data=getattr(obj,column)
                # print('rowdata',row_data)
            if type(row_data).__name__ == 'datetime':
                row_data = row_data.strftime("%Y-%m-%d %H:%M:%S")
            # if index==0:
            #     row_data="<a href='{request_path}/{obj_path}>{data}</a>".format(request_path=request.path,obj_path=obj.id,data=row_data)

            if index == 0:  # add a tag, 可以跳转到修改页
                row_data = "<a href='{request_path}{obj_id}/change/'>{data}</a>".format(request_path=request.path,
                                                                                           obj_id=obj.id,
                                                            data=row_data)
        except FieldDoesNotExist as e:
            if hasattr(admin_class,column):
                column_func=getattr(admin_class,column)
                admin_class.instance=obj
                admin_class.request=request
                row_data=column_func()
        row_ele+='<td>%s</td>'%row_data

    return mark_safe(row_ele)

@register.simple_tag
def render_filter_ele(filter_field,admin_class,filter_condtions):
    #select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' %filter_field
    select_ele = '''<select class="form-control" name='{filter_field}' ><option value=''>----</option>'''
    field_obj = admin_class.model._meta.get_field(filter_field)

    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            # print("choice",choice_item,filter_condtions.get(filter_field),type(filter_condtions.get(filter_field)))
            if filter_condtions.get(filter_field) == str(choice_item[0]):
                selected ="selected"

            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected =''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(filter_field) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected = ''
        # print('---->foreignkey',select_ele)
    if type(field_obj).__name__ in ['DateTimeField','DateField']:
        date_els = []
        today_ele = datetime.now().date()
        date_els.append(['今天', datetime.now().date()])
        date_els.append(["昨天",today_ele - timedelta(days=1)])
        date_els.append(["近7天",today_ele - timedelta(days=7)])
        date_els.append(["本月",today_ele.replace(day=1)])
        date_els.append(["近30天",today_ele - timedelta(days=30)])
        date_els.append(["近90天",today_ele - timedelta(days=90)])
        date_els.append(["近180天",today_ele - timedelta(days=180)])
        date_els.append(["本年",today_ele.replace(month=1,day=1)])
        date_els.append(["近一年",today_ele  - timedelta(days=365)])

        selected = ''
        for item in date_els:
            select_ele += '''<option value='%s' %s>%s</option>''' %(item[1],selected,item[0])


        filter_field_name = "%s__gte" % filter_field


    else:
        filter_field_name = filter_field
        # print('tags---->2', filter_field_name)
    select_ele += "</select>"
    select_ele = select_ele.format(filter_field=filter_field_name)

    return mark_safe(select_ele)


@register.simple_tag
def  build_paginators(query_sets,filter_condtions,previous_orderby,search_text):
    '''返回整个分页元素'''
    page_btns = ''
    filters = ''
    for k,v in filter_condtions.items():
        filters += "&%s=%s" %(k,v)


    added_dot_ele = False #
    for page_num in query_sets.paginator.page_range:
        if page_num < 3 or page_num > query_sets.paginator.num_pages -2 \
                or abs(query_sets.number - page_num) <= 1: #代表最前2页或最后2页 #abs判断前后1页
            ele_class = ""
            if query_sets.number == page_num:
                added_dot_ele = False
                ele_class = "active"
            page_btns += '''<li class="%s"><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>''' % (
            ele_class, page_num, filters,previous_orderby, search_text,page_num)
        # elif abs(query_sets.number - page_num) <= 1: #判断前后1页
        #     ele_class = ""
        #     if query_sets.number == page_num:
        #         added_dot_ele = False
        #         ele_class = "active"
        #     page_btns += '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' % (
        #     ele_class, page_num, filters, page_num)
        else: #显示...
            if added_dot_ele == False: #现在还没加...
                page_btns += '<li><a>...</a></li>'
                added_dot_ele = True


    return mark_safe(page_btns)
@register.simple_tag
def  build_table_header_column(column,orderby_key,filter_conditions,admin_class):
    filters=''
    for k,v in filter_conditions.items():
        filters+='&%s=%s'%(k,v)
    # ele='''<th><a href="?{filters}&o={orderby_key}">{column}</a>
    ele = '''<th><a href="?{filters}&o={orderby_key}">{column}</a>
    {sort_icon}
    </th>'''
    if orderby_key:
        if orderby_key.startswith("-"):
            sort_icon = '''<span class="glyphicon glyphicon-chevron-up"></span>'''
        else:
            sort_icon = '''<span class="glyphicon glyphicon-chevron-down"></span>'''

        if orderby_key.strip("-") == column:  # 排序的就是这个字段
            orderby_key =orderby_key
        else:
            orderby_key = column
            sort_icon = ''
    else:
        orderby_key=column
        sort_icon=''
    try:
        column_verbose_name=admin_class.model._meta.get_field(column).verbose_name
    except FieldDoesNotExist as e:
        column_verbose_name=getattr(admin_class,column).display_name
        ele = '''<th><a href="javascript:void(0)">%s</a>
                </th>''' % (column_verbose_name)
        return mark_safe(ele)
    ele = '''<th><a href="?%s&o=%s">%s</a>
        %s
        </th>'''%(filters,orderby_key,column_verbose_name,sort_icon)
    return mark_safe(ele)

# @register.simple_tag
# def  build_table_header_column(column,orderby_key,filter_condtions):
#     filters = ''
#     for k,v in filter_condtions.items():
#         filters += "&%s=%s" %(k,v)
#
#     ele = '''<th><a href="?{filters}&o={orderby_key}">{column}</a>
#     {sort_icon}
#     </th>'''
#     if orderby_key:
#         if orderby_key.startswith("-"):
#             sort_icon = '''<span class="glyphicon glyphicon-chevron-up"></span>'''
#         else:
#             sort_icon = '''<span class="glyphicon glyphicon-chevron-down"></span>'''
#
#         if orderby_key.strip("-") == column: #排序的就是这个字段
#             orderby_key =orderby_key
#         else:
#             orderby_key = column
#             sort_icon = ''
#
#     else:  #没有排序
#         orderby_key = column
#         sort_icon = ''
#
#     ele = ele.format(orderby_key=orderby_key, column=column,sort_icon=sort_icon,filters=filters)
#     return mark_safe(ele )
@register.simple_tag
def table_change(request,app_name,table_name,obj_id,table_list):
    obj_id=int(obj_id)
    ele='<tr><td>'



    obj=table_list[app_name][table_name].model._meta
    # for i,v in enumerate(obj.fields):
        # print(v.attname)





    return mark_safe(ele)
@register.simple_tag
def table_change_1(request,app_name,table_name,obj_id,table_list):
    ele = ''
    obj = table_list[app_name][table_name].model._meta
    obj1=table_list[app_name][table_name].model.objects.filter(id=obj_id)
    values=[]
    for i,v in enumerate(obj.fields):
        values.append(v.attname)
    # print(values)
    for i in values:

        data=obj1.values(i)[0][i]
        row_data="<td>{column}</td><td><input value={data}></td>".format(column=i,data=data)

        ele+="<tr>%s</tr>"%row_data


    return mark_safe(ele)

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.verbose_name_plural
@register.simple_tag
def get_app_name(admin_class):

    return admin_class.model._meta.app_label
@register.simple_tag
def get_model(admin_class):
    print(admin_class.model._meta.model_name)
    return admin_class.model._meta.model_name

@register.simple_tag

def add_frame(request,obj,admin_class):
    ele=''
    for field in obj:
        # print(field.label,field.name,field.field)
        # print(dir(type(field.field).widget)
        print('dasfasdf')

    return ele

def getele(app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admin[app_name][table_name]
    obj = admin_class.model.objects.get(id=obj_id)

    # print(obj,type(obj))
    # print(obj._meta.related_objects)
    ele = '<ul>'
    # ele += '<li>Delete--%s</li>' % str(obj)

    for m2m_field in obj._meta.many_to_many:


        tags=m2m_field.name
        print(m2m_field)
        m=getattr(obj,tags)
        print('------------>>>>>>>>>>',m.select_related())
        ele += '<li>%s<ul>' % tags
        for m in m.select_related():
            print(m)
            # ele+='  <a href="/king_admin/%s/%s/%s/change/">%s</a>'%(
            # app_name, table_name, obj_id,m.id)
            ele += '<li><a href="/king_admin/%s/%s/%s/change/">%s</a>里面与%s相关的内容[%s]将会被删除</li>' % (
            app_name, table_name, obj_id, tags, obj,m)

        ele += '</ul></li>'






        # print(dir(field_objs))
        # print(field_objs._get_lookup)
        # print(field_objs._get_m2m_attr)
        # print(field_objs._get_m2m_db_table)
        # print(field_objs._get_m2m_reverse_attr)
        # print(field_objs.attname)
        # print(field_objs.get_choices)
        # print(field_objs.get_reverse_related_filter)


    for field_obj in obj._meta.related_objects:

        # print('------------------here we are')
        related_table_name = field_obj.name
        # print('related_table_name', related_table_name)
        related_lookup_key = "%s_set" % related_table_name
        related_objs = getattr(obj, related_lookup_key).all()

        # print(getattr(obj, related_lookup_name).all())
        if related_objs:


            for related_obj in related_objs:
                ele += '<li>%s<ul>' % related_table_name
            #     ele += '  <a href="/king_admin/%s/%s/%s/change/">%s</a><ul>' %(
            # app_name, table_name, obj_id,related_obj.id)
                # print(i.id)
                # print(related_table_name, i)
                m=str(related_table_name)
                # print(app_name,m,'sadf sfsadfas',i.id)
                iele=getele(app_name,m, related_obj.id)
                ele += '<li><a href="/king_admin/%s/%s/%s/change/">%s</a>里面与%s相关的内容将会被删除</li>' %(app_name,table_name,obj_id,related_obj,obj)
                ele+=iele
                ele+='</ul></li>'


    ele += '</ul>'
        # print(str(i).strip('<>'))

    return ele
@register.simple_tag
def make_obj_list(app_name,table_name,objid):
    ele=getele(app_name,table_name,objid)

    # obj = admin_class.model.objects.get(id=obj_id)
    #
    # # print(obj,type(obj))
    # # print(obj._meta.related_objects)
    # ele = '<ul>'
    # for field_obj in obj._meta.related_objects:
    #     inele = ''
    #     print('------------------here we are')
    #     related_table_name = field_obj.name
    #     print('related_table_name', related_table_name)
    #     related_lookup_name = "%s_set" % related_table_name
    #     related_objs = getattr(obj, related_lookup_name).all()
    #
    #     print(getattr(obj, related_lookup_name).all())
    #     if related_objs:
    #         for i in related_objs:
    #             make_obj_list(admin_class,i.id)
    #             print(related_table_name, i)
    #
    #             inele += '<li>%s%s</li>' % (related_table_name, i)
    #
    #     ele += inele
    #     # print(str(i).strip('<>'))
    # ele += '</ul>'
    return mark_safe(ele)