from django.db import models

class UploadFile(models.Model):
    uploadfile = models.FileField(upload_to='uploads/%Y/%m/%d')
