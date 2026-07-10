from flask import Flask, render_template, redirect, url_for, flash, request
import nasa_api
import database
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = "space_app_secret"

database.create_tables()

# ─────────────────────────────────────────
# HOME — Today's APOD
# ─────────────────────────────────────────
@app.route("/")
def home():
    today = str(date.today())
    apod = database.get_apod_by_date(today)
    if not apod:
        apod = nasa_api.get_today_apod()
        if apod:
            database.save_apod(apod)
        else:
            flash("Could not fetch today's APOD. Check your internet connection.", "error")
            return render_template("index.html", apod=None, is_fav=False)

    is_fav = database.is_favourite(apod["id"]) if apod.get("id") else False
    return render_template("index.html", apod=apod, is_fav=is_fav)


# ─────────────────────────────────────────
# GALLERY — Last 30 Days
# ─────────────────────────────────────────
@app.route("/gallery")
def gallery():
    # Fetch last 30 days from NASA and save to DB
    apods = nasa_api.get_last_30_days()
    if apods:
        for apod in apods:
            database.save_apod(apod)

    # Get all from DB
    all_apods = database.get_all_apods()
    return render_template("gallery.html", apods=all_apods)


# ─────────────────────────────────────────
# FAVOURITES
# ─────────────────────────────────────────
@app.route("/favourites")
def favourites():
    favs = database.get_favourites()
    return render_template("favourites.html", favs=favs)

@app.route("/add_favourite/<int:apod_id>")
def add_favourite(apod_id):
    result = database.add_favourite(apod_id)
    if result == "added":
        flash("Added to favourites! ❤️", "success")
    elif result == "already":
        flash("Already in your favourites!", "error")
    return redirect(request.referrer or url_for("home"))

@app.route("/remove_favourite/<int:apod_id>")
def remove_favourite(apod_id):
    database.remove_favourite(apod_id)
    flash("Removed from favourites!", "error")
    return redirect(url_for("favourites"))


# ─────────────────────────────────────────
# SEARCH
# ─────────────────────────────────────────
@app.route("/search")
def search():
    keyword = request.args.get("q", "").strip()
    results = []
    if keyword:
        database.save_search(keyword)
        results = database.search_apods(keyword)
    return render_template("search.html", results=results, keyword=keyword)


# ─────────────────────────────────────────
# STATS
# ─────────────────────────────────────────
@app.route("/stats")
def stats():
    data = database.get_stats()
    return render_template("stats.html", stats=data)


if __name__ == "__main__":
    app.run(debug=True)
