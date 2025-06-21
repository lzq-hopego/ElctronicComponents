from django.db import models

# Create your models here.


class Elctroniccomponents(models.Model):
    # 元器件表
    name=models.CharField("元器件名",max_length=255)
    price=models.FloatField("元器单价")
    model=models.CharField("元器件型号",max_length=255)
    category=models.CharField("元器件分类",max_length=255)
    fengzhuang=models.CharField("元器件封装",max_length=255)
    location=models.CharField("元器件存放位置",max_length=255)
    specifications=models.JSONField("元器件属性",blank=True)
    stock=models.IntegerField("元器件库存")
    image_url=models.TextField("元器件图片链接",blank=True)
    description=models.TextField("描述",blank=True)
    careate_time=models.DateTimeField("入库的时间",blank=True,null=True,auto_now=True)

class ElctroniccomponentsLog(models.Model):
    # 元器操作日志表
    name=models.CharField("元器件名",max_length=255)
    price=models.FloatField("元器单价")
    model=models.CharField("元器件型号",max_length=255)
    category=models.CharField("元器件分类",max_length=255)
    fengzhuang=models.CharField("元器件封装",max_length=255)
    location=models.CharField("元器件存放位置",max_length=255)
    specifications=models.JSONField("元器件属性",blank=True)
    stock=models.IntegerField("元器件库存")
    image_url=models.TextField("元器件图片链接",blank=True)
    description=models.TextField("描述",blank=True)
    uselog=models.CharField("进行的操作",max_length=255)
    index_time=models.DateTimeField("操作的时间",blank=True,null=True,auto_now=True)


