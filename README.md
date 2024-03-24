# About
This is a small game I made for my software engineering course. It has an online score system and leaderboard viewer, multiple users support so you can pass the game to your friends, and some okay gameplay.

In the game you are tasked with landing the lunar excersion module from the Apollo missions on the moon. You have limited fuel and your goal is to land with minimal x and y velocity, with the LEM level. Good luck!

# Setup
Download the repo [here](https://github.com/Kn4ughty/SEASS1/archive/refs/heads/main.zip)
unzip it somewhere

you should probably create a python virtual enviroment but you dont have to.

**Note**

## Unix (Macos)
First cd into the place you downloaded it then run these commands (assuming you have python installed).
The python command might be different depending on your setup, so like try python3 if needed or something.
Setup commands
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Windows (In powershell)
```powershell
python -m venv .venv
```
Then you need to open powershell as administrator and run:
```powershell
Set-ExecutionPolicy Unrestricted
A
```
Then go back to the window from before and run:
```powershell
.venv\Scripts\Activate.ps1
```
Then go back to your administrator window and run:
```powershell
Set-ExecutionPolicy Restricted
pip install -r requirements.txt
```

**Then**

Regarless of operating system you can run: `python test.py` (or `python3 test.py`)


To run the server for local host only run:
```bash
python -m flask --app serv/server.py run
```

To run it so anyone can accsess it. Make sure to install gunicorn.
```bash
gunicorn -w 2 server -b 0.0.0.0:5000
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
| reset | r |
| quit game (anywhere) | escape |

You can scroll the camera in and out with the mouse wheel, but there is no real reason to since the camera manages itself for the most part.
