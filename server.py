from flask import Flask, request, send_file, abort, send_from_directory
from flask_cors import CORS
import tensorflow as tf
from datetime import datetime
import numpy as np
import os
import cv2
import base64
from model.LLE import LLE
from utils.utils import rename, transform

app = Flask(__name__, static_folder="build")
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route("/api", methods=["POST"])
def pixar():
    try:
        print(request.files)

        img_file = request.files["file"]

        filename = img_file.filename
        filename = rename(filename)

        if os.path.exists("./images") == False:
            os.mkdir("./images")

        img_file.save(os.path.join("./images", filename))

    except Exception as error:
        print(error)
        return abort(400)

    else:
        res_path = transform(model, filename, delete_input=True)

        if res_path == "-1":
            return abort(404)

        with open(res_path, "rb") as file:
            encoded = base64.b64encode(file.read())

        return encoded


if __name__ == "__main__":
    # graph = tf.get_default_graph()
    model = LLE(weights='./model/weights.h5')
    app.run(debug=True, port=5000)

