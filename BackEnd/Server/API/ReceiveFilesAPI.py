from flask import Flask, request
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(filename)

    conn = sqlite3.connect('LockBit.db')
    c = conn.cursor()
    c.execute("INSERT INTO Files (Name, Content) VALUES (?, ?)", (filename, file.read()))
    conn.commit()
    conn.close()

    return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
