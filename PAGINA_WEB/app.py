from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
API_KEY = "e38214ce636c8b94653c6fd2c09e9df7"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registro_de_busquedas.db'
db = SQLAlchemy(app)

class Busqueda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(100), nullable=False)
    respuesta_base = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    clima = None

    if request.method == "POST":
        ciudad = request.form["ciudad"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
        respuesta = requests.get(url)
        datos = respuesta.json()
        if datos["cod"] == 200:
            clima = {
                "ciudad": datos["name"],
                "temperatura": datos["main"]["temp"],
                "descripcion": datos["weather"][0]["description"],
                "humedad": datos["main"]["humidity"]
            }
            busqueda = Busqueda(
                pregunta=ciudad,
                respuesta_base=clima["descripcion"]
            )
            db.session.add(busqueda)
            db.session.commit()
        else:
            clima = {
                "error": "Ciudad no encontrada"
            }
    return render_template("index.html", clima=clima)



if __name__ == "__main__":
    app.run(debug=True)