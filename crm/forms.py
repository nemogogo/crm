#__author:zhang_lei
#date:2018/2/7
from django.forms import ModelForm
from crm import models

class enroll_form(ModelForm):
    class Meta:
        model=models.Enrollment
        fields=['enrolled_class','consultant']

class RegistrationForm(ModelForm):
    class Meta:
        model=models.Customer
        fields='__all__'
        exclude=['referral_from','consultant','content','tags','memo','status','consult_course']
        readonly_fields=['qq']
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class']='form-control'
            # if field_name in cls.Meta.readonly_fields:
            #     field_obj.widget.setattr('disabled','disabled')
            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs['disabled'] = 'disabled'
        return ModelForm.__new__(cls)
    def clean_qq(self):
        if self.instance.qq!=self.cleaned_data['qq']:
            self.add_error('qq','qq不能被修改')
        return self.cleaned_data['qq']


class PaymentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            #print(field_name,dir(field_obj))
            field_obj.widget.attrs['class'] = 'form-control'

        return ModelForm.__new__(cls)
    class Meta:
        model = models.Payment
        fields = "__all__"