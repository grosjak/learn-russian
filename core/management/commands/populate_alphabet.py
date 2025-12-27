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
            {'title': 'Basic Vowels', 'desc': 'The foundation of Russian.', 'icon': '🅰️'},
            {'title': 'Basic Consonants', 'desc': 'Common sounds similar to English.', 'icon': '🅱️'},
            {'title': 'Soft Vowels', 'desc': 'Vowels that soften the previous consonant.', 'icon': '🍦'},
            {'title': 'Tricky Consonants', 'desc': 'Sounds unique to Russian.', 'icon': '🐍'},
            {'title': 'Signs & More', 'desc': 'Hard and Soft signs.', 'icon': '🛑'},
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
            {'char': 'А', 'name': 'A', 'trans': 'a', 'vowel': True, 'ex_word': 'Адрес', 'ex_mean': 'Address', 'desc': 'Like "a" in "father".', 'lesson_idx': 0},
            {'char': 'О', 'name': 'O', 'trans': 'o', 'vowel': True, 'ex_word': 'Окно', 'ex_mean': 'Window', 'desc': 'Like "o" in "more" (stressed).', 'lesson_idx': 0},
            {'char': 'У', 'name': 'U', 'trans': 'u', 'vowel': True, 'ex_word': 'Утро', 'ex_mean': 'Morning', 'desc': 'Like "oo" in "moon".', 'lesson_idx': 0},
            {'char': 'Э', 'name': 'E', 'trans': 'e', 'vowel': True, 'ex_word': 'Это', 'ex_mean': 'This', 'desc': 'Like "e" in "edit".', 'lesson_idx': 0},
            {'char': 'Ы', 'name': 'Y', 'trans': 'y', 'vowel': True, 'ex_word': 'Тыл', 'ex_mean': 'Rear', 'desc': 'Deep guttural "i".', 'lesson_idx': 0},

            # Lesson 1: Basic Consonants
            {'char': 'М', 'name': 'Em', 'trans': 'm', 'vowel': False, 'ex_word': 'Мама', 'ex_mean': 'Mom', 'desc': 'Like "m" in "mom".', 'lesson_idx': 1},
            {'char': 'К', 'name': 'Ka', 'trans': 'k', 'vowel': False, 'ex_word': 'Кот', 'ex_mean': 'Cat', 'desc': 'Like "k" in "kitten".', 'lesson_idx': 1},
            {'char': 'Т', 'name': 'Te', 'trans': 't', 'vowel': False, 'ex_word': 'Такси', 'ex_mean': 'Taxi', 'desc': 'Like "t" in "tea".', 'lesson_idx': 1},
            {'char': 'С', 'name': 'Es', 'trans': 's', 'vowel': False, 'ex_word': 'Спорт', 'ex_mean': 'Sport', 'desc': 'Like "s" in "sun".', 'lesson_idx': 1},
            {'char': 'В', 'name': 'Ve', 'trans': 'v', 'vowel': False, 'ex_word': 'Вода', 'ex_mean': 'Water', 'desc': 'Like "v" in "van".', 'lesson_idx': 1},
            {'char': 'Н', 'name': 'En', 'trans': 'n', 'vowel': False, 'ex_word': 'Нет', 'ex_mean': 'No', 'desc': 'Like "n" in "no".', 'lesson_idx': 1},
            
             # Lesson 2: Soft Vowels (+ Й)
            {'char': 'Е', 'name': 'Ye', 'trans': 'ye', 'vowel': True, 'ex_word': 'Европа', 'ex_mean': 'Europe', 'desc': 'Like "ye" in "yes".', 'lesson_idx': 2},
            {'char': 'Ё', 'name': 'Yo', 'trans': 'yo', 'vowel': True, 'ex_word': 'Ёлка', 'ex_mean': 'Fir tree', 'desc': 'Like "yo" in "yonder".', 'lesson_idx': 2},
            {'char': 'И', 'name': 'I', 'trans': 'i', 'vowel': True, 'ex_word': 'Игра', 'ex_mean': 'Game', 'desc': 'Like "ee" in "see".', 'lesson_idx': 2},
            {'char': 'Ю', 'name': 'Yu', 'trans': 'yu', 'vowel': True, 'ex_word': 'Юг', 'ex_mean': 'South', 'desc': 'Like "u" in "use".', 'lesson_idx': 2},
            {'char': 'Я', 'name': 'Ya', 'trans': 'ya', 'vowel': True, 'ex_word': 'Яблоко', 'ex_mean': 'Apple', 'desc': 'Like "ya" in "yard".', 'lesson_idx': 2},
            {'char': 'Й', 'name': 'I Short', 'trans': 'y', 'vowel': False, 'ex_word': 'Йогурт', 'ex_mean': 'Yogurt', 'desc': 'Semivowel "y".', 'lesson_idx': 2},
            
            # Lesson 3: Tricky Consonants
            {'char': 'Ж', 'name': 'Zhe', 'trans': 'zh', 'vowel': False, 'ex_word': 'Журнал', 'ex_mean': 'Magazine', 'desc': 'Like "s" in "pleasure".', 'lesson_idx': 3},
            {'char': 'Ш', 'name': 'Sha', 'trans': 'sh', 'vowel': False, 'ex_word': 'Школа', 'ex_mean': 'School', 'desc': 'Like "sh" in "shoe".', 'lesson_idx': 3},
            {'char': 'Щ', 'name': 'Shcha', 'trans': 'shch', 'vowel': False, 'ex_word': 'Щи', 'ex_mean': 'Soup', 'desc': 'Soft, long "sh".', 'lesson_idx': 3},
            {'char': 'Ч', 'name': 'Che', 'trans': 'ch', 'vowel': False, 'ex_word': 'Чай', 'ex_mean': 'Tea', 'desc': 'Like "ch" in "chips".', 'lesson_idx': 3},
            {'char': 'Ц', 'name': 'Tse', 'trans': 'ts', 'vowel': False, 'ex_word': 'Центр', 'ex_mean': 'Center', 'desc': 'Like "ts" in "cats".', 'lesson_idx': 3},
            {'char': 'Х', 'name': 'Ha', 'trans': 'kh', 'vowel': False, 'ex_word': 'Хлеб', 'ex_mean': 'Bread', 'desc': 'Like "ch" in "loch".', 'lesson_idx': 3},
            {'char': 'Р', 'name': 'Er', 'trans': 'r', 'vowel': False, 'ex_word': 'Россия', 'ex_mean': 'Russia', 'desc': 'Trilled "r".', 'lesson_idx': 3},

            # Lesson 4: The Rest
             {'char': 'Б', 'name': 'Be', 'trans': 'b', 'vowel': False, 'ex_word': 'Банк', 'ex_mean': 'Bank', 'desc': 'Like "b" in "boy".', 'lesson_idx': 4},
             {'char': 'Г', 'name': 'Ge', 'trans': 'g', 'vowel': False, 'ex_word': 'Город', 'ex_mean': 'City', 'desc': 'Like "g" in "go".', 'lesson_idx': 4},
             {'char': 'Д', 'name': 'De', 'trans': 'd', 'vowel': False, 'ex_word': 'Дом', 'ex_mean': 'House', 'desc': 'Like "d" in "do".', 'lesson_idx': 4},
             {'char': 'Л', 'name': 'El', 'trans': 'l', 'vowel': False, 'ex_word': 'Лампа', 'ex_mean': 'Lamp', 'desc': 'Like "l" in "love".', 'lesson_idx': 4},
             {'char': 'П', 'name': 'Pe', 'trans': 'p', 'vowel': False, 'ex_word': 'Парк', 'ex_mean': 'Park', 'desc': 'Like "p" in "pot".', 'lesson_idx': 4},
             {'char': 'Ф', 'name': 'Ef', 'trans': 'f', 'vowel': False, 'ex_word': 'Фото', 'ex_mean': 'Photo', 'desc': 'Like "f" in "fat".', 'lesson_idx': 4},
             {'char': 'З', 'name': 'Ze', 'trans': 'z', 'vowel': False, 'ex_word': 'Зима', 'ex_mean': 'Winter', 'desc': 'Like "z" in "zoo".', 'lesson_idx': 4},
             {'char': 'Ъ', 'name': 'Hard Sign', 'trans': '', 'vowel': False, 'ex_word': 'Подъезд', 'ex_mean': 'Entrance', 'desc': 'Hard sign.', 'lesson_idx': 4},
             {'char': 'Ь', 'name': 'Soft Sign', 'trans': '\'', 'vowel': False, 'ex_word': 'Мать', 'ex_mean': 'Mother', 'desc': 'Soft sign.', 'lesson_idx': 4},
        ]

        for item in data:
            Letter.objects.create(
                character=item['char'],
                name=item['name'],
                transliteration=item['trans'],
                is_vowel=item['vowel'],
                example_word_cyrillic=item['ex_word'],
                example_word_meaning=item['ex_mean'],
                description=item['desc'],
                lesson=lessons[item['lesson_idx']]
            )
            
        self.stdout.write(self.style.SUCCESS(f'Successfully populated {len(data)} letters into 5 lessons'))
