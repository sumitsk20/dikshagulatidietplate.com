from django.contrib import admin

# Register your models here.
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
	list_display = ["user", "is_parent", "parent","timestamp"]
	

# admin.site.register(Comment,CommentAdmin)