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
            
            # Additional heuristic: French verbs often end in er/ir/re, 
            # checking both increases accuracy but Russian morphology is reliable for infinitives.

            batch.append(Word(
                russian=rus,
                french=fra,
                transliteration=phon,
                category=category
            ))
        
        Word.objects.bulk_create(batch)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(batch)} words from JSON.'))
