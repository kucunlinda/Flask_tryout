from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "geheim_voor_flash_berichten"  # nodig voor flash()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # hier zou je normaal de mail versturen naar kucunlinda@gmail.com
        # Voor nu tonen we alleen een klein bedankbericht
        first_name = request.form.get("first_name")
        flash(f"Bedankt voor je bericht, {first_name}!", "success")
        return redirect(url_for("home"))

    return render_template("home.html")


@app.route("/over-ons")
def over_ons():
    return render_template("over_ons.html")


if __name__ == "__main__":
    app.run(debug=True)
