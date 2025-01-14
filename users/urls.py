from django.urls import path
from . import views

app_name='users'

urlpatterns=[
    path('home/', views.Userhome.as_view(), name='home'),
    path('', views.SigninView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('update/profile/',views.AddProfileView.as_view(),name='update_profile'),
    path('profile/',views.ProfileDisplayView.as_view(),name='profile_display'),
    path('administrator/',views.AdminHomeView.as_view(),name="administrator_home"),
    path('administrator/mechanic/request/',views.AllMechanicRequestsView.as_view(),name="all_mec_requests"),
    path('administrator/mechanic/request/<int:pk>/',views.AllMechanicRequestsView.as_view(),name="mec_requests_detail"),
    path('administrator/mechanic/approve/<int:pk>/',views.MechanicApproveView.as_view(),name="mec_requests_approve"),
    path('administrator/add/admin/',views.AdminRegistrationView.as_view(),name="add_admin"),
    
]
