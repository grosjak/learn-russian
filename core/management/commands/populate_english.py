from django.core.management.base import BaseCommand
from core.models import Word, Lesson

class Command(BaseCommand):
    help = 'Populates the database with structured English curriculum'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating English curriculum...')
        import json
        import os
        from django.conf import settings

        # 1. Clear existing English content
        Word.objects.filter(target_language='en').delete()
        Lesson.objects.filter(target_language='en').delete()
        
        # 2. Existing Structured Curriculum (Manual)
        self.stdout.write('Creating manual basic lessons...')
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
                ]
            }
        ]

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
                batch.append(Word(
                    russian=item['en'],
                    french=item['fr'],
                    transliteration='',
                    category='word',
                    target_language='en',
                    lesson=lesson
                ))
            Word.objects.bulk_create(batch)
        
        # 3. Load from JSON dictionary
        json_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'anglais-francais.json')
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'JSON file not found at {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 3a. Irregular Verbs
        irr_verbs = data.get('irregular_verbs', [])
        if irr_verbs:
            lesson_irr = Lesson.objects.create(
                title='Verbes Irréguliers',
                description='Les verbes qui ne suivent pas les règles.',
                icon='⚡',
                order=10, # Place later in curriculum
                target_language='en'
            )
            
            batch_irr = []
            for v in irr_verbs:
                # Use transliteration field to store past forms for "Hint"
                forms = f"Past: {v.get('past')}, PP: {v.get('participle')}"
                batch_irr.append(Word(
                    russian=v.get('base'),
                    french=v.get('fr'),
                    transliteration=forms,
                    category='verb',
                    target_language='en',
                    lesson=lesson_irr
                ))
            Word.objects.bulk_create(batch_irr)
            self.stdout.write(f'Imported {len(batch_irr)} irregular verbs.')

        # 3b. Common Words
        common = data.get('common_words', [])
        if common:
            # Split into chunks of 20 to avoid huge lessons? 
            # Or just one big "Top 100" lesson.
            # Let's do chunks of 30.
            chunk_size = 30
            chunks = [common[i:i + chunk_size] for i in range(0, len(common), chunk_size)]
            
            for i, chunk in enumerate(chunks):
                lesson_common = Lesson.objects.create(
                    title=f'Mots Fréquents {i+1}',
                    description=f'Vocabulaire essentiel partie {i+1}.',
                    icon='📊',
                    order=20 + i,
                    target_language='en'
                )
                
                batch_common = []
                for w in chunk:
                    cat = 'verb' if 'verb' in w.get('type', '') else 'word'
                    batch_common.append(Word(
                        russian=w.get('en'),
                        french=w.get('fr'),
                        transliteration='', # No extra info needed
                        category=cat,
                        target_language='en',
                        lesson=lesson_common
                    ))
                Word.objects.bulk_create(batch_common)
            self.stdout.write(f'Imported {len(common)} common words into {len(chunks)} lessons.')

        self.stdout.write(self.style.SUCCESS(f'Successfully populated English content.'))
