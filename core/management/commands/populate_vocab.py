from django.core.management.base import BaseCommand
from core.models import Word
from transliterate import translit

class Command(BaseCommand):
    help = 'Populates the database with Top Russian vocabulary from new English source'

    def handle(self, *args, **kwargs):
        import json
        import os
        from django.conf import settings

        # New source file
        # Try to use the translated file first
        json_path_fr = os.path.join(settings.BASE_DIR, 'core', 'data', 'russian_fr.json')
        json_path_en = os.path.join(settings.BASE_DIR, 'core', 'data', 'russian.json')
        
        if os.path.exists(json_path_fr):
            json_path = json_path_fr
            self.stdout.write(self.style.SUCCESS(f'Using Translated Dictionary: {json_path}'))
        elif os.path.exists(json_path_en):
            json_path = json_path_en
            self.stdout.write(self.style.WARNING(f'Using English Dictionary (Not yet translated): {json_path}'))
        else:
            self.stdout.write(self.style.ERROR(f'File not found: {json_path_en}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Update or Create words
        count_created = 0
        count_updated = 0
        
        for item in data:
            rus = item.get('word', '').strip()
            
            # Prefer French translation if available, else English
            fra = item.get('french_translation', '').strip()
            if not fra:
                fra = item.get('english_translation', '').strip() # Fallback

            # Prefer French example if available, else English (with context)
            ex_native = item.get('example_sentence_native', '').strip()
            
            ex_trans = item.get('example_sentence_french', '').strip()
            if not ex_trans:
                ex_trans = item.get('example_sentence_english', '').strip()
            
            if ex_native and ex_trans:
                example = f"{ex_native} ({ex_trans})"
            elif ex_native:
                example = ex_native
            else:
                example = ""

            phon = item.get('romanization', '').strip()
            pos = item.get('pos', '').lower()
            
            if not rus or not fra:
                continue


            # Category
            pos = item.get('pos', '').lower()
            # Strict check to avoid 'adverb' matching 'verb'
            if pos == 'verb':
                category = 'verb'
            else:
                category = 'word'
            
            # Example Sentence
            # Format: "Russian sentence. (English translation)"
            ex_native = item.get('example_sentence_native', '').strip()
            ex_eng = item.get('example_sentence_english', '').strip()
            
            example = ""
            if ex_native:
                example = f"{ex_native}"
                if ex_eng:
                    example += f" ({ex_eng})"

            # Handle potential duplicates (Clean up before update)
            existing_dups = Word.objects.filter(russian=rus, target_language='ru')
            if existing_dups.count() > 1:
                keep = existing_dups.order_by('id').first()
                deleted_count, _ = existing_dups.exclude(id=keep.id).delete()
                # print(f"cleaned up {deleted_count} duplicates for '{rus}'")

            word, created = Word.objects.update_or_create(
                russian=rus,
                target_language='ru',
                defaults={
                    'french': eng_def,   # Storing English def in the 'french' field as per plan
                    'transliteration': phon,
                    'category': category,
                    'example_sentence': example
                }
            )
            
            if created:
                count_created += 1
            else:
                count_updated += 1
            
        self.stdout.write(self.style.SUCCESS(f'Finished: {count_created} created, {count_updated} updated from new dictionary.'))
            
