from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns=[
   path('',views.index, name='index'),
   path('logout/',auth_views.LoginView.as_view(template_name = 'registration/login.html')),
   path('update-profile',views.update_profile, name='update_profile'),   
   path('profile/<pk>',views.profile, name = 'profile'),
   path('about/',views.about, name = 'about'),
   path('car-tips/',views.tips, name = 'tips'),
   path('car-issue/',views.issue, name = 'issue'),
   path('car-advice/',views.advice, name = 'advice'),  
   path('sell-your-car/',views.sale, name = 'sale'),  
   path('carnnect-bazaar/',views.bazaar, name = 'bazaar'),  
   path('carnnect-advice&experiences/',views.experience, name = 'experience'),  
   path('response/<post_id>', views.response,name='response'),
   path('events/<int:year>/<str:month>', views.events,name='events'),
   path('calendar/<pk>',views.CalendarView.as_view(), name='calendar'),
   path('event/new',views.event,name='event_new'),
   path('event/edit/<event_id>', views.event, name='event_edit'),
   path('map/',views.map,name='map'),
   path('mechanical/issue/', views.mechanical_issue, name='mechanical_issue'),
   path('contact/', views.contact, name='contact'),
]