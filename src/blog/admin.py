from django.contrib import admin
from django.forms import CheckboxSelectMultiple, FileInput
from django.db import models
from .widgets import ColumnCheckboxSelectMultiple
# Register your models here.
from .models import Post, Category, Tag, Faq


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "all_categories", "all_tags", "last_updated", "created_on", "image_thumb"]
    list_filter = ["last_updated", "created_on"]

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'categories', 'tags'),
        }),
        ('Publish', {
            'fields': (('publish_this_post', 'published_on'), ('created_on', 'last_updated')),
        }),
        ('Featured', {
            'fields': (('featured_image', 'image_thumb'),),
        }),
        ('SEO', {
            'fields': ('seo_keywords', 'seo_desc'),
        }),

    )
    readonly_fields = ('image_thumb', 'published_on', 'created_on', 'last_updated')
    search_fields = ["title", "content"]
    filter_horizontal = ('categories', 'tags')
    formfield_overrides = {
        models.ImageField: {'widget': FileInput},
    }

    class Meta:
        model = Post

    # METHOD TO RESTRICT CURRENT USER TO VIEW TOPICS WRITTEN BY HIM/HER ONLY
    def get_queryset(self, request):
        qs = super(PostModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    # METHOD TO RESTRICT CURRENT USER TO CHANGE TOPICS WRITTEN BY HIM/HER ONLY
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(PostModelAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["name", "created_on"]
    search_fields = ["name"]
    list_filter = ["created_on"]


class TagModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class FaqModelAdmin(admin.ModelAdmin):
    list_display = ["question", "is_active"]
    search_fields = ["question", "answer"]
    list_filter = ["created_on"]


admin.site.register(Tag, TagModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(Faq, FaqModelAdmin)
