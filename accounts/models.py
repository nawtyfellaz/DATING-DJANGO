import random
import os

from datetime import timedelta, date
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

# phone number app
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from localflavor.us.models import USStateField, USSocialSecurityNumberField, USZipCodeField

from dating.utils import random_string_generator, unique_key_generator, get_filename

# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    # print(instance)
    #print(filename)
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
            new_filename=new_filename, 
            final_filename=final_filename
            )

#Email Activation Days before expiration
DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name=None, middle_name=None, surname=None, password=None, is_active=True, is_client=False, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not middle_name:
            raise ValueError("Users must have a middle name")
        if not surname:
            raise ValueError("Users must have a surname")
        if not password:
            raise ValueError("Users must have a password")
        user = self.model(
            email = self.normalize_email(email),
            first_name=first_name,
            middle_name=middle_name,
            surname=surname,
        )
        user.set_password(password) # change user password
        user.client = is_client
        user.staff = is_staff
        user.admin = is_superuser
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_clientuser(self, email, first_name=None, middle_name=None, surname=None, password=None):
        user = self.create_user(
                email,
                first_name=first_name,
                middle_name=middle_name,
                surname=surname,
                password=password,
        )
        user.is_client=True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name=None, middle_name=None, surname=None, password=None):
        user = self.create_user(
                email,
                first_name=first_name,
                middle_name=middle_name,
                surname=surname,
                password=password,
        )
        user.is_client=True
        user.is_staff=True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name=None, middle_name=None, surname=None, password=None):
        user = self.create_user(
                email,
                first_name=first_name,
                middle_name=middle_name,
                surname=surname,
                password=password,
        )
        user.is_client=True
        user.is_staff=True
        user.is_superuser=True
        user.is_active=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name      = models.CharField(max_length=255, null=True,)
    middle_name     = models.CharField(max_length=255, null=True,)
    surname         = models.CharField(max_length=255, null=True,)
    email           = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    is_active       = models.BooleanField(default=True) # can login 
    is_client       = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False) # staff user non superuser
    is_superuser    = models.BooleanField(default=False) # superuser 
    timestamp       = models.DateTimeField(auto_now_add=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'surname' ] #['full_name'] #python manage.py createsuperuser

    objects = MyUserManager()

    def __str__(self):
        return '{} {} {}'.format(self.first_name, self.middle_name, self.surname)
        
    @property
    def full_name(self):
        return self.__str__

    @property
    def short_name(self):
        return '{} {}'.format(self.first_name, self.surname)

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        if self.short_name:
            return self.short_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # @property
    # def is_client(self):
    #     if self.is_superuser or self.is_staff:
    #         return True
    #     return self.client

    # @property
    # def is_staff(self):
    #     if self.is_superuser:
    #         return True
    #     return self.staff

    # @property
    # def is_superuser(self):
    #     return self.admin

    # @property
    # def is_active(self):
    #     return self.active


class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        # does my object have a timestamp in here
        end_range = now
        return self.filter(
                activated = False,
                forced_expired = False
              ).filter(
                timestamp__gt=start_range,
                timestamp__lte=end_range
              )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
                    Q(email=email) | 
                    Q(user__email=email)
                ).filter(
                    activated=False
                )


class EmailActivation(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    email           = models.EmailField()
    key             = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    forced_expired  = models.BooleanField(default=False)
    expires         = models.IntegerField(default=7) # 7 Days
    timestamp       = models.DateTimeField(auto_now_add=True)
    update          = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable() # 1 object
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            # pre activation user signal
            user = self.user
            user.is_active = True
            user.save()
            # post activation signal for user
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', 'https://www.dating.com')
                key_path = reverse("account:email-activate", kwargs={'key': self.key}) # use reverse
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = '1-Click Email Verification'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                            subject,
                            txt_,
                            from_email,
                            recipient_list,
                            html_message=html_,
                            fail_silently=False,
                    )
                return sent_mail
        return False


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_reciever, sender=User)


class Profile(models.Model):
    SEX = (
        ('s', 'SEX'),
        ('m', 'MALE'),
        ('f', 'FEMALE'),
    )
    KIDS = (
        ('no', 'NO'),
        ('yes', 'YES'),
        ('maybe', 'MAYBE')
    )
    SEX_INTEREST = (
        ('m', 'MALE'),
        ('f', 'FEMALE'),
        ('b', 'MALE & FEMALE'),
    )
    MARITAL = (
        ('si', 'SINGLE'),
        ('ma', 'MARRIED'),
        ('di', 'DIVORCED'),
        ('se', 'SEPERATED'),
    )
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username        = models.CharField(max_length=255, null=True, blank=True)
    passport        = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    sex             = models.CharField(max_length=7, blank=True, null=True, choices=SEX, default='s' )
    interest        = models.CharField(max_length=18, blank=True, null=True, choices=SEX_INTEREST, default='m')
    marital         = models.CharField(max_length=18, blank=True, null=True, choices=MARITAL)
    kids            = models.CharField(max_length=5, blank=True, null=True, choices=KIDS)
    next_of_kin     = models.CharField(max_length=255, blank=True, null=True,)
    height          = models.PositiveSmallIntegerField(blank=True, null=True,)
    # weight          = models.CharField()
    # religion        = models.CharField()
    DOB             = models.DateField(max_length=8, blank=True, null=True, help_text="year-month-day")
    phone           = PhoneNumberField(blank=True, help_text='Contact phone number must start with "+123" or any internationalize country code', null=True)#, E164_only=True
    fax             = PhoneNumberField(blank=True, help_text='Contact fax number', null=True)
    address         = models.CharField(max_length=300,  blank=True, null=True)
    city            = models.CharField(max_length=300,  blank=True, null=True)
    zip_code        = USZipCodeField(null=True, blank=True)
    state_province  = USStateField(null=True, blank=True)
    SSN             = USSocialSecurityNumberField(null=True, blank=True, help_text="format: xxx-xx-xxxx (only applies to US Citizens")
    country         = CountryField(blank=True, null=True,)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.short_name)
    
    @property
    def age(self):
        return int((date.today() - self.DOB).days / 365.25)

    def get_absolute_url(self):
        #url = reverse("question_single", kwargs={"id": self.id})
        url = reverse("account:home", kwargs={"username": self.user.username})
        return url

    def like_link(self):
        url = reverse("like_user", kwargs={"id": self.user.id})
        return url

# @receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)

# @receiver(post_save, sender=User)
def save_user_profile(sender, instance, *args, **kwargs):
    instance.profile.save()
post_save.connect(save_user_profile, sender=User)
