import json
import os
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from deep_translator import GoogleTranslator
from requests.exceptions import RequestException

class Command(BaseCommand):
    help = 'Translate dictionary from English to French using Google Translate'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, help='Limit number of words to translate (for testing)')
        parser.add_argument('--reset', action='store_true', help='Start from scratch (ignore existing progress)')

    def handle(self, *args, **options):
        source_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'russian.json')
        dest_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'russian_fr.json')
        
        if not os.path.exists(source_path):
            self.stdout.write(self.style.ERROR(f'Source file not found: {source_path}'))
            return

        with open(source_path, 'r', encoding='utf-8') as f:
             source_data = json.load(f)

        # Load progress
        processed_data = []
        start_index = 0
        
        if os.path.exists(dest_path) and not options['reset']:
            with open(dest_path, 'r', encoding='utf-8') as f:
                try:
                    processed_data = json.load(f)
                    # Create a map of existing words to avoid re-translating
                    existing_words = {item['word'] for item in processed_data}
                    start_index = len(processed_data)
                    self.stdout.write(self.style.SUCCESS(f'Resuming from {start_index} entries found in {dest_path}'))
                except json.JSONDecodeError:
                    self.stdout.write(self.style.WARNING(f'Could not decode {dest_path}, starting over.'))
        
        translator = GoogleTranslator(source='en', target='fr')
        
        total_count = len(source_data)
        limit = options.get('limit')
        if limit:
            self.stdout.write(f"Limit set to {limit} items.")
        
        count = 0
        errors = 0
        
        self.stdout.write(f"Starting translation of {total_count} items...")
        
        # We need to match processed data with source data order or just append?
        # To be safe, let's just iterate source and check if in processed
        # A simpler way given standard order:
        
        # Build dictionary of processed items for fast lookup
        processed_map = {item['word']: item for item in processed_data}
        
        new_data = []
        
        try:
            for i, item in enumerate(source_data):
                word = item.get('word')
                
                # If already translated
                if word in processed_map:
                    new_data.append(processed_map[word])
                    continue
                
                if limit and count >= limit:
                    break

                # Translate
                try:
                    # Clone item
                    new_item = item.copy()
                    
                    # 1. Translate Definition
                    eng_def = item.get('english_translation', '')
                    if eng_def:
                        fr_def = translator.translate(eng_def)
                        new_item['french_translation'] = fr_def
                    else:
                        new_item['french_translation'] = ''

                    # 2. Translate Example
                    eng_ex = item.get('example_sentence_english', '')
                    if eng_ex:
                        fr_ex = translator.translate(eng_ex)
                        new_item['example_sentence_french'] = fr_ex
                    else:
                        new_item['example_sentence_french'] = ''
                    
                    new_data.append(new_item)
                    count += 1
                    
                    # Rate limit kindness
                    time.sleep(0.5) 
                    
                    # Periodic save
                    if count % 20 == 0:
                        self.save_data(dest_path, new_data)
                        self.stdout.write(f"Translated {count} words...")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error translating '{word}': {e}"))
                    errors += 1
                    # Keep original item without trans fields? Or skip?
                    # Let's keep it but without fields so we don't lose data, but maybe retry later?
                    # Better to just not add it to new_data so we retry next run? 
                    # Actually, if we crash, we lose everything since last save.
                    # Let's try to save what we have.
                    if errors > 5:
                        self.stdout.write(self.style.ERROR("Too many errors, stopping."))
                        break
                    time.sleep(5) # Wait longer on error

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nInterrupted by user. Saving progress..."))
        
        # Final Save
        self.save_data(dest_path, new_data)
        self.stdout.write(self.style.SUCCESS(f"Done. Processed {len(new_data)}/{total_count} items. Translated {count} new items."))

    def save_data(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
