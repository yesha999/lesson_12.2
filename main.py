from flask import Flask, render_template, request
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


@app.route('/search/')
def search_page():
    s = request.args.get("name")
    if s is None:
        return 'Введите параметр name'
    if settings['case-sensitive'] is False:
        s = s.lower()
        candidates_search = [candidate for candidate in candidates if s in candidate['name'].lower()]
    else:
        candidates_search = [candidate for candidate in candidates if s in candidate['name']]
    if len(candidates_search):
        return render_template("search_page.html", canidates_count=len(candidates_search),
                               candidates_search=candidates_search)
    return "Кандидатов не найдено"


@app.route('/skill/<skill>')
def skill_page(skill):
    candidates_w_skill = []
    for candidate in candidates:
        if skill in candidate['skills']:
            candidates_w_skill.append(candidate)
    if len(candidates_w_skill) > int(settings['limit']):
        candidates_w_skill = candidates_w_skill[0:settings['limit']]
    return render_template("skills_page.html", candidates_w_skill=candidates_w_skill,
                           candidates_w_skill_count=len(candidates_w_skill), skill=skill)


if __name__ == "__main__":
    app.run()
