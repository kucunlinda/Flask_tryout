import os
import traceback
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

def env_bool(name: str, default: bool = False) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "y", "on")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "geheim_voor_flash_berichten")

# ---- Mail config (Resend SMTP via env vars) ----
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.resend.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", "465"))
app.config["MAIL_USE_SSL"] = env_bool("MAIL_USE_SSL", True)
app.config["MAIL_USE_TLS"] = env_bool("MAIL_USE_TLS", False)

# Resend SMTP credentials:
# User = "resend"
# Pass = your Resend API key (re_...)
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "resend")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")

# FROM must be on your verified domain in Resend (e.g. contact@bijbelplezier.com)
MAIL_FROM = os.environ.get("MAIL_FROM", "contact@bijbelplezier.com")
MAIL_TO = os.environ.get("MAIL_TO", "astar_kucun@hotmail.com")

app.config["MAIL_DEFAULT_SENDER"] = MAIL_FROM

mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name  = request.form.get("last_name", "").strip()
        email      = request.form.get("email", "").strip()
        phone      = request.form.get("phone", "").strip()
        message    = request.form.get("message", "").strip()

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
                recipients=[MAIL_TO],     # <-- alles gaat naar astar_kucun@hotmail.com
                reply_to=email,           # <-- als je 'Reply' doet, ga je naar de invuller
                body=body,
                sender=MAIL_FROM          # <-- afzender op je domein
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
