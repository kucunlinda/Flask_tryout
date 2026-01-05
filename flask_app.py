
import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "geheim_voor_flash_berichten")

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
MAIL_FROM = os.environ.get("MAIL_FROM", "contact@bijbelplezier.com")
MAIL_TO = os.environ.get("MAIL_TO", "astar_kucun@hotmail.com")


def send_email_via_resend(subject: str, text_body: str, reply_to: str | None = None):
    if not RESEND_API_KEY:
        raise RuntimeError("RESEND_API_KEY ontbreekt in Environment Variables.")

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "from": MAIL_FROM,
        "to": [MAIL_TO],
        "subject": subject,
        "text": text_body,
    }

    if reply_to:
        payload["reply_to"] = reply_to

    r = requests.post(url, headers=headers, json=payload, timeout=15)
    if r.status_code >= 400:
        raise RuntimeError(f"Resend error {r.status_code}: {r.text}")


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
            send_email_via_resend(subject=subject, text_body=body, reply_to=email)
            flash("Je bericht is verzonden! Dank je wel.", "success")
        except Exception as e:
            print("EMAIL SEND ERROR:", str(e))
            flash("Bericht kon niet verzonden worden. Probeer later opnieuw.", "danger")

        return redirect(url_for("home"))

    return render_template("home.html")


@app.route("/over-ons")
def over_ons():
    return render_template("over_ons.html")


if __name__ == "__main__":
    app.run(debug=True)
