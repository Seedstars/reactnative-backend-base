from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/v1/accounts/', include('accounts.v1.urls', namespace='accounts_v1')),
    url(r'^api/v1/base/', include('base.v1.urls', namespace='base_v1'))
]
