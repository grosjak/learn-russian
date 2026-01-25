from django.contrib import admin
from .models import Lesson, Letter, Word, UserWordProgress, Story

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_language', 'order')

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('character', 'transliteration', 'name', 'friendship_category')
    list_filter = ('friendship_category',)

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text_root', 'base_form', 'language', 'french', 'category', 'aspect')
    list_filter = ('language', 'category', 'aspect')
    search_fields = ('text_root', 'base_form', 'french', 'russian')

@admin.register(UserWordProgress)
class UserWordProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'needs_review', 'next_review_date', 'interval')
    list_filter = ('needs_review',)

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty')
