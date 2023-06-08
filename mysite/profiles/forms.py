from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['avatar', 'first_name', 'last_name', 'business_sector', 'company', 'expertise', 'resources',
                  'achievements', 'goals', 'requests', 'city', 'date_of_birth', 'hobbies', 'education',
                  'interesting_facts', 'marital_status', 'phone_number', 'website', 'whatsapp_url',
                  'telegram_url', 'instagram_url', 'twitter_url', 'facebook_url', 'vk_url', 'tiktok_url']
