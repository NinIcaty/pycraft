from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from noise import pnoise2

app = Ursina()
window.fullscreen = True

# ================== MODE ==================
INFINITE_BLOCKS = False   # True = Creative | False = Survival

# ================== SKY ==================
Sky(texture='sky_default')

sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))

AmbientLight(color=color.rgba(200,200,200,0.4))

# ================== PLAYER ==================
player = FirstPersonController()
player.height = 2
player.jump_height = 1.5

death_height = -20

# ================== BLOCK DATA ==================
BLOCK_TYPES = {
    "grass": "grass.png",
    "dirt": "dirt.png",
    "stone": "stone.png"
}

inventory = {
    "grass": 0,
    "dirt": 0,
    "stone": 0
}

boxes = []
selected_slot = 0

# ================== WORLD GEN ==================
WORLD_SIZE = 40
height_map = {}

def get_height(x, z):
    return int(pnoise2(x/25, z/25) * 5 + 10)

def create_block(pos, texture):
    box = Entity(
        model='cube',
        position=pos,
        texture=texture,
        collider='box'
    )
    boxes.append(box)
    return box

for x in range(WORLD_SIZE):
    for z in range(WORLD_SIZE):

        height = get_height(x,z)
        height_map[(x,z)] = height

        create_block((x,height,z), BLOCK_TYPES["grass"])

        for i in range(1,3):
            create_block((x,height-i,z), BLOCK_TYPES["dirt"])

        create_block((x,height-3,z), BLOCK_TYPES["stone"])

def get_spawn():
    h = height_map[(10,10)]
    return Vec3(10, h+2, 10)

player.position = get_spawn()

# ================== HOTBAR ==================
hotbar = Entity(parent=camera.ui, model='quad', scale=(0.6,0.1), position=(0,-0.45), color=color.dark_gray)

slots = []
slot_icons = []
slot_text = []

for i, block in enumerate(BLOCK_TYPES):

    slot = Entity(
        parent=hotbar,
        model='quad',
        scale=(0.18,0.8),
        position=(-0.25 + i*0.25, 0),
        color=color.gray
    )

    icon = Entity(
        parent=slot,
        model='quad',
        texture=BLOCK_TYPES[block],
        scale=(0.6,0.6)
    )

    count = Text(
        parent=slot,
        text="0",
        scale=2,
        position=(0.25,-0.35)
    )

    slots.append(slot)
    slot_icons.append(icon)
    slot_text.append(count)

def update_hotbar():
    keys = list(BLOCK_TYPES.keys())

    for i, key in enumerate(keys):

        if INFINITE_BLOCKS:
            slot_text[i].text = "∞"
        else:
            slot_text[i].text = str(inventory[key])

        slots[i].color = color.white if i == selected_slot else color.gray

update_hotbar()

# ================== MENU ==================
menu_panel = Entity(parent=camera.ui, enabled=False)
Panel(parent=menu_panel, scale=(0.4,0.4), color=color.dark_gray)

resume_button = Button(text="Resume", parent=menu_panel, position=(0,0.1))
quit_button = Button(text="Quit", parent=menu_panel, position=(0,-0.1), color=color.red)

def toggle_menu():
    menu_panel.enabled = not menu_panel.enabled
    mouse.locked = not menu_panel.enabled

resume_button.on_click = toggle_menu
quit_button.on_click = application.quit

# ================== UPDATE ==================
def update():

    if player.y < death_height:
        player.position = get_spawn()

    player.speed = 7 if held_keys['control'] else 5

    update_hotbar()

# ================== INPUT ==================
def input(key):

    global selected_slot

    def dist(a,b):
        return ((a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2)**0.5

    if key == 'escape':
        toggle_menu()

    if menu_panel.enabled:
        return

    keys = list(BLOCK_TYPES.keys())
    block_name = keys[selected_slot]

    # PLACE
    if key == 'left mouse down' and mouse.hovered_entity:

        pos = mouse.hovered_entity.position + mouse.normal

        if dist(player.position,pos) > 5:
            return

        if INFINITE_BLOCKS or inventory[block_name] > 0:

            create_block(pos, BLOCK_TYPES[block_name])

            if not INFINITE_BLOCKS:
                inventory[block_name] -= 1

    # BREAK
    if key == 'right mouse down' and mouse.hovered_entity:

        box = mouse.hovered_entity

        if dist(player.position, box.position) > 5:
            return

        tex = str(box.texture)

        if not INFINITE_BLOCKS:
            if "grass" in tex:
                inventory["grass"] += 1
            elif "dirt" in tex:
                inventory["dirt"] += 1
            elif "stone" in tex:
                inventory["stone"] += 1

        boxes.remove(box)
        destroy(box)

    # HOTBAR SELECT
    if key == '1': selected_slot = 0
    if key == '2': selected_slot = 1
    if key == '3': selected_slot = 2

app.run()
