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
        if os.path.exists(dest_path) and not options['reset']:
            with open(dest_path, 'r', encoding='utf-8') as f:
                try:
                    processed_data = json.load(f)
                    self.stdout.write(self.style.SUCCESS(f'Resuming: {len(processed_data)} items already translated.'))
                except json.JSONDecodeError:
                    pass

        # Identify pending items
        # We assume source_data order is constant. 
        # Skip items already in processed_data based on count.
        start_index = len(processed_data)
        pending_items = source_data[start_index:]
        
        limit = options.get('limit')
        if limit:
            pending_items = pending_items[:limit]
            self.stdout.write(f"Limit set to {limit} items.")

        if not pending_items:
             self.stdout.write(self.style.SUCCESS('Nothing new to translate.'))
             return

        translator = GoogleTranslator(source='en', target='fr')
        
        # Prepare batches
        BATCH_SIZE = 50 
        total_batches = (len(pending_items) + BATCH_SIZE - 1) // BATCH_SIZE
        
        self.stdout.write(f"Translating {len(pending_items)} items in {total_batches} batches...")
        
        # We need to extract texts to translate
        # To keep matching correct, we'll process batch by batch entirely
        
        try:
            for i in range(0, len(pending_items), BATCH_SIZE):
                batch_items = pending_items[i:i + BATCH_SIZE]
                
                # Collect texts
                texts_to_translate = []
                map_indices = [] # (item_index_in_batch, field_type) where 0=def, 1=example
                
                for idx, item in enumerate(batch_items):
                    # Definition
                    eng_def = item.get('english_translation', '')
                    if eng_def:
                        texts_to_translate.append(eng_def)
                        map_indices.append((idx, 0))
                    
                    # Example
                    eng_ex = item.get('example_sentence_english', '')
                    if eng_ex:
                        texts_to_translate.append(eng_ex)
                        map_indices.append((idx, 1))

                if not texts_to_translate:
                    # Just append items as is (rare case where mostly empty)
                    processed_data.extend(batch_items)
                    continue

                # Batch Translate with Retry
                retries = 0
                max_retries = 5
                batch_success = False
                
                while retries < max_retries:
                    try:
                        translated_texts = translator.translate_batch(texts_to_translate)
                        batch_success = True
                        break # Success
                    except Exception as e:
                        retries += 1
                        wait_time = retries * 10 # 10s, 20s, 30s, 40s, 50s...
                        
                        warning_msg = str(e)
                        if "Wait one moment" in warning_msg or "429" in warning_msg:
                             self.stdout.write(self.style.WARNING(f"\nRate limit hit (Batch {i//BATCH_SIZE + 1}). Sleeping {wait_time}s..."))
                        else:
                             self.stdout.write(self.style.ERROR(f"\nBatch error: {e}. Retrying in {wait_time}s..."))
                        
                        time.sleep(wait_time)
                
                if not batch_success:
                    self.stdout.write(self.style.ERROR(f"Failed to translate batch {i//BATCH_SIZE + 1} after {max_retries} retries. Skipping."))
                    # We could continue to next batch or stop. 
                    # Let's stop to preserve data integrity vs partial skip
                    break

                # Map back
                text_idx = 0
                for item_idx, field_type in map_indices:
                    if text_idx < len(translated_texts):
                        trans = translated_texts[text_idx]
                        if field_type == 0:
                            batch_items[item_idx]['french_translation'] = trans
                        else:
                            batch_items[item_idx]['example_sentence_french'] = trans
                        text_idx += 1
                
                # Add to processed
                processed_data.extend(batch_items)
                
                # Save periodically
                self.save_data(dest_path, processed_data)
                
                current_count = start_index + i + len(batch_items)
                self.stdout.write(f"Batch {i//BATCH_SIZE + 1}/{total_batches} done. Total: {current_count} words.")
                
                # Standard polite wait between batches
                time.sleep(2)
        
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nInterrupted."))

        self.save_data(dest_path, processed_data)
        self.stdout.write(self.style.SUCCESS(f"Finished functionality. Total translated: {len(processed_data)}"))

    def save_data(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
