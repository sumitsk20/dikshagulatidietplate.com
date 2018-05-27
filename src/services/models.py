from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.image import pillow_backend as backend
from django.db.models.signals import post_save, pre_save


# from captcha.fields import ReCaptchaField


class Subscriber(models.Model):
    """docstring for ClassName"""
    email = models.EmailField(max_length=254, unique=True)
    is_subscribed = models.BooleanField(default=True)


class ServiceManager(models.Manager):
    def active(self, *args, **kwargs):
        # Service.objects.all() = super(ServiceManager, self).all()
        return super(ServiceManager, self).filter(is_active=True).filter(published_on__lte=timezone.now())


def upload_location(instance, filename):
    return "featured_service_images/%s/%s" % (instance.id, filename)


class Service(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=10, null=True, blank=True)
    seo_desc = models.CharField(max_length=160, blank=True, null=True, unique=True,
                                help_text="This must not be more than 160 characters and must relate to Service")
    seo_keywords = models.CharField(max_length=350, blank=True, null=True,
                                    help_text="Try to keep list in Longest to shortest Keyword order. Must contain comma seperated list of key words.")
    featured_image = models.ImageField(upload_to=upload_location,
                                       null=True,
                                       blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    published_on = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = ServiceManager()

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.capitalize()

    def image_thumb(self):
        if self.featured_image:
            return '<img src="/media/%s" width="120" height="90" />' % (self.featured_image)
        return '<img src="/media/featured_post_images/default-featured-image.png" width="120" height="90" />'

    image_thumb.allow_tags = True

    def get_absolute_url(self):
        context = {
            'service_slug': self.slug,
        }
        return reverse("service:service_detail", kwargs=context)

    def save(self, *args, **kwargs):
        if self.id and self.featured_image:
            # checking if previous image is not equalt to current image delete previous image
            try:
                this = Service.objects.get(id=self.id)
                if this.featured_image != self.featured_image:
                    this.featured_image.delete()
            except:
                pass  # when new photo then we do nothing, normal case
        super(Service, self).save(*args, **kwargs)
        if self.featured_image:
            backend.create_thumbnail(self.featured_image.name)


class Appointment(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=254)
    number = models.CharField(max_length=13, blank=True, null=True)
    service = models.ForeignKey(Service, blank=True, null=True)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.capitalize()


def pre_save_service_receiver(sender, instance, *args, **kwargs):
    ##setting publish date
    if instance.is_active == True and not instance.published_on:
        instance.published_on = timezone.now()
    instance.slug = slugify(instance.name)  # create_slug(instance)


pre_save.connect(pre_save_service_receiver, sender=Service)
