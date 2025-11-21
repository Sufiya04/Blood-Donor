from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.
class Donor(models.Model):
    gender_data= [
        ('','Select Gender'),
        ('male','Male'),
        ('female','Female'),
        ('others','Others')
        ]
    blood_group= [
        ('','Select BloodGroup'),
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('O+','O+'),
        ('O-','O-'),
        ('AB+','AB+'),
        ('AB-','AB-')
    ]
    name= models.CharField(max_length=100)
    age= models.IntegerField()
    gender= models.CharField(max_length=10,choices=gender_data)
    blood= models.CharField(max_length=5,choices=blood_group)
    smoker= models.CharField(max_length=3,choices=[('','Are you a smoker?'),('yes','Yes'),('no','No')], default='Are you a smoker?')
    alcoholic= models.CharField(max_length=3, choices=[('','Are you an alcoholic?'),('yes','Yes'),('no','No')], default='Are you an alcoholic?')
    contact= models.CharField(max_length=10)
    units= models.IntegerField()
    health= models.TextField()
    last= models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Recipient(models.Model):
    gender_data=[
        ('','Gender'),
        ('male','Male'),
        ('female','Female'),
        ('others','Others')
    ]
    blood_group=[
        ('','Required Blood Group'),
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('O+','O+'),
        ('O-','O-'),
        ('AB+','AB+'),
        ('AB-','AB-')
    ]
    urgency=[
        ('', 'Urgency Level'),
        ('normal','Normal'),
        ('urgent','Urgent'),
        ('emergency','Emergency')
    ]
    name= models.CharField(max_length=100)
    age= models.IntegerField()
    gender= models.CharField(max_length=6, choices=gender_data)
    blood= models.CharField(max_length=3, choices=blood_group)
    units= models.IntegerField()
    urgent= models.CharField(max_length=10, choices=urgency)
    date= models.DateField()
    hos= models.CharField(max_length=100)
    add= models.CharField(max_length=100)
    requester= models.CharField(max_length=30)
    status= models.CharField(max_length=10, default='Pending', null=True, blank=True)

class BloodStock(models.Model):
    blood= models.CharField(max_length=3)
    units= models.IntegerField(default=0)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email