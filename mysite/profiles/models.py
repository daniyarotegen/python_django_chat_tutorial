from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(AbstractUser):
    BUSINESS_SECTORS = (
        ('agriculture', 'Agriculture'),
        ('construction', 'Construction'),
        ('manufacturing', 'Manufacturing'),
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail'),
        ('transportation', 'Transportation'),
        ('information', 'Information'),
        ('finance', 'Finance and Insurance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education Services')
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    business_sector = models.CharField(choices=BUSINESS_SECTORS, max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    expertise = models.CharField(max_length=100, blank=True, null=True)
    resources = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    requests = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    interesting_facts = models.TextField(blank=True, null=True)
    marital_status = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    whatsapp_url = models.URLField(blank=True, null=True)
    telegram_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    vk_url = models.URLField(blank=True, null=True)
    tiktok_url = models.URLField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="profile_set",
        related_query_name="profile",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="profile_set",
        related_query_name="profile",
    )
