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
# DB処理（分離）
# =========================
def get_all_spots():
    conn = get_db()
    spots = conn.execute("""
        SELECT * FROM sightseeing_spots
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return spots


def insert_spot(name, description, address, price, official_url):
    conn = get_db()
    conn.execute("""
        INSERT INTO sightseeing_spots
        (name, description, address, price, official_url)
        VALUES (?, ?, ?, ?, ?)
    """, (name, description, address, price, official_url))
    conn.commit()
    conn.close()


def delete_spot_db(spot_id):
    conn = get_db()
    conn.execute("""
        DELETE FROM sightseeing_spots
        WHERE id = ?
    """, (spot_id,))
    conn.commit()
    conn.close()


# =========================
# バリデーション
# =========================
def validate_spot_form(name, description, address):
    if not name or not description or not address:
        return False
    return True


# =========================
# ルート：一覧
# =========================
@app.route("/")
def index():
    spots = get_all_spots()
    return render_template("index.html", spots=spots)


# =========================
# 追加
# =========================
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        address = request.form.get("address", "").strip()
        price = request.form.get("price", "").strip()
        official_url = request.form.get("official_url", "").strip()

        # バリデーション
        if not validate_spot_form(name, description, address):
            return "必須項目が空です（名前・説明・住所）", 400

        insert_spot(name, description, address, price, official_url)

        return redirect(url_for("index"))

    return render_template("add.html")


# =========================
# 削除
# =========================
@app.route("/delete/<int:spot_id>")
def delete(spot_id):
    delete_spot_db(spot_id)
    return redirect(url_for("index"))


# =========================
# エラーハンドリング
# =========================
@app.errorhandler(404)
def not_found(e):
    return "ページが見つかりません", 404


@app.errorhandler(500)
def server_error(e):
    return "サーバーエラーが発生しました", 500


# =========================
# 起動
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5001)