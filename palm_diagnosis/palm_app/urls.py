from django.urls import path, include
from . import api, views
from .views import chatbot, home, analyze



urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),     # احتياط
    path('analyze/', views.analyze, name='analyze'),
    path("analyze/", api.analyze_image, name="analyze_image"),
    path('api/analyze/', views.analyze_api, name='api_analyze'),
    path("api/chatbot/", api.chatbot_api, name="chatbot_api"),
    path("accounts/", include("palm_app.registration.urls")),
    path("assistant/", views.chatbot, name="assistant"),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('my-palms/', views.my_palms, name='my_palms'),
    path('api/save-diagnosis/', views.save_diagnosis_api, name='save_diagnosis_api'),
    path("palms/<int:palm_id>/", views.palm_detail, name="palm_detail"),
    path("api/add-palm/", views.add_palm_api, name="add_palm_api"),
    path("profile/avatar/", views.upload_avatar, name="upload_avatar"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]
