from flask import Flask, request, redirect, render_template_string, send_from_directory, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# HTML template as a string with added CSS for styling
html_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>File Upload</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f8f9fa;
        color: #343a40;
        margin: 0;
        padding: 20px;
      }
      .container {
        max-width: 600px;
        margin: auto;
        padding: 20px;
        background-color: #ffffff;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
      }
      h1 {
        color: #007bff;
      }
      form {
        margin-bottom: 20px;
      }
      input[type="file"] {
        display: block;
        margin-bottom: 10px;
      }
      input[type="submit"] {
        background-color: #007bff;
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        cursor: pointer;
      }
      input[type="submit"]:hover {
        background-color: #0056b3;
      }
      h2 {
        margin-top: 40px;
        color: #343a40;
      }
      ul {
        list-style-type: none;
        padding: 0;
      }
      li {
        background-color: #f1f1f1;
        margin: 5px 0;
        padding: 10px;
        border-radius: 4px;
      }
      a {
        text-decoration: none;
        color: #007bff;
      }
      a:hover {
        text-decoration: underline;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Upload a File</h1>
      <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
      </form>
      <h2>Uploaded Files</h2>
      <ul>
        {% for file in files %}
        <li><a href="{{ url_for('uploaded_file', filename=file) }}">{{ file }}</a></li>
        {% endfor %}
      </ul>
    </div>
  </body>
</html>
'''

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(html_template, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
