from django.db import models
from dvadmin.utils.models import CoreModel

# Create your models here.

class KeyInfoModel(CoreModel):
    id_number=models.CharField(max_length=18,verbose_name='身份证号码',help_text='身份证号码',unique=True,blank=True)
    car_id=models.CharField(max_length=7,verbose_name='车牌号',help_text='车牌号',unique=True,blank=True)
    name=models.CharField(max_length=15,verbose_name='姓名',help_text='姓名')
    car_color=models.CharField(max_length=3,verbose_name='车牌颜色')
