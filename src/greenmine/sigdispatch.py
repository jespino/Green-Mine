# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

from greenmine.models import Profile, UserStory, Task, ProjectUserRole
from greenmine.core.utils import normalize_tagname


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Create void user profile if instance is a new user.
    """
    if created and not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if instance.user_story:
        instance.user_story.modified_date = timezone.now()
        instance.user_story.save()



@receiver(post_save, sender=UserStory)
def user_story_post_save(sender, instance, created, **kwargs):
    """
    Auto update meta_category_list on project instance for
    performance improvements.
    """

    if not instance.category or not instance.category.strip():
        return

    category_str = normalize_tagname(instance.category)
    if category_str not in instance.project.meta_category_list:
        instance.project.meta_category_list.append(category_str)

    instance.project.save()


from greenmine.core import signals
from greenmine.core.utils.auth import set_token

from greenqueue import send_task
from django.conf import settings
from django.utils.translation import ugettext
from django.template.loader import render_to_string

@receiver(signals.mail_new_user)
def mail_new_user(sender, user, **kwargs):
    template = render_to_string("email/new.user.html", {
        "user": user,
        "token": set_token(user),
        'current_host': settings.HOST,
    })

    subject = ugettext("Greenmine: wellcome!")
    send_task("send-mail", args = [subject, template, [user.email]])

@receiver(signals.mail_recovery_password)
def mail_recovery_password(sender, user, **kwargs):
    template = render_to_string("email/forgot.password.html", {
        "user": user,
        "token": set_token(user),
        "current_host": settings.HOST,
    })
    subject = ugettext("Greenmine: password recovery.")
    send_task("send-mail", args = [subject, template, [user.email]])


@receiver(signals.mail_milestone_created)
def mail_milestone_created(sender, milestone, user, **kwargs):
    participants_ids = ProjectUserRole.objects\
        .filter(user=user, mail_milestone_created=True, project=milestone.project)\
        .values_list('user__pk', flat=True)

    participants = User.objects.filter(pk__in=participants_ids)

    emails_list = []
    subject = ugettext("Greenmine: sprint created")
    for person in participants:
        template = render_to_string("email/milestone.created.html", {
            "person": person,
            "current_host": settings.HOST,
            "milestone": milestone,
            "user": user,
        })

        emails_list.append([subject, template, [person.email]])

    send_task("send-bulk-mail", args=[emails_list])

@receiver(signals.mail_userstory_created)
def mail_userstory_created(sender, us, user, **kwargs):
    participants_ids = ProjectUserRole.objects\
        .filter(user=user, mail_userstory_created=True, project=us.project)\
        .values_list('user__pk', flat=True)

    participants = User.objects.filter(pk__in=participants_ids)

    emails_list = []
    subject = ugettext("Greenmine: user story created")

    for person in participants:
        template = render_to_string("email/userstory.created.html", {
            "person": person,
            "current_host": settings.HOST,
            "us": us,
            "user": user,
        })

        emails_list.append([subject, template, [person.email]])

    send_task("send-bulk-mail", args=[emails_list])


@receiver(signals.mail_task_created)
def mail_task_created(sender, task, user, **kwargs):
    participants_ids = ProjectUserRole.objects\
        .filter(user=user, mail_task_created=True, project=task.project)\
        .values_list('user__pk', flat=True)

    participants = User.objects.filter(pk__in=participants_ids)

    emails_list = []
    subject = ugettext("Greenmine: task created")

    for person in participants:
        template = render_to_string("email/task.created.html", {
            "person": person,
            "current_host": settings.HOST,
            "task": task,
            "user": user,
        })

        emails_list.append([subject, template, [person.email]])

    send_task("send-bulk-mail", args=[emails_list])


@receiver(signals.mail_task_assigned)
def mail_task_assigned(sender, task, user, **kwargs):
    template = render_to_string("email/task.assigned.html", {
        "person": task.assigned_to,
        "task": task,
        "user": user,
        "current_host": settings.HOST,
    })

    subject = ugettext("Greenmine: task assigned")
    send_task("send-mail", args = [subject, template, [task.assigned_to.email]])
