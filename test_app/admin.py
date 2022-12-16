from django.contrib import admin
from test_app import models


@admin.register(models.TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']


@admin.register(models.TestQuestionsModel)
class TestQuestionsModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'quest', 'test']


@admin.register(models.AnswersQuestionModel)
class AnswersQuestionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'quest', 'is_success']
