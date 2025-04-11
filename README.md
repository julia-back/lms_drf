# Learning Management System

LMS-система,  в которой каждый желающий может размещать свои полезные материалы или курсы.
Реализует функционал подписки на обновления курса. При обновлении курса или урока отправляет
сообщение на почту всем подписанным пользователям. Блокирует пользователей, которые не
авторизовывались юолее 30 дней.


## Содержание
- Установка
- Использование
- Использование через Docker Compose
- Тестирование
- Документация


## Установка
**Клонирование репозитория на локальный репозиторий:**
1. Чтобы клонировать репозиторий с GitHub себе на компьютер, необходимо
получить ссылку на доступ к репозиторию в разделе **Code** на странице
репозитория, выбрать способ взаимодействия с GitHub (**HTTPS**) и **скопировать**
ссылку на репозиторий для клонирования.
2. В главном меню **PyCharm** перейдите в меню **Get from VCS**. 
3. Вставьте ссылку на репозиторий и нажмите на кнопку **Clone**.
4. По окончании клонирования будет открыт проект, вы можете работать с этим проектом.

Или выполните команду ```git clone <ссылка_на_репозиторий>``` 

**Установка зависимостей:** ```poetry install```

**Создайте базу данных и выполните миграции:** ```python manage.py migrate```


## Использование

**Запустите локальный сервер:** ```python manage.py runserver```

**Запустите celery worker:** ```celery -A config worker -l INFO -P```

**Запустите celery beat:** ```celery -A config beat```

**Запустите сервер redis**


**Доступные эндпоинты:**
- GET materials/course/ - список курсов
- GET materials/course/course_id/ - детали конкретного курса
- POST materials/course/ - создание курса
- PUT/PATCH materials/course/course_id/ - редактирование курса
- DELETE materials/course/course_id/ - удаление курса
- materials/lesson_list/ - список уроков
- materials/lesson_detail/lesson_id/ - детали конкретного урока
- materials/lesson_create/ - создание урока
- materials/lesson_update/lesson_id/ - редактирование урока
- materials/lesson_delete/lesson_id/ - удаление урока
- users/token/ - получение токена авторизации
- users/token/refresh/ - обновление токена авторизации
- users/user_register/ - создание пользователя
- users/user_list/ - список пользователей
- users/user_detail/user_id/ - полный профиль конкретного пользователя
- users/user_update/user_id/ - редактирование профиля пользователя
- users/user_delete/user_id/ - удаление пользователя
- users/payment_create/ - создание платежа
- users/payment_list/ - список платежей пользователя
- users/subscription/course_id/ - создание / удаление подписки
- api/schema/swagger-ui/ - документация Swagger
- api/schema/redoc/ - документация Redoc

Модератор может редактировать курсы и уроки других пользователей, но не может
создавать курсы или уроки.

Эндпоинты создания пользователя и получения токена открыты для 
неавторизованных пользователей. Остальные эндпоинты закрыты авторизацией, 
а так же имеют другие ограничения.


## Использование через Docker Compose
1. Выполните команду ```docker-compose up --build -d```
2. Сервер будет доступен по адресу ```localhost:8000```

## Тестирование
Тесты находятся в каждом приложении в директории tests. Вы можете выполнить
проверку, выполнив команду ```python manage.py test```, и проверить покрытие
кода тестами с помощью команды ```coverage run manage.py test```.


## Документация
Документацию можно посмотреть по эндпинтам: 
```api/schema/swagger-ui/``` или ```api/schema/redoc/```.