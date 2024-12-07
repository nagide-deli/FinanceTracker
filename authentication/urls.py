from django.urls import path


from . import views
from .views import SignupView, LoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', LoginView.as_view(), name='signin'),

]