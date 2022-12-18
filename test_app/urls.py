from django.urls import path
from test_app import views
from test_app.apps import TestAppConfig

app_name = TestAppConfig.name

urlpatterns = [
    path("tests/", views.TestsView.as_view(), name="tests"),
    path("questions/", views.QuestView.as_view(), name="quest"),

]
