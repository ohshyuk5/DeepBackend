from django.db import models

# Create your models here.
class Data(models.Model):
    user_id = models.CharField(max_length=128, null=False)
    req_id = models.CharField(max_length=128, null=False)
    video = models.CharField(max_length=256, null=True)
    photo = models.CharField(max_length=256, null=True)
 
    class Meta:
        db_table = "Data" #Table이름을 "User"로 정한다 default 이름은 api_user_user가 된다.