from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import connection


#app = Flask(__name__)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/estacionamento'

#db = SQLAlchemy(app)
app = connection.get_connection()
db = SQLAlchemy(app)


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)

    dt_criacao = db.Column(db.Date)

    cd_placa = db.Column(db.String(50))

    ds_cor = db.Column(db.String(50))

    hr_entrada = db.Column(db.String(50))

    hr_saida = db.Column(db.String(50))

    hr_total = db.Column(db.String(50))

    vl_pago = db.Column(db.String(50))


db.create_all()
