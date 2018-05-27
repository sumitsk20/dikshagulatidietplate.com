from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse

from django.db.models.signals import pre_save
from django.utils import timezone
#from django.utils.html import conditional_escape
from django.utils.html import format_html_join
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from .utils import get_read_time
from ckeditor_uploader.image import pillow_backend as backend



class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)
    slug = models.CharField(max_length =10,null=True,blank=True,editable=False)
    seo_desc = models.CharField(max_length=160,blank=True,null=True,unique=True,help_text="This must not be more than 160 characters.")
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True,blank=True,null=True)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.capitalize()

    def get_absolute_url(self):
        context = {
        'cat_slug':self.slug,
        }
        return reverse("blog:category", kwargs=context)


class Tag(models.Model):
    name = models.CharField(max_length=15, unique=True)
    slug = models.CharField(max_length =10,null=True,blank=True,editable=False)
    seo_desc = models.CharField(max_length=160,blank=True,null=True,unique=True,help_text="This must not be more than 160 characters.")
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.capitalize()

    def get_absolute_url(self):
        context = {
        'tag_slug':self.slug,
        }
        return reverse("blog:tag", kwargs=context)


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(publish_this_post=True).filter(published_on__lte=timezone.now())


def upload_location(instance, filename):

    return "featured_post_images/%s/%s" %(instance.id, filename)

class Post(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, editable = False)
    title = models.CharField(max_length=58,unique=True,help_text="This must not be more than 58 characters.")
    slug = models.SlugField(unique=True,null=True,editable=False)
    featured_image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True)
    content = RichTextUploadingField(null=True,blank=True)
    seo_desc = models.CharField(max_length=160,blank=True,null=True,unique=True,help_text="This must not be more than 160 characters.")
    seo_keywords = models.CharField(max_length=350,blank=True,null=True,help_text="Try to keep list in Longest to shortest Keyword order. Must contain comma seperated list of key words.")
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    publish_this_post = models.BooleanField(default=False)
    published_on = models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True)
    read_time =  models.IntegerField(default=0) # models.TimeField(null=True, blank=True) #assume minutes
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def clean(self):
        self.title = self.title.capitalize()

    def all_categories(self):
            #all_tags_for_post = ', '.join(['<a href="{%tag.get_absolute_url%}">{{tag.name}}</a>'])
        return ', '.join([category.name for category in self.categories.all()])
    all_categories.short_description = "Categories"

    def all_tags(self):
    #     try:
    #         return format_html_join(
    #             ', ', '<a href="{}" target="blank">{}</a>',
    #             [(reverse('', args=[tag]), tag.name)
    #              for tag in self.tags.all()])
    #     except NoReverseMatch:
    #         return conditional_escape(self.tags.all())
    # all_tags.short_description = "Tags"
    #         #all_tags_for_post = ', '.join(['<a href="{%tag.get_absolute_url%}">{{tag.name}}</a>'])
        return ', '.join([tag.name for tag in self.tags.all()])
    all_tags.short_description = "Tags"

    def image_thumb(self):
        if self.featured_image :
            return '<img src="/media/%s" width="120" height="90" />' % (self.featured_image)
        return '<img src="/media/featured_post_images/default-featured-image.png" width="120" height="90" />'
    image_thumb.allow_tags = True   

    def get_absolute_url(self):
        return reverse("blog:post", kwargs={"post_slug": self.slug})

    class Meta:
        #ordering = ["-created_on", "-last_updated"]
        verbose_name = "Post"
        verbose_name_plural = 'Posts'


    def save(self, *args, **kwargs):
        if self.id and self.featured_image:
        #checking if previous image is not equalt to current image delete previous image
            try:
                this = Post.objects.get(id=self.id)
                if this.featured_image != self.featured_image:
                    this.featured_image.delete()
            except: pass # when new photo then we do nothing, normal case
        try:    
            if self.all_tags() not in self.seo_keywords:
                self.seo_keywords = '%s, %s'%(self.all_tags(),self.seo_keywords)
        except: pass
        super(Post, self).save(*args, **kwargs)
        if self.featured_image:
            backend.create_thumbnail(self.featured_image.name)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    ##setting publish date 
    if instance.publish_this_post == True and not instance.published_on:
        instance.published_on = timezone.now()
    instance.slug =slugify(instance.title)
    if instance.content:
        html_string = instance.content
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var

pre_save.connect(pre_save_post_receiver, sender=Post)

def pre_save_category_receiver(sender, instance, *args, **kwargs):
    instance.slug =slugify(instance.name)

pre_save.connect(pre_save_category_receiver, sender=Category)

def pre_save_tag_receiver(sender, instance, *args, **kwargs):
    instance.slug =slugify(instance.name)

pre_save.connect(pre_save_tag_receiver, sender=Tag)




class FaqManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(FaqManager, self).filter(is_active=True)
class Faq(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, editable = False)
    question = models.CharField(max_length=58,unique=True,help_text="This must not be more than 58 characters.")
    answer = RichTextUploadingField(null=True,blank=True)
    is_active = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = FaqManager()

    def __unicode__(self):
        return self.question

    def __str__(self):
        return self.question

    def clean(self):
        self.question = self.question.capitalize()