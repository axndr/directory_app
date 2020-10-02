from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact_app.db'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(50), nullable=False)
    password = db.Column(db.VARCHAR(100), nullable=False)

class Contacts(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    owner = db.Column(db.ForeignKey(Users.id))
    name = db.Column(db.VARCHAR(100), default='Site Admin')
    phone_number = db.Column(db.String(12), nullable=False, default='901-111-1111')

class Sites(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(50), nullable=False)
    address = db.Column(db.VARCHAR(100), nullable=False)
    contact_id = db.Column(db.ForeignKey(Contacts.id))

    def __repr__(self):
        print(f'{self.site_name}')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # if request.form['Login']:
        #     username, password = (request.form['username'], request.form['password'])
        #     exists = db.session.query(Users.username, Users.password).filter_by(username=username, password=password).scalar() is not None
        #     if exists:
        #         return redirect('/')
        #     else:
        #         return f'Could not find account with that username/password.'

        # elif request.form['Register']:
        # new_user_content = request.form['content'].username
        new_user, new_pass = request.form.getlist('content')
        new_user = Users(username=new_user, password=new_pass)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return f'Could not add user: {new_user.username}.'

    return render_template('index.html')


@app.route('/new_user/', methods=['POST'])
def index():
    return render_template('new_user.html')


if __name__ == '__main__':
    app.run(debug=True)