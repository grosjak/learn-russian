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
        json_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'russian.json')
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count_created = 0
        count_updated = 0
        
        for item in data:
            # Mapping new JSON structure to Model
            # "word" -> russian
            # "english_translation" -> french (as we are replacing the slot, even if content is English)
            # "romanization" -> transliteration
            # "pos" -> category (verb detection)
            # "example_sentence_native" + "example_sentence_english" -> example_sentence

            rus = item.get('word', '').strip()
            eng_def = item.get('english_translation', '').strip()
            phon = item.get('romanization', '').strip()
            
            if not rus or not eng_def:
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
            
