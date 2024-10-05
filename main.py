from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
app = Ursina()

# Set the game to start in fullscreen
window.fullscreen = True

# Create the player with FirstPersonController and set lower mouse sensitivity
player = FirstPersonController()
player.mouse_sensitivity = Vec2(1, 1)  # Reduce mouse sensitivity
placeBlock = 'dirt.png'
# Create the sky and terrain
Sky()
boxType = random.randint(1,2)
# Creating the platform/terrain
boxes = []
dirtBoxes = []
grassBoxes = []
invetory = {"grass":0,
            "dirt":0}
for i in range(20):
    for j in range(20):
        boxType = random.randint(1,3)
        if boxType == 1:
            boxType = "dirt.png"
        elif boxType == 2 or boxType== 3:
            boxType = "grass.png"
        box = Button(color=color.white, model='cube', position=(j, 0, i),
                    texture=boxType, parent=scene, origin_y=0.5)
        boxes.append(box)
        if boxType == "dirt.png":
            dirtBoxes.append(box)
        if boxType == "grass.png":
            grassBoxes.append(box)

# Death height, set a threshold below which the player "dies"
death_height = -5

# Pause menu (hidden initially)
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
    # Switch game mode button
    #switch_gamemode_button = Button(text="switch gamemode",parent=menu_panel,position=(0,0.2), scale=(0.2, 0.1))
def update():
    # Check if the player has fallen off the platform (below death_height)
    if player.y < death_height:
        print("Player has fallen! Respawning...")
        player.position = (0, 5, 0)  # Respawn player at a safe position
        player.rotation = (0, 0, 0)  # Reset rotation (optional)

def input(key):
    global placeBlock
    global dirtBoxes
    global grassBoxes
    global invetory
    if key == 'escape':
        toggle_menu()  # Show or hide the menu when 'Esc' is pressed

    # Place a block when left mouse is clicked
    if key == 'left mouse down' and not menu_panel.enabled:  # Prevent placing blocks when the menu is open
        if mouse.hovered_entity:  # Check if the mouse is over an entity (a box)
            hovered_box = mouse.hovered_entity
            new_box_position = hovered_box.position + mouse.normal
            if placeBlock == 'dirt.png' and invetory["dirt"] > 0:            #place dirt
                new_box = Button(color=color.white, model='cube', position=new_box_position,
                                texture=placeBlock, parent=scene, origin_y=0.5)
                boxes.append(new_box)
                dirtBoxes.append(new_box)  
                invetory["dirt"] -= 1  
            else:print("No dirt")

            if placeBlock == 'grass.png' and invetory["grass"] > 0:            #place grass
                new_box = Button(color=color.white, model='cube', position=new_box_position,
                                texture=placeBlock, parent=scene, origin_y=0.5)
                boxes.append(new_box)
                grassBoxes.append(new_box)
                invetory["grass"] -= 1    
            else:print("No grass")     
    # Remove a block when right mouse is clicked
    if key == 'right mouse down' and not menu_panel.enabled:  # Prevent removing blocks when the menu is open
        if mouse.hovered_entity:  # Check if the mouse is over an entity (a box)
            hovered_box = mouse.hovered_entity
            if hovered_box in boxes:
                boxes.remove(hovered_box)
                destroy(hovered_box)
                #Get dirt
                if hovered_box in dirtBoxes:
                    dirtBoxes.remove(hovered_box)
                    invetory["dirt"] += 1
                    print("Got dirt", invetory["dirt"])
                #get grass
                if hovered_box in grassBoxes:
                    grassBoxes.remove(hovered_box)
                    invetory["grass"] += 1
                    print("Got grass", invetory["grass"])
    #set placeBlock
    if key == '1':
        placeBlock = 'dirt.png'
        print("placeBlock is dirt")        
    if key == '2':
        placeBlock = 'grass.png'
        print("placeBlock is grass")    
# Create the menu
create_menu()

app.run()
