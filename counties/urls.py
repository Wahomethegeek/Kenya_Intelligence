from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('counties/', views.county_list, name='county-list'),
    path('counties/compare/', views.county_compare, name='county-compare'),
    path('counties/<slug:slug>/', views.county_detail, name='county-detail'),
    path('counties/<slug:slug>/ai-summary/', views.county_ai_summary, name='county-ai-summary'),
]
