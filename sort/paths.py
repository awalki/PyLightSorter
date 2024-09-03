import glob

from config.config import ConfigManager
from templates.handle_templates import HandleTemplates


class GetPaths:
    def __init__(self, logs_path):
        """
        :param logs_path: путь к папке логов
        """
        self.config = ConfigManager("config.ini")

        self.template = HandleTemplates(self.config.read_key("PyLightSorter", "template")).solve_template()
        self.logs_path = logs_path

        self.cookies_path = self.template["cookies"]
        self.password_path = self.template["password"]
        self.discord_tokens = self.template["search-app"]["discord"]
        self.tdata = self.template["search-app"]["telegram"]

    def get_path(self, incoming_path):
        """
        :return: возвращаются пути к запрошенным папкам
        """
        cookies_globs = glob.iglob(f"{self.logs_path}/**/{self.cookies_path}/*.txt", recursive=True)
        passwords_globs = glob.iglob(f"{self.logs_path}/**/{self.password_path}", recursive=True)
        tdata_globs = glob.iglob(f"{self.logs_path}/**/{self.tdata}/*", recursive=True)
        discord_globs = glob.iglob(f"{self.logs_path}/**/{self.discord_tokens}/*.txt", recursive=True)

        match incoming_path:
            case "tdata":
                return list(tdata_globs)
            case "discord_tokens":
                return list(discord_globs)
            case "cookies":
                return list(cookies_globs)
            case "password":
                return list(passwords_globs)
