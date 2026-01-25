from django.db import migrations

def migrate_word_data(apps, schema_editor):
    Word = apps.get_model('core', 'Word')
    for word in Word.objects.all():
        # Migrate base content
        word.base_form = word.russian
        word.text_root = word.russian
        
        # English specific migration
        if word.language == 'en':
            word.past_tense = word.russian_accented
        
        word.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_target_language_word_language_word_aspect_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_word_data),
    ]
