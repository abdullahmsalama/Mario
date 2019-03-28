To use the code you can install the following:
```
pip install flask_sqlalchemy
pip install flask_marshmallow
pip install marshmallow-sqlalchemy
```
Or install the requirements file using the below command from the terminal
```
pip install -r requirements.txt
```
mario.py expects two inputs, N which is the grid_size and the grid itself containing the princess location as -> ['--m','x-x','--p']
to run mario.py directly, use the below example
```
python mario.py 3 ['--m','x-x','--p']
```
To try the endpoints in the flask application, use the tools for API development such as postman
Run the below command from your terminal
python database_util.py
After this, insert the address in postman http://127.0.0.1:5000/mario
To play the game, send a POST request as the below example
```
{
    "grid_size" : "3",
    "game_grid" : "['--m','x-x','--p']"
}
```
The data saved will include the expected outputs shortest_path and error_flag, and also save the inputs as well as the time of the request as below
```
{
    "error_flag": false,
    "game_grid": "['--m','x-x','--p']",
    "grid_size": 3,
    "log_time": "Thu Mar 28 02:28:24 2019",
    "shortest_path": "[['LEFT', 'DOWN', 'DOWN', 'RIGHT']]"
}
```
You can also retreive all saved tables data by sending a get request
