from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# =========================
# DB接続
# =========================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# 一覧表示
# =========================
@app.route("/")
def index():
    conn = get_db()

    spots = conn.execute("""
        SELECT * FROM sightseeing_spots
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template("index.html", spots=spots)


# =========================
# 追加画面表示
# =========================
@app.route("/add", methods=["GET"])
def add_page():
    return render_template("add.html")


# =========================
# 追加処理
# =========================
@app.route("/add", methods=["POST"])
def add_spot():
    name = request.form["name"]
    description = request.form["description"]
    address = request.form["address"]
    price = request.form["price"]
    official_url = request.form["official_url"]

    conn = get_db()

    conn.execute("""
        INSERT INTO sightseeing_spots
        (name, description, address, price, official_url)
        VALUES (?, ?, ?, ?, ?)
    """, (name, description, address, price, official_url))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# =========================
# 削除
# =========================
@app.route("/delete/<int:spot_id>")
def delete_spot(spot_id):
    conn = get_db()

    conn.execute("""
        DELETE FROM sightseeing_spots
        WHERE id = ?
    """, (spot_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


# =========================
# 起動
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5001)