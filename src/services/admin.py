from django.contrib import admin
from django.forms import FileInput
from django.db import models
# Register your models here.
from .models import Service, Appointment, Subscriber


class ServiceModelAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "last_updated", "created_on", "image_thumb"]
    list_filter = ["last_updated", "created_on"]

    fieldsets = (
        (None, {
            'fields': ('name', 'content'),
        }),
        ('Publish', {
            'fields': (('is_active', 'published_on'), ('created_on', 'last_updated')),
        }),
        ('Featured', {
            'fields': (('featured_image', 'image_thumb'),),
        }),
        ('SEO', {
            'fields': ('seo_desc', 'seo_keywords'),
        }),

    )
    readonly_fields = ('image_thumb', 'published_on', 'created_on', 'last_updated')
    search_fields = ["name", "content"]
    formfield_overrides = {
        models.ImageField: {'widget': FileInput},
    }

    class Meta:
        model = Service

    # METHOD TO RESTRICT CURRENT USER TO VIEW TOPICS WRITTEN BY HIM/HER ONLY
    def get_queryset(self, request):
        qs = super(ServiceModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    # METHOD TO RESTRICT CURRENT USER TO CHANGE TOPICS WRITTEN BY HIM/HER ONLY
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(ServiceModelAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class AppointmentModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "number", "service", "seen"]
    search_fields = ["name", "number", "email"]
    list_filter = ["seen"]


class SubscriberModelAdmin(admin.ModelAdmin):
    list_display = ["email", "is_subscribed"]
    search_fields = ["email"]
    list_filter = ["is_subscribed"]


# admin.site.register(Subscriber, SubscriberModelAdmin)
admin.site.register(Appointment, AppointmentModelAdmin)
admin.site.register(Service, ServiceModelAdmin)
