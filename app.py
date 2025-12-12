from flask import Flask, render_template, request
import os
from themes_classes import THEMES
from tasks_themes import TASKS

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/class/<int:class_num>')
def class_page(class_num):
    themes_dict = THEMES.get(class_num, {})
    return render_template('themes.html', 
                         class_num=class_num, 
                         themes=themes_dict)

@app.route('/theory/<int:class_num>/<theme_key>')
def theory_page(class_num, theme_key):
    themes_dict = THEMES.get(class_num, {})
    
    if theme_key not in themes_dict:
        return "Тема не найдена", 404
    
    filename = f'theory/class{class_num}/{theme_key}.txt'
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            theory = f.read()
    except FileNotFoundError:
        return f"Файл теории не найден: {filename}", 404
    
    return render_template('theory.html',
                         class_num=class_num,
                         theme_key=theme_key,
                         theme_name=themes_dict[theme_key],
                         theory=theory)

@app.route('/tasks/<int:class_num>/<theme_key>', methods=['GET', 'POST'])
def tasks_page(class_num, theme_key):
    themes_dict = THEMES.get(class_num, {})
    
    if theme_key not in themes_dict:
        return "Тема не найдена", 404
    
    tasks_key = f"{class_num}_{theme_key}"
    tasks = TASKS.get(tasks_key, [])
    
    if request.method == 'POST':
        results = []
        for i, task in enumerate(tasks):
            user = request.form.get(f'answer_{i}', '').strip()
            results.append(user == task['answer'].strip())
    else:
        results = []
    
    return render_template('tasks.html',
                         class_num=class_num,
                         theme_key=theme_key,
                         theme_name=themes_dict[theme_key],
                         tasks=tasks,
                         results=results)

if __name__ == "__main__":
    app.run(debug=True)