from __main__ import app, stderr, request
@app.route("/medic_details", methods = ["POST, GET"])
def merge():
    if request.method == "POST":
        pass