from django.core.management.base import BaseCommand
from core.models import Letter, Lesson

class Command(BaseCommand):
    help = 'Populates the database with the Cyrillic alphabet and Lessons'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Letter.objects.all().delete()
        Lesson.objects.all().delete()

        # Define Lessons
        lessons_data = [
            {'title': 'Voyelles Basiques', 'desc': 'Les bases du russe.', 'icon': '🅰️'},
            {'title': 'Consonnes Basiques', 'desc': 'Sons communs similaires au français.', 'icon': '🅱️'},
            {'title': 'Voyelles Molles', 'desc': 'Voyelles qui adoucissent la consonne précédente.', 'icon': '🍦'},
            {'title': 'Consonnes Difficiles', 'desc': 'Sons uniques au russe.', 'icon': '🐍'},
            {'title': 'Signes & Autres', 'desc': 'Signes durs et mous.', 'icon': '🛑'},
        ]
        
        lessons = {}
        for idx, l_data in enumerate(lessons_data):
            lesson = Lesson.objects.create(
                title=l_data['title'],
                description=l_data['desc'],
                order=idx + 1,
                icon=l_data['icon']
            )
            lessons[idx] = lesson

        # Define Letters with Lesson assignment
        # 0: Basic Vowels, 1: Basic Consonants, 2: Soft Vowels, 3: Tricky Consonants, 4: Signs
        data = [
            # Lesson 0: Basic Vowels
            {'char': 'А', 'name': 'A', 'trans': 'a', 'vowel': True, 'ex_word': 'Адрес', 'ex_mean': 'Adresse', 'desc': 'Comme "a" dans "papa".', 'lesson_idx': 0},
            {'char': 'О', 'name': 'O', 'trans': 'o', 'vowel': True, 'ex_word': 'Окно', 'ex_mean': 'Fenêtre', 'desc': 'Comme "o" dans "port".', 'lesson_idx': 0},
            {'char': 'У', 'name': 'U', 'trans': 'u', 'vowel': True, 'ex_word': 'Утро', 'ex_mean': 'Matin', 'desc': 'Comme "ou" dans "loup".', 'lesson_idx': 0},
            {'char': 'Э', 'name': 'E', 'trans': 'e', 'vowel': True, 'ex_word': 'Это', 'ex_mean': 'Çà', 'desc': 'Comme "è" dans "père".', 'lesson_idx': 0},
            {'char': 'Ы', 'name': 'Y', 'trans': 'y', 'vowel': True, 'ex_word': 'Тыл', 'ex_mean': 'Arrière', 'desc': 'Son guttural profond, comme "i" mais du fond de la gorge.', 'lesson_idx': 0},

            # Lesson 1: Basic Consonants
            {'char': 'М', 'name': 'Em', 'trans': 'm', 'vowel': False, 'ex_word': 'Мама', 'ex_mean': 'Maman', 'desc': 'Comme "m" dans "maman".', 'lesson_idx': 1},
            {'char': 'К', 'name': 'Ka', 'trans': 'k', 'vowel': False, 'ex_word': 'Кот', 'ex_mean': 'Chat', 'desc': 'Comme "k" dans "koala".', 'lesson_idx': 1},
            {'char': 'Т', 'name': 'Te', 'trans': 't', 'vowel': False, 'ex_word': 'Такси', 'ex_mean': 'Taxi', 'desc': 'Comme "t" dans "tarte".', 'lesson_idx': 1},
            {'char': 'С', 'name': 'Es', 'trans': 's', 'vowel': False, 'ex_word': 'Спорт', 'ex_mean': 'Sport', 'desc': 'Comme "s" dans "soleil".', 'lesson_idx': 1},
            {'char': 'В', 'name': 'Ve', 'trans': 'v', 'vowel': False, 'ex_word': 'Вода', 'ex_mean': 'Eau', 'desc': 'Comme "v" dans "voiture".', 'lesson_idx': 1},
            {'char': 'Н', 'name': 'En', 'trans': 'n', 'vowel': False, 'ex_word': 'Нет', 'ex_mean': 'Non', 'desc': 'Comme "n" dans "non".', 'lesson_idx': 1},
            
             # Lesson 2: Soft Vowels (+ Й)
            {'char': 'Е', 'name': 'Ye', 'trans': 'ye', 'vowel': True, 'ex_word': 'Европа', 'ex_mean': 'Europe', 'desc': 'Comme "ié" dans "pied".', 'lesson_idx': 2},
            {'char': 'Ё', 'name': 'Yo', 'trans': 'yo', 'vowel': True, 'ex_word': 'Ёлка', 'ex_mean': 'Sapin', 'desc': 'Comme "yo" dans "yoyo" ou "io" dans "radio".', 'lesson_idx': 2},
            {'char': 'И', 'name': 'I', 'trans': 'i', 'vowel': True, 'ex_word': 'Игра', 'ex_mean': 'Jeu', 'desc': 'Comme "i" dans "lit".', 'lesson_idx': 2},
            {'char': 'Ю', 'name': 'Yu', 'trans': 'yu', 'vowel': True, 'ex_word': 'Юг', 'ex_mean': 'Sud', 'desc': 'Comme "iou" dans "youpi".', 'lesson_idx': 2},
            {'char': 'Я', 'name': 'Ya', 'trans': 'ya', 'vowel': True, 'ex_word': 'Яблоко', 'ex_mean': 'Pomme', 'desc': 'Comme "ia" dans "diable".', 'lesson_idx': 2},
            {'char': 'Й', 'name': 'I Court', 'trans': 'y', 'vowel': False, 'ex_word': 'Йогурт', 'ex_mean': 'Yaourt', 'desc': 'Semi-voyelle "ille" comme dans "soleil".', 'lesson_idx': 2},
            
            # Lesson 3: Tricky Consonants
            {'char': 'Ж', 'name': 'Zhe', 'trans': 'zh', 'vowel': False, 'ex_word': 'Журнал', 'ex_mean': 'Journal', 'desc': 'Comme "j" dans "jardin".', 'lesson_idx': 3},
            {'char': 'Ш', 'name': 'Sha', 'trans': 'sh', 'vowel': False, 'ex_word': 'Школа', 'ex_mean': 'École', 'desc': 'Comme "ch" dans "chat".', 'lesson_idx': 3},
            {'char': 'Щ', 'name': 'Shcha', 'trans': 'shch', 'vowel': False, 'ex_word': 'Щи', 'ex_mean': 'Soupe', 'desc': 'Comme "ch" mais plus doux et long, entre "ch" et "s".', 'lesson_idx': 3},
            {'char': 'Ч', 'name': 'Che', 'trans': 'ch', 'vowel': False, 'ex_word': 'Чай', 'ex_mean': 'Thé', 'desc': 'Comme "tch" dans "tchèque".', 'lesson_idx': 3},
            {'char': 'Ц', 'name': 'Tse', 'trans': 'ts', 'vowel': False, 'ex_word': 'Центр', 'ex_mean': 'Centre', 'desc': 'Comme "ts" dans "tsar".', 'lesson_idx': 3},
            {'char': 'Х', 'name': 'Ha', 'trans': 'kh', 'vowel': False, 'ex_word': 'Хлеб', 'ex_mean': 'Pain', 'desc': 'Raclement de gorge, comme le "j" espagnol ou "ch" allemand (Bach).', 'lesson_idx': 3},
            {'char': 'Р', 'name': 'Er', 'trans': 'r', 'vowel': False, 'ex_word': 'Россия', 'ex_mean': 'Russie', 'desc': 'R roulé avec la langue.', 'lesson_idx': 3},

            # Lesson 4: The Rest
             {'char': 'Б', 'name': 'Be', 'trans': 'b', 'vowel': False, 'ex_word': 'Банк', 'ex_mean': 'Bank', 'desc': 'Comme "b" dans "ballon".', 'lesson_idx': 4},
             {'char': 'Г', 'name': 'Ge', 'trans': 'g', 'vowel': False, 'ex_word': 'Город', 'ex_mean': 'Ville', 'desc': 'Comme "g" dans "gare".', 'lesson_idx': 4},
             {'char': 'Д', 'name': 'De', 'trans': 'd', 'vowel': False, 'ex_word': 'Дом', 'ex_mean': 'Maison', 'desc': 'Comme "d" dans "date".', 'lesson_idx': 4},
             {'char': 'Л', 'name': 'El', 'trans': 'l', 'vowel': False, 'ex_word': 'Лампа', 'ex_mean': 'Lampe', 'desc': 'Comme "l" dans "livre".', 'lesson_idx': 4},
             {'char': 'П', 'name': 'Pe', 'trans': 'p', 'vowel': False, 'ex_word': 'Парк', 'ex_mean': 'Parc', 'desc': 'Comme "p" dans "pomme".', 'lesson_idx': 4},
             {'char': 'Ф', 'name': 'Ef', 'trans': 'f', 'vowel': False, 'ex_word': 'Фото', 'ex_mean': 'Photo', 'desc': 'Comme "f" dans "fête".', 'lesson_idx': 4},
             {'char': 'З', 'name': 'Ze', 'trans': 'z', 'vowel': False, 'ex_word': 'Зима', 'ex_mean': 'Hiver', 'desc': 'Comme "z" dans "zèbre".', 'lesson_idx': 4},
             {'char': 'Ъ', 'name': 'Signe Dur', 'trans': '', 'vowel': False, 'ex_word': 'Подъезд', 'ex_mean': 'Entrée', 'desc': 'Signe dur (indique une pause).', 'lesson_idx': 4},
             {'char': 'Ь', 'name': 'Signe Mou', 'trans': '\'', 'vowel': False, 'ex_word': 'Мать', 'ex_mean': 'Mère', 'desc': 'Signe mou (adoucit la consonne précédente).', 'lesson_idx': 4},
        ]
        
        for item in data:
            Letter.objects.create(
                character=item['char'],
                name=item['name'],
                transliteration=item['trans'],
                is_vowel=item['vowel'],
                example_word_rus=item['ex_word'],
                example_word_eng=item['ex_mean'],
                description=item['desc'],
                lesson=lessons[item['lesson_idx']]
            )
            
        self.stdout.write(self.style.SUCCESS(f'Successfully populated {len(data)} letters into 5 lessons (French)'))
