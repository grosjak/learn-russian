from django.db import models

class Lesson(models.Model):
    TARGET_LANGUAGE_CHOICES = [
        ('ru', 'Russe'),
        ('en', 'Anglais'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    icon = models.CharField(max_length=10, default='📝')
    target_language = models.CharField(max_length=2, choices=TARGET_LANGUAGE_CHOICES, default='ru')

    def __str__(self):
        return f"[{self.get_target_language_display()}] {self.title}"

class Letter(models.Model):
    character = models.CharField(max_length=1)
    name = models.CharField(max_length=50)
    transliteration = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    example_word_rus = models.CharField(max_length=50, blank=True)
    example_word_eng = models.CharField(max_length=50, blank=True)
    is_vowel = models.BooleanField(default=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, related_name='letters')

    def __str__(self):
        return f"{self.character} ({self.transliteration})"

class Word(models.Model):
    CATEGORY_CHOICES = [
        ('word', 'Mot'),
        ('verb', 'Verbe'),
    ]
    TARGET_LANGUAGE_CHOICES = [
        ('ru', 'Russe'),
        ('en', 'Anglais'),
    ]
    
    russian = models.CharField(max_length=100)
    french = models.CharField(max_length=100)
    transliteration = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='word')
    target_language = models.CharField(max_length=2, choices=TARGET_LANGUAGE_CHOICES, default='ru')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='words')
    example_sentence = models.TextField(blank=True, help_text="Phrase d'exemple pour illustrer le mot")
    audio = models.FileField(upload_to='audio/words/', null=True, blank=True, help_text="Fichier audio pour la prononciation")

    def __str__(self):
        return f"[{self.get_target_language_display()}] {self.russian} - {self.french}"

class UserWordProgress(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    needs_review = models.BooleanField(default=True)
    last_reviewed = models.DateTimeField(auto_now=True)
    
    # SRS Fields (SM-2 Algorithm)
    next_review_date = models.DateTimeField(null=True, blank=True)
    interval = models.IntegerField(default=1, help_text="Intervalle en jours")
    ease_factor = models.FloatField(default=2.5, help_text="Facteur de facilité")
    streak = models.IntegerField(default=0, help_text="Nombre de réussites consécutives")

    class Meta:
        unique_together = ('user', 'word')

    def __str__(self):
        return f"{self.user.username} - {self.word.russian} ({'Review' if self.needs_review else 'Known'})"

class Story(models.Model):
    DIFFICULTY_CHOICES = [
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper Intermediate'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content_russian = models.TextField(help_text="The full Russian text of the story")
    content_english = models.TextField(help_text="The full English translation")
    difficulty = models.CharField(max_length=2, choices=DIFFICULTY_CHOICES, default='A1')
    created_at = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='stories_audio/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Stories"
