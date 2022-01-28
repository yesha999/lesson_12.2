from flask import Flask, render_template
import json

with open('candidates.json', encoding='utf-8') as file:
    candidates = json.load(file)

with open('settings.json', encoding='utf-8') as file:
    settings = json.load(file)

app = Flask(__name__)


@app.route('/')
def main_page():
    if settings["online"]:
        is_app_work = 'Приложение работает'
    else:
        is_app_work = 'Приложение не работает'
    return render_template("main_page.html", is_app_work=is_app_work)


@app.route('/candidate/<int:number>')
def candidate_page(number):
    for candidate in candidates:
        if int(candidate['id']) == number:
            name = candidate['name']
            picture = candidate['picture']
            position = candidate['position']
            gender = candidate['gender']
            age = candidate['age']
            skills = candidate['skills']
    return render_template("candidate_page.html", name=name, picture=picture, position=position,
                           gender=gender, age=age, skills=skills)


@app.route('/list/')
def list_page():
    return render_template("list_page.html", candidates=candidates)


if __name__ == "__main__":
    app.run()
