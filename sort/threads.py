import threading
import os
import shutil
import uuid

from pathlib import Path
from rich.console import Console
from datetime import datetime

from config.config import ConfigManager
from sort.paths import GetPaths

c = Console()
now = datetime.now()
formatted_now = now.strftime("%H-%M-%S_%Y-%m-%d")
unique_id = uuid.uuid1()

class MyThread(threading.Thread):

    def __init__(self, action):
        """
        :param action: что сейчас будет делать сортер
        """
        super().__init__()
        self.action = action
        self.logs_path = Path("logs")
        self.output = Path("output")
        self.config = ConfigManager("config.ini").read_keys("Services")

        self.cookies = GetPaths(self.logs_path).get_path("cookies")
        self.passwords = GetPaths(self.logs_path).get_path("password")
        self.discord = GetPaths(self.logs_path).get_path("discord_tokens")
        self.tdata = GetPaths(self.logs_path).get_path("tdata")

    def choice_action(self):
        match self.action:
            case "Отсортировать tdata":
                print("Сортируем tdata...")

                self.sort_tdata()
            case "Отсортировать discord tokens":
                print("Сортируем discord tokens...")

                self.sort_ds_tokens()
            case "Отсортировать логи по запросу":
                print("Сортируем логи по запросу...")

                self.sort_logs()

    def sort_tdata(self):
        for tdata in self.tdata:
            dest = os.path.join(self.output / f"tdata-{formatted_now}" / f"tdata-{unique_id}")

            shutil.copytree(tdata, dest, dirs_exist_ok=True)

    def sort_ds_tokens(self):
        tokens_array = []

        for token_file in self.discord:
            with open(token_file, "r") as file:
                tokens_array.extend(file.readlines())

        with open(Path(f"output/discord-tokens-{formatted_now}.txt"), "w") as output_file:
            output_file.writelines(tokens_array)

    @staticmethod
    def search_key_in_file(file_path, key):
        """
        Проверяет, содержится ли ключ в файле по указанному пути.
        """
        if not os.path.isfile(file_path):
            print(f"Файл {file_path} не существует.")
            return False

        try:
            with open(file_path, 'r') as file:
                contents = file.read()
                return key in contents
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")
            return False

    def sort_logs(self):
        for k, v in self.config.items():
            if v != "false":
                for cookie in self.cookies:
                    if self.search_key_in_file(cookie, k):
                        log_path = os.path.dirname(cookie)
                        log_folder = os.path.basename(os.path.dirname(log_path))
                        log = os.path.join('logs', log_folder)

                        dest = os.path.join(self.output / f"result-{formatted_now}" / k, log_folder)

                        if os.path.isdir(log):
                            shutil.copytree(log, dest, dirs_exist_ok=True)

                for password in self.passwords:
                    if self.search_key_in_file(password, k):
                        log_path = os.path.dirname(password)
                        log_folder = os.path.basename(os.path.dirname(log_path))
                        log = os.path.join('logs', log_folder)

                        dest = os.path.join(self.output / f"result-{formatted_now}" / k, log_folder)

                        if os.path.isdir(log):
                            shutil.copytree(log, dest, dirs_exist_ok=True)

    def run(self):
        if not os.path.exists(self.output):
            os.mkdir(self.output)
        if not os.path.exists(self.logs_path):
            os.mkdir(self.logs_path)
        else:
            self.choice_action()











