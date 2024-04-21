from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """

    created_at = models.DateTimeField(_("created"), auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True
