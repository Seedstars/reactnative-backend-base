from django.conf.urls import url

from accounts.v1 import views as account_views

urlpatterns = [
    url(r'^facebooklogin/$', account_views.UserLoginRegisterView.as_view(), name='login'),
    url(r'^onesignal/$', account_views.OneSignalView.as_view(), name='onesignal'),
]
