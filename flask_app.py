from flask import Flask, render_template, request, redirect, url_for, flash
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "een_goed_geheim_woord"  # nodig voor flash-berichten


def send_contact_email(email, phone, message):
    """
    Stuurt een e-mail naar kucunlinda@gmail.com met de gegevens uit het formulier.
    Zorg dat je omgevingsvariabelen EMAIL_USER en EMAIL_PASS hebt ingesteld.
    """
    sender = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")

    if not sender or not password:
        # Tijdens ontwikkeling kun je dit in de console zien
        print("EMAIL_USER of EMAIL_PASS niet ingesteld.")
        print("Bericht dat verstuurd zou worden:")
        print("Van:", email)
        print("Telefoon:", phone)
        print("Bericht:", message)
        return

    msg = EmailMessage()
    msg["Subject"] = "Nieuw bericht via Bijbel Plezier website"
    msg["From"] = sender
    msg["To"] = "kucunlinda@gmail.com"

    body = f"""
Er is een nieuw bericht binnengekomen via het contactformulier van Bijbel Plezier.

E-mail bezoeker: {email}
Telefoonnummer: {phone}

Bericht:
{message}
"""
    msg.set_content(body)

    # Voor Gmail:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        # Eenvoudige validatie
        if not email or not message:
            flash("Vul minstens e-mail en bericht in, alsjeblieft.")
            return redirect(url_for("home"))

        send_contact_email(email, phone, message)
        flash("Bedankt! Je bericht is verstuurd.")
        return redirect(url_for("home"))

    return render_template("home.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
