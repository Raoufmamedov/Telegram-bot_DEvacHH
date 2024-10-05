from flask import Flask, send_file
import pandas as pd
import os
import logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/Salgrade', methods=['GET'])
def get_sg():
    df = pd.read_csv("./grades&sals.csv")
    jsonite = df.to_json(orient='records')
    return jsonite


@app.route('/Salexp', methods=['GET'])
def get_se():
    df = pd.read_csv("./data-engineer_mnmxrursal_exper_("
                     "minmaxmed).csv")
    jsonite = df.to_json(orient='records')
    return jsonite


@app.route('/box', methods=['GET'])
def get_histogram():
    file_path = "./max_sal_rur.png"
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/png')
    else:
        return "Гистограмма не найдена.", 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
