from django.contrib import admin
from test_app import models
from django import forms


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.AnswersQuestionModel
        fields = ('quest', 'test', 'answer', 'is_success',)

    def clean(self):
        cleaned_data = super().clean()
        is_success = cleaned_data.get("is_success")
        if is_success:
            # Проверяем, что у других ответов не установлен чекбокс "Верный ответ"
            answers = models.AnswersQuestionModel.objects.filter(
                quest=cleaned_data.get("quest"))
            answers_cnt = answers.count()
            i = 0
            for answer in answers:
                if answer.is_success:
                    i += 1
                    # raise ValidationError(
                    #     "Нельзя установить более одного верного ответа")
            if i == answers_cnt:
                raise ValidationError(
                    "Нельзя установить более одного верного ответа")
            elif i < 1:
                raise ValidationError(
                    "Должен быть минимум 1 правильный ответ")
        return cleaned_data


class AnswersQuestionModelAdmin(admin.StackedInline):
    form = AnswerForm
    model = models.AnswersQuestionModel
    fields = ('quest', 'test', 'answer', 'is_success',)


class TestQuestionsModelAdmin(admin.TabularInline):
    model = models.TestQuestionsModel


@admin.register(models.TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    inlines = [
        TestQuestionsModelAdmin,
        AnswersQuestionModelAdmin
    ]
