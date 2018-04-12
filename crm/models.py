# import django
# django.setup()
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (AbstractBaseUser,
                                           BaseUserManager,PermissionsMixin)


# Create your models hereels aren't loaded yet..



class Customer(models.Model):
    '''客户表'''
    name=models.CharField(max_length=32,blank=True,null=True)
    qq=models.CharField(max_length=64,unique=True)
    qq_name=models.CharField(max_length=64,blank=True,null=True)
    phone=models.CharField(max_length=64,blank=True,null=True)
    source_choices=((0,'转介绍'),(1,'QQ群'),(2,'官网'),(3,'百度推广'),(4,'51CTO'),(5,'知乎'),(6,'市场推广'))
    source=models.SmallIntegerField(choices=source_choices)
    referral_from=models.CharField(verbose_name='转介绍人qq',max_length=64,blank=True)
    content=models.TextField(verbose_name='咨询详情')
    consult_course=models.ForeignKey('Course',verbose_name='咨询课程',on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", blank=True, null=True)
    status_choices = ((0, '未报名'),
                      (1, '已报名'),
                      )
    status = models.SmallIntegerField(choices=status_choices)
    consultant=models.ForeignKey('UserProfile',on_delete=models.DO_NOTHING)
    memo=models.TextField(verbose_name='备注',null=True)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:

        verbose_name_plural='客户表'

    def __str__(self):
        return "%s %s " % (self.name, self.qq)
class Tag(models.Model):
    name=models.CharField(unique=True,max_length=32)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='标签'
        verbose_name_plural='标签'
class CustomerFollowUp(models.Model):
    customer=models.ForeignKey('Customer',on_delete=models.CASCADE)
    content=models.TextField(verbose_name='跟进内容')
    consultant=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    intention_choices=(
        (0,'2周内报名'),
        (1, '1个月内报名'),(2,'近期无报名计划'),(3,'已在其他机构报名'),

        (4, '已报名'),(5,'已拉黑'),

    )
    intention=models.SmallIntegerField(choices=intention_choices)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return ('<%s,%s>'%(self.customer.qq,self.intention))
    '''客户跟进表'''
    class Meta:

        verbose_name_plural='客户跟进表'
class Course(models.Model):
    '''课程表'''
    name=models.CharField(max_length=64,unique=True)
    price=models.PositiveSmallIntegerField()
    period=models.PositiveSmallIntegerField(verbose_name='周期（月）')
    outline=models.TextField()
    def __str__(self):
        return self.name
    class Meta:

        verbose_name_plural='课程表'
class Branch(models.Model):
    name=models.CharField(max_length=128,unique=True)
    addr=models.CharField(max_length=128)
    def __str__(self):
        return self.name
    class Meta:

        verbose_name_plural='分校表'
class ClassList(models.Model):
    '''班级表'''
    branch=models.ForeignKey('Branch',on_delete=models.CASCADE)
    contract = models.ForeignKey("ContractTemplate", blank=True, null=True,on_delete=models.CASCADE)

    course=models.ForeignKey('Course',on_delete=models.CASCADE)
    semester=models.PositiveSmallIntegerField(verbose_name='学期')
    class_type_choices=(
    (0,'面授(脱产)'),
    (1, '面授(周末)'),
    (2, '网络班'),
    )
    teachers=models.ManyToManyField('UserProfile')
    start_date=models.DateField(verbose_name='开班日期')
    end_date=models.DateField(verbose_name='结业日期',blank=True,null=True)
    def __str__(self):
        return "%s %s %s"%(self.branch,self.course,self.semester)
    class Meta:
        unique_together=('branch','course','semester')



        verbose_name_plural = '班级表'


class CourseRecord(models.Model):
    '''上课记录'''
    from_class=models.ForeignKey('ClassList',verbose_name='班级',on_delete=models.CASCADE)
    day_num=models.PositiveSmallIntegerField(verbose_name='第几节（天）')
    teacher=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    has_homework=models.BooleanField(default=True)
    homework_title = models.CharField(max_length=32,blank=True,null=True)
    homework_content=models.TextField(blank=True,null=True)
    outline=models.TextField(verbose_name='本节课程大纲')
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return ('%s_%s %s'%('courseRecord',self.from_class,self.day_num))
    class Meta:
        unique_together=('from_class','day_num')

        verbose_name_plural = '上课记录'
class StudyRecord(models.Model):
    '''学习记录'''
    student=models.ForeignKey('Enrollment',on_delete=models.CASCADE)
    course_record=models.ForeignKey('CourseRecord',on_delete=models.CASCADE)
    attendance_choices=(
        (0,'已签到'),
        (1,'迟到'),(2,'缺勤'),(3,'早退'),
    )
    attendance=models.SmallIntegerField(choices=attendance_choices,default=0)
    score_choices=(
        (100,'A+'),(90,'A'),(85,'B+'),(80,'B'),(75,'B-'),
        (70, 'C+'),(65,'C'),(60,'A+'),(40,'C-'),(-50,'D'),(-100,'COPY'),(0,'N/A')

    )
    score=models.SmallIntegerField(choices=score_choices)
    memo=models.TextField(blank=True,null=True)
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return ("%s %s %s"%(self.student.customer.name,self.course_record,self.score))
    class Meta:
        unique_together=('student','course_record')

        verbose_name_plural='学习记录表'

class Enrollment(models.Model):
    '''报名表'''
    customer=models.ForeignKey('Customer',on_delete=models.CASCADE)
    enrolled_class=models.ForeignKey('ClassList',verbose_name='所报班级',on_delete=models.CASCADE)
    consultant=models.ForeignKey('UserProfile',verbose_name='课程顾问',on_delete=models.CASCADE)
    contract_agreed=models.BooleanField(verbose_name='学员已同意',default=False)
    contract_approved=models.BooleanField(verbose_name='合同已审核',default=False)
    date=models.DateField(auto_now_add=True)
    def __str__(self):
        return ('%s _%s %s'%('Enrollment',self.customer.name,self.enrolled_class))
    class Meta:
        unique_together=('customer','enrolled_class')
        verbose_name_plural = '报名表'

class ContractTemplate(models.Model):
    '''合同模板'''
    name=models.CharField('合同名称',max_length=32,unique=True)
    template=models.TextField()
    def __str__(self):
        return self.name
class Payment(models.Model):
    '''缴费记录'''
    customer=models.ForeignKey('Customer',on_delete=models.CASCADE)
    course=models.ForeignKey("Course",verbose_name='所报课程',on_delete=models.CASCADE)
    amount=models.SmallIntegerField(verbose_name='数额',default=500)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return ('%s %s  %s'%('Payment',self.customer.name,self.amount))
    class Meta:
        verbose_name_plural = '缴费表'

# class UserProfile(models.Model):
#     '''账号表'''
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     name=models.CharField(max_length=32)
#     roles=models.ManyToManyField('Role')
#     def __str__(self):
#         return (self.name)
class UserProfileManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        """
        Creates and saves a User with the given email,date of birth and password.
        :param email:
        :param name:
        :param password:
        :return:
        """
        if not email:
            raise ValueError('User must have an email address')
        user=self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        self.is_active=True
        user.save(using=self._db)
        return user
    def create_superuser(self,email,name,password):
        """
        Creates and saves a superuser with the given eamil,date of birth and password.
        :param email:
        :param name:
        :param password:
        :return:
        """
        user=self.create_user(
            email,
            password=password,
            name=name,

        )
        user.is_active=True
        user.is_admin=True
        user.save(using=self._db)
        return user
class UserProfile(AbstractBaseUser,PermissionsMixin):

    email=models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )
    name=models.CharField(max_length=32)
    is_active=models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    role = models.ManyToManyField("Role", blank=True, null=True)

    objects=UserProfileManager()
    stu_account = models.ForeignKey("Customer", verbose_name="关联学员账号", blank=True, null=True,
                                    help_text="只有学员报名后方可为其创建账号",on_delete=models.CASCADE)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        #The user is identified by their email address
        return self.email
    def get_short_name(self):
        #The user is identified by their email address
        return self.email
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        "Does the user have a specific permission?"
        #Simplest possible answer:Yes,always
        return True
    def has_module_perms(self,app_label):
        "Does the user have permissions to view the app'app_label"
        #Simplest possible answer:Yes,always
        return True
    class Meta:
        permissions = (
            ('audit_table_list', '可以查看audit每张表里所有的数据'),
            ('audit_table_list_view', '可以访问audit表里每条数据的修改页'),
            ('audit_table_list_change', '可以对audit表里的每条数据进行修改'),
            ('audit_table_obj_add_view', '可以访问audit每张表的数据增加页'),
            ('audit_table_obj_add', '可以对audit每张表进行数据添加'),

        )

class Role(models.Model):
   name=models   .CharField(max_length=32, unique=True)
   menus = models.ManyToManyField('Menu', blank=True)

   def __str__(self):
       return (self.name)

   class Meta:
       verbose_name_plural = '角色表'

class Menu(models.Model):
    '''菜单'''
    name=models.CharField(max_length=32)
    url_type_choices=((0,'alias'),(1,'absolute_url'))
    url_type=models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name=models.CharField(max_length=64,unique=True)
    def __str__(self):
        return self.name