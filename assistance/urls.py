from django.urls import path
from .views import *

app_name='assistance'
urlpatterns=[
    path('',MecHomeView.as_view(),name='mec_home'),
    path("requests/<int:pk>/",ServiceAceptView.as_view(),name='servicce_req'),
    path("requests/",ServiceAceptView.as_view(),name='servicce_req_all'),
    path('requests/<int:pk>/update',RequestStatusUpdateView.as_view(),name='req_status_update'),
    path('requests/mec/<int:pk>/',MechanicServiceRequesrView.as_view(),name="mec_servicce_req"),
    path('requests/mec/',MechanicServiceRequesrView.as_view(),name="mec_servicce_req_display"),
    path('requests/mec/feedback/<int:pk1>/<int:pk2>',ServiceRequestFeedbackView.as_view(),name='mec_servicce_req_feedback'),
    path('administrator/requests/',RequestDisplayView.as_view(),name="request_display"),
    path('administrator/requests/feedback/delete/<int:pk>',RequestFeedbackDeleteVew.as_view(),name="feedback_remove"),

]