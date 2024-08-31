import threading
import time
import os
import shutil
import uuid

from glob import glob
from pathlib import Path
from rich.console import Console
from datetime import datetime

from config.config import ConfigManager
from templates.handle_templates import HandleTemplates

c = Console()

class MyThread(threading.Thread):

    def __init__(self, logs_path, output):
        super().__init__()
        self.logs_path = logs_path
        self.output = output

    def sort_tdata(self, tdata):
        unique_id = uuid.uuid4().hex
        now = datetime.now()
        formatted_date = now.strftime("%H_%M %d-%m-%y")

        tdata_output_path = Path(self.output) / f"result-{formatted_date}" / "tdata" / f"tdata-{unique_id}"
        source_path = Path(tdata)

        try:
            shutil.copytree(source_path, tdata_output_path)

        except Exception as e:
            print(f"An error occurred: {e}")

    def sort_cookies(self, cookies):
        unique_id = uuid.uuid4().hex
        now = datetime.now()
        formatted_date = now.strftime("%H_%M %d-%m-%y")

        # Определяем пути
        cookies_output_path = Path(self.output) / f"result-{formatted_date}" / "cookies"
        source_path = Path(cookies)
        destination_path = cookies_output_path / f"cookies-{unique_id}.txt"

        try:
            # Создаем директории, если они не существуют
            cookies_output_path.mkdir(parents=True, exist_ok=True)

            # Проверяем, что исходный файл существует
            if source_path.is_file():
                shutil.copy(source_path, destination_path)
            else:
                print(f"Source file does not exist: {source_path}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def sort_passwords(self, passwords):
        unique_id = uuid.uuid4().hex
        now = datetime.now()
        formatted_date = now.strftime("%H_%M %d-%m-%y")

        # Определяем пути
        passwords_output_path = Path(self.output) / f"result-{formatted_date}" / "passwords"
        source_path = Path(passwords)
        destination_path = passwords_output_path / f"passwords-{unique_id}.txt"

        try:
            # Создаем директории, если они не существуют
            passwords_output_path.mkdir(parents=True, exist_ok=True)

            # Проверяем, что исходный файл существует
            if source_path.is_file():
                shutil.copy(source_path, destination_path)
            else:
                print(f"Source file does not exist: {source_path}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def run(self):
        current_template = ConfigManager("config.ini").read_key("PyLightSorter", "template")

        template_json = HandleTemplates(current_template).solve_template()

        cookies = template_json["cookies"]
        password = template_json["password"]


        logs_directory = Path(self.logs_path)

        search_app = template_json.get('search-app', {})

        for log_dir in logs_directory.iterdir():
            if log_dir.is_dir():
                cookie_directory = log_dir / cookies

                for k, v in search_app.items():
                    app_dir = log_dir / v

                    tdata_dir = log_dir / search_app["telegram"]
                    ds_dir = log_dir / search_app['discord']

                    if app_dir.is_dir():
                        if app_dir == tdata_dir:
                            # c.print(f"[blue bold]Нашел TDATA {log_dir / search_app['telegram']}")

                            self.sort_tdata(tdata_dir)
                        if app_dir == ds_dir:
                            for file in ds_dir.glob("*.txt"):
                                with file.open('r') as f:
                                    pass
                        else:
                            for file in app_dir.glob('*.txt'):
                                with file.open('r') as f:
                                    pass

                if cookie_directory.is_dir():
                    for file in cookie_directory.glob('*.txt'):
                        with file.open('r') as f:
                            self.sort_cookies(file)

                try:
                    with open(log_dir / password, 'r') as f:
                        self.sort_passwords(log_dir / password)

                        get_config_items = ConfigManager("config.ini").read_keys("Services")

                        for k,v in get_config_items.items():
                            print(k, v)
                except Exception as e:
                    pass









