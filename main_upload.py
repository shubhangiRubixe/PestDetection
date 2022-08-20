
from flask import Flask, render_template, request
import os
from inference import detect_image


UPLOAD_FOLDER = './static'

for f in os.listdir(UPLOAD_FOLDER):
    os.remove(os.path.join(UPLOAD_FOLDER, f))

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def detect(img_path):
    detection = detect_image(img_path)
    return detection

appName = "PestDetection"

# routes
@app.route(f"/{appName}", methods=['GET', 'POST'])
def main():
    return render_template("index_upload.html")


@app.route(f"/{appName}/submit", methods = ['GET', 'POST'])
def get_output():
    
    if request.method == 'POST':
        img = request.files['my_image']
        # print(img)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
        img.save(full_filename)
        # with open('./static/test.jpg', 'wb') as f:
        #     f.read()

        detection= detect(full_filename)
        print(detection)
        # detection.popitem()
        # print(detection)
        return render_template("index_upload.html", prediction = detection, img_path = full_filename)

    else:
        return render_template("index_upload.html")

    



if __name__ =='__main__':
    app.run(host='127.0.0.1', port=5000)
    