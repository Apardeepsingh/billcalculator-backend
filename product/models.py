from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password=None, password2=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", 'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_category', null=True, blank=True)
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    category_name = models.CharField(max_length=100)

    
    def __str__(self):
        return self.category_name



class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_product', null=True, blank=True)
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    itemCode = models.CharField(max_length=255, unique=True)
    itemName = models.CharField(max_length=255)
    itemPrice = models.DecimalField(max_digits=10, decimal_places=2)
    itemCat = models.ManyToManyField(Category, related_name="products", blank=True)

    
    def __str__(self):
        return f"{self.itemCode} - {self.itemName}"
