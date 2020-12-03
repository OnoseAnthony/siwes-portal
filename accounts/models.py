from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)



Session = (
    ('', 'Select Year'),
    ('2018/2019', '2018/2019'),
)

college = (
    ('', 'Select College'),
    ('COLLEGE OF SCIENCE', 'Science'),
    ('COLLEGE OF TECHNOLOGY', 'Technology')
)

Level = (
    ('', 'Select Level'),
    ('300', '300'),
    ('400','400')
)

Department = (
    ('', 'Select Dept'),
    ('Chemistry', 'Chemistry'),
    ('Industrial Chemistry', 'Industrial Chemistry'),
    ('Physics', 'Physics'),
    ('Geophysics', 'Geophysics'),
    ('Geology', 'Geology'),
    ('Computer Science', 'Computer Science'),
    ('Mathematics', 'Mathematics'),
    ('Environmental Management Toxicology', 'Environmental Sci'),
    ('Petroleum Engineering', 'Petroleum Engr'),
    ('Chemical Engineering','Chemical Engr'),
    ('Electrical Electronics Engineering', 'Elect/Elect Engr'),
    ('Mechanical Engineering', 'Mechanical Engr'),
    ('Marine Engineering', 'Marine Engr')
)
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, matric_no, session, image, password=None, iz_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not full_name:
            raise ValueError("Users must have a full name")
        if not matric_no:
            raise ValueError("Users must have a matric_no")
        if not session:
            raise ValueError("Users must choose a session")
        user_obj = self.model(
            email       = self.normalize_email(email),
            full_name   = full_name,
            matric_no   = matric_no,
            session     = session,
            image       = image,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name, matric_no, session,  password=None):
        user = self.create_user(
                email,
                full_name,
                matric_no,
                session,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, email, matric_no, full_name, session, password=None):
        user = self.create_user(
                email,
                full_name,
                matric_no,
                session,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user





class User(AbstractBaseUser):
    email       = models.EmailField(max_length=50,)
    full_name   = models.CharField(max_length=50,)
    matric_no   = models.CharField(max_length=50, unique=True)
    session     = models.CharField(max_length=50, choices=Session,blank=True)
    College     = models.CharField(max_length=50, choices=college, blank=True, null=True)
    level       = models.CharField(max_length=50, choices=Level, blank=True, null=True)
    department  = models.CharField(max_length=50, choices=Department, blank=True, null=True)
    image       = models.ImageField(upload_to='profile_image', blank=True, null=True)
    is_active   = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'matric_no'
    REQUIRED_FIELDS = ['full_name', 'email', 'session'] # Email & Password are required by default.

    objects = UserManager()

    def __str__(self):              # __unicode__ on Python 2
             return self.matric_no

    def get_matric_no(self):
        # The user is identified by their matric number
        return self.matric_no

    def get_email(self):
        return self.email

    def get_level(self):
        return self.level

    def get_College(self):
        return self.College

    def get_department(self):
        return self.department

    def get_session(self):
        return self.session

    def get_image(self):
        return self.image

    def get_full_name(self):
        # The user  name is identified by their full name
        return self.full_name

    def get_short_name(self):
        # The user  name is identified by their full name
        return self.full_name

    def get_department(self):
        # The user is identified by their email address
        return self.department

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def iz_active(self):
        "Is the user active?"
        return self.active

User = get_user_model()



class NewzUpdate(models.Model):
    heading         = models.CharField(max_length=200, blank=True, null=True)
    date            = models.DateTimeField(auto_now_add=True)
    body            = models.TextField(blank=True, null=True)
    by              = models.CharField(max_length=50, default='Admin', blank=True, null=True)
    file            = models.FileField(upload_to='docs', null=True)

    def __str__(self):
        pkz = self.by
        return pkz



class SiwesInformation(models.Model):
    user                        = models.OneToOneField(User)
    bankName                    = models.CharField(max_length=50, blank=True, default='', null=True)
    accountNo                   = models.CharField(max_length=50, blank=True,  null=True, default='')
    sort_code                   = models.CharField(max_length=50, blank=True, null=True)
    phoneNo                     = models.CharField(max_length=50, null=True,blank=True)
    industryName                = models.CharField(max_length=50, default='', blank=True, null=True)
    industryAddress             = models.CharField(max_length=50, default='', blank=True, null=True)
    industrySupervisorname      = models.CharField(max_length=50, default='', blank=True, null=True)
    industrySupervisorPhoneno   = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        pkz = self.user.matric_no
        return pkz


class SupervisorInformation(models.Model):
    user                = models.OneToOneField(User)
    supervisorName      = models.CharField(max_length=50,  blank=True, null=True, default='')
    supervisorPhone     = models.CharField(max_length=50, null=True, blank=True)
    supervisorDept      = models.CharField(max_length=50, blank=True, null=True)
    supervisorEmail     = models.EmailField(blank=True, null=True)

    def __str__(self):
        pkz = self.user.matric_no
        return pkz

""" The create_profiles function creates and attaches supervisors information and siwes information
    for each registered during successful registration
"""
def create_profiles(sender, **kwargs):
    if kwargs['created']:
        siwesinformation           = SiwesInformation.objects.create(user=kwargs['instance'])
        supervisorinformation      = SupervisorInformation.objects.create(user=kwargs['instance'])

post_save.connect(create_profiles, sender=User)
