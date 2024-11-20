from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import View
from .models import *
from .forms import *


# Create your views here.
class MecHomeView(View):
    def get(self,request):
        reqqs= ServiceRequest.objects.filter(mechanic=request.user,status='pending',is_active=True)[:8]
        feedqs=ServiceFeedback.objects.filter(mechanic=request.user,is_active=True).order_by('-created_at')[:5]
        context={
            'serviesrequest':reqqs,
            'serviesfeedback':feedqs,
            
            }
        return render(request,'mec_home.html',context)
    
    
class ServiceAceptView(View):
        def get(self,request,*args,**kwargs):
            id=kwargs.get('pk')
            if id:        
                qs=ServiceRequest.objects.filter(mechanic=request.user,is_active=True).exclude(id=id)
                req=ServiceRequest.objects.get(id=id)
                context={
                    'serviesrequest':qs,
                    'req':req,
                }
                return render(request,'service_request.html',context)
            else:
                qs=ServiceRequest.objects.filter(mechanic=request.user,is_active=True)
                return render(request,'service_request.html',{'serviesrequest':qs})
        
        
class RequestStatusUpdateView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        request_obj=ServiceRequest.objects.get(id=id)
        action=request.POST.get('action')
        if action=='accept':
            request_obj.status='accepted'
            request_obj.save()
            
        if action=='canceled':
            request_obj.status='canceled'
            request_obj.save()
            
        if action=='completed':
            request_obj.status='completed'
            request_obj.save()
            
        if action=='in_progress':
            request_obj.status='in_progress'
            request_obj.save()

        return redirect('assistance:mec_home')
        
        
class MechanicServiceRequesrView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        if id:
            form=MecRequestForm()
        else:
            form=RequestFeedbackForm()
            qs=ServiceRequest.objects.filter(user=request.user,is_active=True)
            return render(request,'my_requests.html',{'service_requests':qs,'feedback_form':form})
        return render(request,'my_requests.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=MecRequestForm(request.POST)
        id=kwargs.get('pk')
        if form.is_valid():
            mechanic_obj=CustomeUser.objects.get(id=id)
            form.instance.user=request.user
            form.instance.mechanic=mechanic_obj
            form.save()
            return redirect('users:home')
        
        return render(request,'my_requests.html',{'form':form})

class ServiceRequestFeedbackView(View):

    def post(self,request,*args,**kwargs):
        service_request_id=kwargs.get('pk1')
        mec_id=kwargs.get('pk2')
        form=RequestFeedbackForm(request.POST)
        if form.is_valid():
            service_request_obj = ServiceRequest.objects.get(id=service_request_id)
            mechanic_obj = CustomeUser.objects.get(id=mec_id)
            form.instance.service_request = service_request_obj
            form.instance.user=request.user
            form.instance.mechanic = mechanic_obj
            form.save()
            return redirect('assistance:mec_servicce_req_display')
            
            
        
class RequestDisplayView(View):
    def get(self,request):
        qs=ServiceRequest.objects.filter(is_active=True).order_by('-request_time')
        return render(request,'all_requests.html',{'requests':qs})
    
class RequestFeedbackDeleteVew(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        feedback_obj=ServiceFeedback.objects.get(id=id)
        action=request.POST.get('action')
        if action=='delete':
            feedback_obj.is_active=False
            feedback_obj.save()
        return redirect('assistance:request_display')
        