from django.urls import path
from .views import *

app_name='rental'

urlpatterns=[
    path('cars/',rental_cars_view,name='rental_cars'),
    path('cars/<int:pk>/',rental_cars_view,name='rental_car_detail'),
    path('rental/create/<int:pk>/',rental_create_view,name="rental_create"),
    path('myrentals/',my_rental_disply_view,name='my_rentals'),
    path('rental/return/<int:pk>/',rent_car_return_view,name="rent_car_return"),
    path('rental/feedback/<int:pk>/',rental_feedback,name="rental_feedback"),
    path('administrator/add/car/',add_car_view,name='add_car'),
    path('administrator/view/car/all/',all_rental_cars_view,name='view_all_cars'),
    path('administrator/view/car/all/<int:pk>',all_rental_cars_view,name='view_car_detail'),
    path('administrator/update/car/<int:pk>',update_car_view,name='update_car_detail'),



    
]
