from django.db import models

# Create your models here.


class Contact(models.Model):
	"""docstring for Contact"""
	entity_type_choices = [
		(1, 'Person'),
		(2, 'Artificial'),
	]
	
	image = models.ImageField(upload_to='contacts/images/', null=True, blank=True)
	entity_type = models.IntegerField(default=1, choices=entity_type_choices)
	registered_name = models.CharField(max_length=50, null=True, blank=True)
	trade_name = models.CharField(max_length=50, null=True, blank=True)
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	middle_name = models.CharField(max_length=50, blank=True, null=True)
	alias = models.CharField(max_length=50, null=False, blank=False)
	tax_num = models.CharField(max_length=12, unique=True, null=True, blank=True)
	ss_num = models.CharField(max_length=20, blank=True, null=True)
	health_num = models.CharField(max_length=20, blank=True, null=True)
	hdmf_num = models.CharField(max_length=20, blank=True, null=True)
	date_of_birth = models.DateField()
	is_client = models.BooleanField(null=False, default=False)
	is_employee = models.BooleanField(null=False, default=False)
	is_deleted = models.BooleanField(default=False)
	vip_alias = models.CharField(max_length=10, null=True, blank=True)

	
	def __str__(self):
		ret = None
		if self.entity_type == 1:
			ret = self.full_name
		else:
			if self.trade_name:
				ret = self.trade_name
			else:
				ret = self.alias
		
		return ret
	
	@property
	def name(self, verbose_name='Name'):
		ret = None
		if self.entity_type == 1:
			ret = self.full_name
		else:
			ret = self.registered_name
		return ret	

	@property
	def full_name(self):
		last_name = self.last_name if self.last_name else ''
		first_name = self.first_name if self.first_name else ''
		middle_name = self.middle_name[0] if self.middle_name else ''

		full_name = '{last}, {first}'.format(last=last_name, first=first_name)
		full_name = ('{last}, {first} {middle}.'.format(last=last_name, first=first_name, middle=middle_name)) if middle_name else full_name
		return full_name

	@property
	def get_employee_id(self):
		if self.employee_set:
			ret = self.employee_set.first
			return ret
		else:
			ret = None
			return ret

	@property
	def get_tin_1(self):
		ret = self.tax_num
		if ret:
			tax_len = len(ret)
			if tax_len == 9 or tax_len == 12:
				# separate every 3 into '-'
				temp = [ret[i:i+3] for i in range(0, tax_len, 3)]
				ret = '-'.join(temp)
		else:
			ret = 'no TIN encoded'
		return ret

class Address(models.Model):
	class Meta:
		verbose_name_plural = 'Addresses'


	city_choices = [
		(1, 'CDO'),
		(2, 'CEB'),
		(3, 'MNL'),
	]

	"""docstring for ClassName"""
	contact = models.ForeignKey(Contact)
	address = models.CharField(max_length=100, blank=True)
	bldg = models.CharField(max_length=50, null=True, blank=True)
	streets = models.CharField(max_length=50, null=True, blank=True)
	town = models.CharField(max_length=50)
	city = models.IntegerField(null=True, blank=True, choices=city_choices)


class Phone(models.Model):
	"""docstring for ClassName"""
	phone_type_choices = [
		(1, 'Telephone'),
		(2, 'Mobile'),
	]

	contact = models.ForeignKey(Contact)
	phone_type = models.IntegerField(default=1, choices=phone_type_choices, null=False)
	number = models.CharField(max_length=50, null=False)
	person = models.CharField(max_length=50, null=True, blank=True)
	is_active = models.BooleanField(default=True)


class Email(models.Model):
	"""docstring for ClassName"""
	phone_type_choices = [
		(1, 'Telephone'),
		(2, 'Mobile'),
	]

	contact = models.ForeignKey(Contact)
	email = models.EmailField(max_length=50)
	person = models.CharField(max_length=50, null=True, blank=True, verbose_name='contact person')
	is_active = models.BooleanField(default=True)
