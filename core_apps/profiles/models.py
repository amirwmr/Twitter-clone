from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from core_apps.common.models import TimeStampedModel

User = get_user_model()

class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        Male = "M", _("Male"),
        FEMALE = "F", _("Female")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(verbose_name=_("phone number"), max_length=30)
    about_me = models.TextField(_("about me"))
    gender = models.CharField(verbose_name=_("gender"), choices= Gender.choices, max_length=20)
    country = CountryField(verbose_name=_("country"), max_length=100)
    city = models.CharField(_("city"), max_length=100)
    profile_photo = models.ImageField(_("profile photo"), default="/profile_default.png")
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)

    def __str__(self):
        return f"{self.user.first_name}'s Profile"

    def follow(self, profile):
        self.followers.add(profile)

    def unfollow(self, profile):
        self.followers.remove(profile)

    def check_following(self, profile):
        return self.followers.filter(pkid=profile.pkid).exists()
