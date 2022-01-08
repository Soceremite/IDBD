from django.db import models
from django.utils import timezone
class User(models.Model):
    username = models.CharField(max_length=20,unique=True, verbose_name = '账号')
    password = models.CharField(max_length=100, verbose_name = '密码')
    create_time = models.DateTimeField(default=timezone.now, verbose_name = '创建日期')
    update_time = models.DateTimeField(default=timezone.now, verbose_name = '更新日期')
    
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'user'
class UserToken(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    token = models.CharField( max_length=64)

class Userinfo(models.Model):
    nickName = models.CharField(max_length=50,default='新用户', verbose_name = '昵称')
    face = models.CharField(max_length=255,default='img/test.jpg', verbose_name = '头像')
    realName = models.CharField(max_length=50, null=True, verbose_name = '真实姓名')
    idcard = models.CharField(max_length=19, null=True, verbose_name = '身份证号')
    drivercard = models.CharField(max_length=13, null=True, verbose_name = '驾驶证号')
    carcard = models.CharField(max_length=20, null=True, verbose_name = '车牌号')
    #sex 0；未知 1：男 2：女
    sex = models.IntegerField(default=0, verbose_name = '性别')
    birth = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, verbose_name = '生日')
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    class Meta:
        db_table = 'userinfo'


class Admin(models.Model):
    adminname = models.CharField(max_length=20, verbose_name = '管理员用户名')
    password = models.CharField(max_length=100, verbose_name = '密码')
    create_time = models.DateTimeField(default=timezone.now, verbose_name = '创建日期')
    update_time = models.DateTimeField(default=timezone.now, verbose_name = '更新日期')
    face = models.CharField(max_length=255,default='img/test.jpg', verbose_name = '头像')
    class Meta:
        db_table = 'admin'    

class AdminToken(models.Model):
    user = models.OneToOneField("Admin", on_delete=models.CASCADE)
    token = models.CharField( max_length=64)

class Police(models.Model):
    username = models.CharField(max_length=20,unique=True, verbose_name = '账号')
    password = models.CharField(max_length=100, verbose_name = '密码')
    policeid = models.CharField(max_length=19, null=True,verbose_name = '警号')
    idcard = models.CharField(max_length=19,null=True, verbose_name = '身份证号')
    realName = models.CharField(max_length=50, null=True, verbose_name = '真实姓名')
    class Meta:
        db_table = 'police'          

class PoliceToken(models.Model):
    police = models.OneToOneField("Police", on_delete=models.CASCADE)
    token = models.CharField( max_length=64)

class Mobile(models.Model):
    user = models.ForeignKey(User,related_name="mobiles",on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now, verbose_name = '起始日期')
    end_time = models.DateTimeField(default=timezone.now, verbose_name = '终止日期')
    class Meta:
        db_table = 'mobile'      

class Drink(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now, verbose_name = '起始日期')
    end_time = models.DateTimeField(default=timezone.now, verbose_name = '终止日期')
    class Meta:
        db_table = 'drink'             

class Smoke(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now, verbose_name = '起始日期')
    end_time = models.DateTimeField(default=timezone.now, verbose_name = '终止日期')
    class Meta:
        db_table = 'smoke'      

#疲劳程度
class Tired(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    degree = models.CharField(max_length=19, default='0',verbose_name = '疲劳指数')
    start_time = models.DateTimeField(default=timezone.now, verbose_name = '起始日期')
    end_time = models.DateTimeField(default=timezone.now, verbose_name = '终止日期')
    class Meta:
        db_table = 'tired'    

#哈欠
class Yawn(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    number = models.CharField(max_length=19, default='0',verbose_name = '哈欠次数')
    start_time = models.DateTimeField(default=timezone.now, verbose_name = '起始日期')
    end_time = models.DateTimeField(default=timezone.now, verbose_name = '终止日期')
    class Meta:
        db_table = 'yawn'   

#眨眼
class Blink(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    number = models.CharField(max_length=19, default='0',verbose_name = '眨眼次数')
    start_time = models.DateTimeField(default=timezone.now, verbose_name = '起始日期')
    end_time = models.DateTimeField(default=timezone.now, verbose_name = '终止日期')
    class Meta:
        db_table = 'blink'    