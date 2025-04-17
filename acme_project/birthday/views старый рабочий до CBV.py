# from django.shortcuts import render


# def birthday(request):
#    context = {}
#    return render(request, 'birthday/birthday.html', context=context)


# birthday/views.py
from django.shortcuts import get_object_or_404, redirect, render

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm

# Импортируем модель дней рождения.
from .models import Birthday

# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown

# Импортируем класс пагинатора.(Для сортировки и постраничного вывода)
from django.core.paginator import Paginator


# def birthday(request):
#    print(request.GET)  # Напечатаем.
# Если есть параметры GET-запроса...
#    if request.GET:
# ...передаём параметры запроса в конструктор класса формы.
# Создаём экземпляр класса формы.
#        form = BirthdayForm(request.GET)  # request.GET
# Если данные валидны...
#        if form.is_valid():
# ...то считаем, сколько дней осталось до дня рождения.
# Пока функции для подсчёта дней нет — поставим pass:
#            pass
# Если нет параметров GET-запроса.
#    else:
# То просто создаём пустую форму.
#        form = BirthdayForm()
# Передаём форму в словарь контекста:
# Добавляем его в словарь контекста под ключом form:
#        context = {'form': form}
# Указываем нужный шаблон и передаём в него словарь контекста.
#    return render(request, 'birthday/birthday.html',  context)
# Проще
def birthday(request, pk=None):
    # Во view-функции birthday(), в строке, где создаётся объект формы,
    #  нужно изменить метод GET на POST: параметры POST-запроса
    # хранятся в объекте request.POST.
    # form = BirthdayForm(request.POST or None)

    # Находим запрошенный объект для редактирования по первичному ключу
    # или возвращаем 404 ошибку, если такого объекта нет.

    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Birthday, pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # Связываем форму с найденным объектом: передаём его в аргумент instance.
    # Передаём в форму либо данные из запроса, либо None.
    # В случае редактирования прикрепляем объект модели.
    # Для передачи фото меняем POST на FILES
    # form = BirthdayForm(request.POST or None, instance=instance)
    form = BirthdayForm(request.POST or None,
                        files=request.FILES or None, instance=instance)
    # Создаём словарь контекста сразу после инициализации формы.
    context = {'form': form}
    # Если форма валидна...
    if form.is_valid():
        # записываем данные в базу
        form.save()
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


# В нашем проекте GET-запрос к странице с формой и POST-запрос,
#  отправленный из формы, обрабатываются одной и той же
# view-функцией — birthday(). Но такой подход — не догма.
# Например, HTML-форма может быть размещена на странице birthday/,
#  а POST-запрос из формы можно отправлять к адресу save_it/
#  — для этого нужно указать атрибут action="save_it/"
#  в теге <form>. И теперь генерировать HTML-форму будет
#  одна view-функция, а получать и обрабатывать данные из
#  формы — другая, связанная с адресом save_it/. Но в
# приложении birthday проще обойтись одной view-функцией.

# Старая рабочая функция
# def birthday_list(request):
    # Получаем все объекты модели Birthday из БД.
#    birthdays = Birthday.objects.all()
    # Передаём их в контекст шаблона.
#    context = {'birthdays': birthdays}
#    return render(request, 'birthday/birthday_list.html', context)

def birthday_list(request):
    # Получаем список всех объектов с сортировкой по id.
    birthdays = Birthday.objects.order_by('id')
    # Создаём объект пагинатора с количеством 10 записей на страницу.
    paginator = Paginator(birthdays, 10)

    # Получаем из запроса значение параметра page.
    page_number = request.GET.get('page')
    # Получаем запрошенную страницу пагинатора.
    # Если параметра page нет в запросе или его значение не приводится к числу,
    # вернётся первая страница.
    page_obj = paginator.get_page(page_number)
    # Вместо полного списка объектов передаём в контекст
    # объект страницы пагинатора
    context = {'page_obj': page_obj}
    return render(request, 'birthday/birthday_list.html', context)


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)
