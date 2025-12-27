from django.core.management.base import BaseCommand
from core.models import Word

class Command(BaseCommand):
    help = 'Populates the database with Top 100 Russian vocabulary'

    def handle(self, *args, **kwargs):
        # User provided list (Top 100 Frequency)
        raw_data = [
          { "rang": 1, "russe": "я", "transcription": "ya", "francais": "je" },
          { "rang": 2, "russe": "и", "transcription": "i", "francais": "et" },
          { "rang": 3, "russe": "не", "transcription": "nié", "francais": "ne...pas" },
          { "rang": 4, "russe": "быть", "transcription": "byt'", "francais": "être" },
          { "rang": 5, "russe": "в", "transcription": "v", "francais": "dans / en" },
          { "rang": 6, "russe": "он", "transcription": "on", "francais": "il" },
          { "rang": 7, "russe": "что", "transcription": "chto", "francais": "que / quoi" },
          { "rang": 8, "russe": "с", "transcription": "s", "francais": "avec" },
          { "rang": 9, "russe": "это", "transcription": "éto", "francais": "c'est / cela" },
          { "rang": 10, "russe": "как", "transcription": "kak", "francais": "comment" },
          { "rang": 11, "russe": "мы", "transcription": "my", "francais": "nous" },
          { "rang": 12, "russe": "на", "transcription": "na", "francais": "sur" },
          { "rang": 13, "russe": "ты", "transcription": "ty", "francais": "tu" },
          { "rang": 14, "russe": "они", "transcription": "ani", "francais": "ils / elles" },
          { "rang": 15, "russe": "весь", "transcription": "viés", "francais": "tout" },
          { "rang": 16, "russe": "но", "transcription": "no", "francais": "mais" },
          { "rang": 17, "russe": "из", "transcription": "iz", "francais": "de (origine)" },
          { "rang": 18, "russe": "у", "transcription": "u", "francais": "chez / près de" },
          { "rang": 19, "russe": "сказать", "transcription": "skazat'", "francais": "dire" },
          { "rang": 20, "russe": "за", "transcription": "za", "francais": "pour / derrière" },
          { "rang": 21, "russe": "тот", "transcription": "tot", "francais": "ce / celui-là" },
          { "rang": 22, "russe": "год", "transcription": "god", "francais": "année" },
          { "rang": 23, "russe": "человек", "transcription": "tchéloviek", "francais": "personne / homme" },
          { "rang": 24, "russe": "мочь", "transcription": "motch'", "francais": "pouvoir" },
          { "rang": 25, "russe": "знать", "transcription": "znat'", "francais": "savoir" },
          { "rang": 26, "russe": "один", "transcription": "adin", "francais": "un / seul" },
          { "rang": 27, "russe": "видеть", "transcription": "vidiét'", "francais": "voir" },
          { "rang": 28, "russe": "кто", "transcription": "kto", "francais": "qui" },
          { "rang": 29, "russe": "время", "transcription": "vriémia", "francais": "temps" },
          { "rang": 30, "russe": "ещё", "transcription": "yécho", "francais": "encore" },
          { "rang": 31, "russe": "говорить", "transcription": "gavarit'", "francais": "parler" },
          { "rang": 32, "russe": "рука", "transcription": "ruka", "francais": "main / bras" },
          { "rang": 33, "russe": "мой", "transcription": "moy", "francais": "mon" },
          { "rang": 34, "russe": "дело", "transcription": "diélo", "francais": "affaire / chose" },
          { "rang": 35, "russe": "или", "transcription": "ili", "francais": "ou" },
          { "rang": 36, "russe": "хотеть", "transcription": "khatiét'", "francais": "vouloir" },
          { "rang": 37, "russe": "глаз", "transcription": "glaz", "francais": "œil" },
          { "rang": 38, "russe": "сам", "transcription": "sam", "francais": "soi-même" },
          { "rang": 39, "russe": "раз", "transcription": "raz", "francais": "fois" },
          { "rang": 40, "russe": "там", "transcription": "tam", "francais": "là-bas" },
          { "rang": 41, "russe": "где", "transcription": "gdié", "francais": "où" },
          { "rang": 42, "russe": "нет", "transcription": "niét", "francais": "non" },
          { "rang": 43, "russe": "да", "transcription": "da", "francais": "oui" },
          { "rang": 44, "russe": "дом", "transcription": "dom", "francais": "maison" },
          { "rang": 45, "russe": "день", "transcription": "dién'", "francais": "jour" },
          { "rang": 46, "russe": "когда", "transcription": "kagda", "francais": "quand" },
          { "rang": 47, "russe": "друг", "transcription": "drug", "francais": "ami" },
          { "rang": 48, "russe": "голова", "transcription": "galava", "francais": "tête" },
          { "rang": 49, "russe": "идти", "transcription": "idti", "francais": "aller (à pied)" },
          { "rang": 50, "russe": "уже", "transcription": "oujé", "francais": "déjà" },
          { "rang": 51, "russe": "жизнь", "transcription": "jizn'", "francais": "vie" },
          { "rang": 52, "russe": "какой", "transcription": "kakoy", "francais": "quel" },
          { "rang": 53, "russe": "без", "transcription": "biéz", "francais": "sans" },
          { "rang": 54, "russe": "слово", "transcription": "slova", "francais": "mot / parole" },
          { "rang": 55, "russe": "хороший", "transcription": "kharoshiy", "francais": "bon" },
          { "rang": 56, "russe": "свой", "transcription": "svoy", "francais": "le sien (propre)" },
          { "rang": 57, "russe": "лицо", "transcription": "litso", "francais": "visage" },
          { "rang": 58, "russe": "любить", "transcription": "lioubit'", "francais": "aimer" },
          { "rang": 59, "russe": "понимать", "transcription": "panimat'", "francais": "comprendre" },
          { "rang": 60, "russe": "место", "transcription": "miésta", "francais": "lieu / place" },
          { "rang": 61, "russe": "важный", "transcription": "vajniy", "francais": "important" },
          { "rang": 62, "russe": "спрашивать", "transcription": "sprashivat'", "francais": "demander" },
          { "rang": 63, "russe": "только", "transcription": "tol'ka", "francais": "seulement" },
          { "rang": 64, "russe": "молодой", "transcription": "maladoy", "francais": "jeune" },
          { "rang": 65, "russe": "дверь", "transcription": "dviér", "francais": "porte" },
          { "rang": 66, "russe": "здесь", "transcription": "zdiés'", "francais": "ici" },
          { "rang": 67, "russe": "работать", "transcription": "rabotat'", "francais": "travailler" },
          { "rang": 68, "russe": "машина", "transcription": "machina", "francais": "voiture / machine" },
          { "rang": 69, "russe": "сидеть", "transcription": "sidiét'", "francais": "être assis" },
          { "rang": 70, "russe": "над", "transcription": "nad", "francais": "au-dessus" },
          { "rang": 71, "russe": "сторона", "transcription": "starana", "francais": "côté" },
          { "rang": 72, "russe": "потом", "transcription": "patom", "francais": "ensuite" },
          { "rang": 73, "russe": "думать", "transcription": "dumat'", "francais": "penser" },
          { "rang": 74, "russe": "сделать", "transcription": "sdélat'", "francais": "faire (perfectif)" },
          { "rang": 75, "russe": "первый", "transcription": "pierviy", "francais": "premier" },
          { "rang": 76, "russe": "перед", "transcription": "piéred", "francais": "devant" },
          { "rang": 77, "russe": "ну", "transcription": "nou", "francais": "bon / eh bien" },
          { "rang": 78, "russe": "под", "transcription": "pod", "francais": "sous" },
          { "rang": 79, "russe": "получить", "transcription": "paluchit'", "francais": "recevoir" },
          { "rang": 80, "russe": "земля", "transcription": "ziémlia", "francais": "terre" },
          { "rang": 81, "russe": "большой", "transcription": "bal'choy", "francais": "grand" },
          { "rang": 82, "russe": "куда", "transcription": "kuda", "francais": "où (direction)" },
          { "rang": 83, "russe": "работа", "transcription": "rabota", "francais": "travail" },
          { "rang": 84, "russe": "часто", "transcription": "tchasta", "francais": "souvent" },
          { "rang": 85, "russe": "нужно", "transcription": "noujna", "francais": "il faut / nécessaire" },
          { "rang": 86, "russe": "читать", "transcription": "tchitat'", "francais": "lire" },
          { "rang": 87, "russe": "два", "transcription": "dva", "francais": "deux" },
          { "rang": 88, "russe": "три", "transcription": "tri", "francais": "trois" },
          { "rang": 89, "russe": "ничто", "transcription": "nichto", "francais": "rien" },
          { "rang": 90, "russe": "кушать", "transcription": "kuchat'", "francais": "manger" },
          { "rang": 91, "russe": "вода", "transcription": "vada", "francais": "eau" },
          { "rang": 92, "russe": "отец", "transcription": "atiéts", "francais": "père" },
          { "rang": 93, "russe": "мать", "transcription": "mat'", "francais": "mère" },
          { "rang": 94, "russe": "голос", "transcription": "golos", "francais": "voix" },
          { "rang": 95, "russe": "письмо", "transcription": "pis'mo", "francais": "lettre (courrier)" },
          { "rang": 96, "russe": "ночь", "transcription": "notch'", "francais": "nuit" },
          { "rang": 97, "russe": "час", "transcription": "tchas", "francais": "heure" },
          { "rang": 98, "russe": "ждать", "transcription": "jdat'", "francais": "attendre" },
          { "rang": 99, "russe": "последний", "transcription": "pasliédniy", "francais": "dernier" },
          { "rang": 100, "russe": "мир", "transcription": "mir", "francais": "monde / paix" }
        ]

        def get_category(word):
            # Simple heuristic: Russian verbs typically end in ть, ти, or чь
            word_lower = word.lower()
            if word_lower.endswith(('ть', 'ти', 'чь')):
                return 'verb'
            return 'word'

        # Clear existing
        Word.objects.all().delete()
        
        # Populate
        batch = []
        for item in raw_data:
            cat = get_category(item['russe'])
            batch.append(Word(
                russian=item['russe'],
                french=item['francais'],
                transliteration=item['transcription'],
                category=cat
            ))
        
        Word.objects.bulk_create(batch)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully populated {len(batch)} items from Top 100 list'))
