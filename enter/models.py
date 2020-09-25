from django.db import models

class Attend(models.Model):
    name = models.CharField(max_length=50)
    nid = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return "%s %s" % (self.nid, self.name)

class Checkin(models.Model):
    STATUS_CHOICES = [
        ('NO', '無法領獎'), 
        ('YET', '尚未領獎'),
        ('TIX', '已使用票券領獎'),
        ('FORM', '已填表單領獎'),
        ('MIX', '已填表單加使用票券領獎'),
    ]

    nid = models.CharField(max_length=15, unique=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default="NO")

    def __str__(self):
        return "%s [%s]" % (self.nid, self.get_status_display())
