from django.urls import path
from .views import  index, signup, login, update_profile, BookView, BookUpdateView

urlpatterns = [
    path('', index),
    path('signup', signup),
    path('login',login),
    path('update_profile',update_profile ),
    path('books/', BookView.as_view(), name="create/get-books"),
    path('book-update/<str:id>/', BookUpdateView.as_view(), name="create/get-books"),

]
