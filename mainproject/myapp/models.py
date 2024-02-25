from django.db import models
from django.contrib.auth.models import User
import uuid

class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4  , editable=False, primary_key=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    
    class Meta:
        abstract=True
    
    
class Amenities(BaseModel):
    aminity_name=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.aminity_name 
    
    
class booking(BaseModel):
    hotel_name=models.CharField(max_length=100)
    hotel_price=models.IntegerField()
    description=models.TextField()
    amenities=models.ManyToManyField(Amenities)
    room_count=models.IntegerField(default=10)
    
    
    
    def __str__(self) -> str:
        return self.hotel_name
    
class HotelImages(BaseModel):
    hotel=models.ForeignKey(booking,related_name="images",on_delete=models.CASCADE)
    images=models.ImageField(upload_to="hotel")
    
   
    
    
class HotelBooking(BaseModel):
    hotel=models.ForeignKey(booking,related_name="hotel_bookings",on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name="user_bookings",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=100,)
    status = models.CharField(max_length=20, choices=[('booked', 'Booked'), ('cancelled', 'Cancelled')], default='booked')
    
    full_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)

    
    start_date=models.DateField()
    end_date=models.DateField()
    booking_type=models.CharField(max_length=100,choices=(('Pre Paid' , 'Pre Paid'),('Post Paid' , 'Post Paid')))
    
class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    subject=models.TextField()
     
    def __str__(self):
        return self.name  
    
    
