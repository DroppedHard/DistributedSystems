from flask import Flask, render_template
from services.FOaaS import FOaaS
import json

app = Flask(__name__)

endpoints = FOaaS.getOperations()


@app.route("/")
def index():
    return render_template(
        "index.html",
        endpoints=list(endpoints.keys()),
        endpoint_info=json.dumps(endpoints),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
