from django.core.management.base import BaseCommand
from core.models import Word

class Command(BaseCommand):
    help = 'Populates the database with Top 200 Russian vocabulary (Translated)'

    def handle(self, *args, **kwargs):
        import json
        import os
        from django.conf import settings

        json_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'dictionnaire_fr_ru_complet.json')
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Reset DB
        deleted, _ = Word.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Deleted {deleted} existing words.'))
        
        batch = []
        for item in data:
            rus = item.get('ru_cyrillic', '').strip()
            fra = item.get('fr', '').strip()
            phon = item.get('ru_phonetique', '').strip()
            
            if not rus or not fra:
                continue

            # Heuristic for Category: Verb detection
            # Russian infinitives usually end in ть, ти, or чь
            if rus.lower().endswith(('ть', 'ти', 'чь')):
                category = 'verb'
            else:
                category = 'word'
            
            # Simple Example Logic for common words
            example = ""
            # Manual map for demo
            examples_map = {
                'быть': 'Я хочу быть счастливым. (I want to be happy)',
                'сказать': 'Что ты хочешь сказать? (What do you want to say?)',
                'говорить': 'Я говорю по-русски. (I speak Russian)',
                'знать': 'Я не знаю. (I do not know)',
                'стать': 'Он станет врачом. (He will become a doctor)',
                'есть': 'Я хочу есть. (I want to eat)',
                'хотеть': 'Я хочу спать. (I want to sleep)',
                'видеть': 'Я вижу тебя. (I see you)',
                'идти': 'Я иду домой. (I am going home)',
                'думать': 'О чем ты думаешь? (What are you thinking about?)',
                'жить': 'Где ты живешь? (Where do you live?)',
                'смотреть': 'Я смотрю телевизор. (I am watching TV)',
                'работать': 'Она работает в школе. (She works at a school)',
                'любить': 'Я люблю тебя. (I love you)',
                'понимать': 'Я не понимаю. (I do not understand)',
            }
            
            if rus in examples_map:
                example = examples_map[rus]

            batch.append(Word(
                russian=rus,
                french=fra,
                transliteration=phon,
                category=category,
                example_sentence=example
            ))
        
        Word.objects.bulk_create(batch)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(batch)} words from JSON.'))
