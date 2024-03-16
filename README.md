# About
This is a small game I made for my software engineering course. 

# Setup
Download the repo [here](https://github.com/Kn4ughty/SEASS1/archive/refs/heads/main.zip)
unzip it somewhere

you should probably create a python virtual enviroment but you dont have to.

**Note**
This setup guide is for unix. I dont know if windows is different not my problem.
If it doesnt work look [here](https://docs.python.org/3/library/venv.html).

First cd into the place you downloaded it then run these commands (assuming you have python installed)
Setup commands
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

then to run you can just type `python test.py`

To run the server in debug mode (doesnt allow other computers to connect, reloads the server as thigns change)
```bash
python -m flask --app serv/server.py run
```

To run the server publically, so everyone on a network can ascces it
```bash
python -m flask --app serv/server.py run --host=0.0.0.0
```


# User guide
On first start, you will be prompted for your name. This will be what is sent to the leaderboard and displayed to other players.
Then in the main menu you can press start game, to as you can guess... start the game.

## Controls

| action       | key(s)   |
| --           | --          |
| steer left   | a, left arrow |
| steer right  | d, right arrow|
| increase throttle | w, up arrow, shift |
| decrease throttle | s, down arrow, l_ctrl |
| shut down engine | x |
| max throttle engine | z |
| reset (**only in show score screen**) | r |
| quit game | escape |
