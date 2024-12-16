import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# Выводим текущее время, чтобы понимать, что установлено на машине
current_time = datetime.now()
print(f"Текущее время на машине: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

def get_video_stats(url):
    # Получаем HTML страницу по ссылке
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка загрузки страницы {url}. Код ошибки: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при запросе страницы {url}: {e}")
        return None
    
    # Парсим HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем playCount на странице
    play_count = None
    for script in soup.find_all('script'):
        if script.string and 'playCount' in script.string:
            try:
                start = script.string.index('"playCount":') + len('"playCount":')
                end = script.string.index(',', start)
                play_count = int(script.string[start:end])
                break
            except Exception as e:
                print(f"Ошибка при парсинге playCount: {e}")
    
    if play_count is not None:
        print(f"Получено количество просмотров: {play_count}")
    return play_count

def wait_for_next_hour():
    # Получаем текущее время
    now = datetime.now()
    # Рассчитываем сколько времени осталось до следующего часа
    seconds_until_next_hour = 3600 - (now.minute * 60 + now.second)
    print(f"Ожидаем до следующего часа. Осталось {seconds_until_next_hour} секунд.")
    time.sleep(seconds_until_next_hour)  # Ждем до следующего часа

def track_video_views(urls, total_time=86400):
    # Структура данных
    data_columns = ['time', 'day_of_week', 'url', 'playCount', 'playCount_diff']
    file_name = 'video_views.csv'
    
    # Создаем файл, если его нет
    try:
        with open(file_name, 'x') as f:
            pd.DataFrame(columns=data_columns).to_csv(f, index=False)
        print("Создан новый файл video_views.csv с заголовками.")
    except FileExistsError:
        print("Файл video_views.csv уже существует, продолжаем работать с ним.")
    
    start_time = time.time()
    print("Начинаем сбор данных о просмотрах...")

    last_play_count = {}  # Словарь для хранения последнего значения просмотров по каждому видео
    while time.time() - start_time < total_time:
        wait_for_next_hour()  # Ждем до следующего часа
        
        for url in urls:
            print(f"Сбор данных с видео: {url}")
            play_count = get_video_stats(url)
            if play_count is not None:
                current_time = datetime.now()  # Текущее время
                formatted_time = current_time.strftime('%Y-%m-%d %H')
                day_of_week = current_time.strftime('%A')  # Получаем день недели
                
                # Вычисляем разницу в просмотрах
                playCount_diff = 0
                if url in last_play_count:
                    playCount_diff = play_count - last_play_count[url]
                    print(f"Просмотры за последний час для видео {url}: {playCount_diff}")
                else:
                    print(f"Первый сбор данных для видео {url}")
                
                # Записываем данные о просмотрах в файл
                row = {'time': formatted_time, 'day_of_week': day_of_week, 'url': url, 'playCount': play_count, 'playCount_diff': playCount_diff}
                
                # Записываем данные сразу в CSV
                try:
                    with open(file_name, 'a', newline='') as f:
                        pd.DataFrame([row]).to_csv(f, header=False, index=False)
                    print(f"Данные для видео {url} записаны в файл.")
                    
                    # Обновляем количество просмотров для следующего раза
                    last_play_count[url] = play_count
                
                except Exception as e:
                    print(f"Ошибка записи в файл для видео {url}: {e}")
        
    print("Сбор данных завершен. Все данные записаны в video_views.csv.")

# Пример использования
video_urls = [
    'https://www.tiktok.com/@ffashionprincess/video/7430399663200685344',  # Замените на реальные ссылки
    'https://www.tiktok.com/@maluxreserva/video/7446084356264824070',
    'https://www.tiktok.com/@parrot.davo/video/7438710010403704097',
    'https://www.tiktok.com/@vitaljalv/video/7431982026355412256',
    'https://www.tiktok.com/@condition_litvin0/video/7431500017870867718',
    'https://www.tiktok.com/@cra1g89/video/7448905942596472086',
    'https://www.tiktok.com/@virrecsgo/video/7449048886049623318',
    'https://www.tiktok.com/@virrecsgo/video/7449048886049623318',
    'https://www.tiktok.com/@twitchclipsroflo/video/7448615399618333974',
    'https://www.tiktok.com/@whyownageqq/video/7401960334388448517',
    'https://www.tiktok.com/@danya.cr0wn/video/7448627979409968390',
    'https://www.tiktok.com/@slyfe.e/video/7447997798458477856',
    'https://www.tiktok.com/@stele420/video/7448975342066322693',
    'https://www.tiktok.com/@stele420/video/7448975342066322693',
    'https://www.tiktok.com/@grinch_strim/video/7437223383814704407',
    'https://www.tiktok.com/@faceofmadness/video/7437031215393230136',
    'https://www.tiktok.com/@whyownageqq/video/7401960334388448517',
    'https://www.tiktok.com/@soulse02/video/7400676789053443349',
    'https://www.tiktok.com/@renatikscam/video/7443410954785672470',
    'https://www.tiktok.com/@cra1g89/video/7448905942596472086',
    'https://www.tiktok.com/@renatikscam/video/7446697762915110166',
    'https://www.tiktok.com/@lordofdepresssion/video/7445179383159049473',
    'https://www.tiktok.com/@brunokenn/video/7432327570881875205',
    'https://www.tiktok.com/@csmoneytrade/video/7436817977544068370',
    'https://www.tiktok.com/@stele420/video/7448681357556944133',
    'https://www.tiktok.com/@stele420/video/7397805913941363973',
    'https://www.tiktok.com/@stele420/video/7443748478003514679',
    'https://www.tiktok.com/@garskocheating/video/7415328206909148423',
    'https://www.tiktok.com/@spxtral7/video/7446867791912733957',
    'https://www.tiktok.com/@g2esports/video/7283883434773187873',
    'https://www.tiktok.com/@g2esports/video/7283883434773187873'
]

track_video_views(video_urls, total_time=86400)  # Сбор данных в течение 24 часов