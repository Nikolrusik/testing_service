from cgi import test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import AnswersQuestionModel, TestModel, TestQuestionsModel, UserResults
from authapp.models import AbstractUserModel
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView, ListView, CreateView, DetailView, DeleteView, UpdateView
from django.shortcuts import HttpResponseRedirect, render
from urllib import request


class TestsView(TemplateView):
    template_name = "test_app/tests.html"

    def get_context_data(self, **kwargs):
        context = super(TestsView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        context['tests'] = TestModel.objects.all()
        context['questions'] = TestQuestionsModel.objects.all()

        return context


class QuestView(TemplateView):
    template_name = "test_app/questions.html"

    def get_context_data(self, **kwargs):
        context = super(QuestView, self).get_context_data(**kwargs)

        if self.request.GET.get('test_id'):
            test_id = self.request.GET.get('test_id')
            test = TestModel.objects.get(id=test_id)
            context['questions'] = TestQuestionsModel.objects.filter(test=test).order_by('id')
            context['first_quest']  = context['questions'].first()
            context['test'] = test
            if 'questions' not in self.request.session:
                self.request.session['questions'] = []
        if self.request.GET.get('quest'):
            quest_id = self.request.GET.get('quest')
            context['quest'] = get_object_or_404(
                TestQuestionsModel, id=quest_id)
            context['answers'] = AnswersQuestionModel.objects.filter(
                quest=context['quest'])
            context['success_answers_count'] = AnswersQuestionModel.objects.filter(
                quest=context['quest'], is_success=True).count()

            if quest_id not in self.request.session['questions']:
                self.request.session['questions'] += [quest_id, ]
        else:
            del self.request.session['questions']
        return context

    def post(self, request, *args, **kwargs):
        if 'test' not in request.session:
            request.session['test'] = []
        test_id = request.POST.get('test_id')
        test = TestModel.objects.get(id=test_id)
        quest = TestQuestionsModel.objects.get(id=request.POST.get('quest_id'))
        next_quest = TestQuestionsModel.objects.filter(
            test=test).filter(id__gt=quest.id).order_by('id').first()

        if request.POST.get('answer_radio'):
            answer = AnswersQuestionModel.objects.get(
                id=request.POST.get('answer_radio'))
            request.session['test'] += [answer.is_success,]
        else:
            selected_values = request.POST.getlist('answer_check')
            result_answer = True
            for i in selected_values:
                answer = AnswersQuestionModel.objects.get(
                    id=i)
                if answer.is_success == False:
                    result_answer = False
            request.session['test'] += [result_answer]

        if next_quest != None:
            return HttpResponseRedirect(f"/questions/?test_id={test_id}&quest={int(next_quest.id)}")
        else:
            user = AbstractUserModel.objects.get(id=request.user.id)
            success_answers = 0
            failure_answers = 0
            for i in request.session['test']:
                if i == True:
                    success_answers += 1
                else:
                    failure_answers += 1
            result = UserResults.objects.create(
                user=user, test=test, success_count=success_answers, failure_count=failure_answers)
            result.save()
            del request.session['questions']
            del request.session['test']
            return HttpResponseRedirect(f"/results/{result.id}")


class UserResultsView(TemplateView):
    template_name = "test_app/results.html"

    def get_context_data(self, id=None, **kwargs):
        context = super(UserResultsView, self).get_context_data(**kwargs)
        context['user_result'] = UserResults.objects.get(id=id)
        context['success'] = int(int(context['user_result'].success_count) * 100 /
                                 (int(context['user_result'].success_count) +
                                  int(context['user_result'].failure_count)))
        return context
