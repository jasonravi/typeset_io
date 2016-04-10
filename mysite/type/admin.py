from django.contrib import admin
from .models import *
from nested_inline.admin import NestedModelAdmin
from django.utils import timezone
# Register your models here.

class ParagraphAdmin(NestedModelAdmin):
    search_fields = ['id','title',]
    list_display = ('id', 'title', 'blog','created_by')
    list_display_links = ('title',)
    readonly_fields = ('id','created_on','created_by')
    """fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['id', 'title', 'blog', 'created_on','created_by']
        })
    ]"""
    def save_model(self, request, obj, form, change):
        if obj.id == None:
            obj.created_by = request.user.username
            obj.created_on = timezone.now()
        obj.save()

class CommentAdmin(NestedModelAdmin):
    search_fields = ['id','paragraph_id',]
    list_display = ('id', 'message_comment', 'paragraph_id','created_by')
    list_display_links = ('message_comment',)
    readonly_fields = ('id','created_on','created_by')
    """fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['id', 'message_comment', 'paragraph_id', 'created_on','created_by']
        })
    ]"""
    def save_model(self, request, obj, form, change):
        if obj.id == None:
            obj.created_by = request.user.username
            obj.created_on = timezone.now()
        obj.save()


admin.site.register(Paragraph,ParagraphAdmin)
admin.site.register(Comment,CommentAdmin)