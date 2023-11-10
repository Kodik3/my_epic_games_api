from typing import Any
import random
from django.core.management.base import BaseCommand
from auths.models import CastomUser




class Command(BaseCommand):

    def gen_usernames(self):
        dictionary = 'j4h2jkhjkHhjg43hghjghjG768hdshhj42ghgg4h3jhjfhdjkJKHkhdhjkHJK67567'
        final_username = 'G'
        for i in range(15):
            final_username+=str(random.choice(dictionary))
        return final_username

    def generate_passwords(self):
        dictionary = 'j4h2jkhjkHhjg43hghjghjG768hdshhj42ghgg4h3jhjfhdjkJKHkhdhjkHJK67567'
        final_password= 'D1'
        for i in range(15):
            final_password+=str(random.choice(dictionary))
        return final_password

    def handle(self, *args, **kwargs):
        num_objects_to_create = 100_000  # Количество объектов для создания

        # Создаем список объектов для bulk_create
        objects_to_create = []
        for _ in range(num_objects_to_create):
            objects_to_create.append(CastomUser(
                email = self.generate_passwords()+self.gen_usernames()+self.generate_passwords()+'@gmail.com',
                name = self.gen_usernames(), 
                password = self.generate_passwords())
            )
        try:
            # Выполняем bulk_create для создания объектов
            CastomUser.objects.bulk_create(objects_to_create, batch_size=1000)  # batch_size можете настроить по вашему усмотрению
            self.stdout.write(self.style.SUCCESS(f'Успешно создано {num_objects_to_create} пользоватлей'))
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f'Ошибка при создании пользоватлей: {str(exc)}'))