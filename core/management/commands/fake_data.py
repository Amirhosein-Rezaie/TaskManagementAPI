from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.contrib.auth.hashers import make_password

# models
from core import models as CoreModels
from action import models as ActionModels

# varieables
faker_fa = Faker('fa_IR')
user_roles = list(CoreModels.Users.Roles)
project_status = list(CoreModels.Projects.Status)
task_levels_score = list(CoreModels.Tasks.Levels)
task_status = list(CoreModels.Tasks.Status)
tag_titles = list(ActionModels.Tags.Titles)
member_status = list(ActionModels.ProjectMembers.Status)


# the command action
class Command(BaseCommand):
    print("Inserting fake data ... \n")

    def handle(self, *args, **options):
        # insert users
        print("inserting into users ... ", end='')
        for _ in range(30):
            CoreModels.Users.objects.create(
                first_name=faker_fa.first_name(),
                last_name=faker_fa.last_name(),
                role=random.choice(user_roles),
                phone=faker_fa.phone_number(),
                username=faker_fa.user_name(),
                password=make_password(faker_fa.password())
            )
        print('OK')

        # insert projects
        print("inserting into projects ... ", end='')
        projects = [
            "TaskForge", "DataNest", "PixelStream", "CloudLoom",
            "CodeHarbor", "FlowTrack", "EchoDesk", "BrightPath",
            "NovaBoard", "LogicHive",
        ]
        for project in projects:
            CoreModels.Projects.objects.create(
                title=project,
                description=faker_fa.texts(max_nb_chars=200),
                user=random.choice(
                    list(CoreModels.Users.objects.filter(role=user_roles[0]))
                ),
                status=random.choice(project_status)
            )
        print('OK')

        # inserting tasks
        print("inserting into tasks ... ", end='')
        for _ in range(len(projects) * 5):
            CoreModels.Tasks.objects.create(
                title=faker_fa.sentence(nb_words=4),
                project=random.choice(
                    list(CoreModels.Projects.objects.all())
                ),
                description=faker_fa.text(max_nb_chars=200),
                user=random.choice(
                    list(CoreModels.Users.objects.all())
                ),
                level=random.choice(task_levels_score),
                deadline=faker_fa.future_date(
                    end_date=f'+{random.randint(3, 14)}d'
                ),
                status=random.choice(task_status),
            )
        print('OK')

        # inserting tags
        print("inserting into tags ... ", end='')
        for _ in range(CoreModels.Tasks.objects.all().count() * 3):
            ActionModels.Tags.objects.create(
                user=random.choice(
                    list(CoreModels.Users.objects.filter(role=user_roles[1]))
                ),
                task=random.choice(
                    CoreModels.Tasks.objects.all()
                ),
                title=random.choice(tag_titles),
            )
        print('OK')

        # inserting scores
        print("inserting into scores ... ", end='')
        for _ in range(CoreModels.Users.objects.filter(role=user_roles[1]).count()):
            ActionModels.Scores.objects.create(
                score=random.randint(1, 5),
                user=random.choice(
                    list(CoreModels.Users.objects.filter(role=user_roles[1]))
                ),
                task=random.choice(
                    CoreModels.Tasks.objects.all()
                ),
            )
        print('OK')

        # inserting project_members
        print("inserting into scores ... ", end='')
        for _ in range(CoreModels.Projects.objects.all().count() * 3):
            ActionModels.ProjectMembers.objects.create(
                member=random.choice(
                    list(CoreModels.Users.objects.filter(role=user_roles[1]))
                ),
                project=random.choice(
                    list(CoreModels.Projects.objects.all())
                ),
                status=random.choice(member_status),
            )
        print('OK')

        print("Completed ... !")
