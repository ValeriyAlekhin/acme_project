# birthday/models.py
from django.db import models

# Импортируется функция-валидатор.
from .validators import real_age
# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', max_length=20, help_text='Необязательное поле', blank=True
    )
    # Валидатор указывается в описании поля.
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    # Добавьте опциональное поле к модели Birthday: возможно, пользователь
    # постесняется публиковать свой портрет — не будем его заставлять.
    # Директория для загрузки файлов из конкретного поля задаётся
    # в классе ImageField в аргументе upload_to. Директория с
    # таким названием будет создана в папке, указанной в
    # астройках MEDIA_ROOT (в settings).
    # Директорию для файлов из поля Birthday.image назовём
    #  birthdays_images:
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})

    class Meta:
        # В этом классе указывается
        # перечень полей, совокупность которых должна быть уникальна;
        # имя ограничения.
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )
