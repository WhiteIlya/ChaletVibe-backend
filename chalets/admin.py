from django import forms
from django.contrib import admin
from .models import Chalet, UserReaction

class ChaletCreationForm(forms.ModelForm):
    class Meta:
        model = Chalet
        fields = ['name', 'image', 'country', 'review', 'chalet_link', 'price', 'ski_resort_link', 'approximate_travel_time', 'beds']

class ChaletChangeForm(forms.ModelForm):
    class Meta:
        model = Chalet
        fields = ['name', 'image', 'country', 'review', 'chalet_link', 'price', 'ski_resort_link', 'approximate_travel_time', 'beds']

class ChaletAdmin(admin.ModelAdmin):
    form = ChaletChangeForm
    add_form = ChaletCreationForm

    list_display = ['name', 'country', 'price', 'beds', 'approximate_travel_time']
    list_filter = ['country']
    search_fields = ['name', 'review', 'country']
    ordering = ['name']

    fieldsets = [
        (None, {'fields': ['name', 'image', 'country', 'review', 'chalet_link', 'price', 'ski_resort_link', 'approximate_travel_time', 'beds']}),
    ]

    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['name', 'image', 'country', 'review', 'chalet_link', 'price', 'ski_resort_link', 'approximate_travel_time', 'beds']
        }),
    ]

class UserReactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'chalet', 'liked']
    list_filter = ['liked']
    search_fields = ['user__email', 'chalet__name']

admin.site.register(UserReaction, UserReactionAdmin)
admin.site.register(Chalet, ChaletAdmin)