import time
name = input('Привіт, ти потрапив в гру про заборонену зону. \n Як тебе звуть? \n')
print('Початок!\n Ти опинився в забороненій зоні')
start = input('Що будеш робити? \n 1) Піти прямо до найближщого будинку, здається він закинутий. \n 2) Спробувати вибратися, але тут усюди забор. \n 3) Піти в місто. \n')
if start == '1':
    print('Хм, тут і правда нікого немає. Ти знайшов ліхтарик і трішки їжи')
    i = 'flashlight, 3food'
    next = input('Що далі? \n 1) Тут є підвал, може там щось є? \n 2) Піти в інший будинок. \n 3) Піти в ліс. \n')
    if next == '2':
        print('Нажаль більше будинків немає, але тут ти знайшов автомат і трішки патронів')
        i = 'flashlight, 3food, machine_gun, 4ammunition'
        next = input('Вже доволі темно, що робити?\n 1) Піти в місто. \n 2) Піти в ліс. \n 3) Піти шукати підвал де можно переночувати. \n 4) Залишитися в цьому будинку і переночувати. \n')
        if next == '4':
            print('Молодець, тут все ж таки безпечніше. Хто його знає щоб було далі?!')
            next = input('Ніч була тихою, вже ранок. Теперь треба рухатися кудись далі, куда підеш? \n 1) Піти в місто. \n 2) Піти в ліс. \n')
            if next == '1':
                print('Ти в місті, ти бачишь дуже багато будинків. Майже на всіх замки і ти не маєшь інструмент щоб зламати їх.')
                next = input("Ти можеш піти в три п'яти поверхових будинки, який обереш? \n Перший; \n Другий; \n Третій \n")
                if next == '3':
                    print('В цьому будинки нікого немає, в інших двух я чув якісь розмови.В цьому будинку ти знайшов трішки їжи, а також пару сигарет.')
                    i = 'flashlight, 7food, machine_gun, 4ammunition, 2cigarettes'
                    next = input(' Ти бачишь не велику лікарню не далеко, але не дуже зрозуміло чи є хтось там. Йдемо туди?! \n')
                    if next == 'Ні':
                        print('Ну і правильно, якщо придивитися я бачив там бандитів, і я не думаю что їхня банда дуже дружелюбна.')
                        next = input('Куди піти? \n 1) супермакрет, \n 2) закинутий парк розваг, \n 3) маленький магазнчик \n ')
                        if next == '1':
                            print('Це доволі великий супермаркет, тут є багото всього. Я знайшов тут сокиру и їжу.')
                            i = 'flashlight, 15food, machine_gun, 4ammunition, 2cigarettes, axe'
                            food = input('Я втомивсля і хочу їсти. \n 1) Поїсти \n 2) Не їсти \n')
                            if food == '1':
                                print('-2 Їжи')
                                i = 'flashlight, 13food, machine_gun, 4ammunition, 2cigarettes, axe'
                                print('Дякую, була дуже смачно.')
                                next = input('Куди йдемо далі? \n 1) Піти ходити по місту. \n 2) Маленький магазинчик не подалік. \n')
                                if next == '2':
                                    print('Думаю це правильне рішення, в місті може бути доволі не безпечно. Тут нічого немає, крім однієї кирки')
                                    i = 'flashlight, 13food, machine_gun, 4ammunition, 2cigarettes, axe, pick'
                                    next = input('Я бачу якусь жінку біля магазинчику, мені вона здається дружелюбною. Може підійдемо поговорити з нею? \n 1) Підійти для розмови \n 2) Вийти через пожежний вихід і втікти. \n')
                                    if next == '1':
                                        print(f"Хм, вона і в правду дружелюбна але вона якась дивна... \n Дівчина: Привіт, стій там де стоїш. Ти хто, кажи швидко?! \n Я: Я, я {name}, я не пам'ятаю як я тут опинився, але я хочу втікти звідси.")
                                        next = input(' Дівчина: Ох, ти теж тут новенький. Я вже тут давно і я також планую втікти звідси. Не хочешь зі мной?   ')
                                        if next == 'Давай':
                                            print('Добре, що ті із собой маєшь що може нами може допомогти втікти звідси')
                                            next = input(f'Я маю:{i}, але що нам допоможе втікти звідси?   ')
                                            if next == 'axe, pick':
                                                print('Дівчина: Так, я думаю це нам допоможе. Я тут не далеко бачила місце де найменьше всього бандитів. Ну і до того ж там стіна тонша, я думаю раніше там вже пробували втіки, але чомусь не вдалось.')
                                                next = input(' Давай тепер спробуємо ми?!   ')
                                                if next == 'Давай':
                                                    print(' Дівчина: Чудово, ходім зі мной я тобі покажу це місце.')
                                                    next = input('Піти чи залишитися?  ')
                                                    if next == 'Піти':
                                                        time.sleep(5)
                                                        print('3 годи по тому...')
                                                        time.sleep(3)
                                                        print('Дівчина: Ось то місце, бачишь хтось вже пробував тут втікти. Я не думаю що нам треба підходити ближще без діла. \n Я: Подивись трішки правіше, там 7 бандитів. Ти маєш зброю? \n Дівчина: Звичайно! А ти? \n Я: Так, але я маю всього лише 4 патрони. \n Дівчина: Добре, тоді інших 3 я візьму на себе. \n Я: Добре ')
                                                        time.sleep(3)
                                                        print('Дівчина: Наче все. Дай мені сокиру, а собі бери кирку.')
                                                        next = input('Дати сокиру?!')
                                                        if next == 'Так':
                                                            print('Дівчина: Добре починай ломати!')
                                                            time.sleep(10)
                                                            print('Все готово, ходім, швидше. Я бачу що там на нас бігуть бандити!')
                                                            time.sleep(3)
                                                            print('Молодець, ти пройшов гру. Ти зміг вибратися не зважаючи на всі труднощі! \n Game by Ruslan Sokolets')
if start == '2':
    print('Він занадто високий а також має на собі колючий дріт під напругою. Коли ти на нього ліз тебе вбило від напруги. На жаль ти програв!:(')
if start == '3':
    print('В місті багато бандитів і ти не маєш зброї для оборони. Вони дуже сильно  поранили тебе, але залишили в живих в одному з будинків. Але найближчим часом ти загинув, із-за нестачі медикаментів і швидкої допомоги.')
    if next == '1':
        print("В підвалі були заручники. Вони були заперти бандитами, із-за того що вони були голодні побачивши тебе вони розірвали тебе на частинки і з'їли Ти загинув :(")
    if next == '3':
        print('В лісі були мутовані тварини, вони дуже швидео знайшли тебе і ти загинув.')
        if next == '1':
            print('Вночі по дорозі до міста ти зустрів бвндитів, нажаль ти не встиг знайти зброю і не зміг захищатися і загинув.')
        if next == '2':
            print('Вночі всі мутовані тварини спали. Ті знайшов шалаш в я кому і заночував, але під ранок коли всі прокинулися вони розірвали тебе на частники по ти ще спав.')
        if next == '3':
            print('Ті пішов шукати підвал в сторону міста. Хм, що це?')
            next = input('Мені сдається що це підвал, залишимося тут чи підемо далі? \n ')
            if next == 'Далі':
                print('Ти пройшов ще пару кілометрів і нічого не знайшов')
                next = input('Ти можешь повернутися. Але куди? \n 1) В закинуті будинки \n 2) В закинутий підвал \n ')
                if next == '1':
                    print('Молодець, тат все ж таки безпечніше. Хто його знає щоб було далі?!')
                    next = input(
                        'Ніч була тихою, вже ранок. Теперь треба рухатися кудись далі, куда підеш? \n 1) Піти в місто. \n 2) Піти в ліс. \n')
                    if next == '1':
                        print('Ти в місті, ти бачишь дуже багато будинків. Майже на всіх замки і ти не маєшь інструмент щоб зламати їх.')
                        next = input("Ти можеш піти в три п'яти поверхових будинки, який обереш? \n Перший; \n Другий; \n Третій \n")
                        if next == '3':
                            print('В цьому будинки нікого немає, в інших двух я чув якісь розмови.В цьому будинку ти знайшов трішки їжи, а також пару сигарет.')
                            i = 'flashlight, 7food, machine_gun, 4ammunition, 2cigarettes'
                            next = input(' Ти бачишь не велику лікарню не далеко, але не дуже зрозуміло чи є хтось там. Йдемо туди?! \n')
                            if next == 'Ні':
                                print('Ну і правильно, якщо придивитися я бачив там бандитів, і я не думаю что їхня банда дуже дружелюбна.')
                                next = input('Куди піти? \n 1) супермакрет, \n 2) закинутий парк розваг, \n 3) маленький магазнчик \n ')
                                if next == '1':
                                    print('Це доволі великий супермаркет, тут є багото всього. Я знайшов тут сокиру и їжу.')
                                    i = 'flashlight, 15food, machine_gun, 4ammunition, 2cigarettes, axe'
                                    food = input('Я втомивсля і хочу їсти. \n 1) Поїсти \n 2) Не їсти \n')
                                    if food == '1':
                                        print('-2 Їжи')
                                        i = 'flashlight, 13food, machine_gun, 4ammunition, 2cigarettes, axe'
                                        print('Дякую, була дуже смачно.')
                                        next = input('Куди йдемо далі? \n 1) Піти ходити по місту. \n 2) Маленький магазинчик не подалік. \n')
                                        if next == '2':
                                            print('Думаю це правильне рішення, в місті може бути доволі не безпечно. Тут нічого немає, крім однієї кирки')
                                            i = 'flashlight, 13food, machine_gun, 4ammunition, 2cigarettes, axe, pick'
                                            next = input('Я бачу якусь жінку біля магазинчику, мені вона здається дружелюбною. Може підійдемо поговорити з нею? \n 1) Підійти для розмови \n 2) Вийти через пожежний вихід і втікти. \n')
                                            if next == '1':
                                                print(f"Хм, вона і в правду дружелюбна але вона якась дивна... \n Дівчина: Привіт, стій там де стоїш. Ти хто, кажи швидко?! \n Я: Я, я {name}, я не пам'ятаю як я тут опинився, але я хочу втікти звідси.")
                                                next = input(' Дівчина: Ох, ти теж тут новенький. Я вже тут давно і я також планую втікти звідси. Не хочешь зі мной?   ')
                                                if next == 'Давай':
                                                    print('Добре, що ті із собой маєшь що може нами може допомогти втікти звідси')
                                                    next = input(f'Я маю:{i}, але що нам допоможе втікти звідси?   ')
                                                    if next == 'axe, pick':
                                                        print('Дівчина: Так, я думаю це нам допоможе. Я тут не далеко бачила місце де найменьше всього бандитів. Ну і до того ж там стіна тонша, я думаю раніше там вже пробували втіки, але чомусь не вдалось.')
                                                        next = input(' Давай тепер спробуємо ми?!   ')
                                                        if next == 'Давай':
                                                            print(' Дівчина: Чудово, ходім зі мной я тобі покажу це місце.')
                                                            next = input('Піти чи залишитися?  ')
                                                            if next == 'Піти':
                                                                time.sleep(5)
                                                                print('3 годи по тому...')
                                                                time.sleep(3)
                                                                print('Дівчина: Ось то місце, бачишь хтось вже пробував тут втікти. Я не думаю що нам треба підходити ближще без діла. \n Я: Подивись трішки правіше, там 7 бандитів. Ти маєш зброю? \n Дівчина: Звичайно! А ти? \n Я: Так, але я маю всього лише 4 патрони. \n Дівчина: Добре, тоді інших 3 я візьму на себе. \n Я: Добре ')
                                                                time.sleep(3)
                                                                print('Дівчина: Наче все. Дай мені сокиру, а собі бери кирку.')
                                                                next = input('Дати сокиру?!')
                                                                if next == 'Так':
                                                                    print('Дівчина: Добре починай ломати!')
                                                                    time.sleep(10)
                                                                    print('Все готово, ходім, швидше. Я бачу що там на нас бігуть бандити!')
                                                                    time.sleep(3)
                                                                    print('Молодець, ти пройшов гру. Ти зміг вибратися не зважаючи на всі труднощі! \n Game by Ruslan Sokolets')
            if next == '2':
                print("В підвалі були заручники. Вони були заперти бандитами, із-за того що вони були голодні побачивши тебе вони розірвали тебе на частинки і з'їли Ти загинув :(")


                                                        
                                                        
                                                        
                                                
                                
