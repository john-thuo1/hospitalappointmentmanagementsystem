from django.urls import path
from api.views import (ussd_callback)

urlpatterns = [
    path('ussd_callback/', ussd_callback, name='ussd_callback'),
]
