from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import time, json

with open('config.json', 'r') as fh:
	config = json.loads(fh.read())["timerboard"]["database"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:%s@%s/%s' % (config["username"], config["password"], config["host"], config["database"])
db = SQLAlchemy(app)
db.create_all()


class Timer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	system = db.Column(db.String(12))
	planet = db.Column(db.String(6))
	moon = db.Column(db.Integer)
	owner = db.Column(db.String(64))
	time = db.Column(db.DateTime)
	notes = db.Column(db.String(256))

	def __init__(self, system, planet, moon, owner, time, notes):
		self.system = system
		self.planet = planet
		self.moon = moon
		self.owner = owner
		self.time = time
		self.notes = notes

	def __repr__(self):
		return '<Timer %r>' % self.time

	def to_unix_time(self):
		return int(time.mktime(self.time.timetuple()))

	def to_json(self):
		return json.dumps(self.to_dict())

	def to_dict(self):
		return {
			"id": self.id,
			"system": self.system,
			"planet": self.planet,
			"moon": self.moon,
			"owner": self.owner,
			"time": self.to_unix_time(),
			"notes": self.notes
			}
