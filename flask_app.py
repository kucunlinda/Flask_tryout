import os
import traceback
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "geheim_voor_flash_berichten")

# Gmail SMTP config (values come from Render Environment variables)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")  # your gmail
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")  # your gmail app password
app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

mail = Mail(app)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        message = request.form.get("message", "").strip()

        if not (first_name and last_name and email and message):
            flash("Vul alle verplichte velden in.", "danger")
            return redirect(url_for("home"))

        subject = f"Nieuw bericht via Bijbelplezier van {first_name} {last_name}"
        body = (
            f"Naam: {first_name} {last_name}\n"
            f"E-mail: {email}\n"
            f"Telefoon: {phone}\n\n"
            f"Bericht:\n{message}\n"
        )

        try:
            msg = Message(
                subject=subject,
                recipients=[app.config["MAIL_USERNAME"]],
                reply_to=email,
                body=body,
            )
            mail.send(msg)
            flash("Je bericht is verzonden! Dank je wel.", "success")

        except Exception:
            print("MAIL ERROR TRACEBACK:\n", traceback.format_exc())
            flash("Bericht kon niet verzonden worden. Probeer later opnieuw.", "danger")

        return redirect(url_for("home"))

    return render_template("home.html")


@app.route("/over-ons")
def over_ons():
    return render_template("over_ons.html")


if __name__ == "__main__":
    app.run(debug=True)
