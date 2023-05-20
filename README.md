### **Описание проекта:**

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведения делятся на категории, им также может быть присвоен жанр. Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти, из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. Пользователи могут оставлять комментарии к отзывам.


### **Используемые технологии:**

Python, 
Django, 
REST API


### **Авторы проекта:**

Николай Синьков https://github.com/meveladron - Auth/Users,

Мурат Кертиев https://github.com/Murat-Kertiev - Categories/Genres/Titles,

Екатерина Мужжухина https://github.com/katekatekatem - Review/Comments (team leader)


### **Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

> git clone git@github.com:katekatekatem/api_yamdb.git
> 
> cd api_yamdb

Cоздать и активировать виртуальное окружение:

> python -m venv venv
> 
> source venv/scripts/activate

Установить зависимости из файла requirements.txt:

> python -m pip install --upgrade pip
> 
> pip install -r requirements.txt

Выполнить миграции:

> python manage.py migrate

Запустить проект:

> python manage.py runserver

### **Документация к проекту:**

После запуска проекта перейти по ссылке - http://127.0.0.1:8000/redoc/.

### **Примеры запросов к API:**

### ***Отзывы***

GET .../api/v1/titles/{title_id}/reviews/

Получить список всех отзывов к произведению по id. Права доступа: Доступно без токена.

Пример ответа: 

> [
>
>   {
>
>     "count": 0,
>
>     "next": "string",
>
>     "previous": "string",
>
>     "results": [
>
>       {
>
>         "id": 0,
>
>         "text": "string",
>
>         "author": "string",
>
>         "score": 1,
>
>         "pub_date": "2019-08-24T14:15:22Z"
>
>       }
>
>     ]
>
>   }
>
> ]

POST .../api/v1/titles/{title_id}/reviews/

Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение. Права доступа: Аутентифицированные пользователи.

> {
>
>     "text": "string",
>
>     "score": 1
>
> } 

Пример ответа:

> {
>
>   "id": 0,
>
>   "text": "string",
>
>   "author": "string",
>
>   "score": 1,
>
>   "pub_date": "2019-08-24T14:15:22Z"
>
> }

GET или PATCH .../api/v1/titles/{title_id}/reviews/{review_id}/

Получить отзыв GET по id для указанного произведения. Права доступа: Доступно без токена.

Частично обновить PATCH отзыв по id. Права доступа: Автор отзыва, модератор или администратор.

Пример запроса для PATCH:

> {
>
>   "text": "string", 
>
>   "score": 1
>
> }

Пример ответа для GET и PATCH:

> {
>
>   "id": 0,
>
>   "text": "string",
>
>   "author": "string",
>
>   "score": 1,
>
>   "pub_date": "2019-08-24T14:15:22Z"
>
> }

DELETE .../api/v1/titles/{title_id}/reviews/{review_id}/

Удалить отзыв по id Права доступа: Автор отзыва, модератор или администратор.

### ***Комментарии***

GET .../api/v1/titles/{title_id}/reviews/{review_id}/comments/

Получить список всех комментариев к отзыву по id. Права доступа: Доступно без токена.

Пример ответа: 

> [
>
>   {
>
>     "count": 0,
>
>     "next": "string",
>
>     "previous": "string",
>
>     "results": [
>
>       {
>
>         "id": 0,
>
>         "text": "string",
>
>         "author": "string",
>
>         "pub_date": "2019-08-24T14:15:22Z"
>
>       }
>
>     ]
>
>   }
>
> ]

POST .../api/v1/titles/{title_id}/reviews/{review_id}/comments/

Добавить новый комментарий к отзыву. Права доступа: Аутентифицированные пользователи.

> {
>
>     "text": "string",
>
> } 

Пример ответа:

> {
>
>   "id": 0,
>
>   "text": "string",
>
>   "author": "string",
>
>   "pub_date": "2019-08-24T14:15:22Z"
>
> }

GET или PATCH .../api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

Получить комментарий GET для отзыва по id. Права доступа: Доступно без токена.

Частично обновить комментарий PATCH к отзыву по id. Права доступа: Автор комментария, модератор или администратор.

Пример запроса для PATCH:

> {
>
>   "text": "string"
>
> }

Пример ответа для GET и PATCH:

> {
>
>   "id": 0,
>
>   "text": "string",
>
>   "author": "string",
>
>   "pub_date": "2019-08-24T14:15:22Z"
>
> }

DELETE .../api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

Удалить комментарий к отзыву по id. Права доступа: Автор комментария, модератор или администратор.
