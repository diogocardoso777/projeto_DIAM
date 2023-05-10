from django.contrib import admin
from django.urls import path
from .models import Country, Team, Sport, Forum
from django import forms


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Country, CountryAdmin)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'country']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'country']


admin.site.register(Team, TeamAdmin)


class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['name']


class SportAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(Sport, SportAdmin)


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['name', 'genre']


class ForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'id']


admin.site.register(Forum, ForumAdmin)

