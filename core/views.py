from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Lesson, Letter, Word, UserWordProgress
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
            
    elif mode in ['words', 'verbs', 'revision']:
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
            category = 'word' if mode == 'words' else 'verb'
            words = list(Word.objects.filter(category=category, target_language=lang))

        if len(words) > 0:
            random.shuffle(words)
            # Take up to 15 words for a session (Reduced from 20)
            selected = words[:15]
            
            for word in selected:
                questions.append({
                    'type': 'flashcard',
                    'id': word.id,
                    'front': word.russian,
                    'back': word.french,
                    'trans': word.transliteration,
                    'breakdown': get_letter_breakdown(word.russian),
                    'category': word.category,
                    'is_revision': mode == 'revision',
                    'example': word.example_sentence
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
                'word': word.russian, # 'russian' field stores Eng word
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
                'prompt': f'Que signifie "{word.russian}" ?',
                'correct': word.french,
                'options': options,
                'main_word': word.russian,
                'example': word.example_sentence
            })
            
            # Type B: Match Word (Fr -> En)
            options_en = [w.russian for w in distractors] + [word.russian]
            random.shuffle(options_en)
             
            questions.append({
                'type': 'select_word',
                'prompt': f'Comment dit-on "{word.french}" ?',
                'correct': word.russian,
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
def update_word_status(request, word_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # data.get('known') is true if user knew the word
            is_known = data.get('known', False)
            
            word = get_object_or_404(Word, pk=word_id)
            
            # Update or create progress entry
            progress, created = UserWordProgress.objects.get_or_create(
                user=request.user,
                word=word
            )
            
            # If known -> needs_review = False. If failed -> needs_review = True
            progress.needs_review = not is_known
            progress.save()
            
            return JsonResponse({'status': 'ok', 'needs_review': progress.needs_review})
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
