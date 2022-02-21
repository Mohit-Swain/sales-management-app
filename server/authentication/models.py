from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
# Create your models here.

class MyUserManager(UserManager):
  def create_user(self,email,first_name=None,last_name=None,password=None, **extra_fields):
    if not email:
      raise ValueError('Users must have an Email address')
    if not first_name:
      raise ValueError('Users must have a First Name')
    if not last_name:
          raise ValueError('Users must have a Last Name')
    if not password:
          raise ValueError('Users must have a Password')
    
    user = self.model(
      email = self.normalize_email(email),
      first_name = first_name,
      last_name = last_name,
      **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self,email,first_name,last_name,password, **extra_fields):
    extra_fields['is_superuser'] = True
    extra_fields['is_staff'] = True
    extra_fields['is_approved'] = True

    return self.create_user(email,first_name,last_name,password,**extra_fields)

class User(AbstractUser):
  username = None
  email = models.EmailField('email address', unique=True)
  phone_number = models.DecimalField(max_digits=10,decimal_places=0,null=True)
  is_approved = models.BooleanField(default=False)

  SALES_ADMIN = 'SA'
  SALES_REPRESENTATIVE = 'SR'
  USER_TYPES = [
    (SALES_ADMIN,'Sales Admin'),
    (SALES_REPRESENTATIVE,'Sales Representative')
  ]

  user_type = models.CharField(max_length=2,choices=USER_TYPES,default=SALES_REPRESENTATIVE)

  manager_id = models.ForeignKey('self',
                                  on_delete=models.SET_NULL,
                                  limit_choices_to={'user_type' : SALES_ADMIN},
                                  related_name='managed_users',
                                  null=True,
                                  default=None
                                )
  objects = MyUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name','last_name']

  def __str__(self):
      return f'{self.first_name} {self.last_name} ({self.email})'



class Lead(models.Model):
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)
  name = models.CharField(max_length=150)
  email = models.EmailField(
      max_length=255,
      unique=True,
  )
  phone_number = models.DecimalField(max_digits=10,decimal_places=0)
  
  HOT = 'HOT'
  COLD = 'COLD'
  MEDIUM = 'MED'
  SOLD = 'SOLD'
  
  LEAD_STATE = [
    (HOT, 'hot'),
    (COLD,'cold'),
    (MEDIUM,'medium'),
    (SOLD,'sold')
  ]
  state = models.CharField(max_length=4,choices=LEAD_STATE,null=True,default=None)
  user_id = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,default=None)

class Remark(models.Model):
  created_at = models.DateTimeField(default=timezone.now)
  remark = models.TextField()
  lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE)
  user_id = models.ForeignKey(User,on_delete=models.CASCADE)

