import json

class HandleTemplates:

    def __init__(self, template):
        self.template = template

    def solve_template(self):
        with open(f"templates/{self.template}.json", 'r') as file:
            return json.load(file)