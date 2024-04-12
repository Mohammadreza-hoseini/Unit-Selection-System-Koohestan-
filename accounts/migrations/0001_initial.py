# Generated by Django 4.2.11 on 2024-03-26 14:33

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserRole",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "role",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "student"),
                            (2, "professor"),
                            (3, "ITManager"),
                            (4, "educationalAssistant"),
                        ],
                        default=1,
                        verbose_name="سطح دسترسی",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Professor",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("firstname", models.CharField(max_length=256, verbose_name="نام")),
                (
                    "lastname",
                    models.CharField(max_length=256, verbose_name="نام خانوادگی"),
                ),
                (
                    "professor_number",
                    models.CharField(
                        max_length=256, unique=True, verbose_name="شماره استادی"
                    ),
                ),
                ("password", models.CharField(max_length=256, verbose_name="رمز عبور")),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="ایمیل"
                    ),
                ),
                (
                    "national_code",
                    models.CharField(max_length=11, unique=True, verbose_name="کد ملی"),
                ),
                ("expertise", models.CharField(max_length=256, verbose_name="تخصص")),
                (
                    "degree",
                    models.CharField(max_length=256, verbose_name="مرتبه یا درجه"),
                ),
                (
                    "professor",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="professor_user_role",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="نوع کاربر",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("firstname", models.CharField(max_length=256, verbose_name="نام")),
                (
                    "lastname",
                    models.CharField(max_length=256, verbose_name="نام خانوادگی"),
                ),
                (
                    "student_number",
                    models.CharField(
                        max_length=256, unique=True, verbose_name="شماره دانشجویی"
                    ),
                ),
                ("password", models.CharField(max_length=256, verbose_name="رمز عبور")),
                (
                    "avatar",
                    models.URLField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="تصویر پروفایل",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="ایمیل"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=11, unique=True, verbose_name="شماره تلفن"
                    ),
                ),
                (
                    "national_code",
                    models.CharField(max_length=11, unique=True, verbose_name="کد ملی"),
                ),
                (
                    "gender",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "male"), (2, "female")],
                        default=1,
                        verbose_name="جنسیت",
                    ),
                ),
                ("birth_date", models.DateField(verbose_name="تاریخ تولد")),
                ("entry_year", models.DateField(verbose_name="سال ورودی")),
                (
                    "incoming_semester",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "first"), (2, "second")],
                        default=1,
                        verbose_name="ترم ورودی",
                    ),
                ),
                (
                    "average",
                    models.FloatField(blank=True, null=True, verbose_name="معدل"),
                ),
                (
                    "military_service_status",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "male"), (2, "female")],
                        verbose_name="وضعیت نظام وظیفه",
                    ),
                ),
                ("years", models.IntegerField(default=1, verbose_name="سنوات")),
                (
                    "student",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student_user_role",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="نوع کاربر",
                    ),
                ),
                (
                    "supervisor",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student_supervisor",
                        to="accounts.professor",
                        verbose_name="انتخاب استاد راهنما",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ITManager",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("firstname", models.CharField(max_length=256, verbose_name="نام")),
                (
                    "lastname",
                    models.CharField(max_length=256, verbose_name="نام خانوادگی"),
                ),
                (
                    "it_manager_number",
                    models.CharField(
                        max_length=256, unique=True, verbose_name="شماره منیجر آیتی"
                    ),
                ),
                ("password", models.CharField(max_length=256, verbose_name="رمز عبور")),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="ایمیل"
                    ),
                ),
                (
                    "national_code",
                    models.CharField(max_length=11, unique=True, verbose_name="کد ملی"),
                ),
                (
                    "IT_manager",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ITManager_user_role",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="نوع کاربر",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EducationalAssistant",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "assistant",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="EducationalAssistant_assistant",
                        to="accounts.professor",
                        verbose_name="معاون آموزشی",
                    ),
                ),
                (
                    "educational_assistant",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="EducationalAssistant_user_role",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="نوع کاربر",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="University",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("address", models.TextField(verbose_name="آدرس دانشگاه")),
                ("phone", models.CharField(verbose_name="شماره تماس")),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="ایمیل"
                    ),
                ),
                (
                    "educational_assistant",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="university_educational_assistant",
                        to="accounts.professor",
                        verbose_name="معاون آموزشی دانشگاه",
                    ),
                ),
                (
                    "university_president",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="university_university_president",
                        to="accounts.professor",
                        verbose_name="رئیس دانشگاه",
                    ),
                ),
            ],
            options={
                "unique_together": {("educational_assistant", "university_president")},
            },
        ),
    ]
