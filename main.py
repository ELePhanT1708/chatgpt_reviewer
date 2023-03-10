import csv
import re
from typing import List

import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Устанавливаем API-ключ OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Функция для классификации отзыва
def classify_review(review):
    # Подготавливаем запрос к OpenAI API
    prompt = (
        f"rate the review from 1 to 10, where 10 is the most enthusiastic and 1 is the most negative.: '{review}'")
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.7,
    )
    # Use regular expression to find digits from 1 to 10 in the text
    digits = re.findall(r'10|[1-9]', completions.choices[0].text.strip())
    # Print the digits found in the text
    print("Digits found in the text:", digits)
    # Получаем оценку тональности от OpenAI API
    rating = int(completions.choices[0].text.strip())
    # Ограничиваем оценку от 1 до 10
    rating = max(min(rating, 10), 1)
    return rating


class Manager:
    input_data: List[List[str]]

    def __init__(self, path):
        self.input_csv = path

    def load_csv(self):
        with open(self.input_csv, 'r') as input:
            data = csv.reader(input, delimiter=';')

            data = [row for row in data]
            self.input_data = data

    def create_results_csv(self):
        directory = ''.join(self.input_csv.split('/')[:-1])
        output_name = self.input_csv.split('/')[-1].split('.')[0] + '_analyzed.csv'
        with open(os.path.join(directory, output_name), 'w') as output:
            writer = csv.writer(output, delimiter=';')
            self.input_data[0].append('rate')
            writer.writerow(self.input_data[0])
            for i, row_data in enumerate(self.input_data[1:]):
                rate = self.classify_review(row_data[1])
                self.input_data[i+1].append(rate)
                writer.writerow(self.input_data[i+1])



    @staticmethod
    def classify_review(review):
        # Подготавливаем запрос к OpenAI API
        prompt = (
            f"rate the review from 1 to 10, where 10 is the most enthusiastic and 1 is the most negative.: '{review}'")
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=10,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # text = "This is some text that contains digits like 2 and 8."

        # Use regular expression to find digits from 1 to 10 in the text
        digits = re.findall(r'10|[1-9]', completions.choices[0].text)

        # Print the digits found in the text
        print("completion", completions)
        print("Digits found in the text:", digits)


        # Получаем оценку тональности от OpenAI API


        # Ограничиваем оценку от 1 до 10
        rating = max(min(min(map(int, digits)), 10), 1)

        return rating



if __name__ == '__main__':
    # Пример использования функции
    # review = "As someone who has struggled with anxiety and stress for years, I've found Welltory to be incredibly " \
    #          "helpful. The app's stress tracking and HRV analysis have helped me better understand my body's response " \
    #          "to stress, and the guided meditations and breathing exercises have been a lifesaver when I'm feeling " \
    #          "overwhelmed. "
    # rating = classify_review(review)
    # print(rating)  # Выводит: 1
    manager = Manager(path='Welltory/data_rate.csv')
    # data = manager.load_csv()
    manager.load_csv()
    manager.create_results_csv()
    # rates = []
    # for review in data:
    #     rates.append(classify_review(review))
    # print(rates)
