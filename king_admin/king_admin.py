#__author:zhang_lei
#date:2018/1/26
# from django.contrib import  admin
from crm import models
from django.shortcuts import render,HttpResponse,redirect
class BbaseAdmin:
    list_display=[]
    list_filters=[]
    search_fields=[]
    list_per_page=3
    ordering='id'
    filter_horizontal=[]
    readonly_fields = []
    actions = ['delete_selected_objs','add_list']
    readonly_table = False
    def delete_selected_objs(self,request,query_set):
        print('delete')

        print(query_set)
        table_name=query_set[0]._meta.model_name
        app_name=query_set[0]._meta.app_label
        admin_class = enabled_admin[app_name][table_name]

        # query_set.update(status=0)
        print("delete_confirm------------------->>>>>>>",request.POST.get('delete_confirm'))
        if request.POST.get('delete_confirm')=='yes':
            print('dsfasdf sa')
            for obj in query_set:
                print('--------',obj)
                obj.delete()
            return redirect("/king_admin/%s/%s/" % (app_name, table_name))
        else:
            return render(request,'king_admin/obj_delete1.html',{'app_name': app_name,
                                                          'table_name': table_name,
                                                          'objs': query_set,
                                                          'admin_class': admin_class,})
    def add_list(self,request,query_set):
        print('23')
    def default_clean_form(self):
        pass

enabled_admin={}
class CustomerAdmin(BbaseAdmin):
    list_display = ('id','qq','name','referral_from','source','date','status','enroll')
    list_filters = ['source','consultant','date']
    search_fields = ['qq', 'name', "consultant__name"]
    filter_horizontal = ['tags',]
    readonly_fields=['qq','qq_name','tags']
    def default_clean_form(self):
        print('<<<<<-----',self.instance)
        consult_content=self.cleaned_data.get('content','')
        if len(consult_content)<15:
            return self.ValidationError(
                    'field length should be more15',
                    code='invalid',
                    params={}
                )


    def enroll(self):
        print(self.instance)
        if self.instance.status ==0:
            link_name='报名'
        else:
            link_name='报名新课程'

        return '''<a href="/crm/customer/%s/enrollment/" >%s</a>'''%(self.instance.id,link_name)

    enroll.display_name = '报名链接'
    # def clean_name(self):#这里打开就会有名字就会是none
    #     clean_data=self.cleaned_data["name"]
    #     if not clean_data:
    #         self.add_error('name', "cannot be null")
    #     print('---->>>self.name',clean_data)

    #     if not self.cleand_data['name']:
    #         self.add_error('name','name should not be null')

class CustomerFollowUpAdmin(BbaseAdmin):
    list_display = ('id','customer','consultant','date')
    list_filters = ['customer','consultant']
class CourseAdmin(BbaseAdmin):
    list_display = ('name',)
    search_fields = ['name']
class UserProfileAdmin(BbaseAdmin):
    list_display = ('email','name','last_login')
    def default_clean_form(self):
        pass

class EnrollmentAdmin(BbaseAdmin):
    list_display = ('customer', 'consultant', 'contract_agreed','date')
class CourseRecordAdmin(BbaseAdmin):
    list_display = ('from_class','teacher','date')
    actions = ['initialize_studyrecords', ]
    errors=[]
    def initialize_studyrecords(self,request,queryset):
        if len(queryset)>1:
            return HttpResponse("只能选择一个班级")
        print('---->>>注册的学生',queryset[0].from_class.enrollment_set.all())
        new_obj_list=[]
        for enroll_obj in queryset[0].from_class.enrollment_set.all():
            new_obj_list.append(models.StudyRecord(
                student=enroll_obj,
                course_record=queryset[0],
                attendance=0,
                score=0
            ))
        try:
            models.StudyRecord.objects.bulk_create(new_obj_list)
        except Exception as e:
            return redirect("/king_admin/crm/studyrecord/?course_record=%s" % queryset[0].id)
            # return HttpResponse('批量创建学习记录失败，请检查该节课是否已经有对应的学习记录')

        return redirect("/king_admin/crm/studyrecord/?course_record=%s" % queryset[0].id)

    initialize_studyrecords.display_name = '初始化学习记录'
class StudyRecordAdmin(BbaseAdmin):
    list_display = ('student','attendance','score')
    list_filters = ['course_record','student']
def register(model_class,admin_class=None):
    if not admin_class:
        admin_class=BbaseAdmin
        print(dir(model_class))
        for field in model_class._meta.fields:

            admin_class.list_display.append(field.name)
    if model_class._meta.app_label not in enabled_admin:
        enabled_admin[model_class._meta.app_label]={}

    enabled_admin[model_class._meta.app_label][model_class._meta.model_name]=admin_class
    admin_class.model = model_class

class PaymentAdmin(BbaseAdmin):
    list_display = ('customer','course','amount')

register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
register(models.Course,CourseAdmin)
register(models.ClassList)

register(models.UserProfile,UserProfileAdmin)
register(models.Enrollment,EnrollmentAdmin)
register(models.Payment,PaymentAdmin)
register(models.StudyRecord,StudyRecordAdmin)
register(models.CourseRecord,CourseRecordAdmin)

