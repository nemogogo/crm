#__author:zhang_lei
#date:2018/1/30
from django.forms import forms,ModelForm
from django.utils.translation import ugettext as _
from django.forms import ValidationError
from crm import models

def creat_model_form(request,admin_class):

    class Meta:
        model=admin_class.model
        fields="__all__"
    def default_clean(self):
        error_list = []
        self.ValidationError = ValidationError
        if not hasattr(admin_class, "is_add_form"):
            print("-------------------default_clean")
            print('------------->>>instance',self.instance)
            print('----------->>>>>',admin_class.readonly_fields)

            for field in admin_class.readonly_fields:
                field_val = getattr(self.instance, field)
                field_from_page = self.cleaned_data.get(field)
                if field in admin_class.filter_horizontal:
                    field_val = getattr(self.instance, field).select_related()
                    print(dir(field_val))
                    field_val=str(field_val.order_by('id'))
                    field_from_page=str(field_from_page.order_by('id'))
                print( (field_val), field_from_page)
                if field_val!= field_from_page:
                    error_list.append(ValidationError(
                        _("Field %(field)s is readonly,data should be %(val)s"),
                        code='invalid',
                        params={'field': field, 'val': field_val}
                    ))

        response=admin_class.default_clean_form(self)
        if response:
            error_list.append(response)
        if error_list:
            print(error_list)
            raise ValidationError(error_list)

    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            # print(field_name,dir(field_obj))
            # field_obj.widget.attrs['class'] = 'form-control'
            # field_obj.widget.attrs['maxlength'] = getattr(field_obj,'max_length' ) if hasattr(field_obj,'max_length') \
            #     else ""
            if not hasattr(admin_class, "is_add_form"):  # 代表这是添加form,不需要disabled
                if field_name in admin_class.readonly_fields:
                    field_obj.widget.attrs['disabled'] = 'disabled'

            # if hasattr(admin_class, "clean_%s" % field_name):
            #     field_clean_func = getattr(admin_class, "clean_%s" % field_name)
            #     setattr(cls, "clean_%s" % field_name, field_clean_func)
            if hasattr(admin_class,"clean_%s"%field_name):
                clean_func=getattr(admin_class,"clean_%s"%field_name)
                setattr(cls,"clean_%s"%field_name,clean_func)

        return ModelForm.__new__(cls)

    _model_form_class=type("DynamicModelForm",(ModelForm,),{'Meta':Meta})

    setattr(_model_form_class, '__new__', __new__)
    setattr(_model_form_class, 'clean', default_clean)
    return _model_form_class