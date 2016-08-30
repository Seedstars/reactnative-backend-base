from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/v1/accounts/', include('accounts.v1.urls', namespace='accounts_v1')),
    url(r'^api/v1/device/', include('device.v1.urls', namespace='device_v1'))
]
