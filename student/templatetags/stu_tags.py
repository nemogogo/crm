#__author:zhang_lei
#date:2018/2/9

from django import template
from django.db.models import Sum

register=template.Library()

@register.simple_tag
def get_score(enroll_obj,customer_obj):
    study_records = enroll_obj.studyrecord_set. \
        filter(course_record__from_class_id=enroll_obj.enrolled_class.id)

    # for record in study_records:
    # #     print('-->',record)
    # print(enroll_obj.enrolled_class.course_record_set)
    return study_records.aggregate(Sum('score'))

    # studyrecord_objs=enroll_obj.enrolled_class.course_record_set.studyrecord_set.filter(course_record__from_class_id=enroll_obj.enrolled_class.id)
    # return studyrecord_objs.aggregate(sum('score'))