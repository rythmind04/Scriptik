import time
import psutil
import pygetwindow as gw
from pywinauto.application import Application


# Ключевые слова для поиска в заголовках окон
KEYWORDS = ["казино", "casino", "слоты", "слот", "азартные игры", "vodka", "1win", "казик",
            "водка казино", "свит бонанза", "sweet bonanza", "vulkan", "вулкан", "кент", "kent", "азино", "azino", "dog house", "дог хаус", "порно",
             "porn", "порнуха", "геи", "gay", "porno", "noodlemagazine"]

exception = ["казино: песни, альбомы, плейлисты", "vk.com/audios", "restore"]

# Получаем все процессы браузеров
def get_browser_processes():
    browsers = ["chrome.exe", "firefox.exe", "msedge.exe", "opera.exe"]
    browser_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in browsers:
            browser_processes.append(proc)
    return browser_processes


# Проверка заголовков всех открытых окон
def monitor_browser_windows():
    while True:
        windows = gw.getAllTitles()  # Получаем все заголовки окон
        for title in windows:
            print(f'Вкладки: {title}')
            # Пропускаем окна, если они в списке исключений
            if any(exc in title.lower() for exc in exception):
                continue

            # Проверяем окна на запрещённые ключевые слова
            for keyword in KEYWORDS:
                if keyword in title.lower():
                    print(f"Найдено запрещенное слово в окне: {title}")
                    close_window_by_title(title)
                    return

        time.sleep(5)  # Пауза между проверками

# Закрываем окно по его заголовку
def close_window_by_title(title):
    windows = gw.getWindowsWithTitle(title)
    if windows:
        for window in windows:
            print(f"Закрываем окно: {window.title}")
            try:
                app = Application().connect(handle=window._hWnd)
                app.kill()  # Закрываем окно
            except Exception as e:
                print(f"Ошибка при закрытии окна: {e}")

if __name__ == "__main__":
    while True:
        monitor_browser_windows()
        time.sleep(10)  # Проверка каждые 10 секунд