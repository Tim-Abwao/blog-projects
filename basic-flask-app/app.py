from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
fruits = ["Mangoes", "Apples", "Cherries", "Strawberries", "Pears"]


@app.route("/")
def index() -> str:
    """Creates the home-page, with a form to capture user input.

    Returns:
        str: Rendered HTML.
    """
    return render_template(
        "fruits.html", title="ACME Fruit Store", fruit_list=fruits
    )


@app.route("/checkout", methods=["GET", "POST"])
def checkout() -> str:
    """Creates the checkout page that displays user input.

    Returns:
        str: Rendered HTML
    """
    if request.method == "POST":
        basket = request.form.getlist("fruit")

        if not basket:
            basket = ["No fruits selected."]

        return render_template("fruits.html", selection=basket)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
