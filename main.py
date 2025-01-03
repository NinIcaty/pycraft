from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

window.fullscreen = True

player = FirstPersonController()
player.mouse_sensitivity = Vec2(12, 12)  # Sensitivity
player.position = (10, 0, 10)
player.height = 2
player.jump_height = 1.5
placeBlock = 'dirt.png'
player.height = 2
player.jump_height = 1.5

Sky()

# Creating the platform
boxes = []
dirtBoxes = []
grassBoxes = []
stoneBoxes = []
inventory = {"grass": 0, "dirt": 0, "stone": 0}

# Create the terrain
for i in range(30):
    for j in range(30):

        boxType = random.randint(1, 10)
        if boxType == 1 or boxType == 2:
            boxType = "dirt.png"
        elif boxType == 3 or boxType == 4 or boxType == 5 or boxType == 6 or boxType == 7 or boxType == 8 or boxType == 9 or boxType == 10 :
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
        # layer 2
        boxType = random.randint(1, 6)
        if boxType == 1 or boxType == 2 or boxType == 3 or boxType == 4:
            boxType = "dirt.png"
        elif boxType == 5:
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
        # layer 3
        boxType = random.randint(1, 9)
        if boxType == 1 or boxType == 2:
            boxType = "dirt.png"
        elif boxType == 3:
            boxType = "grass.png"
        elif boxType == 6 or boxType == 5 or boxType == 4 or boxType == 7 or boxType == 8 or boxType == 9:
            boxType = "stone.png"

        box = Button(color=color.white, model='cube', position=(j, -2, i),
                     texture=boxType, parent=scene, origin_y=0.5)
        boxes.append(box)

        if boxType == "dirt.png":
            dirtBoxes.append(box)
        elif boxType == "grass.png":
            grassBoxes.append(box)
        elif boxType == "stone.png":
            stoneBoxes.append(box)

death_height = -6

menu_panel = None

def toggle_menu():
    global menu_panel
    if menu_panel.enabled:
        menu_panel.disable()
        mouse.locked = True
    else:
        menu_panel.enable()
        mouse.locked = False

def create_menu():
    global menu_panel
    menu_panel = Entity(parent=camera.ui, enabled=False)
    menu_bg = Panel(parent=menu_panel, scale=(0.5, 0.5), color=color.dark_gray)

    # Quit button
    quit_button = Button(text="Quit", parent=menu_panel, position=(0, -0.1), scale=(0.2, 0.1), color=color.red)
    quit_button.on_click = application.quit

    # Resume button
    resume_button = Button(text="Resume", parent=menu_panel, position=(0, 0.1), scale=(0.2, 0.1))
    resume_button.on_click = toggle_menu

def update():
    if player.y < death_height:
        print("Player has fallen! Respawning...")
        player.position = (10, 1, 10)  # Respawn player
        player.rotation = (0, 0, 0)

    # Sprinting
    if held_keys['control']:
        player.speed = 7.5 # Sprint speed
    else:
        player.speed = 5  # Normal speed

def input(key):
    global placeBlock
    global dirtBoxes
    global grassBoxes
    global stoneBoxes
    global inventory

    def distance_3d(a, b):
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2) ** 0.5

    if key == 'escape':
        toggle_menu()

    # Place block
    if key == 'left mouse down' and not menu_panel.enabled:
        if mouse.hovered_entity:
            hovered_box = mouse.hovered_entity
            new_box_position = hovered_box.position + mouse.normal

            # Distance check
            if distance_3d(player.position, new_box_position) > 5:
                print("Too far to place block.")
                return

            if placeBlock == 'dirt.png' and inventory["dirt"] > 0:  # Place dirt
                new_box = Button(color=color.white, model='cube', position=new_box_position,
                                 texture=placeBlock, parent=scene, origin_y=0.5)
                boxes.append(new_box)
                dirtBoxes.append(new_box)
                inventory["dirt"] -= 1
            elif placeBlock == 'dirt.png':
                print("No dirt")

            if placeBlock == 'grass.png' and inventory["grass"] > 0:  # Place grass
                new_box = Button(color=color.white, model='cube', position=new_box_position,
                                 texture=placeBlock, parent=scene, origin_y=0.5)
                boxes.append(new_box)
                grassBoxes.append(new_box)
                inventory["grass"] -= 1
            elif placeBlock == 'grass.png':
                print("No grass")

            if placeBlock == 'stone.png' and inventory["stone"] > 0:  # Place stone
                new_box = Button(color=color.white, model='cube', position=new_box_position,
                                 texture=placeBlock, parent=scene, origin_y=0.5)
                boxes.append(new_box)
                stoneBoxes.append(new_box)
                inventory["stone"] -= 1
            elif placeBlock == 'stone.png':
                print("No stone")
#Break block
    if key == 'right mouse down' and not menu_panel.enabled:
        if mouse.hovered_entity:
            hovered_box = mouse.hovered_entity

            # Distance check
            if distance_3d(player.position, hovered_box.position) > 5:
                print("Too far to remove block.")
                return

            if hovered_box in boxes:
                boxes.remove(hovered_box)
                destroy(hovered_box)

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


create_menu()

app.run()
