from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.DashboardLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', views.password_change, name='password_change'),
    path('', views.overview, name='overview'),
    path('content/', views.content, name='content'),
    path('content/<slug:module>/', views.module_list, name='module_list'),
    path('content/<slug:module>/create/', views.module_create, name='module_create'),
    path('content/<slug:module>/<int:pk>/', views.module_detail, name='module_detail'),
    path('content/<slug:module>/<int:pk>/edit/', views.module_update, name='module_update'),
    path('content/<slug:module>/<int:pk>/delete/', views.module_delete, name='module_delete'),
    path('messages/', views.messages_inbox, name='messages'),
    path('settings/', views.settings, name='settings'),
]
