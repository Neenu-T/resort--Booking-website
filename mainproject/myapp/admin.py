from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Amenities)
admin.site.register(booking)
admin.site.register(HotelImages)
admin.site.register(Contact)
class BookingAdmin(admin.ModelAdmin):
    list_display=('full_name','email','phone','hotel','user','start_date','end_date','booking_type')
admin.site.register(HotelBooking,BookingAdmin)