from django.core.management.base import BaseCommand
from core.models import Story

class Command(BaseCommand):
    help = 'Populate initial stories'

    def handle(self, *args, **options):
        stories = [
            
        # Dictionary of common words to pre-populate static translations
        # This acts as a fallback for the words in the stories to ensure instant lookup
        COMMON_TRANSLATIONS = {
            # Pronouns
            'я': 'je', 'меня': 'moi/me', 'мне': 'à moi', 'ты': 'tu', 'тебя': 'toi', 'тебе': 'à toi',
            'он': 'il', 'его': 'lui/son', 'она': 'elle', 'её': 'elle/sa', 'мы': 'nous', 'нас': 'nous',
            'вы': 'vous', 'вас': 'vous', 'они': 'ils', 'их': 'eux/leur', 'это': "c'est",
            
            # Verbs (Common forms)
            'зовут': 'appelle', 'есть': 'est/a', 'любит': 'aime', 'работает': 'travaille',
            'живет': 'vit', 'живем': 'vivons', 'хочу': 'veux', 'люблю': 'aime',
            'знаю': 'sais', 'думаю': 'pense', 'говорит': 'parle', 'вижу': 'vois',
            
            # Nouns (Family, People)
            'семья': 'famille', 'мама': 'maman', 'папа': 'papa', 'брат': 'frère', 'сестра': 'sœur',
            'друг': 'ami', 'студент': 'étudiant', 'врач': 'médecin', 'учитель': 'enseignant',
            'человек': 'personne', 'люди': 'gens', 'дом': 'maison', 'город': 'ville',
            
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

        # Enhanced stories with translations
        updated_stories = []
        
        # Helper to generate word map
        def generate_glossary(text):
            words = text.lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '').split()
            glossary = {}
            for w in words:
                if w in COMMON_TRANSLATIONS:
                    glossary[w] = COMMON_TRANSLATIONS[w]
                # Add bare-bones identity if easier? No, better to leave empty to fallback or nothing.
            return glossary

        raw_stories = [
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
            },

            # --- NEW BATCH 20 STORIES (5 per level) ---

            # A1 Additional
            {
                'title': 'Мой кот (My Cat)',
                'slug': 'my-cat',
                'difficulty': 'A1',
                'content_russian': """У меня есть кот. Его зовут Барсик.
Барсик очень красивый. Он белый и пушистый.
Он любит спать на диване. Ещё он любит играть с мячом.
Барсик ест рыбу и пьёт молоко. Я очень люблю моего кота.""",
                'content_english': """I have a cat. His name is Barsik.
Barsik is very beautiful. He is white and fluffy.
He likes to sleep on the sofa. He also likes to play with a ball.
Barsik eats fish and drinks milk. I love my cat very much."""
            },
            {
                'title': 'В парке (In the Park)',
                'slug': 'in-the-park',
                'difficulty': 'A1',
                'content_russian': """Сегодня хорошая погода. Я иду в парк.
В парке много людей. Они гуляют и отдыхают.
Дети играют на плошадке. Птицы поют песни.
Я сижу на скамейке и читаю книгу.
Мне нравится этот парк. Здесь очень тихо и красиво.""",
                'content_english': """Today the weather is good. I am going to the park.
There are many people in the park. They are walking and relaxing.
Children are playing on the playground. Birds are singing songs.
I am sitting on a bench and reading a book.
I like this park. It is very quiet and beautiful here."""
            },
            {
                'title': 'Мой дом (My House)',
                'slug': 'my-house',
                'difficulty': 'A1',
                'content_russian': """Это мой дом. Он маленький, но уютный.
Здесь есть кухня, спальня и гостиная.
На столе стоит ваза с цветами. На стене висит картина.
Моя комната светлая. Я там учу русский язык.
Я люблю быть дома.""",
                'content_english': """This is my house. It is small but cozy.
There is a kitchen, a bedroom and a living room.
There is a vase with flowers on the table. There is a picture hanging on the wall.
My room is bright. I study Russian there.
I like being at home."""
            },
            {
                'title': 'В магазине одежды (In the Clothing Store)',
                'slug': 'clothing-store',
                'difficulty': 'A1',
                'content_russian': """— Здравствуйте! У вас есть джинсы?
— Да, конечно. Какой у вас размер?
— Мой размер 42.
— Вот эти синие джинсы. Померяйте, пожалуйста.
— Спасибо. Они мне нравятся. Сколько они стоят?
— Две тысячи рублей.""",
                'content_english': """— Hello! Do you have jeans?
— Yes, of course. What is your size?
— My size is 42.
— Here are these blue jeans. Try them on, please.
— Thank you. I like them. How much do they cost?
— Two thousand rubles."""
            },
            {
                'title': 'Мой друг (My Friend)',
                'slug': 'my-friend-a1',
                'difficulty': 'A1',
                'content_russian': """Это Антон. Он мой лучший друг.
Антону двадцать пять лет. Он высокий и сильный.
Он любит футбол и кино. Мы часто гуляем вместе.
Антон работает в банке. Он очень умный.
Я рад, что у меня есть такой друг.""",
                'content_english': """This is Anton. He is my best friend.
Anton is twenty-five years old. He is tall and strong.
He likes football and cinema. We often walk together.
Anton works in a bank. He is very smart.
I am glad that I have such a friend."""
            },

            # A2 Additional
            {
                'title': 'Выходные на даче (Weekend at the Dacha)',
                'slug': 'weekend-dacha',
                'difficulty': 'A2',
                'content_russian': """В прошлые выходные мы ездили на дачу.
Дача находится недалеко от Москвы, в лесу.
Мы собирали грибы и ягоды. Вечером мы делали шашлык.
Было очень весело. Мы пели песни и играли на гитаре.
В воскресенье мы поехали домой уставшие, но счастливые.""",
                'content_english': """Last weekend we went to the dacha.
The dacha is located not far from Moscow, in the forest.
We picked mushrooms and berries. In the evening we made shashlik (barbecue).
It was very fun. We sang songs and played the guitar.
On Sunday we went home tired but happy."""
            },
            {
                'title': 'Моя учёба (My Studies)',
                'slug': 'my-studies',
                'difficulty': 'A2',
                'content_russian': """Я учусь в университете на факультете истории.
Учёба трудная, но интересная. У нас много лекций и семинаров.
Скоро у меня будут экзамены. Я должен много читать.
Мой любимый предмет — история России.
После университета я хочу работать в музее.""",
                'content_english': """I study at the university at the faculty of history.
Studying is difficult but interesting. We have many lectures and seminars.
Soon I will have exams. I must read a lot.
My favorite subject is Russian history.
After university I want to work in a museum."""
            },
            {
                'title': 'Поход в театр (Trip to the Theater)',
                'slug': 'trip-theater',
                'difficulty': 'A2',
                'content_russian': """Вчера я ходил в Большой театр. Мы смотрели балет "Лебединое озеро".
Театр очень красивый внутри. Там много золота и света.
Балерины танцевали прекрасно. Музыка была волшебной.
В антракте мы пили шампанское в буфете.
Это был незабываемый вечер.""",
                'content_english': """Yesterday I went to the Bolshoi Theater. We watched the ballet "Swan Lake".
The theater is very beautiful inside. There is a lot of gold and light.
The ballerinas danced beautifully. The music was magical.
In the intermission we drank champagne in the buffet.
It was an unforgettable evening."""
            },
            {
                'title': 'Письмо другу (Letter to a Friend)',
                'slug': 'letter-friend',
                'difficulty': 'A2',
                'content_russian': """Привет, Дима! Как твои дела?
Я сейчас в отпуске. Я отдыхаю в Сочи.
Здесь тепло и солнечно. Я каждый день плаваю в море.
Вчера я ездил на экскурсию в горы. Вид был потрясающий.
Я привезу тебе сувенир. До встречи!""",
                'content_english': """Hi Dima! How are you?
I am on vacation now. I am relaxing in Sochi.
It is warm and sunny here. I swim in the sea every day.
Yesterday I went on an excursion to the mountains. The view was amazing.
I will bring you a souvenir. See you!"""
            },
            {
                'title': 'Покупка подарка (Buying a Gift)',
                'slug': 'buying-gift',
                'difficulty': 'A2',
                'content_russian': """Завтра у мамы день рождения. Я ищу подарок.
Я был в торговом центре, но ничего не купил.
Может быть, купить ей книгу? Она любит читать романы.
Или красивые цветы? Розы или тюльпаны.
Я думаю, лучше всего купить большой торт и цветы.""",
                'content_english': """Tomorrow is Mom's birthday. I am looking for a gift.
I was at the mall but didn't buy anything.
Maybe buy her a book? She likes reading novels.
Or beautiful flowers? Roses or tulips.
I think it is best to buy a big cake and flowers."""
            },

            # B1 Additional
            {
                'title': 'Традиции гостеприимства (Traditions of Hospitality)',
                'slug': 'hospitality',
                'difficulty': 'B1',
                'content_russian': """В России очень важны традиции гостеприимства.
Если вас пригласили в гости, нельзя приходить с пустыми руками.
Обычно гости приносят торт, конфеты или вино.
Хозяева всегда готовят много еды. Стол должен быть полным.
Русские люди любят сидеть на кухне и разговаривать о жизни до поздней ночи.""",
                'content_english': """In Russia, traditions of hospitality are very important.
If you are invited to visit, you cannot come empty-handed.
Usually guests bring a cake, sweets (candy) or wine.
Hosts always cook a lot of food. The table must be full.
Russian people love sitting in the kitchen and talking about life until late at night."""
            },
            {
                'title': 'Жизнь в мегаполисе (Life in a Metropolis)',
                'slug': 'metropolis-life',
                'difficulty': 'B1',
                'content_russian': """Жизнь в большом городе имеет свои плюсы и минусы.
С одной стороны, здесь много работы, развлечений и возможностей.
С другой стороны, плохая экология, шум и пробки на дорогах.
Люди в мегаполисе всегда спешат и часто испытывают стресс.
Однако ритм большого города заряжает энергией и мотивирует развиваться.""",
                'content_english': """Life in a big city has its pros and cons.
On the one hand, there is a lot of work, entertainment and opportunities.
On the other hand, bad ecology, noise and traffic jams.
People in a metropolis are always in a hurry and often experience stress.
However, the rhythm of a big city recharges with energy and motivates to develop."""
            },
            {
                'title': 'Моё хобби - Фотография (My Hobby - Photography)',
                'slug': 'photography-hobby',
                'difficulty': 'B1',
                'content_russian': """Я увлекаюсь фотографией уже пять лет.
Мне нравится ловить моменты и сохранять их на память.
Я люблю снимать природу, особенно закаты и рассветы.
Недавно я купил новую камеру и теперь учусь обрабатывать фото.
Моя мечта — организовать свою собственную выставку фотографий.""",
                'content_english': """I have been into photography for five years already.
I like catching moments and saving them as a memory.
I like shooting nature, especially sunsets and sunrises.
Recently I bought a new camera and now I am learning to process photos.
My dream is to organize my own photo exhibition."""
            },
            {
                'title': 'Праздник Масленица (Maslenitsa Holiday)',
                'slug': 'maslenitsa',
                'difficulty': 'B1',
                'content_russian': """Масленица — это весёлый праздник проводов зимы.
Он длится целую неделю перед Великим постом.
Главный символ Масленицы — это блины, которые символизируют солнце.
Люди гуляют на улице, сжигают чучело зимы и радуются весне.
Это время, когда нужно прощать обиды и мириться с близкими.""",
                'content_english': """Maslenitsa is a fun holiday of seeing off winter.
It lasts a whole week before the Great Lent.
The main symbol of Maslenitsa is pancakes (blini), which symbolize the sun.
People walk outside, burn the effigy of winter and rejoice at spring.
This is a time when one needs to forgive offenses and make up with loved ones."""
            },
            {
                'title': 'Изучение языков (Learning Languages)',
                'slug': 'learning-languages',
                'difficulty': 'B1',
                'content_russian': """Изучение иностранного языка открывает двери в новый мир.
Это не только грамматика и слова, но и культура другого народа.
Самое трудное — начать говорить и не бояться делать ошибки.
Регулярная практика — ключ к успеху. Нужно слушать, читать и говорить каждый день.
Знание языков помогает путешествовать и находить друзей по всему миру.""",
                'content_english': """Learning a foreign language opens doors to a new world.
It's not just grammar and words, but also the culture of another people.
The hardest thing is to start speaking and not be afraid of making mistakes.
Regular practice is the key to success. You need to listen, read and speak every day.
Knowledge of languages helps to travel and find friends all over the world."""
            },

            # B2 Additional
            {
                'title': 'Глобализация (Globalization)',
                'slug': 'globalization',
                'difficulty': 'B2',
                'content_russian': """Глобализация — это процесс объединения мира в единую систему.
Благодаря интернету и транспорту границы стираются.
Мы можем общаться с людьми на другом конце света за секунды.
Однако глобализация угрожает культурному разнообразию.
Маленькие языки и традиции могут исчезнуть под влиянием массовой культуры.
Важно сохранять свою уникальность, будучи частью глобального мира.""",
                'content_english': """Globalization is the process of uniting the world into a single system.
Thanks to the internet and transport, borders are being erased.
We can communicate with people on the other side of the world in seconds.
However, globalization threatens cultural diversity.
Small languages and traditions may disappear under the influence of mass culture.
It is important to preserve one's uniqueness while being part of a global world."""
            },
            {
                'title': 'Литература Золотого Века (Golden Age Literature)',
                'slug': 'golden-age-lit',
                'difficulty': 'B2',
                'content_russian': """XIX век называют Золотым веком русской литературы.
В это время творили Пушкин, Лермонтов, Гоголь, Толстой и Достоевский.
Их произведения поднимают вечные философские вопросы о добре и зле.
Язык классической литературы богат, выразителен и сложен.
Чтение классики в оригинале позволяет глубже понять русскую душу.""",
                'content_english': """The 19th century is called the Golden Age of Russian literature.
At this time Pushkin, Lermontov, Gogol, Tolstoy and Dostoevsky created (worked).
Their works raise eternal philosophical questions about good and evil.
The language of classical literature is rich, expressive and complex.
Reading classics in the original allows one to understand the Russian soul deeper."""
            },
            {
                'title': 'Космические исследования (Space Exploration)',
                'slug': 'space-exploration',
                'difficulty': 'B2',
                'content_russian': """Россия имеет богатую историю освоения космоса.
Полёт Юрия Гагарина в 1961 году стал поворотным моментом в истории человечества.
Сегодня учёные разрабатывают проекты колонизации Марса и Луны.
Космические технологии помогают нам в повседневной жизни (спутниковая связь, GPS).
Несмотря на риски, стремление человека к звёздам остаётся неизменным.""",
                'content_english': """Russia has a rich history of space exploration.
Yuri Gagarin's flight in 1961 became a turning point in history of humanity.
Today scientists are developing projects for colonization of Mars and the Moon.
Space technologies help us in everyday life (satellite communication, GPS).
Despite the risks, man's striving for the stars remains unchanged."""
            },
            {
                'title': 'Психология успеха (Psychology of Success)',
                'slug': 'psychology-success',
                'difficulty': 'B2',
                'content_russian': """Что такое успех? Для кого-то это карьера, для кого-то — семья.
Психологи утверждают, что уверенность в себе играет ключевую роль.
Неудачи — это не конец, а возможность научиться чему-то новому.
Важно ставить реалистичные цели и двигаться к ним шаг за шагом.
Настоящий успех приносит не только деньги, но и внутреннее удовлетворение.""",
                'content_english': """What is success? For someone it is career, for someone — family.
Psychologists claim that self-confidence plays a key role.
Failures are not the end, but an opportunity to learn something new.
It is important to set realistic goals and move towards them step by step.
True success brings not only money, but also inner satisfaction."""
            },
            {
                'title': 'Виртуальная реальность (Virtual Reality)',
                'slug': 'virtual-reality',
                'difficulty': 'B2',
                'content_russian': """Виртуальная реальность (VR) всё больше проникает в нашу жизнь.
Она используется не только в играх, но и в обучении, медицине и архитектуре.
С помощью VR можно посетить музей в другой стране, не выходя из дома.
Однако чрезмерное погружение в виртуальный мир может привести к изоляции.
Технологии должны дополнять реальность, а не заменять её полностью.""",
                'content_english': """Virtual reality (VR) is penetrating our life more and more.
It is used not only in games, but also in education, medicine and architecture.
With the help of VR one can visit a museum in another country without leaving home.
However, excessive immersion in the virtual world can lead to isolation.
Technologies must complement reality, not replace it completely."""
            },
        ]

        for s in raw_stories:
            # Generate static glossary
            glossary = generate_glossary(s['content_russian'])
            
            story, created = Story.objects.get_or_create(
                slug=s['slug'],
                defaults={
                    'title': s['title'],
                    'difficulty': s['difficulty'],
                    'content_russian': s['content_russian'],
                    'content_english': s['content_english'],
                    'word_translations': glossary
                }
            )
            if not created:
                # Update with glossary if existing
                story.word_translations = glossary
                story.save()
                self.stdout.write(f"Updated story: {s['title']}")
            else:
                self.stdout.write(self.style.SUCCESS(f"Created story: {s['title']}"))
