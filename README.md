# Task Manager

Проект Task Manager - это приложение на Django для управления проектами, спринтами и задачами. В этом проекте реализованы следующие функции:

Авторизация  
Юнит-тесты  
REST API с использованием сериализаторов DRF  
Логирование  
Графическое представление для пользователей  
Уведомление пользователей по почте при изменении или создании задачи  

## Структура приложения
Проект имеет следующую структуру:  

models.py - описание моделей данных  
views.py - описание представлений  
templates/ - шаблоны страниц  
auth.py - файлы для авторизации  
tests.py - юнит-тестирование  
serializers.py - описание сериализаторов для REST API  
urls.py - описание маршрутов  
signals.py - описание сигналов  
api_views.py - представления для REST API  

## Модели данных
В проекте используется следующие модели данных:  

Project (название, описание, дата создания)  
Sprint (название, описание, дата начала, дата окончания, проект, статус)  
Task (название, описание, дата создания, исполнитель, спринт, статус)  
Status (название, описание)  
TaskHistory (задача, дата изменения, статус)  
Notification (задача, исполнитель, дата создания)  

## Установка и использование
Для установки и запуска проекта, выполните следующие команды:


cd task_manager  
pip install -r requirements.txt  
python manage.py migrate  
python manage.py runserver  
