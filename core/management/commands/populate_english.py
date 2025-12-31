from django.core.management.base import BaseCommand
from core.models import Word, Lesson

class Command(BaseCommand):
    help = 'Populate English vocabulary'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating English data...')

        # Data Structure
        # tuple: (English/Base, translation, Category, Extra/PastForm)
        
        basics = [
            ('Hello', 'Bonjour', 'word', ''),
            ('Goodbye', 'Au revoir', 'word', ''),
            ('Please', 'S\'il vous plaît', 'word', ''),
            ('Thank you', 'Merci', 'word', ''),
            ('Yes', 'Oui', 'word', ''),
            ('No', 'Non', 'word', ''),
            ('How are you?', 'Comment allez-vous ?', 'word', ''),
            ('I am fine', 'Je vais bien', 'word', ''),
            ('What is your name?', 'Quel est votre nom ?', 'word', ''),
            ('My name is...', 'Je m\'appelle...', 'word', ''),
            ('Where are you from?', 'D\'où venez-vous ?', 'word', ''),
            ('I am from France', 'Je viens de France', 'word', ''),
        ]

        phrasal_verbs = [
            ('Give up', 'Abandonner', 'verb', ''),
            ('Look for', 'Chercher', 'verb', ''),
            ('Turn on', 'Allumer', 'verb', ''),
            ('Turn off', 'Éteindre', 'verb', ''),
            ('Get up', 'Se lever', 'verb', ''),
            ('Find out', 'Découvrir', 'verb', ''),
            ('Grow up', 'Grandir', 'verb', ''),
            ('Go on', 'Continuer', 'verb', ''),
            ('Wake up', 'Se réveiller', 'verb', ''),
            ('Put on', 'Mettre (vêtement)', 'verb', ''),
        ]

        # For Irregular verbs: (Infinitive, Translation, 'verb', PastSimple)
        irregulars = [
            ('Go', 'Aller', 'verb', 'Went'),
            ('See', 'Voir', 'verb', 'Saw'),
            ('Buy', 'Acheter', 'verb', 'Bought'),
            ('Eat', 'Manger', 'verb', 'Ate'),
            ('Drink', 'Boire', 'verb', 'Drank'),
            ('Do', 'Faire', 'verb', 'Did'),
            ('Have', 'Avoir', 'verb', 'Had'),
            ('Make', 'Fabriquer/Faire', 'verb', 'Made'),
            ('Take', 'Prendre', 'verb', 'Took'),
            ('Come', 'Venir', 'verb', 'Came'),
            ('Know', 'Savoir/Connaître', 'verb', 'Knew'),
            ('Think', 'Pensera', 'verb', 'Thought'),
            ('Get', 'Obtenir', 'verb', 'Got'),
            ('Give', 'Donner', 'verb', 'Gave'),
            ('Speak', 'Parler', 'verb', 'Spoke'),
        ]

        all_data = basics + phrasal_verbs + irregulars

        count_created = 0
        count_updated = 0

        for eng, fr, cat, extra in all_data:
            # We use 'russian' to store the English word/phrase
            # We use 'russian_accented' to store the extra form (Past Simple) or alternative
            
            word, created = Word.objects.update_or_create(
                russian=eng, # Storing English in 'russian' field
                target_language='en',
                defaults={
                    'french': fr,
                    'category': cat,
                    'russian_accented': extra, # Storing Past Simple here for irregulars
                    'target_language': 'en'
                }
            )

            if created:
                count_created += 1
            else:
                count_updated += 1

        self.stdout.write(self.style.SUCCESS(f'English Data: {count_created} created, {count_updated} updated.'))
