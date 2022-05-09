from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
from django.urls import reverse
# Create your models here.

CATEGORY_CHOICES = (
    ('Car-Owner', 'Car Owner'),
    ('Mechanic/Garage', 'Mechanic/Garage'),
    ('Spareparts-Retailer', 'Spare Parts Retailer'),
)
MODEL_CHOICES = (
    ('Toyota', 'Toyota'),
    ('Nissan', 'Nissan'),
    ('Subaru', 'Subaru'),
    ('Mitsubishi', 'Mitsubishi'),
    ('Mercedes', 'Mercedes Benz'),
    ('BMW', 'BMW'),
    ('Audi', 'Audi'),
    ('Volkswagen', 'Volkswagen'),
    ('Honda', 'Honda'),
    ('Land Rover', 'Land Rover'),
    ('Ford', 'Ford'),
)
YEAR_CHOICES = [
    (2021, '2021'),
    (2020, '2020'),
    (2019, '2019'),
    (2018, '2018'),
    (2017, '2017'),
    (2016, '2016'),
    (2015, '2015'),
    (2014, '2014'),
    (2013, '2013'),
    (2012, '2012'),
    (2011, '2011'),
    (2010, '2010'),
    (2009, '2009'),
    (2008, '2008'),
    (2007, '2007'),
    (2006, '2006'),
    (2005, '2005'),
    (2004, '2004'),
    (2003, '2003'),
    (2002, '2002'),
    (2001, '2001'),
    (2000, '2000'),
    (1999, '1999'),
    (1998, '1998'),
    (1997, '1997'),
]
TRANSMISSION_CHOICES = (
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
)


class Profile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_pic = CloudinaryField('image')
    description = models.CharField(max_length=250)
    mobile_number = models.IntegerField(blank=True)
    email = models.CharField(max_length=60)
    category = models.CharField(
        max_length=60, choices=CATEGORY_CHOICES, default="Car-Owner")

    def create_profile(self):
        self.save()

    def update_profile(self):
        self.update()

    def delete_profile(self):
        self.delete()

    def __str__(self):
        return self.user


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='poste')
    issue = HTMLField()
    issue_picture = CloudinaryField('image')
    make = models.CharField(
        max_length=60, choices=MODEL_CHOICES, default="Toyota", null=True)
    model = models.CharField(max_length=50)
    year = models.IntegerField(choices=YEAR_CHOICES)
    posted_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.issue


class Advice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advice = HTMLField(null=True)
    posted_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.advice


class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    picture = CloudinaryField('image')
    picture2 = CloudinaryField('image')
    picture3 = CloudinaryField('image')
    make = models.CharField(
        max_length=60, choices=MODEL_CHOICES, default="Toyota", null=True)
    model = models.CharField(max_length=50)
    year = models.IntegerField(choices=YEAR_CHOICES)
    description = models.CharField(max_length=250)
    engine_size = models.CharField(max_length=100)
    price = models.IntegerField(null=True)
    posted_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.description


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    advice = models.ForeignKey(Advice, on_delete=models.CASCADE, null=True)
    responses = HTMLField()
    shop = models.CharField(max_length=60,null=True)
    location = models.CharField(max_length=60, null=True)
    schedule_time = models.DateTimeField(null=True)
    posted_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.responses


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'    
