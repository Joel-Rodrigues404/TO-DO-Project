from django.urls import path
from . import views


urlpatterns = [
    path('hellowolrd/', views.hellowolrd),
    path('' , views.tasklist, name='task-list'),
    path('seunome/<str:nome>', views.seunome, name='seu-nome'),
    path('newtask/', views.newtask, name='new-task'),
    path('edit/<int:id>', views.editTask , name='edit-task'),
    path('changestatus/<int:id>', views.changestatus , name='change-status'),
    path('delete/<int:id>', views.deletetask , name='delete-task'),
    path('task/<int:id>', views.taskview, name='task-view'),
]
