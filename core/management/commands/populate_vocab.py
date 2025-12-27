from django.core.management.base import BaseCommand
from core.models import Word

class Command(BaseCommand):
    help = 'Populates the database with extended Russian vocabulary'

    def handle(self, *args, **kwargs):
        words_data = [
            # --- VERBS (Top frequency) ---
            {'russian': 'Быть', 'french': 'Être', 'transliteration': 'Byt', 'category': 'verb'},
            {'russian': 'Идти', 'french': 'Aller (à pied)', 'transliteration': 'Idti', 'category': 'verb'},
            {'russian': 'Ехать', 'french': 'Aller (transport)', 'transliteration': 'Ye-khat', 'category': 'verb'},
            {'russian': 'Мочь', 'french': 'Pouvoir', 'transliteration': 'Moch', 'category': 'verb'},
            {'russian': 'Знать', 'french': 'Savoir', 'transliteration': 'Znat', 'category': 'verb'},
            {'russian': 'Говорить', 'french': 'Parler', 'transliteration': 'Go-vo-rit', 'category': 'verb'},
            {'russian': 'Видеть', 'french': 'Voir', 'transliteration': 'Vi-det', 'category': 'verb'},
            {'russian': 'Слышать', 'french': 'Entendre', 'transliteration': 'Sly-shat', 'category': 'verb'},
            {'russian': 'Есть', 'french': 'Manger', 'transliteration': 'Yest', 'category': 'verb'},
            {'russian': 'Пить', 'french': 'Boire', 'transliteration': 'Pit', 'category': 'verb'},
            {'russian': 'Спать', 'french': 'Dormir', 'transliteration': 'Spat', 'category': 'verb'},
            {'russian': 'Хотеть', 'french': 'Vouloir', 'transliteration': 'Kho-tet', 'category': 'verb'},
            {'russian': 'Любить', 'french': 'Aimer', 'transliteration': 'Lyu-bit', 'category': 'verb'},
            {'russian': 'Делать', 'french': 'Faire', 'transliteration': 'De-lat', 'category': 'verb'},
            {'russian': 'Думать', 'french': 'Penser', 'transliteration': 'Du-mat', 'category': 'verb'},
            {'russian': 'Понимать', 'french': 'Comprendre', 'transliteration': 'Po-ni-mat', 'category': 'verb'},
            {'russian': 'Жить', 'french': 'Vivre', 'transliteration': 'Zhit', 'category': 'verb'},
            {'russian': 'Смотреть', 'french': 'Regarder', 'transliteration': 'Smo-tret', 'category': 'verb'},
            {'russian': 'Работать', 'french': 'Travailler', 'transliteration': 'Ra-bo-tat', 'category': 'verb'},
            {'russian': 'Играть', 'french': 'Jouer', 'transliteration': 'Ig-rat', 'category': 'verb'},
            {'russian': 'Читaть', 'french': 'Lire', 'transliteration': 'Chi-tat', 'category': 'verb'},
            {'russian': 'Писать', 'french': 'Écrire', 'transliteration': 'Pi-sat', 'category': 'verb'},
            {'russian': 'Давать', 'french': 'Donner', 'transliteration': 'Da-vat', 'category': 'verb'},
            {'russian': 'Брать', 'french': 'Prendre', 'transliteration': 'Brat', 'category': 'verb'},
            {'russian': 'Начинать', 'french': 'Commencer', 'transliteration': 'Na-chi-nat', 'category': 'verb'},
            {'russian': 'Ждать', 'french': 'Attendre', 'transliteration': 'Zhdat', 'category': 'verb'},

            # --- WORDS (Common nouns/adverbs/phrases) ---
            {'russian': 'Привет', 'french': 'Salut', 'transliteration': 'Pri-vet', 'category': 'word'},
            {'russian': 'Спасибо', 'french': 'Merci', 'transliteration': 'Spa-si-bo', 'category': 'word'},
            {'russian': 'Пожалуйста', 'french': 'S\'il vous plaît', 'transliteration': 'Po-zha-lu-sta', 'category': 'word'},
            {'russian': 'Да', 'french': 'Oui', 'transliteration': 'Da', 'category': 'word'},
            {'russian': 'Нет', 'french': 'Non', 'transliteration': 'Net', 'category': 'word'},
            {'russian': 'Хорошо', 'french': 'Bien', 'transliteration': 'Kho-ro-sho', 'category': 'word'},
            {'russian': 'Плохо', 'french': 'Mal', 'transliteration': 'Plo-kho', 'category': 'word'},
            {'russian': 'Друг', 'french': 'Ami', 'transliteration': 'Drug', 'category': 'word'},
            {'russian': 'Дом', 'french': 'Maison', 'transliteration': 'Dom', 'category': 'word'},
            {'russian': 'Кот', 'french': 'Chat', 'transliteration': 'Kot', 'category': 'word'},
            {'russian': 'Собака', 'french': 'Chien', 'transliteration': 'So-ba-ka', 'category': 'word'},
            {'russian': 'Мама', 'french': 'Maman', 'transliteration': 'Ma-ma', 'category': 'word'},
            {'russian': 'Папа', 'french': 'Papa', 'transliteration': 'Pa-pa', 'category': 'word'},
            {'russian': 'Вода', 'french': 'Eau', 'transliteration': 'Vo-da', 'category': 'word'},
            {'russian': 'Хлеб', 'french': 'Pain', 'transliteration': 'Khleb', 'category': 'word'},
            {'russian': 'Еда', 'french': 'Nourriture', 'transliteration': 'Ye-da', 'category': 'word'},
            {'russian': 'День', 'french': 'Jour', 'transliteration': 'Den', 'category': 'word'},
            {'russian': 'Ночь', 'french': 'Nuit', 'transliteration': 'Noch', 'category': 'word'},
            {'russian': 'Утро', 'french': 'Matin', 'transliteration': 'Ut-ro', 'category': 'word'},
            {'russian': 'Вечер', 'french': 'Soir', 'transliteration': 'Ve-cher', 'category': 'word'},
            {'russian': 'Молоко', 'french': 'Lait', 'transliteration': 'Mo-lo-ko', 'category': 'word'},
            {'russian': 'Кофе', 'french': 'Café', 'transliteration': 'Ko-fe', 'category': 'word'},
            {'russian': 'Чай', 'french': 'Thé', 'transliteration': 'Chay', 'category': 'word'},
            {'russian': 'Школа', 'french': 'École', 'transliteration': 'Shko-la', 'category': 'word'},
            {'russian': 'Работа', 'french': 'Travail', 'transliteration': 'Ra-bo-ta', 'category': 'word'},
            {'russian': 'Машина', 'french': 'Voiture', 'transliteration': 'Ma-shi-na', 'category': 'word'},
            {'russian': 'Город', 'french': 'Ville', 'transliteration': 'Go-rod', 'category': 'word'},
            {'russian': 'Страна', 'french': 'Pays', 'transliteration': 'Stra-na', 'category': 'word'},
            {'russian': 'Мир', 'french': 'Monde/Paix', 'transliteration': 'Mir', 'category': 'word'},
            {'russian': 'Человек', 'french': 'Personne/Homme', 'transliteration': 'Che-lo-vek', 'category': 'word'},
            {'russian': 'Женщина', 'french': 'Femme', 'transliteration': 'Zhen-shchi-na', 'category': 'word'},
            {'russian': 'Мужчина', 'french': 'Homme', 'transliteration': 'Muzh-chi-na', 'category': 'word'},
            {'russian': 'Ребенок', 'french': 'Enfant', 'transliteration': 'Re-byo-nok', 'category': 'word'},
            {'russian': 'Большой', 'french': 'Grand', 'transliteration': 'Bol-shoy', 'category': 'word'},
            {'russian': 'Маленький', 'french': 'Petit', 'transliteration': 'Ma-len-kiy', 'category': 'word'},
            {'russian': 'Сегодня', 'french': 'Aujourd\'hui', 'transliteration': 'Se-god-nya', 'category': 'word'},
            {'russian': 'Завтра', 'french': 'Demain', 'transliteration': 'Zav-tra', 'category': 'word'},
            {'russian': 'Вчера', 'french': 'Hier', 'transliteration': 'Vche-ra', 'category': 'word'},
            {'russian': 'Где', 'french': 'Où', 'transliteration': 'Gde', 'category': 'word'},
            {'russian': 'Кто', 'french': 'Qui', 'transliteration': 'Kto', 'category': 'word'},
            {'russian': 'Что', 'french': 'Quoi', 'transliteration': 'Chto', 'category': 'word'},
            {'russian': 'Почему', 'french': 'Pourquoi', 'transliteration': 'Po-che-mu', 'category': 'word'},
            {'russian': 'Как', 'french': 'Comment', 'transliteration': 'Kak', 'category': 'word'},
            {'russian': 'Здравствуйте', 'french': 'Bonjour (formel)', 'transliteration': 'Zdrav-stvoy-te', 'category': 'word'},
            {'russian': 'До свидания', 'french': 'Au revoir', 'transliteration': 'Do svi-da-ni-ya', 'category': 'word'},
        ]

        # Clear existing to avoid duplicates if running multiple times (or better, get_or_create)
        # Assuming explicit overwrite is better for now to ensure quality
        Word.objects.all().delete()

        for w in words_data:
            Word.objects.create(**w)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully populated {len(words_data)} vocabulary items'))
