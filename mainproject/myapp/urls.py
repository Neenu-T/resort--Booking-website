
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("",views.index,name="index"),
     path("about",views.about,name="about"),
    path("bookingnew",views.bookingnew,name="booking"),
    path("register",views.register,name="register"),
    path("gallery",views.gallery,name="gallery"),
    path("login_page",views.login_page,name="login"),
    path('logout',views.logoutuser, name="logout"),
    path("contact1",views.contact1,name="contact1"),
    path("hotel-detail<uid>",views.hotel_detail,name="hotel_detail"),
    path("payment-success<uid>",views.PaymentSuccessful,name="payment-success"),
    path("payment-failed<uid>",views.PaymentFailed,name="payment-failed"),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    
    path("payment",views.payment,name="payment"),
   
    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()


