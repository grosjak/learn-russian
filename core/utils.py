
# Common Russian-French translations for static glossary generation
COMMON_TRANSLATIONS = {
    # Pronouns
    'я': 'je', 'меня': 'moi/me', 'мне': 'à moi', 'ты': 'tu', 'тебя': 'toi', 'тебе': 'à toi',
    'он': 'il', 'его': 'lui/son', 'она': 'elle', 'её': 'elle/sa', 'мы': 'nous', 'нас': 'nous',
    'вы': 'vous', 'вас': 'vous', 'они': 'ils', 'их': 'eux/leur', 'это': "c'est",
    
    # Verbs (Common forms)
    'зовут': 'appelle', 'есть': 'est/a', 'любит': 'aime', 'работает': 'travaille',
    'живет': 'vit', 'жибем': 'vivons', 'хочу': 'veux', 'люблю': 'aime',
    'знаю': 'sais', 'думаю': 'pense', 'говорит': 'parle', 'вижу': 'vois',
    'будет': 'sera',
    
    # Nouns (Family, People)
    'семья': 'famille', 'мама': 'maman', 'папа': 'papa', 'брат': 'frère', 'сестра': 'sœur',
    'друг': 'ami', 'студент': 'étudiant', 'врач': 'médecin', 'учитель': 'enseignant',
    'человек': 'personne', 'люди': 'gens', 'дом': 'maison', 'город': 'ville',
    'школа': 'école', 'парк': 'parc', 'спорт': 'sport', 'музыка': 'musique',
    
    # Connectors
    'и': 'et', 'а': 'et/mais', 'но': 'mais', 'или': 'ou', 'потому': 'parce que',
    'что': 'que/quoi', 'где': 'où', 'как': 'comment', 'когда': 'quand',
    
    # Adjectives
    'большой': 'grand', 'маленький': 'petit', 'красивый': 'beau', 'хороший': 'bon',
    'новый': 'nouveau', 'старый': 'vieux', 'русский': 'russe', 'интересный': 'intéressant',
    'белый': 'blanc', 'черный': 'noir', 'красный': 'rouge',
     
     # Time
     'сегодня': 'aujourd\'hui', 'вчера': 'hier', 'завтра': 'demain',
     'день': 'jour', 'ночь': 'nuit', 'утро': 'matin', 'вечер': 'soir',
     'время': 'temps', 'год': 'année', 'лет': 'ans'
}

def generate_glossary(text):
    """
    Parses Russian text and returns a dictionary of word -> translation
    for words found in COMMON_TRANSLATIONS.
    """
    if not text:
        return {}
        
    words = text.lower().replace('.', ' ').replace(',', ' ').replace('!', ' ').replace('?', ' ').split()
    glossary = {}
    for w in words:
        w = w.strip()
        if w in COMMON_TRANSLATIONS:
            glossary[w] = COMMON_TRANSLATIONS[w]
    return glossary
