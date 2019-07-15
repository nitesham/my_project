from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('trainer/', login_required(views.TrainerForm), name='trainer'),
    path('add_trainer/', login_required(views.Add_trainer_data), name='add_trainer'),
    path('update/<int:id>', login_required(views.update_trainer), name='update_trainer'),
    path('alltrainer/',login_required(views.AllTrainer),name="alltrainer"),
    path('search/', login_required(views.SearchTrainer), name='search_trainer'),
    
]