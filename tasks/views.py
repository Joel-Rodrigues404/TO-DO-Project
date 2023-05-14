from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from tasks.models import Task
from .forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.

@login_required(login_url='/accounts/login')
def tasklist(request):
    # tasks = Task.objects.all().order_by('-created_at')
    # tasks = get_list_or_404(Task.objects.order_by('-created_at'))

    search = request.GET.get('search')
    filter = request.GET.get('filter')
    task_done_recently = Task.objects.filter(done='done', update_at__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count()
    tasks_done = Task.objects.filter(done='done', user=request.user).count()
    tasks_doing = Task.objects.filter(done='doing', user=request.user).count()
    if search:

        tasks = Task.objects.filter(title__icontains=search, user=request.user)
    elif filter:
        tasks = Task.objects.filter(done=filter, user=request.user)
    else:
        tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user)

        paginator = Paginator(tasks_list, 3)
        
        page = request.GET.get('page')

        tasks = paginator.get_page(page)

    return render(request, 'tasks/list.html', {'tasks': tasks, 'task_done_recently':task_done_recently,
                                               'tasks_done':tasks_done, 'tasks_doing':tasks_doing})

@login_required(login_url='/accounts/login')
def taskview(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})


@login_required(login_url='/accounts/login')
def newtask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.user = request.user
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})

@login_required(login_url='/accounts/login')
def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task.save()
            return redirect('/')
        else:
            return render(request, 'tasks/editTask.html', {'form': form, 'task': task})
    else:
        return render(request, 'tasks/editTask.html', {'form': form, 'task': task})
    
@login_required(login_url='/accounts/login')
def deletetask(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    
    messages.info(request, 'Mensagem deletada com sucesso.',)

    return redirect('/')
@login_required(login_url='/accounts/login')
def changestatus(request, id):
    task = get_object_or_404(Task, pk=id)

    if task.done == 'doing':
        task.done = 'done'
    else:
        task.done = 'doing'

    task.save()
    return redirect('/')

    
def hellowolrd(request):
    return HttpResponse('hellowolrd')

def seunome(request, nome):
    return render(request, 'tasks/seunome.html', {'nome': nome})