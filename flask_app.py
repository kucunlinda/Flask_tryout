import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "geheim")

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        first_name = request.form.get("first_name", "")
        last_name = request.form.get("last_name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        message = request.form.get("message", "")

        if not (first_name and last_name and email and message):
            flash("Vul alle verplichte velden in.", "danger")
            return redirect(url_for("home"))

        email_data = {
            "from": "Bijbelplezier <contact@bijbelplezier.com>",
            "to": ["kucunlinda@gmail.com"],
            "subject": f"Nieuw bericht van {first_name} {last_name}",
            "html": f"""
                <p><strong>Naam:</strong> {first_name} {last_name}</p>
                <p><strong>E-mail:</strong> {email}</p>
                <p><strong>Telefoon:</strong> {phone}</p>
                <p><strong>Bericht:</strong><br>{message}</p>
            """
        }

        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json=email_data,
        )

        if response.status_code == 200:
            flash("Je bericht is verzonden! Dank je wel.", "success")
        else:
            flash("Verzenden mislukt. Probeer later opnieuw.", "danger")

        return redirect(url_for("home"))

    return render_template("home.html")


@app.route("/over-ons")
def over_ons():
    return render_template("over_ons.html")


if __name__ == "__main__":
    app.run(debug=True)
