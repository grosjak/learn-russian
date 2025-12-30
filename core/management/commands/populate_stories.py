from django.core.management.base import BaseCommand
from core.models import Story

class Command(BaseCommand):
    help = 'Populate initial stories'

    def handle(self, *args, **options):
        stories = [
            {
                'title': 'Моя семья (My Family)',
                'slug': 'my-family',
                'difficulty': 'A1',
                'content_russian': """Меня зовут Иван. Я студент. Мне двадцать лет.
У меня большая семья. Это мой отец. Его зовут Борис. Он врач. Он работает в больнице.
Это моя мать. Её зовут Анна. Она учительница. Она работает в школе.
У меня есть брат и сестра. Мой брат — инженер, а моя сестра — студентка.
Мы живём в Москве. Наш дом большой и красивый.
В выходные мы часто гуляем в парке. Мы любим спорт и музыку.""",
                'content_english': """My name is Ivan. I am a student. I am twenty years old.
I have a big family. This is my father. His name is Boris. He is a doctor. He works in a hospital.
This is my mother. Her name is Anna. She is a teacher. She works in a school.
I have a brother and a sister. My brother is an engineer, and my sister is a student.
We live in Moscow. Our house is big and beautiful.
On weekends we often walk in the park. We love sports and music."""
            },
            {
                'title': 'В кофейне (In the coffee shop)',
                'slug': 'coffee-shop',
                'difficulty': 'A1',
                'content_russian': """— Здравствуйте!
— Здравствуйте! Что вы хотите?
— Я хочу кофе с молоком и круассан, пожалуйста.
— Большой или маленький кофе?
— Большой, пожалуйста.
— Сахар нужен?
— Да, два сахара.
— Хорошо. С вас 350 рублей.
— Вот, пожалуйста.
— Спасибо. Ваш кофе будет готов через минуту.
— Спасибо!""",
                'content_english': """— Hello!
— Hello! What do you want?
— I want coffee with milk and a croissant, please.
— Big or small coffee?
— Big, please.
— Do you need sugar?
— Yes, two sugars.
— Okay. That will be 350 rubles.
— Here you go.
— Thank you. Your coffee will be ready in a minute.
— Thank you!"""
            }
        ]

        for s in stories:
            story, created = Story.objects.get_or_create(
                slug=s['slug'],
                defaults={
                    'title': s['title'],
                    'difficulty': s['difficulty'],
                    'content_russian': s['content_russian'],
                    'content_english': s['content_english']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created story: {s['title']}"))
            else:
                self.stdout.write(f"Story already exists: {s['title']}")
