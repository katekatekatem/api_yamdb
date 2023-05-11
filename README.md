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
