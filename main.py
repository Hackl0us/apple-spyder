import logging

import flask

import airpods_update_detection
import software_update_rss

app = flask.Flask(__name__)
app.config["DEBUG"] = False

logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['GET'])
def api_welcome():
    return flask.render_template('index.html')


@app.route('/apple-spyder/software-release', methods=['GET'])
def api_check_software_release():
    software_update_rss.main()
    return "Done"


@app.route('/apple-spyder/accessory-ota-update', methods=['GET'])
def api_check_accessory_ota_update():
    airpods_update_detection.main()
    return "Done"


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8888)
