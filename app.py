from flask import Flask, render_template, request, session
import os
from werkzeug.utils import secure_filename
 
#*** Backend operation
 
# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('static', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__)
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'
 
 
@app.route('/')
def index():
    return render_template('index.html')
# app.add_url_rule('/home', '/sample', index)


 
@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        print('uploaded_img',uploaded_img)
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        print('img_filename',img_filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        session['input_image_file_name']=img_filename
        print('your session output',session['uploaded_img_file_path'])
        return render_template('next_page.html')
 
@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)
    print(img_file_path)
    img_filename = session.get('input_image_file_name')
    print(img_filename)
    # Display image in Flask application web page
    return render_template('show_image.html', user_image = img_file_path,img_filename = img_filename )
 
if __name__=='__main__':
    app.run(debug = True)