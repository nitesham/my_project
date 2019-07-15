from django.db import models
from django.forms import ModelForm
from django import forms
import datetime


# Create your models here.
STATUS = (
    (0, 'Start'),
    (1, 'Stop'),
)

BATCH = (
    ('morning', 'Morning'),
    ('evening', 'Evening'),
)

class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(('First Name'), max_length=50)
    last_name = models.CharField(('Last Name'), max_length=50)
    mobile_number = models.CharField(('Mobile Number'), max_length=10, unique=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=300, blank=True)
    dob = models.DateField(default='dd/mm/yyyy')
    batch = models.CharField(
                                max_length=30,
                                choices=BATCH,
                                default=BATCH[0][0]
                            )
    photo = models.FileField(upload_to='trainer/', blank=True)
    stop = models.IntegerField(('Status'), choices=STATUS, default=STATUS[0][0], blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class AddTrainerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddTrainerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].error_messages = {'required': 'Please enter first name'}
        self.fields['last_name'].error_messages = {'required': 'Please enter last name'}

    class Meta:
        model = Trainer
        # fields = ['first_name', 'last_name', 'mobile_number', 'email', 'address', 'subscription_type', 'subscription_period', 'amount']
        fields = '__all__'
        # exclude = ['registration_upto']
        widgets = {
        # 'registration_date': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
        'address': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        # 'medical_history': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        'dob': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
        'photo': forms.FileInput(attrs={'accept': 'image/*;capture=camera'})
        }

    def clean_mobile_number(self, *args, **kwargs):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number.isdigit():
            raise forms.ValidationError('Mobile number should be a number')
        if Trainer.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError('This mobile number has already been registered.')
        else:
            if len(str(mobile_number)) == 10:
                return mobile_number
            else:
                raise forms.ValidationError('Mobile number should be 10 digits long.')
        return mobile_number

    # def clean_amount(self):
    #     amount = self.cleaned_data.get('amount')
    #     if not amount.isdigit():
    #         raise forms.ValidationError('Amount should be a number')
    #     return amount

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('dob')
        first_name = cleaned_data.get('first_name').capitalize()
        last_name = cleaned_data.get('last_name').capitalize()
        queryset = Trainer.objects.filter(
                        first_name=first_name,
                        last_name=last_name,
                        dob=dob
                    ).count()
        if queryset > 0:
            raise forms.ValidationError('This member already exists!')


class SearchForm(forms.Form):
    search = forms.CharField(label='Search Trainer', max_length=100, required=False)

    def clean_search(self, *args, **kwargs):
        search = self.cleaned_data.get('search')
        if search == '':
            raise forms.ValidationError('Please enter a name in search box')
        return search


class UpdateTrainerGymForm(forms.Form):
    
    mobile_number = forms.CharField(widget=forms.TextInput()) 
    email     = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),)
    batch = forms.ChoiceField(choices=BATCH)
    stop = forms.ChoiceField(label='Status', choices=STATUS)
    address= forms.CharField(
     widget=forms.Textarea(attrs={'placeholder': 'Please enter the  description','cols': 80, 'rows': 3}),)

    def clean_mobile_number(self, *args, **kwargs):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number.isdigit():
            raise forms.ValidationError('Mobile number should be a number')
        if Trainer.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError('This mobile number has already been registered.')
        else:
            if len(str(mobile_number)) == 10:
                return mobile_number
            else:
                raise forms.ValidationError('Mobile number should be 10 digits long.')
        return mobile_number

class UpdateTrainerInfoForm(forms.Form):
    first_name     = forms.CharField(max_length=50)
    last_name      = forms.CharField(max_length=50)
    photo          = forms.FileField(label='Update Photo', required=False)
    dob            = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker        form-control', 'type': 'date'}),)
