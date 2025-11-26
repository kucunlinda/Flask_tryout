from flask import Flask, render_template, request
import os
import smtplib
import ssl
from email.message import EmailMessage

app = Flask(__name__)

# -------------------------
#  E-MAIL INSTELLINGEN
# -------------------------

EMAIL_ADDRESS = "kucunlinda@gmail.com"
# Stel dit in als omgevingsvariabele VOORDAT je Flask start
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


def send_contact_email(data: dict):
    """Verstuur een mail met de inhoud van het contactformulier."""
    if not EMAIL_PASSWORD:
        # In ontwikkeling: fout gooien zodat je ziet wat er mis is
        raise RuntimeError(
            "EMAIL_PASSWORD omgevingsvariabele niet ingesteld. "
            "Maak een Gmail app-wachtwoord en stel deze in."
        )

    msg = EmailMessage()
    msg["Subject"] = f"Nieuw bericht via Bijbelplezier van {data['first_name']} {data['last_name']}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    body = (
        f"Er is een nieuw bericht via het contactformulier:\n\n"
        f"Naam: {data['first_name']} {data['last_name']}\n"
        f"E-mail: {data['email']}\n"
        f"Telefoonnummer: {data['phone']}\n\n"
        f"Bericht:\n{data['message']}\n"
    )
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


# -------------------------
#  ROUTE
# -------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    success_message = None
    error_message = None

    if request.method == "POST":
        form_data = {
            "first_name": request.form.get("first_name", "").strip(),
            "last_name": request.form.get("last_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "message": request.form.get("message", "").strip(),
        }

        try:
            send_contact_email(form_data)
            success_message = "Bedankt voor je bericht! We nemen zo snel mogelijk contact met je op."
        except Exception:
            error_message = "Er ging iets mis bij het verzenden van je bericht. Probeer het later opnieuw."

    return render_template(
        "home.html",
        success_message=success_message,
        error_message=error_message,
    )


if __name__ == "__main__":
    app.run(debug=True)
