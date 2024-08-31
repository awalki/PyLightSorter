import inquirer

class Question:

    def __init__(self, name, message):
        self.name = name
        self.message = message

    def send(self):
        questions = [
            inquirer.Text(name=self.name, message=self.message),
        ]

        answers = inquirer.prompt(questions)

        return answers

    @staticmethod
    def confirm():
        questions = [
            inquirer.List(
                "continue",
                message="Запустить сортер",
                choices=["Да", "Нет"],
            ),
        ]

        answers = inquirer.prompt(questions)

        return answers

