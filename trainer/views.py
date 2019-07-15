from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from . models import AddTrainerForm, Trainer,SearchForm,UpdateTrainerGymForm,UpdateTrainerInfoForm
from notifications.config import get_notification_count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import post_save
from notifications.config import my_handler
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

def model_save(model):
    post_save.disconnect(my_handler, sender=Trainer)
    model.save()
    post_save.connect(my_handler, sender=Trainer)




# Create your views here.
def TrainerForm(request):
    form = AddTrainerForm()
    context = {
        'form': form,
        'subs_end_today_count': get_notification_count(),
    }
    return render(request, 'add_trainer.html', context)

def Add_trainer_data(request):
    view_all = Trainer.objects.all()
    success = 0
    trainer = None
    if request.method == 'POST':
        form = AddTrainerForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.first_name = request.POST.get('first_name').capitalize()
            temp.last_name = request.POST.get('last_name').capitalize()
            model_save(temp)
            success = 'Successfully Added Member'
            

            # Add payments if payment is 'paid'
            form = AddTrainerForm()
            trainer = Trainer.objects.last()
            print(trainer)

        context = {
            'add_success': success,
            'form': form,
            'trainer': trainer,
            'subs_end_today_count': get_notification_count(),
        }
        return render(request, 'add_trainer.html', context)
    else:
        form = AddTrainerForm()
        context = {
            'form': form,
            'subs_end_today_count': get_notification_count(),
        }
    return render(request, 'add_trainer.html', context)

def AllTrainer(request):
    print("hi")
    view_all = Trainer.objects.filter(stop=0).order_by('first_name')
    paginator = Paginator(view_all, 20)
    try:
        page = request.GET.get('page', 1)
        view_all = paginator.page(page)
    except PageNotAnInteger:
        view_all = paginator.page(1)
    except EmptyPage:
        view_all = paginator.page(paginator.num_pages)
    search_form = SearchForm()
    # get all members according to their batches
    evening = Trainer.objects.filter(batch='evening', stop=0).order_by('first_name')
    morning = Trainer.objects.filter(batch='morning', stop=0).order_by('first_name')
    stopped = Trainer.objects.filter(stop=1).order_by('first_name')
    context = {
        'all': view_all,
        'morning': morning,
        'evening': evening,
        'stopped': stopped,
        'search_form': search_form,
        'subs_end_today_count': get_notification_count(),
    }
    return render(request, 'view_trainer.html', context)

def SearchTrainer(request):
    if request.method == 'POST':
        if 'clear' in request.POST:
            return redirect('alltrainer')
        search_form = SearchForm(request.POST)
        result = 0
        if search_form.is_valid():
            first_name = request.POST.get('search')
            result = Trainer.objects.filter(first_name__icontains=first_name)
            print(result)

        view_all = Trainer.objects.all()
        # get all members according to their batches
        evening = Trainer.objects.filter(batch='evening')
        morning = Trainer.objects.filter(batch='morning')

        context = {
            'all': view_all,
            'morning': morning,
            'evening': evening,
            'search_form': search_form,
            'result': result,
            'subs_end_today_count': get_notification_count(),
        }
        return render(request, 'view_trainer.html', context)
    else:
        search_form = SearchForm()
    return render(request, 'view_trainer.html', {'search_form': search_form})



def update_trainer(request, id):
    if request.method == 'POST' and request.POST.get('export'):
        return export_all(Trainer.objects.filter(pk=id))
    if request.method == 'POST' and request.POST.get('no'):
        return redirect('/')
    if request.method == 'POST' and request.POST.get('gym_trainer'):
        print("hi")
    elif request.method == 'POST' and request.POST.get('info'):
        object = Trainer.objects.get(pk=id)
        object.first_name = request.POST.get('first_name')
        object.last_name = request.POST.get('last_name')
        object.dob = request.POST.get('dob')

        # for updating photo
        if 'photo' in request.FILES:
            myfile = request.FILES['photo']
            fs = FileSystemStorage(base_url="")
            photo = fs.save(myfile.name, myfile)
            object.photo = fs.url(photo)
        model_save(object)

        trainer = Trainer.objects.get(pk=id)
        print(trainer)
        gym_trainer_form = UpdateTrainerGymForm(initial={
                                'mobile_number': trainer.mobile_number,
                                'email': trainer.email,
                                'address': trainer.address,
                                'batch': trainer.batch,
                                'stop': trainer.stop,
                                })

        trainer_info_form = UpdateTrainerInfoForm(initial={
                                'first_name': trainer.first_name,
                                'last_name': trainer.last_name,
                                'dob': trainer.dob,
                                })
        context={
                            'gym_form': gym_trainer_form,
                            'info_form': trainer_info_form,
                            'user': trainer,
                            'subs_end_today_count': get_notification_count(),
                        }
        return render(request, 'trainer_update.html', context)

    else:
        trainer = Trainer.objects.get(pk=id)
        print(trainer)
        gym_trainer_form = UpdateTrainerGymForm(initial={
                                'mobile_number': trainer.mobile_number,
                                'email': trainer.email,
                                'address': trainer.address,
                                'batch': trainer.batch,
                                'stop': trainer.stop,
                                })

        trainer_info_form = UpdateTrainerInfoForm(initial={
                                'first_name': trainer.first_name,
                                'last_name': trainer.last_name,
                                'dob': trainer.dob,
                                })
        context={
                            'gym_form': gym_trainer_form,
                            'info_form': trainer_info_form,
                            'user': trainer,
                            'subs_end_today_count': get_notification_count(),
                        }
        return render(request, 'trainer_update.html', context)
       
        # return HttpResponse("yes")