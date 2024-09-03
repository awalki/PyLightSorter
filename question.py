import inquirer

class Question:

    def __init__(self, name, message, choices: list):
        """
        Инициация, отцы, отцы, отцы, отцы, отца (окси лифт, кто не понял)
        :param name: имя по которому идентифицируется вопрос
        :param message: текст вопроса пользователю
        :param choices: список из ответов предложенных пользователю
        """
        self.name = name
        self.message = message
        self.choices = choices

    def send(self):
        """
        Вопрос с ограниченным числом выборов
        :return: ответ пользователя
        """
        questions = [
            inquirer.List(
                self.name,
                message=self.message,
                choices=self.choices,
            ),
        ]

        answer = inquirer.prompt(questions)

        return answer

    @staticmethod
    def confirm():
        """
        Вопрос с 1 ответом из 2 предложенных
        :return: ответ ("Да" или "Нет") от пользователя
        """
        questions = [
            inquirer.List(
                "continue",
                message="Запустить сортер",
                choices=["Да", "Нет"],
            ),
        ]

        answer = inquirer.prompt(questions)

        return answer

