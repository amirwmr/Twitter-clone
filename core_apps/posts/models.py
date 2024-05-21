from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import TimeStampedModel

User = get_user_model()

class Post(TimeStampedModel):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(verbose_name=_("Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    text = models.TextField(_("Post Content")) # could use richtext
    # like, comment, views,...

    def __str__(self):
        return f"{self.title} by {self.text}"

...