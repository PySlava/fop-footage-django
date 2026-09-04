# 🏢 ФОП Кадри

Веб-система для автоматизації кадрового обліку та документообігу ФОП.

## 🚀 Функціонал
* Ведення обліку декількох ФОП та їх працівників.
* Автоматична генерація наказів про прийняття на роботу (PDF).
* Формування повідомлення до ДПС (XML).
* Автоматичне ведення табеля робочого часу та розрахунок зарплати.

## 🛠 Технології
* **Backend:** Python 3.11+, Django 5.x
* **Database:** PostgreSQL
* **Frontend:** HTML5, Bootstrap 5
* **Documents:** PDF generation, XML (DPS format), Excel

## 🔧 Локальне розгортання
1. Клонувати репозиторій: `git clone https://github.com/PySlava/fop_kadry.git`
2. Створити та активувати venv: `python -m venv venv && source venv/bin/activate`
3. Встановити залежності: `pip install -r requirements.txt`
4. Створити `.env` на основі `.env.example`
5. Виконати міграції: `python manage.py migrate`
6. Запустити сервер: `python manage.py runserver`