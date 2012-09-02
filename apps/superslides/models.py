from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from easy_thumbnails.fields import ThumbnailerImageField

class Slide(TimeStampedModel):
    name = models.CharField(_('Title'), max_length=200)
    caption = models.CharField(_('Caption'), max_length=255, blank=True, null=True,
            help_text="Displayed below the slide, if a caption exists.")
    image = ThumbnailerImageField(_('Image'), blank=True, upload_to=settings.SUPERSLIDES_ROOT)
    published=models.BooleanField(_('Published'), default=True)

    class Meta:
        verbose_name=_('Slide')
        verbose_name_plural=_('Slides')

    def __unicode__(self):
        return u'%s' % self.name

