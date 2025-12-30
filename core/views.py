from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Letter, Lesson, Word, UserWordProgress, Story
from .utils import generate_glossary
import json
import random

def select_language(request):
    """
    Sets the target language in the session.
    If 'lang' param is missing, clears the selection (Redirects to choice page).
    """
    lang = request.GET.get('lang')
    
    if not lang:
        # Reset language selection
        if 'target_language' in request.session:
            del request.session['target_language']
    elif lang in ['ru', 'en']:
        request.session['target_language'] = lang
        
    return redirect('home')

@login_required
def home(request):
    """
    Home view: Shows categories (Alphabet, Vocabulary).
    Filters content based on selected language.
    """
    target_lang = request.session.get('target_language')
    
    # If no language is set, render a selection page (or redirect to one)
    if not target_lang:
        return render(request, 'core/language_selection.html')
        
    return render(request, 'core/home.html', {
        'target_language': target_lang
    })

@login_required
def roadmap(request):
    lang = request.session.get('target_language', 'ru')
    lessons = Lesson.objects.filter(target_language=lang).order_by('order')
    return render(request, 'core/roadmap.html', {'lessons': lessons})

@login_required
def vocabulary(request):
    return render(request, 'core/vocabulary.html')

@login_required
def stories_list(request):
    stories = Story.objects.all().order_by('created_at')
    return render(request, 'core/stories/list.html', {'stories': stories})

@login_required
def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug)
    
    # Self-healing: if glossary is empty, generate it now
    if not story.word_translations:
        story.word_translations = generate_glossary(story.content_russian)
        story.save(update_fields=['word_translations'])
        
    return render(request, 'core/stories/detail.html', {'story': story})

@login_required
def lookup_word(request):
    word_text = request.GET.get('word', '').strip()
    if not word_text:
        return JsonResponse({'found': False})
    
    # Simple direct lookup
    # Enhancements needed later: lemmatization, stripping endings
    # For now, exact match or simple stripping
    
    # Try exact match first
    # Using 'russian' field
    word = Word.objects.filter(russian__iexact=word_text).first()
    
    if not word:
        # Try stripping punctuation just in case JS didn't clean it all
        clean_word = "".join(c for c in word_text if c.isalnum())
        word = Word.objects.filter(russian__iexact=clean_word).first()

    if word:
        translation = word.french
        # If the 'french' field holds English (as per our dict switch), it returns that.
        return JsonResponse({
            'found': True,
            'word': word.russian,
            'translation': translation
        })
    else:
        return JsonResponse({'found': False})


@login_required
def revision_list(request):
    # Get all words marked as needs_review for the current user
    progress_entries = UserWordProgress.objects.filter(
        user=request.user, 
        needs_review=True
    ).select_related('word')
    
    words = [entry.word for entry in progress_entries]
    
    return render(request, 'core/revision_list.html', {'words': words})

@login_required
def practice(request, mode):
    # Reuse lesson_session template but data will come from a different API endpoint
    return render(request, 'core/lesson_session.html', {'mode': mode})

@login_required
def practice_data(request, mode):
    questions = []
    
    if mode == 'alphabet':
        # Alphabet might be language specific. For now, assume 'ru' implies Cyrillic alphabet logic.
        # If 'en', we might practice phonemes? Or maybe just hide alphabet mode for 'en' initially.
        # Let's keep existing logic but maybe filter by language if we add English alphabet later?
        # Actually, Letter model does not have target_language yet. 
        # But 'Alphabet' button should probably only show if lang == 'ru'.
        # For 'en', we might skip this.
        
        # However, to be safe, let's just use existing letters.
        letters = list(Letter.objects.all())
        # Pick 10 random letters (Reduced from 15)
        selected = random.sample(letters, min(len(letters), 10))
        
        for letter in selected:
             # Mix of Sound->Char and Char->Sound
             # Sound -> Char
            all_letters = list(Letter.objects.exclude(id=letter.id))
            distractors = random.sample(all_letters, 3) if len(all_letters) >= 3 else all_letters
            options = [l.character for l in distractors] + [letter.character]
            random.shuffle(options)
            
            questions.append({
                'type': 'select_char',
                'prompt': f'Laquelle est "{letter.transliteration}" ?',
                'correct': letter.character,
                'options': options,
                'main_sound': letter.transliteration
            })
            
            # Char -> Sound
            options_sound = [l.transliteration for l in distractors] + [letter.transliteration]
            random.shuffle(options_sound)
            
            questions.append({
                'type': 'select_sound',
                'prompt': 'Quel son fait cette lettre ?',
                'correct': letter.transliteration,
                'options': options_sound,
                'main_char': letter.character
            })

        random.shuffle(questions)

        # Add Grid Question at the beginning (Must be AFTER shuffle)
        questions.insert(0, {
            'type': 'alphabet_grid',
            'letters': [{'char': l.character, 'trans': l.transliteration} for l in letters]
        })
            

    elif mode == 'audio_challenge':
        # Ghost Mode: Audio -> Select Translation
        # Use all words (Frontend will use TTS if no audio file)
        words = list(Word.objects.filter(category='word'))
        if len(words) < 5:
            # Fallback if few words have audio: take all and UI will use TTS fallback if implemented or just show text
            # For now, let's assume we have some. If empty, return empty.
            pass
            
        if words:
            random.shuffle(words)
            selected = words[:15]
            
            for word in selected:
                # Distractors (French translations)
                all_words = list(Word.objects.exclude(id=word.id))
                distractors = random.sample(all_words, 3) if len(all_words) >= 3 else all_words
                options = [w.french for w in distractors] + [word.french]
                random.shuffle(options)
                
                questions.append({
                    'type': 'listen_and_select',
                    'id': word.id,
                    'prompt': '🎧 Écoutez...', # Text hidden, only audio icon
                    'audio_url': word.audio.url if word.audio else None,
                    'correct': word.french, # User selects French
                    'options': options,
                    'reveal_word': word.russian_accented or word.russian, # Show after answer
                    'example': word.example_sentence
                })

    elif mode in ['words', 'verbs', 'revision', 'daily']:
        if mode == 'revision':
            # Revision mode: only words flagged as needing review for this user
            if request.user.is_authenticated:
                words = [
                    p.word for p in UserWordProgress.objects.filter(
                        user=request.user, 
                        needs_review=True
                    ).select_related('word')
                ]
            else:
                words = []
        else:
            lang = request.session.get('target_language', 'ru')
            
            if mode == 'daily':
                # Deterministic random selection based on today's date
                import datetime
                today = datetime.date.today()
                # Use today's ordinal as seed
                seed_val = today.toordinal()
                
                # We need a fresh random instance to not affect global state
                # But python's random.seed affects global. 
                # Better: fetch all IDs, select deterministically.
                
                all_words = list(Word.objects.filter(target_language=lang))
                
                if all_words:
                    rng = random.Random(seed_val)
                    # Select 10 items mixed
                    words = rng.sample(all_words, min(len(all_words), 10))
                else:
                    words = []
            else:
                category = 'word' if mode == 'words' else 'verb'
                words = list(Word.objects.filter(category=category, target_language=lang))

        if len(words) > 0:
            # Shuffle the session question order (presentation order) 
            # For daily, the SET of words is fixed, but order can be random each time or fixed?
            # Let's random shuffle the presentation order so it feels like a test
            random.shuffle(words)
            # Take up to 15 words for a session (Daily is capped at 10 above)
            selected = words[:15]
            
            for word in selected:
                questions.append({
                    'type': 'input_text',
                    'id': word.id,
                    'prompt': word.french, # Show French, ask for Russian
                    'correct': word.russian, # Check against raw Russian
                    'display_correct': word.russian_accented or word.russian, # For feedback
                    'category': word.category,
                    'is_revision': mode == 'revision',
                    'example': word.example_sentence,
                    'audio_url': word.audio.url if word.audio else None,
                    'transliteration': word.transliteration
                })
    
    return JsonResponse({'questions': questions})

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    return render(request, 'core/lesson_session.html', {'lesson': lesson})

@login_required
def lesson_data(request, lesson_id):
    """API to get questions for the lesson"""
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    questions = []

    # Logic for Russian (Letters based)
    if lesson.target_language == 'ru':
        letters = list(lesson.letters.all())
        
        # 1. Intro Cards
        for letter in letters:
            questions.append({
                'type': 'intro',
                'char': letter.character,
                'name': letter.name,
                'trans': letter.transliteration,
                'desc': letter.description
            })
            
        # 2. Quiz Questions
        for letter in letters:
            all_letters = list(Letter.objects.exclude(id=letter.id))
            
            # Type A: Select Char
            distractors_char = random.sample(all_letters, 3) if len(all_letters) >= 3 else all_letters
            options_char = [l.character for l in distractors_char] + [letter.character]
            random.shuffle(options_char)
            
            questions.append({
                'type': 'select_char',
                'prompt': f'Laquelle est "{letter.transliteration}" ?',
                'correct': letter.character,
                'options': options_char,
                'main_sound': letter.transliteration 
            })
            
            # Type B: Select Sound
            distractors_sound = random.sample(all_letters, 3) if len(all_letters) >= 3 else all_letters
            options_sound = [l.transliteration for l in distractors_sound] + [letter.transliteration]
            random.shuffle(options_sound)
            
            questions.append({
                'type': 'select_sound',
                'prompt': 'Quel son fait cette lettre ?',
                'correct': letter.transliteration,
                'options': options_sound,
                'main_char': letter.character
            })
            
        intro_q = [q for q in questions if q['type'] == 'intro']
        test_q = [q for q in questions if q['type'] != 'intro']
        random.shuffle(test_q)
        final_sequence = intro_q + test_q

    # Logic for English (Word based)
    else:
        words = list(lesson.words.all())
        
        # 1. Intro Cards (New Words)
        for word in words:
            questions.append({
                'type': 'intro_word',
                'word': word.russian_accented or word.russian, # 'russian' field stores Eng word
                'translation': word.french,
                'category': word.category,
                'example': word.example_sentence
            })
            
        # 2. Quiz Questions
        for word in words:
            # Type A: Match Translation (En -> Fr)
            all_words = list(Word.objects.filter(target_language='en').exclude(id=word.id))
            distractors = random.sample(all_words, 3) if len(all_words) >= 3 else all_words
            options = [w.french for w in distractors] + [word.french]
            random.shuffle(options)
            
            questions.append({
                'type': 'select_translation',
                'prompt': f'Que signifie "{word.russian_accented or word.russian}" ?',
                'correct': word.french,
                'options': options,
                'main_word': word.russian_accented or word.russian,
                'example': word.example_sentence
            })
            
            # Type B: Match Word (Fr -> En)
            options_en = [w.russian_accented or w.russian for w in distractors] + [word.russian_accented or word.russian]
            random.shuffle(options_en)
             
            questions.append({
                'type': 'select_word',
                'prompt': f'Comment dit-on "{word.french}" ?',
                'correct': word.russian_accented or word.russian,
                'options': options_en,
                'main_word': word.french, # Source word to display if needed
                'example': word.example_sentence
            })
            
        # Shuffle logic similar to Russian
        intro_q = [q for q in questions if q['type'] == 'intro_word']
        test_q = [q for q in questions if q['type'] != 'intro_word']
        random.shuffle(test_q)
        final_sequence = intro_q + test_q
    
    return JsonResponse({'questions': final_sequence})


@csrf_exempt
@login_required
def validate_answer(request):
    """
    API to validate user input against the correct word.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            word_id = data.get('word_id')
            user_input = data.get('user_input', '')
            
            word = get_object_or_404(Word, pk=word_id)
            
            from .services import TextValidationService
            result = TextValidationService.validate(user_input, word.russian)
            
            return JsonResponse({
                'status': 'ok',
                'is_correct': result['is_correct'],
                'similarity': result['similarity'],
                'diff_html': result['diff_html'],
                'correct_answer': word.russian_accented or word.russian
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
@login_required
def update_word_status(request, word_id):
    """
    Update progress using SM-2 algorithm.
    Requires 'quality' (0-5) in the body.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quality = int(data.get('quality', 0))
            
            word = get_object_or_404(Word, pk=word_id)
            
            progress, created = UserWordProgress.objects.get_or_create(
                user=request.user,
                word=word
            )
            
            from .services import SM2Service
            srs_data = SM2Service.calculate_review(
                quality,
                progress.interval if not created else 0,
                progress.ease_factor,
                progress.streak
            )
            
            progress.interval = srs_data['interval']
            progress.ease_factor = srs_data['ease_factor']
            progress.next_review_date = srs_data['next_review_date']
            progress.streak = srs_data['streak']
            progress.needs_review = srs_data['next_review_date'] <= timezone.now()
            progress.save()
            
            return JsonResponse({
                'status': 'ok',
                'next_review': progress.next_review_date.isoformat(),
                'interval': progress.interval
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

def get_letter_breakdown(word):
    trans_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '(hard)', 'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    breakdown = []
    for char in word:
        lower = char.lower()
        if lower in trans_map:
            breakdown.append({'char': char, 'sound': trans_map[lower]})
        elif char.strip(): # Ignore pure whitespace in breakdown if confusing, but keeping punctuation is good
            breakdown.append({'char': char, 'sound': char})
    return breakdown

@login_required
def grammar_practice(request):
    return render(request, 'core/grammar/gender_lab.html')

@login_required
@login_required
def get_grammar_gender_data(request):
    attempt = int(request.GET.get('attempt', 0))
    if attempt > 10:
        return JsonResponse({'error': 'Too many retries'}, status=404)

    # Filter for words that have "nice" endings for A1 level (exclude soft sign for now if possible)
    # We can try to filter at DB level to be more efficient
    candidates = Word.objects.filter(category='word').exclude(russian__endswith='ь')
    
    count = candidates.count()
    if count == 0:
         # Fallback to all words if we can't find easy ones
        candidates = Word.objects.filter(category='word')
        count = candidates.count()
        
    if count == 0:
        return JsonResponse({'error': 'No words'}, status=404)
    
    # Pick random
    random_idx = random.randint(0, count - 1)
    word = candidates[random_idx]
    
    ru = word.russian.lower().strip()
    
    gender = '?'
    explanation = ""
    
    # Heuristic rules
    if ru.endswith(('а', 'я')):
        gender = 'f'
        explanation = f"Terminaison en -{ru[-1]} -> Féminin"
        if ru in ['папа', 'дядя', 'дедушка', 'мужчина']:
            gender = 'm'
            explanation = "Exception : Désigne un homme -> Masculin"
            
    elif ru.endswith(('о', 'е', 'ё', 'мя')):
        gender = 'n'
        explanation = f"Terminaison en -{ru[-1]} -> Neutre"
        
    else:
        # Check if it really ends with a soft sign (if we fell back)
        if ru.endswith('ь'):
             # Retry with incremented attempt
             return redirect(f"{request.path}?attempt={attempt+1}")
             
        # Consonant (or й)
        gender = 'm'
        explanation = "Terminaison consonne/й -> Masculin"
        
    return JsonResponse({
        'word': word.russian,
        'translation': word.french,
        'phonetic': word.transliteration,
        'gender': gender,
        'explanation': explanation
    })
