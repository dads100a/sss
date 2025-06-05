from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
db = SQLAlchemy(app)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_place = db.Column(db.String(200), nullable=False)
    residence = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    application_date = db.Column(db.String(10), default=datetime.now().strftime("%d.%m.%Y"))

# Создание базы данных в контексте приложения
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create_application():
    if request.method == 'POST':
        new_application = Application(
            last_name=request.form['last_name'],
            first_name=request.form['first_name'],
            middle_name=request.form['middle_name'],
            birth_date=request.form['birth_date'],
            gender=request.form['gender'],
            birth_place=request.form['birth_place'],
            residence=request.form['residence'],
            phone_number=request.form['phone_number'],
        )
        db.session.add(new_application)
        db.session.commit()
        return redirect(url_for('applications'))
    return render_template('create_application.html')

@app.route('/applications', methods=['GET'])
def applications():
    all_applications = Application.query.all()
    return render_template('applications.html', applications=all_applications)

@app.route('/application/<int:id>', methods=['GET'])
def application_detail(id):
    application = Application.query.get_or_404(id)
    return render_template('application_detail.html', application=application)

@app.route('/delete/<int:id>', methods=['GET'])
def delete_application(id):
    application = Application.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    return redirect(url_for('applications'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

