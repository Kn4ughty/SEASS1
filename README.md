# About
This is a small game I made for my software engineering course. 

# Setup
you should probably create a virtual enviroment but you dont have to.

**Note**
This setup guide is for unix. I dont know if windows is different not my problem.
If it doesnt work look [here](https://docs.python.org/3/library/venv.html).

Setup commands
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

then to run you can just type `python test.py`

To run the server run 
```bash
python -m flask --app server.py run
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
