from django.core.management.base import BaseCommand
from core.models import Word, Lesson

class Command(BaseCommand):
    help = 'Populate English vocabulary'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating English data...')

        # Data Structure
        # tuple: (English/Base, translation, Category, Extra/PastForm, ExampleEn, ExampleFr)
        
        basics = [
            ('Hello', 'Bonjour', 'word', '', 'Hello my friend.', 'Bonjour mon ami.'),
            ('Goodbye', 'Au revoir', 'word', '', 'Goodbye, see you soon.', 'Au revoir, à bientôt.'),
            ('Please', 'S\'il vous plaît', 'word', '', 'Help me, please.', 'Aidez-moi, s\'il vous plaît.'),
            ('Thank you', 'Merci', 'word', '', 'Thank you for your help.', 'Merci pour votre aide.'),
            ('Yes', 'Oui', 'word', '', 'Yes, I agree.', 'Oui, je suis d\'accord.'),
            ('No', 'Non', 'word', '', 'No, I cannot.', 'Non, je ne peux pas.'),
            ('How are you?', 'Comment allez-vous ?', 'word', '', 'How are you today?', 'Comment allez-vous aujourd\'hui ?'),
            ('I am fine', 'Je vais bien', 'word', '', 'I am fine, thanks.', 'Je vais bien, merci.'),
            ('What is your name?', 'Quel est votre nom ?', 'word', '', 'Hello, what is your name?', 'Bonjour, quel est votre nom ?'),
            ('My name is...', 'Je m\'appelle...', 'word', '', 'My name is John.', 'Je m\'appelle John.'),
            ('Where are you from?', 'D\'où venez-vous ?', 'word', '', 'Where are you from originally?', 'D\'où venez-vous à l\'origine ?'),
            ('I am from France', 'Je viens de France', 'word', '', 'I am from France.', 'Je viens de France.'),
        ]

        phrasal_verbs = [
            ('Give up', 'Abandonner', 'verb', '', 'Never give up your dreams.', 'N\'abandonnez jamais vos rêves.'),
            ('Look for', 'Chercher', 'verb', '', 'I look for my keys.', 'Je cherche mes clés.'),
            ('Turn on', 'Allumer', 'verb', '', 'Turn on the light.', 'Allumez la lumière.'),
            ('Turn off', 'Éteindre', 'verb', '', 'Turn off the TV.', 'Éteignez la télé.'),
            ('Get up', 'Se lever', 'verb', '', 'I get up at 7 AM.', 'Je me lève à 7h.'),
            ('Find out', 'Découvrir', 'verb', '', 'I found out the truth.', 'J\'ai découvert la vérité.'),
            ('Grow up', 'Grandir', 'verb', '', 'When I grow up, I will be a pilot.', 'Quand je grandirai, je serai pilote.'),
            ('Go on', 'Continuer', 'verb', '', 'Go on, please.', 'Continuez, s\'il vous plaît.'),
            ('Wake up', 'Se réveiller', 'verb', '', 'I wake up early.', 'Je me réveille tôt.'),
            ('Put on', 'Mettre (vêtement)', 'verb', '', 'Put on your coat.', 'Mets ton manteau.'),
        ]

        # For Irregular verbs: (Infinitive, Translation, 'verb', PastSimple, ExampleEn, ExampleFr)
        irregulars = [
            ('Go', 'Aller', 'verb', 'Went', 'I go to school.', 'Je vais à l\'école.'),
            ('See', 'Voir', 'verb', 'Saw', 'I see a bird.', 'Je vois un oiseau.'),
            ('Buy', 'Acheter', 'verb', 'Bought', 'I buy some bread.', 'J\'achète du pain.'),
            ('Eat', 'Manger', 'verb', 'Ate', 'I eat an apple.', 'Je mange une pomme.'),
            ('Drink', 'Boire', 'verb', 'Drank', 'I drink water.', 'Je bois de l\'eau.'),
            ('Do', 'Faire', 'verb', 'Did', 'I do my homework.', 'Je fais mes devoirs.'),
            ('Have', 'Avoir', 'verb', 'Had', 'I have a car.', 'J\'ai une voiture.'),
            ('Make', 'Fabriquer/Faire', 'verb', 'Made', 'I make a cake.', 'Je fais un gâteau.'),
            ('Take', 'Prendre', 'verb', 'Took', 'I take the bus.', 'Je prends le bus.'),
            ('Come', 'Venir', 'verb', 'Came', 'Come here!', 'Viens ici !'),
            ('Know', 'Savoir/Connaître', 'verb', 'Knew', 'I know the answer.', 'Je connais la réponse.'),
            ('Think', 'Penser', 'verb', 'Thought', 'I think so.', 'Je pense que oui.'),
            ('Get', 'Obtenir', 'verb', 'Got', 'I get a gift.', 'Je reçois un cadeau.'),
            ('Give', 'Donner', 'verb', 'Gave', 'Give me that.', 'Donne-moi ça.'),
            ('Speak', 'Parler', 'verb', 'Spoke', 'I speak English.', 'Je parle anglais.'),
            ('Fight', 'Se battre', 'verb', 'Fought', 'I fight for justice.', 'Je me bats pour la justice.'),
        ]

        all_data = basics + phrasal_verbs + irregulars

        count_created = 0
        count_updated = 0

        for eng, fr, cat, extra, ex_en, ex_fr in all_data:
            # We use 'russian' to store the English word/phrase
            # We use 'russian_accented' to store the extra form (Past Simple) or alternative
            
            # Combine Example: "English (French)"
            full_example = f"{ex_en}\n({ex_fr})"

            word, created = Word.objects.update_or_create(
                russian=eng, # Storing English in 'russian' field
                target_language='en',
                defaults={
                    'french': fr,
                    'category': cat,
                    'russian_accented': extra, # Storing Past Simple here for irregulars
                    'target_language': 'en',
                    'example_sentence': full_example
                }
            )

            if created:
                count_created += 1
            else:
                count_updated += 1

        self.stdout.write(self.style.SUCCESS(f'English Data: {count_created} created, {count_updated} updated.'))
