from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import time
import mario

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mario_db.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class GameLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_time = db.Column(db.String(120))
    grid_size = db.Column(db.Integer)
    game_grid = db.Column(db.String(120))
    shortest_path = db.Column(db.String(120))
    error_flag = db.Column(db.Boolean)

    def __init__(self, log_time, grid_size, game_grid, shortest_path, error_flag):
        self.log_time = log_time
        self.grid_size = grid_size
        self.game_grid = game_grid
        self.shortest_path = shortest_path
        self.error_flag = error_flag

class GameLogSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('log_time', 'grid_size', 'game_grid', 'shortest_path', 'error_flag')

game_log_schema = GameLogSchema()
games_log_schema = GameLogSchema(many=True)


# endpoint to create new game log
@app.route("/mario", methods=["POST"])
def add_game_log():
    log_time = time.ctime()
    grid_size = request.json['grid_size']
    game_grid = request.json['game_grid']
    shortest_path, error_flag = mario.play(eval(grid_size), eval(game_grid))
    new_log = GameLog(log_time, grid_size, game_grid, str(shortest_path), error_flag)

    db.session.add(new_log)
    db.session.commit()

    return game_log_schema.jsonify(new_log)

# endpoint to show all game logs
@app.route("/mario", methods=["GET"])
def get_game_logs():
    all_logs = GameLog.query.all()
    result = games_log_schema.dump(all_logs)
    return jsonify(result)

# endpoint to get game log by id
@app.route("/mario/<id>", methods=["GET"])
def get_game_logs_by_id(id):
    log = GameLog.query.get(id)
    return game_log_schema.jsonify(log)

if __name__ == '__main__':
    #creates the table
    db.create_all()
    app.run(debug=True)