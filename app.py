from flask_pymongo import PyMongo
from flask import Flask, render_template
from flask import jsonify
from flask import request
from bson.son import SON
from bson.objectid import ObjectId
from bson.json_util import dumps

application = Flask(__name__)

application.config["MONGO_URI"] = "mongodb+srv://kunwar:kunwar$123@cluster0.z3w9w.mongodb.net/Covid?retryWrites=true&w=majority"

mongo = PyMongo(application)

def parse_json(data):
    return dumps(data)

@application.route('/')
def home():
   return render_template('index.html')

@application.route('/recentstats', methods=['GET'])
def get_recent_covid_stats():
  stats = mongo.db.stats
  output = []
  for s in stats.find().sort('date', -1).limit(10):
    del s['_id']
    output.append(s)
  return jsonify({'result' : output})

@application.route('/allstats', methods=['GET'])
def get_all_covid_stats():
  stats = mongo.db.stats
  output = []
  for s in stats.find().sort('date', -1):
    output.append(parse_json(s))
  return jsonify({'result' : output})

@application.route('/statbyid', methods=['GET'])
def get_id_stats():
  id = request.args.get('id')
  stat = mongo.db.stats.find_one({"_id": ObjectId(id)})
  return jsonify({'result' : parse_json(stat)})

if __name__ == '__main__':
    application.run(debug=True)