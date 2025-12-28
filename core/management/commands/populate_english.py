from django.core.management.base import BaseCommand
from core.models import Word, Lesson

class Command(BaseCommand):
    help = 'Populates the database with structured English curriculum'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating English curriculum...')

        # 1. Clear existing English content
        Word.objects.filter(target_language='en').delete()
        Lesson.objects.filter(target_language='en').delete()
        
        # 2. Define Curriculum
        curriculum = [
            {
                'title': 'Introduction',
                'desc': 'Les bases absolues.',
                'icon': '👋',
                'words': [
                    {'en': 'Hello', 'fr': 'Bonjour'},
                    {'en': 'Goodbye', 'fr': 'Au revoir'},
                    {'en': 'Please', 'fr': 'S\'il vous plaît'},
                    {'en': 'Thank you', 'fr': 'Merci'},
                    {'en': 'Yes', 'fr': 'Oui'},
                    {'en': 'No', 'fr': 'Non'},
                    {'en': 'Car', 'fr': 'Voiture'},
                    {'en': 'House', 'fr': 'Maison'},
                ]
            },
            {
                'title': 'Nombres & Couleurs',
                'desc': 'Compter et décrire.',
                'icon': '🎨',
                'words': [
                    {'en': 'One', 'fr': 'Un'},
                    {'en': 'Two', 'fr': 'Deux'},
                    {'en': 'Three', 'fr': 'Trois'},
                    {'en': 'Red', 'fr': 'Rouge'},
                    {'en': 'Blue', 'fr': 'Bleu'},
                    {'en': 'Green', 'fr': 'Vert'},
                    {'en': 'White', 'fr': 'Blanc'},
                    {'en': 'Black', 'fr': 'Noir'},
                ]
            },
            {
                'title': 'Nourriture',
                'desc': 'Manger et boire.',
                'icon': '🍎',
                'words': [
                    {'en': 'Apple', 'fr': 'Pomme'},
                    {'en': 'Bread', 'fr': 'Pain'},
                    {'en': 'Water', 'fr': 'Eau'},
                    {'en': 'Milk', 'fr': 'Lait'},
                    {'en': 'Coffee', 'fr': 'Café'},
                    {'en': 'Tea', 'fr': 'Thé'},
                    {'en': 'Cheese', 'fr': 'Fromage'},
                    {'en': 'Cake', 'fr': 'Gâteau'},
                ]
            },
            {
                'title': 'Verbes Basiques',
                'desc': 'Actions du quotidien.',
                'icon': '🏃',
                'words': [
                    {'en': 'To eat', 'fr': 'Manger', 'cat': 'verb'},
                    {'en': 'To drink', 'fr': 'Boire', 'cat': 'verb'},
                    {'en': 'To sleep', 'fr': 'Dormir', 'cat': 'verb'},
                    {'en': 'To go', 'fr': 'Aller', 'cat': 'verb'},
                    {'en': 'To have', 'fr': 'Avoir', 'cat': 'verb'},
                    {'en': 'To be', 'fr': 'Être', 'cat': 'verb'},
                ]
            }
        ]

        total_words = 0
        for idx, module in enumerate(curriculum):
            lesson = Lesson.objects.create(
                title=module['title'],
                description=module['desc'],
                icon=module['icon'],
                order=idx + 1,
                target_language='en'
            )
            
            batch = []
            for item in module['words']:
                category = item.get('cat', 'word')
                batch.append(Word(
                    russian=item['en'],
                    french=item['fr'],
                    transliteration='',
                    category=category,
                    target_language='en',
                    lesson=lesson
                ))
            
            Word.objects.bulk_create(batch)
            total_words += len(batch)
            self.stdout.write(f'Created lesson "{module["title"]}" with {len(batch)} words.')

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {len(curriculum)} English lessons with {total_words} words.'))
