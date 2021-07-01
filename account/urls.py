from django.urls import path

from account.views import *

urlpatterns = [
    path('register/', RegView.as_view()),
    path('activation/', ActView.as_view()),
    path('login/', LogView.as_view()),
    path('logout/', OutView.as_view()),
    path('rest_pass/', RestPassView.as_view()),
]