from django import forms
from .models import *
from django.forms import ModelForm, DateInput
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile        
        fields=['first_name','last_name','profile_pic','description','mobile_number','email','category']
        
class PostForm(forms.ModelForm):
    class Meta:
        model=Post        
        fields=['issue','issue_picture','make','model','year']
        
class AdviceForm(forms.ModelForm):
    class Meta:
        model=Advice        
        fields=['advice']  
        
class SaleForm(forms.ModelForm):
    class Meta:
        model=Sale        
        fields=['picture','picture2','picture3','make','model','year','description','price','engine_size'] 
        
class ResponseForm(forms.ModelForm):
    class Meta:
        model=Response   
        widgets = {
          'schedule_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
          
        }     
        fields=['responses','shop','location','schedule_time']                         

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
          'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
          'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ['title','description','start_time','end_time']

    def __init__(self, *args, **kwargs):
      super(EventForm, self).__init__(*args, **kwargs)
      # input_formats to parse HTML5 datetime-local input to datetime field
      self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
      self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
