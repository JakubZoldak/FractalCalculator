from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
import os
import BoxCnt   # python script where Box Counting in ImageJ is done

UPLOAD_FOLDER = './Images'
ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['SECRET_KEY'] = 'edlhnv#</?oa@;amdol{]}[BBM' #to make your app safe, choose your secret key which nobody knows
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and not allowed_file(file.filename):
            flash(f'Wrong type of file, please use one of types {ALLOWED_EXTENSIONS}')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image succesfully on server')
            global address
            address = UPLOAD_FOLDER+'/'+'{}'.format(file.filename)
            dim = BoxCnt.DimensionCalculator(address)
            flash(f'Box Counting dimension of '+'{}'.format(file.filename) + f' is {dim}')
            return redirect(url_for('results'))
    return render_template('calculator.html')

@app.route('/result', methods=['GET', 'POST'])
def results():
    os.remove(address)  # delete analyzed image on server
    return render_template('results.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0') #this set up allows all the users in local network connect to the app, for "privat" usage set e.g. host = '127.0.0.1'

#Mainly from: https://www.quora.com/How-do-I-save-an-image-in-a-file-using-Flask