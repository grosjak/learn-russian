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

        # 3a. Irregular Verbs (Existing)
        irr_verbs = data.get('irregular_verbs', [])
        if irr_verbs:
            lesson_irr = Lesson.objects.create(
                title='Verbes Irréguliers',
                description='Les verbes qui ne suivent pas les règles.',
                icon='⚡',
                order=10, 
                target_language='en'
            )
            
            # Simple examples map for irregular verbs
            examples_irr = {
                'be': 'I am happy.',
                'go': 'I go to school.',
                'eat': 'I eat an apple.',
                'drink': 'I drink water.',
                'have': 'I have a car.',
                'see': 'I see a bird.',
                'take': 'I take the bus.',
                'get': 'I get up early.',
                'do': 'I do my homework.',
                'make': 'I make a cake.'
            }

            batch_irr = []
            for v in irr_verbs:
                base = v.get('base')
                forms = f"Past: {v.get('past')}, PP: {v.get('participle')}"
                ex = examples_irr.get(base, f"I {base} something.") # Generic fallback

                batch_irr.append(Word(
                    russian=base,
                    french=v.get('fr'),
                    transliteration=forms,
                    category='verb',
                    target_language='en',
                    lesson=lesson_irr,
                    example_sentence=ex
                ))
            Word.objects.bulk_create(batch_irr)
            self.stdout.write(f'Imported {len(batch_irr)} irregular verbs.')

        # 3b. Verbes en Contexte (NEW)
        # We select some common verbs to show in sentences
        context_verbs = [
            {'en': 'Want', 'fr': 'Vouloir', 'ex': 'I want a pizza.'},
            {'en': 'Need', 'fr': 'Avoir besoin', 'ex': 'I need help.'},
            {'en': 'Like', 'fr': 'Aimer', 'ex': 'I like chocolate.'},
            {'en': 'Love', 'fr': 'Adorer', 'ex': 'I love my dog.'},
            {'en': 'Know', 'fr': 'Savoir', 'ex': 'I know the answer.'},
            {'en': 'Think', 'fr': 'Penser', 'ex': 'I think it is good.'},
            {'en': 'Understand', 'fr': 'Comprendre', 'ex': 'I understand you.'},
        ]

        lesson_context = Lesson.objects.create(
            title='Verbes en Contexte',
            description='Apprenez avec des phrases.',
            icon='🗣️',
            order=15,
            target_language='en'
        )
        
        batch_context = []
        for v in context_verbs:
             batch_context.append(Word(
                russian=v['en'],
                french=v['fr'],
                transliteration='',
                category='verb',
                target_language='en',
                lesson=lesson_context,
                example_sentence=v['ex']
            ))
        Word.objects.bulk_create(batch_context)


        # 3c. Common Words
        common = data.get('common_words', [])
        if common:
            chunk_size = 12 # Reduced from 30 for shorter lessons
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
                        lesson=lesson_common,
                        example_sentence="" # Could add logic here too
                    ))
                Word.objects.bulk_create(batch_common)
            self.stdout.write(f'Imported {len(common)} common words into {len(chunks)} lessons.')

        self.stdout.write(self.style.SUCCESS(f'Successfully populated English content.'))
