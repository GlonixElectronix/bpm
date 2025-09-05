from django.db.models.signals import post_migrate
from django.dispatch import receiver
from background_task.models import Task
from core.background_tasks import preaggregate_daily_summaries

@receiver(post_migrate)
def schedule_preaggregate_daily_summaries(sender, **kwargs):
    if not Task.objects.filter(task_name="core.background_tasks.preaggregate_daily_summaries").exists():
        preaggregate_daily_summaries(repeat=86400)  # every 24 hours
