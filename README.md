# Autostart-click
Code that can automatically start programs and execute mouse clicks

# Guten Morgen Launcher lets you:
Add any programs you want to start in the morning (or whenever).  
Set multiple click positions for each program (e.g. to skip popups or log in).  
Launch them all in order with a delay in between.  
Automatically simulate mouse clicks using pyautogui.  

# How to use it
Run the script with Python.  
Click "Programm hinzufügen" to add apps (e.g. Discord, Spotify, etc.).  
Select a program and click "Klickposition(en) hinzufügen" — you have 5 seconds to move your mouse where it should click.  
Set a delay between program launches (in seconds).  
Click "Alle Programme starten" to run them all one after another, with your saved clicks.  

# Saving data
%USERPROFILE%\GutenMorgenLauncher\programs.json on Windows  
Or the home folder equivalent on other systems  

# Notes
This is just a personal/fun automation helper.  
pyautogui simulates real mouse clicks — the window you’re clicking must be visible and not covered.  
Make sure "Always on Top" is disabled, or the clicks won't work properly.  
