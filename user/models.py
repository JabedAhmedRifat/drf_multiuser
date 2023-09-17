from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_developer = models.BooleanField('student', default=False)
    is_marketer = models.BooleanField('marketer', default=False)
    is_tester = models.BooleanField('tester', default=False)
    
    def __str__(self):
        return self.is_developer
    
    def __str__(self):
        return self.is_marketer
    
    def __str__(self):
        return self.is_tester
    
    
    
    
    

