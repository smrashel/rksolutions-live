from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser


class Company(models.Model):
    name = models.CharField('Company Name', max_length = 200)
    contact_number = models.CharField('Contact Number', max_length = 200, unique = True)
    email_address = models.EmailField('Email', max_length = 200, unique = True, null = True, blank = True)
    address = models.CharField('Address', max_length = 200)
    joining_date = models.DateField('Joining Date', null = True, blank = True)
    company_logo = models.ImageField('Company Logo',null = True, blank = True)
    is_active = models.BooleanField('Active', default = True)
    is_paid = models.BooleanField('Paid', default = False)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name='Updated By'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Company Name', null=True, blank=True)


class Member(models.Model): 
    gym = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Gym Name', null=True, blank=True)
    member_id = models.CharField('Member Id', max_length = 6, unique = True, null = True, blank = True)
    name = models.CharField('Member Name', max_length = 200)
    contact_number = models.CharField('Contact Number', max_length = 16, unique = True, null = True, blank = True)
    nid_number = models.CharField('NID Number', max_length = 16, unique = True, null = True, blank = True)
    email_address = models.EmailField('Email', max_length = 200, unique = True, null = True, blank = True)
    height = models.CharField('Height in Inc', max_length = 3, null = True, blank = True)
    weight = models.CharField('Weight in Kg', max_length = 3, null = True, blank = True)
    joining_date = models.DateField('Joining Date', null = True, blank = True)
    member_pic = models.ImageField('Member Picture',null = True, blank = True)
    is_active = models.BooleanField('Active', default = True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name='Added By'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=False, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name='Updated By'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
    
    def __str__(self):
        return self.name


class Trainer(models.Model): 
    gym = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Gym Name', null=True, blank=True)
    name = models.CharField('Member Name', max_length = 200)
    contact_number = models.CharField('Contact Number', max_length = 16, unique = True, null = True, blank = True)
    email_address = models.EmailField('Email', max_length = 200, unique = True, null = True, blank = True)
    height = models.CharField('Height in Inc', max_length = 3, unique = True, null = True, blank = True)
    weight = models.CharField('Weight in Kg', max_length = 3, unique = True, null = True, blank = True)
    joining_date = models.DateField('Joining Date', null = True, blank = True)
    is_active = models.BooleanField('Active', default = True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name='Added By'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=False, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name='Updated By'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = 'Trainer'
        verbose_name_plural = 'Trainers'

    def __str__(self):
        return self.name


class Income(models.Model):
    gym = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Gym Name', null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='Member')
    payment_month = models.DateField('Payment Month')
    payment_date = models.DateField('Payment Date', null = True, blank = True)
    payment_amount = models.IntegerField('Payment Amount', default = 0)
    remark = models.CharField('Remark', max_length = 200, null = True, blank = True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name='Added By'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=False, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name='Updated By'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = 'Income'
        verbose_name_plural = 'Incomes'

 
class Expense(models.Model):
    gym = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Gym Name')
    expense_date = models.DateField('Expense Date', null = True, blank = True)
    particular = models.CharField('Particular', max_length = 200)
    amount = models.IntegerField('Amount', default = 0)
    remark = models.CharField('Remark', max_length = 200, null = True, blank = True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name='Added By'
    )
    added_date = models.DateTimeField('Added Date', auto_now_add=False, null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True, related_name='+', verbose_name='Updated By'
    )
    updated_date = models.DateTimeField('Updated Date', auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def __str__(self):
        return self.particular