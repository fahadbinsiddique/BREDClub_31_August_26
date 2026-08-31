from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('board-members/', views.board_members, name='board_members'),
    path('executive-committee/', views.executive_committee, name='executive_committee'),
    path('activities/', views.activities, name='activities'),
    path('training/', views.training, name='training'),
    path('events/', views.events, name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('notice/', views.notice, name='notice'),
    path('notice/<slug:slug>/', views.notice_detail, name='notice_detail'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('contact/', views.contact, name='contact'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots'),
    path('e-x=t/', views.ext, name='ext'),
]
