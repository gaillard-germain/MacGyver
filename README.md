# MacGyver

MacGyver is a game that i created for my third project in my OpenClassRooms formation.  
it use python 3.8 and pygame 2.0.0.dev6 (use pip install requirement.txt to install it in your python3 venv)  
**! at this time pygame 2.0.0.dev6 is the only version supported in a python3.8 virtual environment.**

##About the structure

The game's maze is create with the structure.txt file. It must have 15 lines and 15 characters.  
'w' = wall  
' ' = corridor  
's' = start position  
'e' = end (position to reach)  
'g' = guard  
**! Only 1 guard, 1 start and 1 end.**  
So, you can modify it to create your own map.  

##About Graphism

Images are from resources given with the project's instructions (https://s3-eu-west-1.amazonaws.com/course.oc-static.com/projects/macgyver_ressources.zip), but i allowed myself to modified and create some with Gimp. Just to get it prettier...

##About the game  

main function is in macgyver.py  
**To launch the game : python3 macgyver.py**  

Use Arrow keys to move MacGyver.  
To win you need to : grab the 3 components (appears randomly in the maze) to make a syringe, go drug the guard and escape.  
If you try to pass the guard without the syringe, you'll lose.  
