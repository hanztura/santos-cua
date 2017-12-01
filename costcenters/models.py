from django.db import models

from contacts.models import Contact

# Create your models here.
class Branch(models.Model):
	parent = models.ForeignKey('self', null=True, blank=True, related_name='branches')
	contact = models.OneToOneField(Contact, null=True, blank=True)
	alias = models.CharField(max_length=50, null=True, blank=True)
	is_deleted = models.BooleanField(default=False)
	
	class Meta:
		verbose_name_plural = 'Branches'

	def __str__(self):
		if self.parent:
			return ' | '.join([str(self.parent), str(self.alias)])
		else:
			return str(self.alias)


class Project(models.Model):
	parent = models.ForeignKey('self', null=True, blank=True, related_name='sub_projects')
	branch = models.ForeignKey(Branch, null=True, blank=True, related_name='projects')
	contact = models.OneToOneField(Contact, null=True, blank=True)
	alias = models.CharField(max_length=50)
	remarks = models.CharField(max_length=100, null=True, blank=True)
	is_deleted = models.BooleanField(default=False)
	
	def __str__(self):
		return self.alias

	@property
	def is_sub_project(self):
		if self.parent:
			ret = True
		else:
			ret = False
		return ret


class Work(models.Model):
	work_name = models.CharField(max_length=50, verbose_name='name')
	description = models.CharField(max_length=100)
	is_deleted = models.BooleanField(default=False)
	
	def __str__(self):
		return self.work_name