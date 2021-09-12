from typing import Counter
from django.db import models


class Member(models.Model):
    LEVEL_CHOICES = [
        ('B1', '大一'),
        ('B2', '大二'),
        ('B3', '大三'),
        ('B4', '大四'),
        ('M1', '碩一'),
        ('M2', '碩二'),
    ]

    STATUS_CHOICES = [
        ('UR', '審核中'),
        ('M', '已入社'),
        ('NP', '未付款'),
    ]

    PAY_CHOICES = [
        ('C', '現金'),
        ('R', '匯款'),
    ]

    SCHOOL_CHOICES = [
        ('Y', '逢甲大學'),
        ('N', '其他學校'),
    ]
    name = models.CharField(max_length=50)
    nid = models.CharField(max_length=15, unique=True)
    dept = models.CharField(max_length=20)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    # 不能用 unique=True，因為空字串也會被判斷成一樣
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default="UR")
    pay = models.CharField(max_length=2, choices=PAY_CHOICES, default="C")
    bankAccount = models.CharField(max_length=5, null=True, blank=True)
    is_FCU = models.CharField(max_length=5, choices=SCHOOL_CHOICES,default="Y")
    school = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "%s %s [%s]" % (self.nid, self.name, self.get_status_display())


class secret(models.Model):
    """
    保密協議
    """
    name = models.CharField(max_length=50)
    nid = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=15, null=True,
                             unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

class receipt(models.Model):
    """
    紀錄收據的編號
    """
    count = models.IntegerField()