# Volleyball Team Tuning

Captaining a volleyball team is no easy task, especially when it comes to organizing your players on the court.   
This UI is a simple tool for visualizing and tuning team composition for up to eight players (six players on the court and two on the bench).

## Installation

This is a standalone application that uses native Python packages.  It was written and tested in Python 3.7.
Simply download the 'tuner.py' file and use the appropriate Python version.

## Usage

Run 'tuner.py' in a terminal. 

### Functionality

- Add players using the "Add Players" field. 
- Delete players from the court by right-clicking and selecting "Delete."
- Drag and drop players onto the court. 
- Click "Rotate" to rotate players CW.  
- Click "Reset" 

### Notes

- You cannot add more than eight players to the court at any time.  
- Dragging players past a position occupied by another player temporarily bumps that player from their position.
- Once you drag that player past that position, the original player snaps back into position.  

## Future Improvements

- Tune multiple teams at once.  
- Assign a postion (Setter, Middle, Outside, Opposite) to a player. 
- Leverage ML to automatically populate and balance teams.  