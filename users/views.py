from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.views.generic import View
from .forms import *
from assistance.models import *
from rental.models import Car

class RegistrationView(View):
    def get(self,request):
        form= CustomUserCreationForm()
        return render(request,'register.html',{'form':form})
    
    def post(self,request,):
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect(reverse('users:login'))
        return render(request,'register.html',{'form':form})
    
    
class SigninView(View):
    def get(self,request):
        return render(request,'login.html')
    
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user=authenticate(request,username=username,password=password)
        next_url = request.GET.get('next')
        if next_url:
                del request.GET['next']
        
        if user is not None:
            login(request, user)  
            if user.user_type == 'administrator':
                return redirect('users:administrator_home')
            elif user.user_type == 'user':
                return redirect(reverse('users:home'))
            elif user.user_type == 'mechanic':
                return redirect(reverse('assistance:mec_home'))
            else:
                messages.error(request, "User type not recognized.")
                return redirect(reverse('users:login'))
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')        
        

        
class Userhome(View):
    def get(self,request,*args,**kwargs):
        qs=MechanicProfile.objects.filter(is_approved=True,is_active=True,available=True).order_by('-average_rating')[:6]
        cars=Car.objects.all()
        location_query = request.GET.get('location', '').strip()  
        if location_query:
            mec_data = MechanicProfile.objects.filter(
              Q(location__loc_name__icontains=location_query),
              is_approved=True,
              is_active=True,
              available=True
            ).order_by('-average_rating')[:6]
        else:
            mec_data = MechanicProfile.objects.filter(is_approved=True,is_active=True,available=True).order_by('-average_rating')[:6]

        context={
            'mec_data':qs,
            'cars':cars,
            'mec_near_me':mec_data
            
        }
        return render(request,'user_home.html',context)
   

class AddProfileView(View):
    def get(self,request,*args,**kwargs):
        if request.user.user_type == 'user':
            user_profile = get_object_or_404(UserProfile, user=request.user)
            form=UserProfileForm( instance=user_profile)
            return render(request,'user_profile_add.html',{'form':form})
        if request.user.user_type == 'mechanic':
            mec_profile = get_object_or_404(MechanicProfile, user=request.user)
            form=UserProfileForm( instance=mec_profile)
            return render(request,'user_profile_add.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
            if request.user.user_type == 'user':
                user_profile = get_object_or_404(UserProfile, user=request.user)
                form=UserProfileForm(request.POST,request.FILES,instance=user_profile)
                if form.is_valid():
                    user_profile = form.save() 
                    return redirect(reverse('users:home'))
            if request.user.user_type == 'mechanic':
                mec_profile = get_object_or_404(MechanicProfile, user=request.user)
                form=UserProfileForm(request.POST,request.FILES,instance=mec_profile)
                if form.is_valid():
                    mec_profile = form.save() 
                    return redirect(reverse('users:home'))

            return render(request,'user_profile_add.html',{'form':form})

class ProfileDisplayView(View):
    def get(self,request):
        if request.user.user_type == 'mechanic':
            qs=MechanicProfile.objects.get(id=request.user.mechanic_profile.id)
        if request.user.user_type == 'user':
            qs=UserProfile.objects.get(id=request.user.user_profile.id)

        return render(request,'profile.html',{'data':qs})
    
    
class AdminHomeView(View):
    def get(self,request):
        return render(request,'administrator_home.html')
    
class AllMechanicRequestsView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=MechanicProfile.objects.all().order_by('-created_at')
        if id:
            try:
                # Use get_object_or_404 to simplify object retrieval and 404 handling
                mec_detail = get_object_or_404(MechanicProfile, id=id)
                return render(request, 'mechanic_requests.html', {'mec_data': qs, 'mec_detail': mec_detail})
            except MechanicProfile.DoesNotExist:
                # Provide a fallback or message if needed
                return render(request, 'mechanic_requests.html', {'mec_data': qs, 'error': 'Mechanic not found.'})
        
        # If no 'id', return only the full list
        return render(request, 'mechanic_requests.html', {'mec_data': qs})
    

class MechanicApproveView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        mec_obj=MechanicProfile.objects.get(id=id)
        action=request.POST.get('action')
        if action=='is_approved':
            mec_obj.is_approved=True
            mec_obj.save()
        elif action == 'revoke_approval':
            mec_obj.is_approved = False
            mec_obj.save()
        return redirect('users:all_mec_requests')
