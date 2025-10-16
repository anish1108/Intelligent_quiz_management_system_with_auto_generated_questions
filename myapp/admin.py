# from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Profile, Quiz, Category, SubCategory

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'avatar')  


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'questions')  


@admin.register(Category)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name',)   


@admin.register(SubCategory)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name',)  

# @admin.register(QuizAttempt)
# class QuizAdmin(admin.ModelAdmin):
#     list_display = ('score')  

# @admin.register(Leaderboard)
# class QuizAdmin(admin.ModelAdmin):
#     list_display = ('score')   
    