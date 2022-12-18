from django.contrib import admin
from test_app import models


# @admin.register(models.AnswersQuestionModel)
class AnswersQuestionModelAdmin(admin.TabularInline):
    model = models.AnswersQuestionModel


class TestQuestionsModelAdmin(admin.TabularInline):
    model = models.TestQuestionsModel


@admin.register(models.TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    inlines = [
        TestQuestionsModelAdmin,
        AnswersQuestionModelAdmin
    ]
