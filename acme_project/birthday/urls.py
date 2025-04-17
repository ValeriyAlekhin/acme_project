from django.urls import path

from . import views

app_name = 'birthday'

# Теперь перенастроим маршрутизацию: в файле birthday/urls.py
#  в маршруте с name='list' замените вызов view-функции
#  birthday_list на обращение к методу as_view() класса
#  BirthdayListView. Этот метод есть у всех встроенных
#  CBV и наследуется в пользовательских классах.
urlpatterns = [
    # path('', views.birthday, name='create'),
    path('', views.BirthdayCreateView.as_view(), name='create'),
    # path('list/', views.birthday_list, name='list'),
    path('list/', views.BirthdayListView.as_view(), name='list'),
    path('<int:pk>/', views.BirthdayDetailView.as_view(), name='detail'),
    # для редактирования добавляем путь
    # path('<int:pk>/edit/', views.birthday, name='edit'),
    path('<int:pk>/edit/', views.BirthdayUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/',
         views.BirthdayDeleteView.as_view(), name='delete'
         ),
]
