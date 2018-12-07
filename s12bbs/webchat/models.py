from django.db import models
from bbs.models import UserProfile

# Create your models here.

class WebGroup(models.Model):
    name =models.CharField(max_length=64)
    brief = models.CharField(max_length=255, blank=True,null=True)
    owner = models.ForeignKey(UserProfile)
    admins = models.ManyToManyField(UserProfile, blank=True, related_name="group_admins")
    members = models.ManyToManyField(UserProfile, blank=True, related_name="group_members")
    max_members = models.IntegerField(default=200)

    def __str__(self):
        return self.name

# {"from": "1", "from_name": "Seven Qi", "to": "3", "contact_type": "single", "msg_content": "123", "msg_type": "text", "head_img": "1.jpg"}
class WebRecord(models.Model):
    from_name = models.CharField(max_length=64)
    from_user_id = models.IntegerField()
    to_name = models.CharField(max_length=64)
    to_user_id = models.IntegerField()
    contact_type = models.CharField(max_length=64)
    msg_content = models.CharField(max_length=10000)
    msg_type = models.CharField(max_length=64)
    head_img = models.CharField(max_length=64)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.to_name





