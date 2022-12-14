from django.db import models
from authapp.models import AbstractUserModel


class TestModel(models.Model):
    name = models.CharField(verbose_name="Test name", max_length=200)
    description = models.TextField(
        verbose_name="Description for test", blank=True, null=True)


class TestQuestionsModel(models.Model):
    quest = models.CharField(verbose_name="Quest")
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE)


class AnswersQuestionModel(models.Model):
    answer = models.CharField(verbose_name="Answer option", max_length=300)
    is_success = models.BooleanField(verbose_name="Success", default=False)
    quest = models.ForeignKey(TestQuestionsModel, on_delete=models.CASCADE)


class UserResults(models.Model):
    user = models.ForeignKey(AbstractUserModel, on_delete=models.CASCADE)
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE)
    success_count = models.CharField(
        verbose_name="Success quests", max_length=50)
    Nosuccess_count = models.CharField(
        verbose_name="Nosuccess quests", max_length=50)
