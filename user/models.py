import datetime

from django.db import models
from django.utils.functional import cached_property
# Create your models here.
from django.forms import BooleanField


class User(models.Model):
    """用户数据模型"""
    SEX = (
        ('M','男'),
        ('F','女'),
    )
    nickname = models.CharField(max_length=32,unique=True)
    phonenumber = models.CharField(max_length=16,unique=True)
    sex = models.CharField(max_length=8,choices=SEX)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    avatar = models.CharField(max_length=256)
    location = models.CharField(max_length=32)
    """property装饰器把类中的方法作为一个属性进行操作，使用类似user = User(),user.age即可得到返回值，不用加括号age()"""
    @cached_property#这个装饰器的作用跟装饰器@property类似，只是这个装饰器功能封装的更加全面，封装了类似语句if 'my_profile' not in self.__dict__:的功能，意思时被它装饰的方法只会执行一次，如果age属性已经存在就不会执行，如果不存在age属性，被它装饰的方法才会执行
    def age(self):
        tody = datetime.date.today()
        birth_date = datetime.date(self.birth_year,self.birth_month,self.birth_day)
        return (tody-birth_date).days//365
    """通过类创建一个对象的时候，对象拥有的属性可以通过objects.__dict__的方法获取，返回的是一个字典，下面会用到这个知识点"""
    @property
    def profile(self):
        """用户配置项，使用id手动关联另外一张表（一对一关联）"""
        if 'my_profile' not in self.__dict__:
        #上面的if语句可以用python提供的更方便的方法hasattr判断一个属性是否在对象中:if not hasattr(self, 'my_profile'),添加了这个if语句，当我们在调用这个属性执行这个方法时，只会去数据库中查询一次，提高了代码的效率
            my_profile,_ = Profile.objects.get_or_create(id=self.id)#这里下划线”_“也是一个变量名
            self.my_profile = my_profile
        return self.my_profile

class Profile(models.Model):
    """用户配置项"""
    SEX = (
        ('M', '男'),
        ('F', '女'),
    )
    dating_sex = models.CharField(default='女',max_length=8, choices=SEX, verbose_name='匹配的性别')
    location = models.CharField(max_length=32,verbose_name='目标城市')

    min_distance = models.IntegerField(default=1,verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10,verbose_name='最大查找范围')

    min_dating_age = models.IntegerField(default=18,verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=45,verbose_name='最大交友年龄')

    vibration= models.BooleanField(default=True,verbose_name='是否开启震动')
    only_matche =models.BooleanField(default=True,verbose_name='是否允许匹配的人查看我的相册')
    auto_play= models.BooleanField(default=True,verbose_name='是否自动播放视频')





