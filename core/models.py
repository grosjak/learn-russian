from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    icon = models.CharField(max_length=10, default='📝')

    def __str__(self):
        return self.title

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
        ('word', 'Word'),
        ('verb', 'Verb'),
    ]
    
    russian = models.CharField(max_length=100)
    french = models.CharField(max_length=100)
    transliteration = models.CharField(max_length=100)
    transliteration = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='word')

    def __str__(self):
        return f"{self.russian} - {self.french}"

class UserWordProgress(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    needs_review = models.BooleanField(default=True)
    last_reviewed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'word')

    def __str__(self):
        return f"{self.user.username} - {self.word.russian} ({'Review' if self.needs_review else 'Known'})"
