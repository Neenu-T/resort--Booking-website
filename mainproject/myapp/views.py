from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import (Amenities, booking,HotelBooking,Contact)
from django.db.models import Q
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid

from django.urls import reverse




def check_booking(start_date  , end_date ,uid , room_count):
    qs=HotelBooking.objects.filter(
         start_date__lte=start_date,
         end_date__gte=end_date,
         hotel__uid = uid
        )
    if len(qs)>=room_count:
        return False
    return True

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def bookingnew(request):
    amenities_objs = Amenities.objects.all()
    hotels_objs = booking.objects.all()
    
    

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    print(amenities)
   
    if sort_by:
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')

    if search:
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains = search) |
            Q(description__icontains=search))


    if len(amenities):
        hotels_objs = hotels_objs.filter(amenities__aminity_name__in = amenities)



    context = {'amenities_objs' : amenities_objs , 'hotels_objs' : hotels_objs,'sort_by':sort_by,
               'search':search,'amenities':amenities
               }
   
    return render(request,"bookingnew.html",context)

def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user_obj=User.objects.filter(username=username)
        
        if user_obj.exists():
            messages.warning(request, "username already exists.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user=User.objects.create(username=username)
        user.set_password(password)
        user.save()
        return redirect('login')
        
        
            
    return render(request,"register.html")

def gallery(request):
    return render(request,"gallery.html")

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username = username , password = password)
        if not user_obj:
            messages.warning(request, 'Invalid password ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request,user_obj)
        return redirect('booking')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request ,'login_page.html')
def logoutuser(request):
    logout(request)
    return redirect('login')


def contact1(request):
    
    if request.method=="POST":
        contact=Contact()
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        contact.name=name
        contact.email=email
        contact.subject=subject
        contact.save()
        
        messages.success(request, 'Thanks for contacting us')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    return render(request,"contact.html")

def hotel_detail(request,uid):
    hotel_obj=booking.objects.get(uid=uid)
    # host=request.get_host()
    # paypal_checkout={
    #     'business':settings.PAYPAL_RECEIVER_EMAIL,
    #     'amount':hotel_obj.hotel_price,
    #     'resort_name':hotel_obj.hotel_name,
    #     'invoice':uuid.uuid4(),
    #     'currency_code':'USD',
    #     'notify_url':f"https://{host}{reverse('paypal-ipn')}",
    #     'return_url':f"http://{host}{reverse('payment-success',kwargs={'hotel_obj.uid':hotels_obj.uid})}",
    #     'cancel_url':f"http://{host}{reverse('payment-failed',kwargs={'hotel_obj.uid':hotels_obj.uid})}",
    # }
    # paypal_payment=PayPalPaymentsForm(initial=paypal_checkout)
    # context={
    #     'paypal':paypal_payment
    # }
    
    if request.method=="POST":
        checkin=request.POST.get('checkin')
        checkout=request.POST.get('checkout')
        full_name=request.POST.get('full_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        # payment_status=request.get('payment_status')
        hotel=booking.objects.get(uid=uid)
        
     
        
        if not check_booking(checkin,checkout,uid,hotel.room_count):
            messages.warning(request, 'Hotel is already booked in thses dates')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        hotel_booking=HotelBooking.objects.create(hotel=hotel,full_name=full_name,email=email,phone=phone, user=request.user,start_date=checkin
                                    ,end_date=checkout,booking_type='Post Paid')
        booking_id = hotel_booking.uid
        messages.success(request, 'Your booking has been saved')
        
        latest_booking = HotelBooking.objects.filter(hotel=hotel).order_by('-created_at').first()
        return render(request, "payment.html", {'latest_booking': latest_booking,'booking_id': booking_id})
                                  
        
        
    return render(request,"hotel_detail.html",{'hotels_obj':hotel_obj})

def booked_data(request):
   
    booked_data = HotelBooking.objects.all()
    return render(request, 'booked_data.html', {'booked_data': booked_data})

def cancel_booking(request, booking_id):
   booking = HotelBooking.objects.get(id=booking_id)

   if request.method == 'POST':
        
       booking.delete()  

        # Redirect to a confirmation or booking list page
       return HttpResponseRedirect('hotel-detail')

   return render(request, 'cancel_booking_confirmation.html', {'booking': booking})

def payment(request):
   
   return render(request,"payment.html")  

def PaymentSuccessful(request,uid):
    hotel_obj=booking.objects.get(uid=uid)
    return render(request,"payment-success.html",{'hotels_obj':hotel_obj})

def PaymentFailed(request,uid):
    hotel_obj=booking.objects.get(uid=uid)
    return render(request,"payment-failed.html",{'hotels_obj':hotel_obj})
    