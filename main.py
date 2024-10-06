from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Set the game to start in fullscreen
window.fullscreen = True

# Create the player with FirstPersonController and set lower mouse sensitivity
player = FirstPersonController()
player.mouse_sensitivity = Vec2(1, 1)  # Reduce mouse sensitivity
player.position = (10, 0, 10)  # Set player position to the center of the terrain

placeBlock = 'dirt.png'

# Create the sky and terrain
Sky()

# Creating the platform/terrain
boxes = []
dirtBoxes = []
grassBoxes = []
stoneBoxes = []
inventory = {"grass": 0, "dirt": 0, "stone": 0}

# Create the terrain
for i in range(20):
    for j in range(20):
        
        boxType = random.randint(1, 6)
        if boxType == 1 or boxType == 2:
            boxType = "dirt.png"
        elif boxType == 3 or boxType == 4 or boxType == 5:
            boxType = "grass.png"
        elif boxType == 6:
            boxType = "stone.png"
        
        box = Button(color=color.white, model='cube', position=(j, 0, i),
                     texture=boxType, parent=scene, origin_y=0.5)
        boxes.append(box)
        
        if boxType == "dirt.png":
            dirtBoxes.append(box)
        elif boxType == "grass.png":
            grassBoxes.append(box)
        elif boxType == "stone.png":
            stoneBoxes.append(box)
        #layer 2
        boxType = random.randint(1, 6)
        if boxType == 1 or boxType == 2:
            boxType = "dirt.png"
        elif boxType == 3 or boxType == 4 or boxType == 5:
            boxType = "grass.png"
        elif boxType == 6:
            boxType = "stone.png"
        
        box = Button(color=color.white, model='cube', position=(j, -1, i),
                     texture=boxType, parent=scene, origin_y=0.5)
        boxes.append(box)
        
        if boxType == "dirt.png":
            dirtBoxes.append(box)
        elif boxType == "grass.png":
            grassBoxes.append(box)
        elif boxType == "stone.png":
            stoneBoxes.append(box)
        #layer 3
        boxType = random.randint(1, 6)
        if boxType == 1 or boxType == 2:
            boxType = "dirt.png"
        elif boxType == 3 or boxType == 4 or boxType == 5:
            boxType = "grass.png"
        elif boxType == 6:
            boxType = "stone.png"
        
        box = Button(color=color.white, model='cube', position=(j, -3, i),
                     texture=boxType, parent=scene, origin_y=0.5)
        boxes.append(box)
        
        if boxType == "dirt.png":
            dirtBoxes.append(box)
        elif boxType == "grass.png":
            grassBoxes.append(box)
        elif boxType == "stone.png":
            stoneBoxes.append(box)

# Death height player dies at y -6
death_height = -6

# Pause menu ,hide menu panel
menu_panel = None

def toggle_menu():
    global menu_panel
    if menu_panel.enabled:
        menu_panel.disable()  # Hide the menu
        mouse.locked = True  # Resume the game, lock the mouse
    else:
        menu_panel.enable()  # Show the menu
        mouse.locked = False  # Unlock the mouse to interact with the menu

def create_menu():
    global menu_panel
    menu_panel = Entity(parent=camera.ui, enabled=False)
    menu_bg = Panel(parent=menu_panel, scale=(0.5, 0.5), color=color.dark_gray)
    
    # Quit button
    quit_button = Button(text="Quit", parent=menu_panel, position=(0, -0.1), scale=(0.2, 0.1), color=color.red)
    quit_button.on_click = application.quit  # Quit the game when clicked

    # Resume button
    resume_button = Button(text="Resume", parent=menu_panel, position=(0, 0.1), scale=(0.2, 0.1))
    resume_button.on_click = toggle_menu  # Hide the menu and resume the game when clicked

def update():
    # Check if the player has fallen off the platform (below death_height)
    if player.y < death_height:
        print("Player has fallen! Respawning...")
        player.position = (10, 1, 10)  # Respawn player
        player.rotation = (0, 0, 0)  

def input(key):
    global placeBlock
    global dirtBoxes
    global grassBoxes
    global stoneBoxes
    global inventory
    
    if key == 'escape':
        toggle_menu()  # Show or hide the menu when Esc is presed

    # Place  block command
    if key == 'left mouse down' and not menu_panel.enabled:  # Prevent placing blocks when the menu is open
        if mouse.hovered_entity:  # Check if the mouse is over an entity (a box)
            hovered_box = mouse.hovered_entity
            new_box_position = hovered_box.position + mouse.normal
            
            if placeBlock == 'dirt.png' and inventory["dirt"] > 0:  # place dirt
                new_box = Button(color=color.white, model='cube', position=new_box_position,
                                 texture=placeBlock, parent=scene, origin_y=0.5)
                boxes.append(new_box)
                dirtBoxes.append(new_box)  
                inventory["dirt"] -= 1  
            else:
                print("No dirt")

            if placeBlock == 'grass.png' and inventory["grass"] > 0:  # place grass
                new_box = Button(color=color.white, model='cube', position=new_box_position,
                                 texture=placeBlock, parent=scene, origin_y=0.5)
                boxes.append(new_box)
                grassBoxes.append(new_box)
                inventory["grass"] -= 1    
            else:
                print("No grass")

            if placeBlock == 'stone.png' and inventory["stone"] > 0:  # place stone
                new_box = Button(color=color.white, model='cube', position=new_box_position,
                                 texture=placeBlock, parent=scene, origin_y=0.5)
                boxes.append(new_box)
                stoneBoxes.append(new_box)
                inventory["stone"] -= 1    
            else:
                print("No stone")     
                
    # Remove  block 
    if key == 'right mouse down' and not menu_panel.enabled:  # Prevent removing blocks when the menu is open
        if mouse.hovered_entity:  # Check if the mouse is over an entity (a box)
            hovered_box = mouse.hovered_entity
            if hovered_box in boxes:
                boxes.remove(hovered_box)
                destroy(hovered_box)
                
                # Update inventory based on the removed block
                if hovered_box in dirtBoxes:
                    dirtBoxes.remove(hovered_box)
                    inventory["dirt"] += 1
                    print("Got dirt", inventory["dirt"])
                if hovered_box in grassBoxes:
                    grassBoxes.remove(hovered_box)
                    inventory["grass"] += 1
                    print("Got grass", inventory["grass"])
                if hovered_box in stoneBoxes:
                    stoneBoxes.remove(hovered_box)
                    inventory["stone"] += 1
                    print("Got stone", inventory["stone"])

    # Set placeBlock
    if key == '1':
        placeBlock = 'dirt.png'
        print("placeBlock is dirt")        
    if key == '2':
        placeBlock = 'grass.png'
        print("placeBlock is grass")    
    if key == '3':
        placeBlock = 'stone.png'
        print("placeBlock is stone") 

# Create the menu
create_menu()

app.run()
