from django.conf.urls import url

from . import views as base_views

urlpatterns = [
    url(r'^diagnostic/$', base_views.DiagnosticServiceView.as_view(), name='store-data'),
]
