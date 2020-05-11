from django.urls import re_path, path
from app_users.api import views

app_name = "app_users_api"

urlpatterns = [
    # re_path('^edit/(?P<oem_id>\d+)/$', views.OemView.as_view(), name='update'),
    # re_path('', views.get_data, name='get-data'),
    # re_path('^new/$', views.OemView.as_view(), name='new'),
    re_path('^register/$', views.RegisterAppUserAPIView.as_view(), name='app_user_register'),
    re_path('^login/$', views.LoginAppUserAPIView.as_view(), name='app_user_login'),
    re_path('^changestatus/$', views.ChangeStatusAPIView.as_view(), name='app_user_login'),
    re_path('^showexperts/$', views.UsersStatusAPIView.as_view(), name='app_user_login'),
    # re_path('', views.OemListView.as_view(), name='list'),
]