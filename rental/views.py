from django.shortcuts import render,redirect
from django.contrib import messages
from datetime import datetime
from .models import *
from .forms import *
# Create your views here.
def rental_cars_view(request,*args,**kwargs):
    id=kwargs.get('pk')
    qs=Car.objects.filter(is_active=True,is_available=True)
   
    if id:
        try:
            car_detail=qs.get(id=id)
            return render(request,'rental_cars.html',{'cars':qs,'car_detail':car_detail})
        except:
            messages.error(request,'Sorry this car is NOT AVALIBLE check these cars that are avalible')
            return render(request,'rental_cars.html',{'cars':qs})
     
    return render(request,'rental_cars.html',{'cars':qs})

def rental_create_view(request,*args,**kwargs):
    id=kwargs.get('pk')
    car_obj=Car.objects.get(id=id)
    if request.method == 'POST':

        rental_start_day = request.POST.get('rental_start_date')
        rental_end_day = request.POST.get('rental_end_date')
        total_amount = request.POST.get('calculated_amound')
        
        try:
                start_date = datetime.strptime(rental_start_day, '%Y-%m-%d')
                end_date = datetime.strptime(rental_end_day, '%Y-%m-%d')
        except ValueError:
                messages.error(request, "Invalid date format.")
                return redirect('rental:rental_car_detail', id=id)

        # Ensure end date is after start date
        if end_date <= start_date:
                messages.error(request, "End date must be after start date.")
                return redirect('rental:rental_car_detail', id=id)

        # Create a new Rental instance
        rental = Rental.objects.create(
                    car=car_obj,
                    user=request.user,
                    rental_start_date=start_date,
                    rental_end_date=end_date,
                    total_amount=total_amount
                )
        if rental:
            car_obj.is_available = False
            car_obj.save()
        messages.success(request, f"Rental created successfully! Total amount: {total_amount}")
        return redirect('rental:rental_cars')
    return render(request,'rental_cars.htm')


def my_rental_disply_view(request):
    qs=Rental.objects.filter(user=request.user,is_active=True).exclude(is_completed=True)
    pqs=Rental.objects.filter(user=request.user,is_active=True).exclude(is_completed=False)
    
    return render(request,'my_rentals.html',{'currently_rented':qs,'priviosly_rented':pqs})

def rent_car_return_view(request,*args,**kwargs):
    id=kwargs.get('pk')
    rent_obj=Rental.objects.get(id=id)
    print(rent_obj)
    action=request.POST.get('action')
    print(action)
    if action == "rent_completed" :
        rent_obj.is_completed = True
        rent_obj.save()
        print("ssssss")
        
    return redirect('rental:my_rentals')
    
    
def rental_feedback(request,*args,**kwargs):
    if request.method == 'POST':
        id = kwargs.get('pk')
        try:
            form=RentalFeedbackForm(request.POST)
            rental_obj=Rental.objects.get(id=id)
            if form.is_valid():
                form.instance.user=request.user
                form.instance.rental=rental_obj
                form.save()
                return redirect('rental:my_rentals')
        except:
            messages.error('sorrt you already given a feedback ')
            return redirect('rental:my_rentals')

    else:
        form=RentalFeedbackForm()
        
    return render(request,'feedback.html',{'form':form})

def add_car_view(request):
    if request.method=='POST':
        form=AddCarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrator_home')
    else:
        form=AddCarForm()
    return render(request,'add_car.html',{'form':form})


def all_rental_cars_view(request,*args,**kwargs):
    id=kwargs.get('pk')

    qs=Car.objects.all(is_active=True) 
    if id:
        try:
            car_detail=qs.get(id=id)
            return render(request,'all_cars.html',{'cars':qs,'car_detail':car_detail})
        except:
            # messages.error(request,'Sorry this car is NOT AVALIBLE check these cars that are avalible')
            return render(request,'all_cars.html',{'cars':qs})
     

    return render(request,'all_cars.html',{'cars':qs})
