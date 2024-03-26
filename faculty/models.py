from django.db import models
import uuid

# Create your models here.
from accounts.models import University


class Faculty(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=256, verbose_name='نام دانشکده')
    phone = models.CharField(max_length=256, unique=True, verbose_name='شماره دانشکده')
    address = models.TextField(verbose_name='آدرس دانشکده')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculty_university',
                                   verbose_name='انتخاب دانشگاه')

    def __str__(self):
        return self.name


class Major(models.Model):
    id = models.CharField(default=uuid.uuid4, editable=False, primary_key=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='major_faculty',
                                verbose_name='انتخاب دانشکده')
    name = models.CharField(max_length=256, verbose_name='نام رشته')
    department = models.CharField(max_length=256, verbose_name='گروه آموزشی')
    number_of_units = models.PositiveBigIntegerField(verbose_name='تعداد واحد')
    education_level = models.CharField(max_length=256, verbose_name='مقطع تحصیلی')

    def __str__(self):
        return f"{self.faculty.name} - {self.name}"
