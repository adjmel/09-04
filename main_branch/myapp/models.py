from django.db import models

#In your app’s models.py, create a UserProfile model to store 
#user-specific 2FA information:

from django.contrib.auth.models import User
from django.db import models
from django_otp.plugins.otp_totp.models import TOTPDevice

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    devices = models.ManyToManyField(TOTPDevice)
