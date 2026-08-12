from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.config["SECRET_KEY"] = "coffee-hunter-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "coffee_hunter.db"

SAMPLE_COFFEES = [
    {
        "id": 1,
        "name": "Ethiopian Yirgacheffe",
        "origin": "Ethiopia",
        "roast": "Light",
        "flavor": "Floral, citrus, blueberry",
        "description": "A bright and aromatic coffee with delicate floral notes and a juicy finish."
    },
    {
        "id": 2,
        "name": "Colombian Supremo",
        "origin": "Colombia",
        "roast": "Medium",
        "flavor": "Caramel, red fruit, cocoa",
        "description": "Balanced and smooth, with sweet caramel character and a rich cocoa finish."
    },
    {
        "id": 3,
        "name": "Brazil Santos",
        "origin": "Brazil",
        "roast": "Medium",
        "flavor": "Chocolate, nuts, caramel",
        "description": "Comforting and full-bodied with classic chocolate and toasted nut flavors."
    },
    {
        "id": 4,
        "name": "Sumatra Mandheling",
        "origin": "Indonesia",
        "roast": "Dark",
        "flavor": "Earthy, spice, dark chocolate",
        "description": "Deep and syrupy with earthy complexity, gentle spice, and dark chocolate."
    },
    {
        "id": 5,
        "name": "Guatemala Antigua",
        "origin": "Guatemala",
        "roast": "Medium",
        "flavor": "Cocoa, orange, brown sugar",
        "description": "A refined Central American cup with cocoa sweetness and a citrus lift."
    },
    {
        "id": 6,
        "name": "Costa Rica Tarrazú",
        "origin": "Costa Rica",
        "roast": "Light",
        "flavor": "Honey, citrus, stone fruit",
        "description": "Clean and lively with honey-like sweetness and bright stone-fruit acidity."
    },
]


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS collection (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coffee_id INTEGER NOT NULL UNIQUE,
                name TEXT NOT NULL,
                origin TEXT NOT NULL,
                roast TEXT NOT NULL,
                flavor TEXT NOT NULL,
                description TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                notes TEXT DEFAULT '',
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


@app.route("/")
def index():
    query = request.args.get("q", "").strip().lower()

    if query:
        coffees = [
            coffee for coffee in SAMPLE_COFFEES
            if query in coffee["name"].lower()
            or query in coffee["origin"].lower()
            or query in coffee["roast"].lower()
            or query in coffee["flavor"].lower()
        ]
    else:
        coffees = SAMPLE_COFFEES

    with get_db() as conn:
        saved_ids = {
            row["coffee_id"]
            for row in conn.execute("SELECT coffee_id FROM collection")
        }

    return render_template(
        "index.html",
        coffees=coffees,
        query=query,
        saved_ids=saved_ids
    )


@app.route("/save", methods=["POST"])
def save_coffee():
    try:
        coffee_id = int(request.form["coffee_id"])
        rating = int(request.form.get("rating", 5))
    except (ValueError, KeyError):
        flash("Invalid coffee or rating.", "error")
        return redirect(url_for("index"))

    coffee = next((c for c in SAMPLE_COFFEES if c["id"] == coffee_id), None)

    if coffee is None:
        flash("Coffee not found.", "error")
        return redirect(url_for("index"))

    rating = max(1, min(5, rating))
    notes = request.form.get("notes", "").strip()

    with get_db() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO collection
            (coffee_id, name, origin, roast, flavor, description, rating, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coffee["id"],
            coffee["name"],
            coffee["origin"],
            coffee["roast"],
            coffee["flavor"],
            coffee["description"],
            rating,
            notes
        ))
        conn.commit()

    flash(f'{coffee["name"]} was added to your collection.', "success")
    return redirect(url_for("collection"))


@app.route("/collection")
def collection():
    with get_db() as conn:
        coffees = conn.execute("""
            SELECT *
            FROM collection
            ORDER BY saved_at DESC
        """).fetchall()

    return render_template("collection.html", coffees=coffees)


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_coffee(item_id):
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM collection WHERE id = ?",
            (item_id,)
        )
        conn.commit()

    if cursor.rowcount:
        flash("Coffee removed from your collection.", "success")
    else:
        flash("Collection item not found.", "error")

    return redirect(url_for("collection"))


@app.context_processor
def inject_year():
    from datetime import datetime
    return {"current_year": datetime.now().year}


init_db()

if __name__ == "__main__":
    app.run(debug=True)
