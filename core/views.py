from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Lesson, Letter, Word
import random

def home(request):
    return render(request, 'core/home.html')

def roadmap(request):
    lessons = Lesson.objects.all()
    return render(request, 'core/roadmap.html', {'lessons': lessons})

def vocabulary(request):
    return render(request, 'core/vocabulary.html')

def practice(request, mode):
    # Reuse lesson_session template but data will come from a different API endpoint
    return render(request, 'core/lesson_session.html', {'mode': mode})

def practice_data(request, mode):
    questions = []
    
    if mode == 'alphabet':
        letters = list(Letter.objects.all())
        # Pick 15 random letters
        selected = random.sample(letters, min(len(letters), 15))
        
        for letter in selected:
             # Mix of Sound->Char and Char->Sound
             # Sound -> Char
            all_letters = list(Letter.objects.exclude(id=letter.id))
            distractors = random.sample(all_letters, 3) if len(all_letters) >= 3 else all_letters
            options = [l.character for l in distractors] + [letter.character]
            random.shuffle(options)
            
            questions.append({
                'type': 'select_char',
                'prompt': f'Which one is "{letter.transliteration}"?',
                'correct': letter.character,
                'options': options,
                'main_sound': letter.transliteration
            })
            
            # Char -> Sound
            options_sound = [l.transliteration for l in distractors] + [letter.transliteration]
            random.shuffle(options_sound)
            
            questions.append({
                'type': 'select_sound',
                'prompt': 'What sound does this letter make?',
                'correct': letter.transliteration,
                'options': options_sound,
                'main_char': letter.character
            })
            
    elif mode in ['words', 'verbs']:
        category = 'word' if mode == 'words' else 'verb'
        words = list(Word.objects.filter(category=category))
        selected = random.sample(words, min(len(words), 15))
        
        for word in selected:
            # Rus -> French (Select Trans)
            all_words = list(Word.objects.exclude(id=word.id))
            distractors = random.sample(all_words, 3) if len(all_words) >= 3 else all_words
            options = [w.french for w in distractors] + [word.french]
            random.shuffle(options)
            
            questions.append({
                'type': 'select_trans', 
                'prompt': f'Translate "{word.russian}"',
                'correct': word.french,
                'options': options,
                'main_char': word.russian 
            })

            # French -> Rus (Select Char/Word)
            options_rus = [w.russian for w in distractors] + [word.russian]
            random.shuffle(options_rus)

            questions.append({
                'type': 'select_char', 
                'prompt': f'Translate "{word.french}"',
                'correct': word.russian,
                'options': options_rus,
                'main_sound': word.french 
            })

    random.shuffle(questions)
    return JsonResponse({'questions': questions})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    return render(request, 'core/lesson_session.html', {'lesson': lesson})

def lesson_data(request, lesson_id):
    """API to get questions for the lesson"""
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    letters = list(lesson.letters.all())
    
    questions = []
    
    # 1. Intro Cards (Show all new letters first)
    for letter in letters:
        questions.append({
            'type': 'intro',
            'char': letter.character,
            'name': letter.name,
            'trans': letter.transliteration,
            'desc': letter.description
        })
        
    # 2. Quiz Questions
    # We want to test each letter in the lesson multiple times
    
    for letter in letters:
        # Get distractors from OUTSIDE the current lesson to avoid confusion? 
        # Or mixed? Random from all letters is best.
        all_letters = list(Letter.objects.exclude(id=letter.id))
        
        # --- Type A: "Select the character for [Sound]" ---
        # Options: 4 Cyrillic Characters
        distractors_char = random.sample(all_letters, 3) if len(all_letters) >= 3 else all_letters
        options_char = [l.character for l in distractors_char] + [letter.character]
        random.shuffle(options_char)
        
        questions.append({
            'type': 'select_char',
            'prompt': f'Which one is "{letter.transliteration}"?', # e.g. "Which one is 'Zh'?"
            'correct': letter.character,
            'options': options_char,
            'main_sound': letter.transliteration 
        })
        
        # --- Type B: "What sound does [Char] make?" ---
        # Options: 4 Transliterations/Sounds
        distractors_sound = random.sample(all_letters, 3) if len(all_letters) >= 3 else all_letters
        options_sound = [l.transliteration for l in distractors_sound] + [letter.transliteration]
        random.shuffle(options_sound)
        
        questions.append({
            'type': 'select_sound',
            'prompt': 'What sound does this letter make?',
            'correct': letter.transliteration,
            'options': options_sound,
            'main_char': letter.character
        })

    # Shuffle the quiz part
    intro_q = [q for q in questions if q['type'] == 'intro']
    test_q = [q for q in questions if q['type'] != 'intro']
    random.shuffle(test_q)
    
    # Present Intros first, then randomized tests
    final_sequence = intro_q + test_q
    
    return JsonResponse({'questions': final_sequence})
