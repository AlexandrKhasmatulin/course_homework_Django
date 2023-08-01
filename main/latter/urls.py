from django.urls import path, include

from main.latter import views
from main.latter.apps import LatterConfig
from main.latter.views import SmsLetterDeleteView, SmsLetterUpdateView, SmsLetterCreateView, catalog, \
    smslatters

app_name = LatterConfig.name

urlpatterns = [
    path('', smslatters, name='list'),
    path("catalog/<int:pk>", catalog, name='catalog'),
    path("create/", SmsLetterCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", SmsLetterUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", SmsLetterDeleteView.as_view(), name="delete"),
    path('send_email/', views.send_email, name='send_email'),
    path('index/', views.index, name='index'),

]