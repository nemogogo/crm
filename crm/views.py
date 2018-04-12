from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
import string,random
# Create your views here.

def index(req):
    return render(req,'index.html')

def customer_list(req):

    return render(req,'sales/customers.html')
def acc_login(req):
    errors={}
    if req.method=='POST':
        _username=req.POST.get('username')
        _password=req.POST.get('password')
        print('aaa')

        user=authenticate(username=_username,password=_password)
        if user:
            login(req,user)
            url_name=req.GET.get('next','/king_admin')
            return redirect(url_name)
        else:
            errors['errors']="Wrong Email address or password"

    return render(req,'login.html',{'errors':errors})

def acc_logout(req):
    logout(req)
    return redirect('/account/login1/')
from crm import forms
from crm import models
from django.db import IntegrityError
from django.core.cache import cache
def enrollment(req,customer_id):
    customer_obj=models.Customer.objects.get(id=customer_id)
    msg={}
    enroll_obj=None
    if req.method=='POST':
        enroll_form = forms.enroll_form(req.POST)
        msgs='''请将此链接发送给客户进行填写:
                http://localhost:8000/crm/customer/registration/{enroll_obj_id}/{random_str}/'''
        if enroll_form.is_valid():
            try:
                print('enroll---',enroll_form.cleaned_data)
                enroll_form.cleaned_data['customer']=customer_obj
                enroll_obj=models.Enrollment.objects.create(**enroll_form.cleaned_data)
                # enroll_obj = models.Enrollment(**enroll_form.cleaned_data)
                # enroll_obj.save()
                print(enroll_obj)
                random_str = "".join(random.sample(string.ascii_lowercase + string.digits, 8))
                cache.set(enroll_obj.id, random_str, 3000)
                msg['msg']=msgs.format(enroll_obj_id=enroll_obj.id,random_str=random_str)


            except IntegrityError as e:


                enroll_obj=models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                         enrolled_class_id=enroll_form.cleaned_data['enrolled_class'].id)
                if enroll_obj.contract_agreed: #学生已经同意了
                    return redirect("/crm/contract_review/%s/"%enroll_obj.id)
                enroll_form.add_error('__all__','此条信息已创建，不能重复创建')

                random_str = "".join(random.sample(string.ascii_lowercase + string.digits, 8))
                cache.set(enroll_obj.id, random_str,3000)
                msg['msg'] = msgs.format(enroll_obj_id=enroll_obj.id,random_str=random_str)


    else:

        enroll_form=forms.enroll_form()
    return render(req,'sales/enrollment.html',{'enroll_form':enroll_form,
                                               'customer_obj':customer_obj,
                                               'msg':msg,
                                               'enroll_obj':enroll_obj
                                               })
import os
from perfectcrm import settings
def stu_registration(request,enroll_id,random_str):
    if cache.get(enroll_id) == random_str:
        enroll_obj = models.Enrollment.objects.get(id=enroll_id)
        if request.method=='POST':
            if request.is_ajax():
                print("ajax post, ", request.FILES)
                enroll_data_dir = "%s/%s" %(settings.ENROLLED_DATA,enroll_id)
                if not os.path.exists(enroll_data_dir):
                    os.makedirs(enroll_data_dir,exist_ok=True)

                for k,file_obj in request.FILES.items():
                    with open("%s/%s"%(enroll_data_dir, file_obj.name), "wb") as f:
                        for chunk in file_obj.chunks():
                            f.write(chunk)

                return HttpResponse("success")
            registrtion_form =forms.RegistrationForm(request.POST,instance=enroll_obj.customer)
            if registrtion_form .is_valid():
                registrtion_form.save()
                enroll_obj.contract_agreed=True
                enroll_obj.save()
                status=enroll_obj.contract_agreed
                return render(request,'sales/registration.html',{'status':status})
            print(request.POST)

        else:
            registrtion_form = forms.RegistrationForm(instance=enroll_obj.customer)
            if enroll_obj.contract_agreed==True:
                status=1
            else:
                status=0
    else:
        return HttpResponse('链接超时')





    return render(request,"sales/registration.html",{"registration_obj":registrtion_form,'enroll_obj':enroll_obj,
                                                      'status':status})


def payment(request,enroll_id):

    enroll_obj=models.Enrollment.objects.get(id=enroll_id)
    errors=[]
    if request.method=='POST':
        payamount=request.POST.get('amount')
        if payamount:
            payamount=int(payamount)
            if payamount<500:
                errors.append('金额不得低于500元')
            else:
                payment_obj=models.Payment.objects.create(
                    customer=enroll_obj.customer,
                    course=enroll_obj.enrolled_class.course,
                    amount=payamount,

                )
                enroll_obj.contract_approved=True
                enroll_obj.save()
                enroll_obj.customer.status=1
                enroll_obj.customer.save()
                return redirect('/king_admin/crm/customer/')
        else:
            errors.append('缴费金额不得低于500元')



    return render(request, "sales/payment.html", {'enroll_obj': enroll_obj,
                                                  'errors':errors })

def contract_review(request,enroll_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    enroll_form = forms.RegistrationForm(instance=enroll_obj)
    print('enroll_form',enroll_form)
    customer_form = forms.enroll_form(instance=enroll_obj.customer)

    payment_form = forms.PaymentForm()

    return render(request, 'sales/contract_review.html', {

                                                "enroll_obj":enroll_obj,
                                                "payment_form":payment_form,
                                                 'enroll_obj':enroll_obj,
                                                "enroll_form":enroll_form,
                                                'customer_form':customer_form})

def enrollment_rejection(request,enroll_id):

    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    enroll_obj.contract_agreed = False
    enroll_obj.save()

    return  redirect("/crm/customer/%s/enrollment/" %enroll_obj.customer.id)
