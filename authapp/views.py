from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import AbstractUserModel
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    def form_valid(self, form):
        ret = super().form_valid(form)

        message = ("Login success!<br>Hi")
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))


class RegistrationFormView(TemplateView):
    template_name = "authapp/register.html"

    def post(self, request, *args, **kwargs):
        try:
            if all(
                (
                    request.POST.get("email"),
                    request.POST.get('username'),
                    request.POST.get("password1"),
                    request.POST.get(
                        "password1") == request.POST.get("password2"),
                )
            ):
                new_user = AbstractUserModel.objects.create(
                    email=request.POST.get("email"),
                    username=request.POST.get('username')
                )
                new_user.set_password(request.POST.get("password1"))
                new_user.save()
            return HttpResponseRedirect(reverse_lazy("authapp:login"))
        except Exception as exp:
            messages.add_message(
                request,
                messages.WARNING,
            )
            pass
            return HttpResponseRedirect(reverse_lazy("authapp:register"))


class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, "See you later!")
        return super().dispatch(request, *args, **kwargs)
