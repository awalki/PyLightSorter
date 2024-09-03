from tabulate import tabulate

from question import Question
from config.config import ConfigManager
from sort.threads import MyThread

config = ConfigManager("config.ini")

template_choices = ["lumma", "meta", "redline", "vidar"]
template_question = Question("template", "Выберите шаблон (пока работает только lumma)", template_choices)

action_choices = ["Отсортировать tdata", "Отсортировать discord tokens", "Отсортировать логи по запросу"]
action_question = Question("action", "Выберите, что должен сделать сортер", action_choices)

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

    if config.read_key("PyLightSorter", "template") != "false":
        current_template = config.read_key("PyLightSorter", "template")

        settings = [
            ["Шаблон", current_template],
        ]
        header = ["Ключ", "Значение"]

        print("\nВаши настройки")
        print(tabulate(settings, headers=header, tablefmt="grid"), end="\n\n")
    else:
        user_template = template_question.send()

        config.change_key("PyLightSorter", "template", user_template["template"])

    user_action = action_question.send()
    yes_or_no = action_question.confirm()

    if yes_or_no["continue"] != "Да":
        exit(1)
    else:
        my_thread = MyThread(user_action["action"])
        my_thread.start()
        my_thread.join()

