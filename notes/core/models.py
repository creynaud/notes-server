from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def uuid():
    return str(uuid4())


def revision():
    return "0-{0}".format(uuid())


class Document(models.Model):
    uuid = models.CharField(_('UUID'), max_length=255, default=uuid,
                            unique=True, db_index=True)
    revision = models.CharField(_('Revision'), max_length=255,
                                default=revision)

    def save(self, *args, **kwargs):
        revision_number = int(self.revision[:self.revision.index('-')])
        self.revision = "{0}-{1}".format(revision_number + 1, uuid())
        super(Document, self).save(*args, **kwargs)


class Note(Document):
    date = models.DateTimeField(_('Date'), default=timezone.now)
    title = models.TextField(_('Title'), null=True, blank=True)
    text = models.TextField(_('Text'), null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name=_('Owner'),
                              related_name='notes')

    class Meta:
        ordering = ['date']

    def __unicode__(self):
        return u"{0}: {1}".format(self.title, self.text)
