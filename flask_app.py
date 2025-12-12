import os
import traceback
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "geheim_voor_flash_berichten")

# =========================
# Mail configuratie (Resend SMTP)
# =========================
app.config["MAIL_SERVER"] = "smtp.resend.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")   # van Render
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")   # van Render
app.config["MAIL_DEFAULT_SENDER"] = "contact@bijbelplezier.com"

mail = Mail(app)

# =========================
# HOME + CONTACTFORMULIER
# =========================
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
                recipients=["astar_kucun@hotmail.com"],  # 👈 TO-adres
                reply_to=email,
                body=body,
            )
            mail.send(msg)
            flash("Je bericht is verzonden! Dank je wel.", "success")

        except Exception:
            print("MAIL ERROR:\n", traceback.format_exc())
            flash("Bericht kon niet verzonden worden. Probeer later opnieuw.", "danger")

        return redirect(url_for("home"))

    return render_template("home.html")

# =========================
# OVER ONS PAGINA
# =========================
@app.route("/over-ons")
def over_ons():
    return render_template("over_ons.html")

# =========================
# START APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
