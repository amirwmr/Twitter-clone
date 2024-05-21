from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            raise ValueError(_("You must provide a valid email address."))

    def create_user(self, first_name, last_name, email, password, **extra_field):
        if not first_name:
            raise ValueError(_("Users must have a first name."))
        if not last_name:
            raise ValueError(_("Users must have a last name."))
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Users must have an email address."))

        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_field)
        user.set_password(password)

        extra_field.setdefault("is_staff", False)
        extra_field.setdefault("is_superuser", False)

        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_field):
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser", True)
        extra_field.setdefault("is_active", True)

        if extra_field.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff = True."))
        if extra_field.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser = True."))
        if extra_field.get("is_active") is not True:
            raise ValueError(_("Superuser must have is_active = True."))
        if not password:
            raise ValueError(_("Superuser must have password."))
        if not email:
            raise ValueError(_("Users must have an email address."))

        user = self.create_user(first_name, last_name, email, password, **extra_field)
        return user
