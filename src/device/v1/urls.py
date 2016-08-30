from django.conf.urls import url

from . import views as base_views

urlpatterns = [
    url(r'^order_device/$', base_views.OrderDeviceView.as_view(), name='order_device'),
    url(r'^validate_order_device_data/$', base_views.ValidateOrderDeviceView.as_view(),
        name='validate_order_device_data')
]
