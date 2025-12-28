from django.core.management.base import BaseCommand
from core.models import Word, Lesson

class Command(BaseCommand):
    help = 'Populates the database with initial English vocabulary'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating English content...')

        # 1. Clear existing English content to avoid duplicates during dev
        deleted_count, _ = Word.objects.filter(target_language='en').delete()
        self.stdout.write(f'Deleted {deleted_count} existing English words.')

        # 2. Add Basic Words (Nouns/Adjectives)
        words_data = [
            {'en': 'Hello', 'fr': 'Bonjour', 'cat': 'word'},
            {'en': 'Cat', 'fr': 'Chat', 'cat': 'word'},
            {'en': 'Dog', 'fr': 'Chien', 'cat': 'word'},
            {'en': 'House', 'fr': 'Maison', 'cat': 'word'},
            {'en': 'Car', 'fr': 'Voiture', 'cat': 'word'},
            {'en': 'Apple', 'fr': 'Pomme', 'cat': 'word'},
            {'en': 'Water', 'fr': 'Eau', 'cat': 'word'},
            {'en': 'Bread', 'fr': 'Pain', 'cat': 'word'},
            {'en': 'Friend', 'fr': 'Ami', 'cat': 'word'},
            {'en': 'Book', 'fr': 'Livre', 'cat': 'word'},
        ]

        # 3. Add Basic Verbs
        verbs_data = [
            {'en': 'To eat', 'fr': 'Manger', 'cat': 'verb'},
            {'en': 'To drink', 'fr': 'Boire', 'cat': 'verb'},
            {'en': 'To sleep', 'fr': 'Dormir', 'cat': 'verb'},
            {'en': 'To run', 'fr': 'Courir', 'cat': 'verb'},
            {'en': 'To speak', 'fr': 'Parler', 'cat': 'verb'},
            {'en': 'To love', 'fr': 'Aimer', 'cat': 'verb'},
            {'en': 'To go', 'fr': 'Aller', 'cat': 'verb'},
            {'en': 'To have', 'fr': 'Avoir', 'cat': 'verb'},
            {'en': 'To be', 'fr': 'Être', 'cat': 'verb'},
            {'en': 'To do', 'fr': 'Faire', 'cat': 'verb'},
        ]

        batch = []
        for item in words_data + verbs_data:
            batch.append(Word(
                russian=item['en'], # Storing English word in 'russian' field for now as it's the "Foreign" field
                french=item['fr'],
                transliteration='', # English doesn't really need transliteration for French speakers usually, or IPA?
                category=item['cat'],
                target_language='en'
            ))

        Word.objects.bulk_create(batch)
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(batch)} English words/verbs.'))
