from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 仮データ
spots = [
    {
        "id": 1,
        "name": "東京タワー",
        "description": "東京のシンボル",
        "address": "東京都港区芝公園4-2-8",
        "price": "1200円",
        "official_url": "https://www.tokyotower.co.jp/"
    },
    {
        "id": 2,
        "name": "清水寺",
        "description": "京都を代表する観光名所",
        "address": "京都府京都市東山区清水1-294",
        "price": "500円",
        "official_url": "https://www.kiyomizudera.or.jp/"
    }
]


@app.route("/")
def index():
    return render_template("index.html", spots=spots)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        address = request.form["address"]
        price = request.form["price"]
        official_url = request.form["official_url"]

        new_spot = {
            "id": len(spots) + 1,
            "name": name,
            "description": description,
            "address": address,
            "price": price,
            "official_url": official_url
        }

        spots.append(new_spot)

        return redirect(url_for("index"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)