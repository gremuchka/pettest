from django.urls import path, include
from .views import *
from knox import views as knox_views

app_name = 'pets'
urlpatterns = [
    path('pets', PetCreateView.as_view()),
    path('all/', PetListView.as_view()),
    path('details/<int:pk>', PetDetailViews.as_view()),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path("profile/<int:pk>", UserProfileDetailView.as_view(), name="profile"),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

]
