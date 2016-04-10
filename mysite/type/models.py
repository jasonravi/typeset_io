from django.db import models
from datetime import datetime
from time import strftime
import sys
# Create your models here.

class UnixTimestampField(models.DateTimeField):
    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True  # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        typ = ['TIMESTAMP']
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value:
            return None
        return strftime('%Y-%m-%d %H:%M:%S', value.timetuple())

class Paragraph(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300,verbose_name='Title')
    blog =  models.CharField(max_length=3000,verbose_name='Blog')
    created_on = UnixTimestampField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'paragraph'

    def __unicode__(self):
        return "%s" % (unicode(self.title))

class Comment(models.Model):
	id = models.AutoField(primary_key=True)
	message_comment = models.CharField(max_length=300,verbose_name='Comment')
	paragraph_id = models.IntegerField()
	created_on = UnixTimestampField(auto_now=True)
	created_by = models.CharField(max_length=50, blank=True,null=True)
	class Meta:
		managed = False
		db_table = 'Comment'
	def __unicode__(self):
		return "%s" % (unicode(self.message_comment))

	def save(self, *args, **kwargs):
		super(Comment,self).save(*args, **kwargs)
