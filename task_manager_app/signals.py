from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Notification
from django.conf import settings


@receiver(post_save, sender=Task)
def send_task_notification(sender, instance, created, **kwargs):
    if instance.assigned_to is not None:
        if created:
            # Создание уведомления при создании новой задачи

            Notification.objects.create(task=instance, assigned_to=instance.assigned_to)
        else:
            # Создание уведомления при изменении статуса задачи
            task_history = instance.task_history.order_by("-created_at").first()
            if task_history and task_history.status != instance.status:
                Notification.objects.create(
                    task=instance, assigned_to=instance.assigned_to
                )
        # Отправка уведомления на почту
        subject = "Новая задача" if created else "Изменение статуса задачи"
        message = f"Задача {instance.name} была создана или её статус был изменён на {instance.status}"
        recipient_list = [instance.assigned_to.email]
        send_mail(
            subject,
            message,
            "djangoKovalchukis@yandex.ru",
            recipient_list,
            fail_silently=False,
        )
