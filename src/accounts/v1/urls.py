from django.conf.urls import url

import accounts.v1.views

urlpatterns = [
    url(r'^login-facebook/$', accounts.v1.views.UserLoginRegisterView.as_view(), name='login_facebook'),
    url(r'^onesignal/$', accounts.v1.views.OneSignalView.as_view(), name='onesignal'),
    url(r'^register/$', accounts.v1.views.UserRegisterView.as_view(), name='register'),
    url(r'^login/$', accounts.v1.views.UserLoginView.as_view(), name='login'),
    url(r'^logout/$', accounts.v1.views.UserLogoutView.as_view(), name='logout'),
]
