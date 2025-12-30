from django.core.management.base import BaseCommand
from core.models import Story

class Command(BaseCommand):
    help = 'Populate initial stories'

    def handle(self, *args, **options):
        stories = [
            {
                'title': 'Моя семья (My Family)',
                'slug': 'my-family',
                'difficulty': 'A1',
                'content_russian': """Меня зовут Иван. Я студент. Мне двадцать лет.
У меня большая семья. Это мой отец. Его зовут Борис. Он врач. Он работает в больнице.
Это моя мать. Её зовут Анна. Она учительница. Она работает в школе.
У меня есть брат и сестра. Мой брат — инженер, а моя сестра — студентка.
Мы живём в Москве. Наш дом большой и красивый.
В выходные мы часто гуляем в парке. Мы любим спорт и музыку.""",
                'content_english': """My name is Ivan. I am a student. I am twenty years old.
I have a big family. This is my father. His name is Boris. He is a doctor. He works in a hospital.
This is my mother. Her name is Anna. She is a teacher. She works in a school.
I have a brother and a sister. My brother is an engineer, and my sister is a student.
We live in Moscow. Our house is big and beautiful.
On weekends we often walk in the park. We love sports and music."""
            },
            {
                'title': 'В кофейне (In the coffee shop)',
                'slug': 'coffee-shop',
                'difficulty': 'A1',
                'content_russian': """— Здравствуйте!
— Здравствуйте! Что вы хотите?
— Я хочу кофе с молоком и круассан, пожалуйста.
— Большой или маленький кофе?
— Большой, пожалуйста.
— Сахар нужен?
— Да, два сахара.
— Хорошо. С вас 350 рублей.
— Вот, пожалуйста.
— Спасибо. Ваш кофе будет готов через минуту.
— Спасибо!""",
                'content_english': """— Hello!
— Hello! What do you want?
— I want coffee with milk and a croissant, please.
— Big or small coffee?
— Big, please.
— Do you need sugar?
— Yes, two sugars.
— Okay. That will be 350 rubles.
— Here you go.
— Thank you. Your coffee will be ready in a minute.
— Thank you!"""
            },
            {
                'title': 'На рынке (At the market)',
                'slug': 'at-the-market',
                'difficulty': 'A1',
                'content_russian': """— Добрый день! Сколько стоят эти яблоки?
— Добрый день! Яблоки стоят сто рублей за килограмм.
— Они свежие?
— Да, очень свежие и сладкие. Попробуйте!
— Спасибо. Вкусные. Дайте, пожалуйста, два килограмма.
— Что-нибудь ещё?
— Да, мне нужны помидоры и огурцы.
— Помидоры — двести рублей, огурцы — сто пятьдесят.
— Хорошо. Килограмм помидоров и килограмм огурцов.
— Вот ваши продукты. С вас 550 рублей.""",
                'content_english': """— Good afternoon! How much are these apples?
— Good afternoon! The apples cost one hundred rubles per kilogram.
— Are they fresh?
— Yes, very fresh and sweet. Try one!
— Thank you. Delicious. Give me two kilograms, please.
— Anything else?
— Yes, I need tomatoes and cucumbers.
— Tomatoes are two hundred rubles, cucumbers are one hundred fifty.
— Okay. A kilogram of tomatoes and a kilogram of cucumbers.
— Here are your groceries. That will be 550 rubles."""
            },
            {
                'title': 'Мой день (My day)',
                'slug': 'my-day',
                'difficulty': 'A1',
                'content_russian': """Я обычно встаю в семь часов утра.
Сначала я иду в душ и чищу зубы. Потом я завтракаю.
На завтрак я ем кашу и пью чай.
В восемь часов я иду на работу. Я работаю в офисе.
Я работаю много, но мне нравится моя работа.
В час дня у меня обед. Я люблю есть суп и салат.
Вечером я иду домой. Я ужинаю, читаю книгу или смотрю телевизор.
Я ложусь спать в одиннадцать часов.""",
                'content_english': """I usually get up at seven o'clock in the morning.
First I go to the shower and brush my teeth. Then I have breakfast.
For breakfast I eat porridge and drink tea.
At eight o'clock I go to work. I work in an office.
I work a lot, but I like my job.
At one o'clock in the afternoon I have lunch. I like to eat soup and salad.
In the evening I go home. I have dinner, read a book or watch TV.
I go to bed at eleven o'clock."""
            },
            {
                'title': 'Знакомство (Meeting)',
                'slug': 'meeting',
                'difficulty': 'A1',
                'content_russian': """— Привет! Меня зовут Саша. А тебя?
— Привет! Меня зовут Маша. Очень приятно.
— Мне тоже. Ты учишься или работаешь?
— Я студентка. Я учусь в университете. А ты?
— Я работаю программистом.
— Интересно! Ты любишь свою работу?
— Да, очень. А что ты изучаешь?
— Я изучаю историю.
— Здорово. Давай выпьем кофе?
— Давай!""",
                'content_english': """— Hi! My name is Sasha. And you?
— Hi! My name is Masha. Nice to meet you.
— Me too. Do you study or work?
— I am a student. I study at the university. And you?
— I work as a programmer.
— Interesting! Do you like your job?
— Yes, very much. And what do you study?
— I study history.
— Cool. Let's have some coffee?
— Let's!"""
            },
            # Level A2
            {
                'title': 'Поездка в Санкт-Петербург (Trip to St. Petersburg)',
                'slug': 'trip-to-spb',
                'difficulty': 'A2',
                'content_russian': """В прошлом году я ездил в Санкт-Петербург. Это очень красивый город.
Я был там летом, когда были белые ночи. Было светло даже ночью!
Мы много гуляли по центру города. Мы видели Эрмитаж, Невский проспект и Петропавловскую крепость.
Мне очень понравились каналы и мосты. Мы катались на лодке по реке Неве.
Погода была хорошая, но иногда шёл дождь. В Санкт-Петербурге часто идёт дождь.
Я купил сувениры для моей семьи. Я хочу поехать туда снова.""",
                'content_english': """Last year I went to St. Petersburg. It is a very beautiful city.
I was there in summer when there were white nights. It was light even at night!
We walked a lot in the city center. We saw the Hermitage, Nevsky Prospect and the Peter and Paul Fortress.
I really liked the canals and bridges. We took a boat ride on the Neva River.
The weather was good, but sometimes it rained. It often rains in St. Petersburg.
I bought souvenirs for my family. I want to go there again."""
            },
            # Level B1
            {
                'title': 'Русская зима (Russian Winter)',
                'slug': 'russian-winter',
                'difficulty': 'B1',
                'content_russian': """Все говорят, что русская зима очень холодная. И это правда.
Но зима в России — это также очень красивое время года. Всё вокруг белое от снега.
Дети любят зиму, потому что можно кататься на санках, лыжах и коньках.
Многие люди ездят на дачу, чтобы отдохнуть на природе. Там они топят баню и пьют горячий чай с мёдом.
Самый главный праздник зимой — это Новый год. Россияне готовят много вкусной еды, например, салат Оливье.
Они украшают ёлку и дарят друг другу подарки. В полночь бьют куранты на Красной площади.""",
                'content_english': """Everyone says that the Russian winter is very cold. And it's true.
But winter in Russia is also a very beautiful time of the year. Everything around is white with snow.
Children love winter because they can go sledding, skiing and skating.
Many people go to their dacha to relax in nature. There they heat the banya and drink hot tea with honey.
The most important holiday in winter is New Year. Russians cook a lot of delicious food, for example, Olivier salad.
They decorate the Christmas tree and give each other gifts. At midnight the chimes strike on Red Square."""
            },
            # Level B2
            {
                'title': 'Технологии и будущее (Technology and Future)',
                'slug': 'tech-future',
                'difficulty': 'B2',
                'content_russian': """В современном мире технологии развиваются с невероятной скоростью.
Влияние искусственного интеллекта на нашу жизнь становится всё более заметным.
С одной стороны, это открывает перед человечеством огромные возможности: автоматизация рутинных задач, улучшение медицины и образования.
С другой стороны, возникают этические вопросы и опасения по поводу потери рабочих мест.
Многие эксперты спорят о том, сможет ли компьютер когда-нибудь полностью заменить человека.
Важно найти баланс между технологическим прогрессом и сохранением человеческих ценностей.
Мы должны учиться адаптироваться к изменениям и использовать технологии во благо общества.""",
                'content_english': """In the modern world, technologies are developing at an incredible speed.
The influence of artificial intelligence on our life is becoming more and more noticeable.
On the one hand, this opens up huge opportunities for humanity: automation of routine tasks, improvement of medicine and education.
On the other hand, ethical questions and concerns about job losses arise.
Many experts argue about whether a computer will ever be able to completely replace a human.
It is important to find a balance between technological progress and the preservation of human values.
We must learn to adapt to changes and use technologies for the benefit of society."""
            }
        ]

        for s in stories:
            story, created = Story.objects.get_or_create(
                slug=s['slug'],
                defaults={
                    'title': s['title'],
                    'difficulty': s['difficulty'],
                    'content_russian': s['content_russian'],
                    'content_english': s['content_english']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created story: {s['title']}"))
            else:
                self.stdout.write(f"Story already exists: {s['title']}")
