from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/LockBit.db'
db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.String, primary_key=True)
    statement = db.Column(db.Integer)

@app.route('/api', methods=['POST'])
def api():
    id = request.json['id']
    record = Record.query.get(id)
    if record and record.statement == 0:
        record.statement = 1
        db.session.commit()
        return {'value': 1}
    else:
        return {'value': 0}

if __name__ == '__main__':
    app.run(debug=True)
