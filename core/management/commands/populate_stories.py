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
            # Level A2 (Adding 4 more -> Total 5)
            {
                'title': 'Мой любимый фильм (My favorite movie)',
                'slug': 'favorite-movie',
                'difficulty': 'A2',
                'content_russian': """Мой любимый фильм — это старая советская комедия.
Я смотрел его много раз. Он очень смешной и добрый.
Там играют известные актёры. Сюжет простой, но интересный.
Мы часто смотрим этот фильм всей семьёй на Новый год.
Я люблю этот фильм, потому что он напоминает мне о детстве.""",
                'content_english': """My favorite movie is an old Soviet comedy.
I watched it many times. It is very funny and kind.
Famous actors play there. The plot is simple but interesting.
We often watch this movie with the whole family on New Year.
I love this movie because it reminds me of my childhood."""
            },
            {
                'title': 'В ресторане (At the restaurant)',
                'slug': 'at-the-restaurant',
                'difficulty': 'A2',
                'content_russian': """Вчера мы были в ресторане. Мы праздновали день рождения друга.
Ресторан был очень уютный. Там играла тихая музыка.
Мы заказали пиццу, салат и вино. Еда была вкусная.
Официант был вежливый и быстрый.
Мы много разговаривали и смеялись. Это был отличный вечер.""",
                'content_english': """Yesterday we were at a restaurant. We celebrated a friend's birthday.
The restaurant was very cozy. Quiet music was playing there.
We ordered pizza, salad and wine. The food was delicious.
The waiter was polite and fast.
We talked and laughed a lot. It was a great evening."""
            },
            {
                'title': 'Планы на лето (Plans for summer)',
                'slug': 'summer-plans',
                'difficulty': 'A2',
                'content_russian': """Скоро будет лето. Я хочу поехать на море.
Я люблю плавать и загорать. Я хочу жить в отеле рядом с пляжем.
Мои друзья хотят поехать в горы. Они любят ходить в походы.
Мы ещё не решили, куда поедем. Может быть, мы разделимся.
Главное — это хорошо отдохнуть.""",
                'content_english': """Soon it will be summer. I want to go to the sea.
I like to swim and sunbathe. I want to live in a hotel near the beach.
My friends want to go to the mountains. They like hiking.
We haven't decided where we will go yet. Maybe we will split up.
The main thing is to have a good rest."""
            },
            {
                'title': 'Моя квартира (My apartment)',
                'slug': 'my-apartment',
                'difficulty': 'A2',
                'content_russian': """Я живу в маленькой квартире. Там есть одна комната и кухня.
В комнате стоит диван, стол и телевизор. На окне стоят цветы.
Кухня светлая и удобная. Я люблю готовить там завтрак.
У меня нет балкона, но есть большие окна.
Мне нравится мой дом, потому что он уютный.""",
                'content_english': """I live in a small apartment. There is one room and a kitchen.
In the room there is a sofa, a table and a TV. There are flowers on the window.
The kitchen is bright and comfortable. I like to cook breakfast there.
I do not have a balcony, but have big windows.
I like my home because it is cozy."""
            },

            # Level B1 (Adding 4 more -> Total 5)
            {
                'title': 'Путешествие на поезде (Train Travel)',
                'slug': 'train-travel',
                'difficulty': 'B1',
                'content_russian': """Путешествовать на поезде по России — это особое приключение.
Расстояния огромные, и поездка может длиться несколько дней.
В поезде люди часто знакомятся и пьют чай из стаканов с подстаканниками.
Можно смотреть в окно на леса, поля и деревни.
Многие иностранцы мечтают проехать по Транссибирской магистрали.
Это уникальный шанс увидеть настоящую Россию.""",
                'content_english': """Traveling by train in Russia is a special adventure.
Distances are huge, and the trip can last several days.
In the train, people often meet and drink tea from glasses with glass holders.
You can look out the window at forests, fields and villages.
Many foreigners dream of traveling on the Trans-Siberian Railway.
This is a unique chance to see real Russia."""
            },
            {
                'title': 'Спорт в моей жизни (Sport in my life)',
                'slug': 'sport-life',
                'difficulty': 'B1',
                'content_russian': """Я стараюсь вести здоровый образ жизни.
Два раза в неделю я хожу в спортзал. Я бегаю на дорожке и поднимаю гантели.
Летом я люблю кататься на велосипеде в парке. Это помогает мне расслабиться.
Зимой я иногда катаюсь на лыжах, хотя это трудно.
Спорт даёт мне энергию и хорошее настроение. Я считаю, что движение — это жизнь.""",
                'content_english': """I try to lead a healthy lifestyle.
Twice a week I go to the gym. I run on the treadmill and lift dumbbells.
In summer I like to ride a bike in the park. It helps me relax.
In winter I sometimes go skiing, although it is difficult.
Sport gives me energy and a good mood. I believe that movement is life."""
            },
            {
                'title': 'Москвы не сразу строилась (Moscow wasn\'t built in a day)',
                'slug': 'moscow-history',
                'difficulty': 'B1',
                'content_russian': """Москва — древний город с богатой историей.
Она была основана Юрием Долгоруким в 1147 году.
Кремль — это сердце Москвы. Раньше он был деревянным, а сейчас кирпичный.
Город пережил много пожаров и войн, но всегда восстанавливался.
Сегодня Москва — это огромный мегаполис, который никогда не спит.
Здесь старинные церкви стоят рядом с небоскрёбами.""",
                'content_english': """Moscow is an ancient city with a rich history.
It was founded by Yuri Dolgorukiy in 1147.
The Kremlin is the heart of Moscow. Previously it was wooden, and now is brick.
The city survived many fires and wars, but always recovered.
Today Moscow is a huge metropolis that never sleeps.
Here ancient churches stand next to skyscrapers."""
            },
            {
                'title': 'Русская кухня (Russian Cuisine)',
                'slug': 'russian-cuisine',
                'difficulty': 'B1',
                'content_russian': """Русская кухня очень сытная и разнообразная.
Самое известное блюдо — это борщ. Это суп из свёклы, капусты и мяса.
Ещё русские любят блины. Их едят с маслом, икрой или сметаной.
Пельмени — это тоже популярное блюдо, похожее на равиоли.
Традиционные напитки — это квас и морс.
Если вы приедете в Россию, обязательно попробуйте пирожки.""",
                'content_english': """Russian cuisine is very hearty and varied.
The most famous dish is borsch. It is a soup made of beets, cabbage and meat.
Russians also like pancakes (blini). They are eaten with butter, caviar or sour cream.
Pelmeni is also a popular dish, similar to ravioli.
Traditional drinks are kvas and mors.
If you come to Russia, be sure to try pirozhki."""
            },

            # Level B2 (Adding 4 more -> Total 5)
            {
                'title': 'Экологические проблемы (Environmental Issues)',
                'slug': 'ecology',
                'difficulty': 'B2',
                'content_russian': """Загрязнение окружающей среды — одна из главных проблем современности.
Мы используем слишком много пластика, который загрязняет океаны.
Изменение климата приводит к таянию ледников и повышению уровня моря.
Необходимо переходить на возобновляемые источники энергии, такие как солнце и ветер.
Каждый человек может внести свой вклад, сортируя мусор и экономя воду.
Мы ответственны за планету, которую оставим нашим детям.""",
                'content_english': """Environmental pollution is one of the main problems of our time.
We use too much plastic, which pollutes the oceans.
Climate change leads to melting glaciers and rising sea levels.
It is necessary to switch to renewable energy sources, such as sun and wind.
Every person can contribute by sorting garbage and saving water.
We are responsible for the planet we leave to our children."""
            },
            {
                'title': 'Образование онлайн (Online Education)',
                'slug': 'online-education',
                'difficulty': 'B2',
                'content_russian': """Пандемия изменила наш подход к обучению.
Онлайн-курсы стали невероятно популярны во всём мире.
Это удобно, так как можно учиться в любое время и в любом месте.
Однако дистанционное обучение требует высокой самодисциплины.
Многим студентам не хватает живого общения с преподавателями и одногруппниками.
Вероятно, будущее за гибридным форматом, который объединяет лучшее из обоих миров.""",
                'content_english': """The pandemic has changed our approach to learning.
Online courses have become incredibly popular all over the world.
It is convenient, as you can study anytime and anywhere.
However, distance learning requires high self-discipline.
Many students lack live communication with teachers and classmates.
Probably, the future belongs to a hybrid format that combines the best of both worlds."""
            },
            {
                'title': 'Искусство и культура (Art and Culture)',
                'slug': 'art-culture',
                'difficulty': 'B2',
                'content_russian': """Русская литература и музыка известны во всём мире.
Произведения Толстого и Достоевского заставляют задуматься о смысле жизни.
Музыка Чайковского и Рахманинова трогает сердца слушателей.
Русский балет считается одним из лучших в мире.
Искусство помогает нам понять друг друга и преодолеть культурные барьеры.
Посещение музеев и театров обогащает наш внутренний мир.""",
                'content_english': """Russian literature and music are famous all over the world.
The works of Tolstoy and Dostoevsky make one think about the meaning of life.
The music of Tchaikovsky and Rachmaninoff touches the hearts of listeners.
Russian ballet is considered one of the best in the world.
Art helps us understand each other and overcome cultural barriers.
Visiting museums and theaters enriches our inner world."""
            },
            {
                'title': 'Работа и карьера (Work and Career)',
                'slug': 'work-career',
                'difficulty': 'B2',
                'content_russian': """Выбор профессии — это важное решение в жизни каждого человека.
Раньше люди часто работали на одном месте всю жизнь.
Сейчас ситуация изменилась: люди чаще меняют работу и ищут новые возможности.
Важно постоянно учиться и развивать новые навыки (soft skills).
Умение работать в команде и адаптироваться к изменениям ценится работодателями.
Успешная карьера требует не только знаний, но и настойчивости.""",
                'content_english': """Choosing a profession is an important decision in every person's life.
Previously, people often worked in one place all their lives.
Now the situation has changed: people change jobs more often and look for new opportunities.
It is important to constantly learn and develop new skills (soft skills).
The ability to work in a team and adapt to changes is valued by employers.
A successful career requires not only knowledge, but also perseverance."""
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
