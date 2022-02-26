from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.

class MyUserManager(UserManager):
  def create_user(self,email,first_name,last_name,password, **extra_fields):
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
    extra_fields['user_type'] = 'SA'
    return self.create_user(email,first_name,last_name,password,**extra_fields)

class User(AbstractUser):
  username = None
  # created_at is same as date_joined
  first_name = models.CharField('first name', max_length=150)
  last_name = models.CharField('last name', max_length=150)
  email = models.EmailField('email address', unique=True)
  phone_number = models.DecimalField('Phone no',max_digits=10,decimal_places=0,null=True,blank=True)
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
                                  null=True,
                                  blank=True,
                                  help_text='Only Sales Admin'
                                )
  profile = models.ImageField(null=True,blank=True)
  objects = MyUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name','last_name']
  def has_module_perms(self, app_label):
    return self.is_superuser or self.is_staff

  def has_perm(self, perm, obj=None):
    return self.is_superuser or self.is_staff

  def __str__(self):
      return f'{self.first_name} {self.last_name} ({self.email})'



class Lead(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
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
  state = models.CharField(max_length=4,choices=LEAD_STATE,null=True,blank=True)
  user_id = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,help_text='Only Sales Representative')

  def __str__(self) -> str:
    return f'{self.name} ({self.email})'

class Remark(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  remark = models.TextField()
  lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE)
  user_id = models.ForeignKey(User,on_delete=models.CASCADE)

