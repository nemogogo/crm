from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from crm import models
def index(request):
    print('sdafsdf asd')
    print(request.user.name)


    return render(request,'student/stu_index.html')
from perfectcrm import settings
def studyrecords(request,enroll_obj_id):
    print('sadfasdfsadfasdfasdf')
    enroll_obj = models.Enrollment.objects.get(id=enroll_obj_id)

    return render(request,"student/studyrecords.html",{"enroll_obj":enroll_obj})
import os
import time
import json
def homework_detail(request,study_record_id):
    print('yes')
    studyrecord_obj= models.StudyRecord.objects.get(id=study_record_id)
    homework_path="{base_dir}/{class_id}/{course_record_id}/{studyrecord_id}/".\
        format(base_dir=settings.HOMEWORK_DIR,
               class_id=studyrecord_obj.student.enrolled_class_id,
               course_record_id=studyrecord_obj.course_record_id,
               studyrecord_id=studyrecord_obj.id
               )
    if not os.path.isdir(homework_path):
        os.makedirs(homework_path, exist_ok=True)
    file_lists = []
    if request.method == "POST":
        print(request.FILES)
        #class_id/course_record_id/studyrecord_id
        for k,file_obj in request.FILES.items():
            with open("%s/%s"%(homework_path,file_obj.name),"wb" ) as f :
                for chunk in file_obj.chunks():
                    f.write(chunk)
    for file_name in os.listdir(homework_path):
        f_path = "%s/%s" % (homework_path,file_name)
        modify_time =time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.stat(f_path).st_mtime) )
        file_lists.append([file_name,  os.stat(f_path).st_size,modify_time])
    if request.method == "POST":
        return HttpResponse(json.dumps({"status": 0,
                                        "msg": "file upload success",
                                        'file_lists':file_lists}))
    print("file lists",file_lists)


    return render(request,'student/homework_detail.html',{'study_record':studyrecord_obj,
                                                          'study_record_id':study_record_id,
                                                          'file_lists':file_lists})