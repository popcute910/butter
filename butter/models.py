from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator

from mysite import settings

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(verbose_name='Username', max_length=20, unique=True, validators=[MinLengthValidator(5,), RegexValidator(r'^[a-zA-Z0-9]*$',)])
    email = models.EmailField(verbose_name='Email', max_length=50, unique=True)
    nickname = models.CharField(verbose_name='Name', max_length=10, blank=False, null=False)
    date_of_birth = models.DateField(verbose_name="Birth of date", blank=True, null=True)
    image = models.ImageField(verbose_name='Image', upload_to="image/", blank=True, null=True)
    url = models.URLField(verbose_name='URL', blank=True, null=True)
    introduction = models.TextField(verbose_name='Introduction', max_length=300, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    #AbstractBaseUserにはMyUserManagerが必要
    objects = MyUserManager()
    #一意の識別子として使用されます
    USERNAME_FIELD = 'email'
    #ユーザーを作成するときにプロンプ​​トに表示されるフィールド名のリストです。
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Connection(models.Model):
    follower = models.ForeignKey(MyUser, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(MyUser, related_name='following', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)

class Post(models.Model):
    post_user = models.ForeignKey(MyUser, related_name='post_user', on_delete=models.CASCADE)
    post_text = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.post_text

