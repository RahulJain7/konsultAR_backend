from django.urls import re_path, path
from admin_user.api import views

app_name = "admin_user_api"

urlpatterns = [
    # re_path('^edit/(?P<oem_id>\d+)/$', views.OemView.as_view(), name='update'),
    # re_path('', views.get_data, name='get-data'),
    # re_path('^new/$', views.OemView.as_view(), name='new'),
    re_path('^register/$', views.RegisterAdminUserAPIView.as_view(), name='admin_user_register'),

    # re_path('', views.OemListView.as_view(), name='list'),
]