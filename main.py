from tabulate import tabulate

from question import Question
from config.config import ConfigManager
from sort.threads import MyThread

config = ConfigManager("config.ini")

question = Question("thread-count", "Введите кол-во потоков")

if __name__ == "__main__":
    print("""
  _____       _      _       _     _    _____            _            
 |  __ \     | |    (_)     | |   | |  / ____|          | |           
 | |__) |   _| |     _  __ _| |__ | |_| (___   ___  _ __| |_ ___ _ __ 
 |  ___/ | | | |    | |/ _` | '_ \| __|\___ \ / _ \| '__| __/ _ \ '__|
 | |   | |_| | |____| | (_| | | | | |_ ____) | (_) | |  | ||  __/ |   
 |_|    \__, |______|_|\__, |_| |_|\__|_____/ \___/|_|   \__\___|_|   
         __/ |          __/ |                                         
        |___/          |___/                                          
    """)

    if config.read_key("PyLightSorter", "threads") != "false":
        current_threads = config.read_key("PyLightSorter", "threads")
        current_template = config.read_key("PyLightSorter", "template")

        settings = [
            ["Потоки", current_threads],
            ["Шаблон", current_template],
        ]
        header = ["Ключ", "Значение"]

        print("\nВаши настройки")
        print(tabulate(settings, headers=header, tablefmt="grid"), end="\n\n")
    else:
        thr_count = question.send()

        config.change_key("PyLightSorter", "threads", thr_count["thread-count"])

    yes_or_no = question.confirm()

    if yes_or_no["continue"] != "Да":
        exit(1)
    else:
        my_thread = MyThread("logs", "output")
        my_thread.start()
        my_thread.join()

