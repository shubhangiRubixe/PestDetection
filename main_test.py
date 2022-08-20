
from flask import Flask, render_template, request
import os
from testcv2 import get_op
import cv2


UPLOAD_FOLDER = './static'

for f in os.listdir(UPLOAD_FOLDER):
    os.remove(os.path.join(UPLOAD_FOLDER, f))

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index_upload.html")


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
    
    if request.method == 'POST':
        img = request.files['my_image']
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
        img.save('./static/test.jpg')
        # new_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'test.jpg')
        # os.rename(full_filename,new_filename)
        
        # cv2.imwrite(r'C:\Users\Datamites\Downloads\tfod-v2-maskrcnn-deploy\tfod-v2-maskrcnn-deploy\static\test.jpg', img)
        get_op()

        # image_op = os.listdir(r"C:/Users/Datamites/Downloads/tfod-v2-maskrcnn-deploy/tfod-v2-maskrcnn-deploy/static/output.jpg")
        # full_filename=r'C:\Users\Datamites\Downloads\tfod-v2-maskrcnn-deploy\tfod-v2-maskrcnn-deploy\test_cv\output.jpg'
        # pic_filename = os.path.join(full_filenamepeople_dir, "output.jpg")


        
        
      
        return render_template("index_upload.html",prediction='done')

    else:
        return render_template("index_upload.html")

    



if __name__ =='__main__':
    app.run(host='127.0.0.1', port=5000)
    