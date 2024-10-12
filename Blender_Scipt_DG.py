import bpy
import math
import random
from mathutils import Euler, Vector
from pathlib import Path
import bpy_extras

def randomly_rotate_object(obj_to_change):
    """
    Applies random rotation to the object
    """
    random_rot = (0, 0, random.random() * 2 * math.pi)
    obj_to_change.rotation_euler = Euler(random_rot, 'XYZ')

def randomly_position_object(obj_to_change, position_range, existing_positions, min_distance):
    """
    Applies random position to the object within the given range, ensuring no overlap
    """
    while True:
        random_pos = (
            random.uniform(position_range[0][0], position_range[0][1]),
            random.uniform(position_range[1][0], position_range[1][1]),
            random.uniform(position_range[2][0], position_range[2][1])
        )
        
        # Check for overlap
        overlap = False
        for pos in existing_positions:
            distance = math.sqrt(sum((random_pos[i] - pos[i])**2 for i in range(3)))
            if distance < min_distance:
                overlap = True
                break
        
        if not overlap:
            obj_to_change.location = random_pos
            existing_positions.append(random_pos)
            break

def apply_texture(obj, image_path):
    """
    Applies a texture to an object
    """
    # Get the material or create one if it doesn't exist
    if len(obj.data.materials) == 0:
        mat = bpy.data.materials.new(name="FlagMaterial")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]

    # Enable 'Use Nodes'
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)

    # Create Principled BSDF node
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = 0, 0

    # Create Material Output node
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = 400, 0

    # Link BSDF to Material Output
    mat.node_tree.links.new(bsdf.outputs['BSDF'], material_output.inputs['Surface'])

    # Create Image Texture node
    tex_image = nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load(image_path)
    tex_image.location = -400, 0

    # Link Image Texture to BSDF
    mat.node_tree.links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])

def calculate_bounding_box(obj, scene, camera):
    """
    Calculate the bounding box of the object in the rendered image in YOLO format.
    """
    # Get the bounding box coordinates in world space
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    # Get the 2D coordinates in the image space
    render = scene.render
    bbox_2d = [bpy_extras.object_utils.world_to_camera_view(scene, camera, coord) for coord in bbox_corners]

    # Normalize coordinates to image size and flip the y-coordinate
    resolution_x = render.resolution_x
    resolution_y = render.resolution_y
    bbox_2d = [(coord.x, 1.0 - coord.y) for coord in bbox_2d]

    # Find the bounding box edges
    min_x = min(coord[0] for coord in bbox_2d)
    max_x = max(coord[0] for coord in bbox_2d)
    min_y = min(coord[1] for coord in bbox_2d)
    max_y = max(coord[1] for coord in bbox_2d)

    # Calculate the center, width, and height of the bounding box
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max_x - min_x
    height = max_y - min_y

    return center_x, center_y, width, height

def randomly_adjust_camera_height(camera, height_range):
    """
    Adjust the camera height randomly within the given range
    """
    camera.location.z = random.uniform(height_range[0], height_range[1])

# Paths to the flag textures
flag_textures = {

  "Afghanistan": (r"D:\Flags\Afghanistan.png", 0),
    "Albania": (r"D:\Flags\Albania.png", 1),
    "Algeria": (r"D:\Flags\Algeria.png", 2),
    "Andorra": (r"D:\Flags\Andorra.png", 3),
    "Angola": (r"D:\Flags\Angola.png", 4),
    "Antigua and Barbuda": (r"D:\Flags\Antigua_and_Barbuda.png", 5),
    "Argentina": (r"D:\Flags\Argentina.png", 6),
    "Armenia": (r"D:\Flags\Armenia.png", 7),
    "Australia": (r"D:\Flags\Australia.png", 8),
    "Austria": (r"D:\Flags\Austria.png", 9),
    "Azerbaijan": (r"D:\Flags\Azerbaijan.png", 10),
    "Bahamas": (r"D:\Flags\Bahamas.png", 11),
    "Bahrain": (r"D:\Flags\Bahrain.png", 12),
    "Bangladesh": (r"D:\Flags\Bangladesh.png", 13),
    "Barbados": (r"D:\Flags\Barbados.png", 14),
    "Belarus": (r"D:\Flags\Belarus.png", 15),
    "Belgium": (r"D:\Flags\Belgium.png", 16),
    "Belize": (r"D:\Flags\Belize.png", 17),
    "Benin": (r"D:\Flags\Benin.png", 18),
    "Bhutan": (r"D:\Flags\Bhutan.png", 19),
    "Bolivia": (r"D:\Flags\Bolivia.png", 20),
    "Bosnia and Herzegovina": (r"D:\Flags\Bosnia_and_Herzegovina.png", 21),
    "Botswana": (r"D:\Flags\Botswana.png", 22),
    "Brazil": (r"D:\Flags\Brazil.png", 23),
    "Brunei": (r"D:\Flags\Brunei.png", 24),
    "Bulgaria": (r"D:\Flags\Bulgaria.png", 25),
    "Burkina Faso": (r"D:\Flags\Burkina_Faso.png", 26),
    "Burundi": (r"D:\Flags\Burundi.png", 27),
    "Cabo Verde": (r"D:\Flags\Cabo_Verde.png", 28),
    "Cambodia": (r"D:\Flags\Cambodia.png", 29),
    "Cameroon": (r"D:\Flags\Cameroon.png", 30),
    "Canada": (r"D:\Flags\Canada.png", 31),
    "Central African Republic": (r"D:\Flags\Central_African_Republic.png", 32),
    "Chad": (r"D:\Flags\Chad.png", 33),
    "Chile": (r"D:\Flags\Chile.png", 34),
    "China": (r"D:\Flags\China.png", 35),
    "Colombia": (r"D:\Flags\Colombia.png", 36),
    "Comoros": (r"D:\Flags\Comoros.png", 37),
    "Congo, Democratic Republic of the": (r"D:\Flags\Congo_Democratic_Republic_of_the.png", 38),
    "Congo, Republic of the": (r"D:\Flags\Congo_Republic_of_the.png", 39),
    "Costa Rica": (r"D:\Flags\Costa_Rica.png", 40),
    "Croatia": (r"D:\Flags\Croatia.png", 41),
    "Cuba": (r"D:\Flags\Cuba.png", 42),
    "Cyprus": (r"D:\Flags\Cyprus.png", 43),
    "Czech Republic": (r"D:\Flags\Czech_Republic.png", 44),
    "Denmark": (r"D:\Flags\Denmark.png", 45),
    "Djibouti": (r"D:\Flags\Djibouti.png", 46),
    "Dominica": (r"D:\Flags\Dominica.png", 47),
    "Dominican Republic": (r"D:\Flags\Dominican_Republic.png", 48),
    "East Timor (Timor-Leste)": (r"D:\Flags\East_Timor.png", 49),
    "Ecuador": (r"D:\Flags\Ecuador.png", 50),
    "Egypt": (r"D:\Flags\Egypt.png", 51),
    "El Salvador": (r"D:\Flags\El_Salvador.png", 52),
    "Equatorial Guinea": (r"D:\Flags\Equatorial_Guinea.png", 53),
    "Eritrea": (r"D:\Flags\Eritrea.png", 54),
    "Estonia": (r"D:\Flags\Estonia.png", 55),
    "Eswatini": (r"D:\Flags\Eswatini.png", 56),
    "Ethiopia": (r"D:\Flags\Ethiopia.png", 57),
    "Fiji": (r"D:\Flags\Fiji.png", 58),
    "Finland": (r"D:\Flags\Finland.png", 59),
    "France": (r"D:\Flags\France.png", 60),
    "Gabon": (r"D:\Flags\Gabon.png", 61),
    "Gambia": (r"D:\Flags\Gambia.png", 62),
    "Georgia": (r"D:\Flags\Georgia.png", 63),
    "Germany": (r"D:\Flags\Germany.png", 64),
    "Ghana": (r"D:\Flags\Ghana.png", 65),
    "Greece": (r"D:\Flags\Greece.png", 66),
    "Grenada": (r"D:\Flags\Grenada.png", 67),
    "Guatemala": (r"D:\Flags\Guatemala.png", 68),
    "Guinea": (r"D:\Flags\Guinea.png", 69),
    "Guinea_Bissau": (r"D:\Flags\Guinea_Bissau.png", 70),
    "Guyana": (r"D:\Flags\Guyana.png", 71),
    "Haiti": (r"D:\Flags\Haiti.png", 72),
    "Honduras": (r"D:\Flags\Honduras.png", 73),
    "Hungary": (r"D:\Flags\Hungary.png", 74),
    "Iceland": (r"D:\Flags\Iceland.png", 75),
    "India": (r"D:\Flags\India.png", 76),
    "Indonesia": (r"D:\Flags\Indonesia.png", 77),
    "Iran": (r"D:\Flags\Iran.png", 78),
    "Iraq": (r"D:\Flags\Iraq.png", 79),
    "Ireland": (r"D:\Flags\Ireland.png", 80),
    "Israel": (r"D:\Flags\Israel.png", 81),
    "Italy": (r"D:\Flags\Italy.png", 82),
    "Jamaica": (r"D:\Flags\Jamaica.png", 83),
    "Japan": (r"D:\Flags\Japan.png", 84),
    "Jordan": (r"D:\Flags\Jordan.png", 85),
    "Kazakhstan": (r"D:\Flags\Kazakhstan.png", 86),
    "Kenya": (r"D:\Flags\Kenya.png", 87),
    "Kiribati": (r"D:\Flags\Kiribati.png", 88),
    "Korea, North": (r"D:\Flags\Korea_North.png", 89),
    "Korea, South": (r"D:\Flags\Korea_South.png", 90),
    "Kosovo": (r"D:\Flags\Kosovo.png", 91),
    "Kuwait": (r"D:\Flags\Kuwait.png", 92),
    "Kyrgyzstan": (r"D:\Flags\Kyrgyzstan.png", 93),
    "Laos": (r"D:\Flags\Laos.png", 94),
    "Latvia": (r"D:\Flags\Latvia.png", 95),
    "Lebanon": (r"D:\Flags\Lebanon.png", 96),
    "Lesotho": (r"D:\Flags\Lesotho.png", 97),
    "Liberia": (r"D:\Flags\Liberia.png", 98),
    "Libya": (r"D:\Flags\Libya.png", 99),
    "Liechtenstein": (r"D:\Flags\Liechtenstein.png", 100),
    "Lithuania": (r"D:\Flags\Lithuania.png", 101),
    "Luxembourg": (r"D:\Flags\Luxembourg.png", 102),
    "Madagascar": (r"D:\Flags\Madagascar.png", 103),
    "Malawi": (r"D:\Flags\Malawi.png", 104),
    "Malaysia": (r"D:\Flags\Malaysia.png", 105),
    "Maldives": (r"D:\Flags\Maldives.png", 106),
    "Mali": (r"D:\Flags\Mali.png", 107),
    "Malta": (r"D:\Flags\Malta.png", 108),
    "Marshall Islands": (r"D:\Flags\Marshall_Islands.png", 109),
    "Mauritania": (r"D:\Flags\Mauritania.png", 110),
    "Mauritius": (r"D:\Flags\Mauritius.png", 111),
    "Mexico": (r"D:\Flags\Mexico.png", 112),
    "Micronesia": (r"D:\Flags\Micronesia.png", 113),
    "Moldova": (r"D:\Flags\Moldova.png", 114),
    "Monaco": (r"D:\Flags\Monaco.png", 115),
    "Mongolia": (r"D:\Flags\Mongolia.png", 116),
    "Montenegro": (r"D:\Flags\Montenegro.png", 117),
    "Morocco": (r"D:\Flags\Morocco.png", 118),
    "Mozambique": (r"D:\Flags\Mozambique.png", 119),
    "Myanmar (Burma)": (r"D:\Flags\Myanmar.png", 120),
    "Namibia": (r"D:\Flags\Namibia.png", 121),
    "Nauru": (r"D:\Flags\Nauru.png", 122),
    "Nepal": (r"D:\Flags\Nepal.png", 123),
    "Netherlands": (r"D:\Flags\Netherlands.png", 124),
    "New Zealand": (r"D:\Flags\New_Zealand.png", 125),
    "Nicaragua": (r"D:\Flags\Nicaragua.png", 126),
    "Niger": (r"D:\Flags\Niger.png", 127),
    "Nigeria": (r"D:\Flags\Nigeria.png", 128),
    "North Macedonia": (r"D:\Flags\North_Macedonia.png", 129),
    "Norway": (r"D:\Flags\Norway.png", 130),
    "Oman": (r"D:\Flags\Oman.png", 131),
    "Pakistan": (r"D:\Flags\Pakistan.png", 132),
    "Palau": (r"D:\Flags\Palau.png", 133),
    "Palestine": (r"D:\Flags\Palestine.png", 134),
    "Panama": (r"D:\Flags\Panama.png", 135),
    "Papua New Guinea": (r"D:\Flags\Papua_New_Guinea.png", 136),
    "Paraguay": (r"D:\Flags\Paraguay.png", 137),
    "Peru": (r"D:\Flags\Peru.png", 138),
    "Philippines": (r"D:\Flags\Philippines.png", 139),
    "Poland": (r"D:\Flags\Poland.png", 140),
    "Portugal": (r"D:\Flags\Portugal.png", 141),
    "Qatar": (r"D:\Flags\Qatar.png", 142),
    "Romania": (r"D:\Flags\Romania.png", 143),
    "Russia": (r"D:\Flags\Russia.png", 144),
    "Rwanda": (r"D:\Flags\Rwanda.png", 145),
    "Saint Kitts and Nevis": (r"D:\Flags\Saint_Kitts_and_Nevis.png", 146),
    "Saint Lucia": (r"D:\Flags\Saint_Lucia.png", 147),
    "Saint Vincent and the Grenadines": (r"D:\Flags\Saint_Vincent_and_the_Grenadines.png", 148),
    "Samoa": (r"D:\Flags\Samoa.png", 149),
    "San Marino": (r"D:\Flags\San_Marino.png", 150),
    "Sao Tome and Principe": (r"D:\Flags\Sao_Tome_and_Principe.png", 151),
    "Saudi Arabia": (r"D:\Flags\Saudi_Arabia.png", 152),
    "Senegal": (r"D:\Flags\Senegal.png", 153),
    "Serbia": (r"D:\Flags\Serbia.png", 154),
    "Seychelles": (r"D:\Flags\Seychelles.png", 155),
    "Sierra Leone": (r"D:\Flags\Sierra_Leone.png", 156),
    "Singapore": (r"D:\Flags\Singapore.png", 157),
    "Slovakia": (r"D:\Flags\Slovakia.png", 158),
    "Slovenia": (r"D:\Flags\Slovenia.png", 159),
    "Solomon Islands": (r"D:\Flags\Solomon_Islands.png", 160),
    "Somalia": (r"D:\Flags\Somalia.png", 161),
    "South Africa": (r"D:\Flags\South_Africa.png", 162),
    "South Sudan": (r"D:\Flags\South_Sudan.png", 163),
    "Spain": (r"D:\Flags\Spain.png", 164),
    "Sri Lanka": (r"D:\Flags\Sri_Lanka.png", 165),
    "Sudan": (r"D:\Flags\Sudan.png", 166),
    "Suriname": (r"D:\Flags\Suriname.png", 167),
    "Sweden": (r"D:\Flags\Sweden.png", 168),
    "Switzerland": (r"D:\Flags\Switzerland.png", 169),
    "Syria": (r"D:\Flags\Syria.png", 170),
    "Taiwan": (r"D:\Flags\Taiwan.png", 171),
    "Tajikistan": (r"D:\Flags\Tajikistan.png", 172),
    "Tanzania": (r"D:\Flags\Tanzania.png", 173),
    "Thailand": (r"D:\Flags\Thailand.png", 174),
    "Togo": (r"D:\Flags\Togo.png", 175),
    "Tonga": (r"D:\Flags\Tonga.png", 176),
    "Trinidad and Tobago": (r"D:\Flags\Trinidad_and_Tobago.png", 177),
    "Tunisia": (r"D:\Flags\Tunisia.png", 178),
    "Turkey": (r"D:\Flags\Turkey.png", 179),
    "Turkmenistan": (r"D:\Flags\Turkmenistan.png", 180),
    "Tuvalu": (r"D:\Flags\Tuvalu.png", 181),
    "Uganda": (r"D:\Flags\Uganda.png", 182),
    "Ukraine": (r"D:\Flags\Ukraine.png", 183),
    "United Arab Emirates": (r"D:\Flags\United_Arab_Emirates.png", 184),
    "United Kingdom": (r"D:\Flags\United_Kingdom.png", 185),
    "United States": (r"D:\Flags\United_States.png", 186),
    "Uruguay": (r"D:\Flags\Uruguay.png", 187),
    "Uzbekistan": (r"D:\Flags\Uzbekistan.png", 188),
    "Vanuatu": (r"D:\Flags\Vanuatu.png", 189),
    "Vatican City": (r"D:\Flags\Vatican_City.png", 190),
    "Venezuela": (r"D:\Flags\Venezuela.png", 191),
    "Vietnam": (r"D:\Flags\Vietnam.png", 192),
    "Yemen": (r"D:\Flags\Yemen.png", 193),
    "Zambia": (r"D:\Flags\Zambia.png", 194),
    "Zimbabwe": (r"D:\Flags\Zimbabwe.png",195),
    
}

# The objects to apply the textures to
flag_objects = [
    bpy.context.scene.objects['Flag'],
    bpy.context.scene.objects['Flag.001'],
    bpy.context.scene.objects['Flag.002'],
    bpy.context.scene.objects['Flag.003'],
    bpy.context.scene.objects['Flag.004']
]

# The camera object
camera_object = bpy.context.scene.camera

# Define the range for random positions (xmin, xmax), (ymin, ymax), (zmin, zmax)
position_range = ((-60, 60), (-19, 46), (10, 10))

# Define the range for camera height adjustments (zmin, zmax)
camera_height_range = (85, 170)

# Minimum distance to avoid overlap
min_distance = 10

# Number of images to generate
num_images_to_generate = 50

for img_idx in range(num_images_to_generate):
    # Randomly determine how many flags to show (between 1 and 5)
    num_flags_to_show = random.randint(1, len(flag_objects))
    
    # Randomly select which flags to show
    flags_to_show = random.sample(flag_objects, num_flags_to_show)
    
    # Hide all flags initially
    for flag_obj in flag_objects:
        flag_obj.hide_render = True
    
    # Show selected flags
    selected_textures = random.sample(list(flag_textures.values()), len(flags_to_show))
    existing_positions = []
    for flag_obj, (texture_path, class_id) in zip(flags_to_show, selected_textures):
        flag_obj.hide_render = False
        apply_texture(flag_obj, texture_path)
        randomly_rotate_object(flag_obj)
        randomly_position_object(flag_obj, position_range, existing_positions, min_distance)
    
    randomly_adjust_camera_height(camera_object, camera_height_range)
    
    # Render the image
    img_file_path = f'D:/Renderd/Land_7/flags_image_{img_idx + 300 + 1}_land7.png'
    bpy.context.scene.render.filepath = img_file_path
    bpy.ops.render.render(write_still=True)
    
    # Calculate and save bounding boxes
    bbox_file_path = f'D:/Renderd/Land_7/flags_image_{img_idx + 300 + 1}_land7.txt'
    with open(bbox_file_path, 'w') as f:
        for flag_obj, (texture_path, class_id) in zip(flags_to_show, selected_textures):
            min_x, min_y, max_x, max_y = calculate_bounding_box(flag_obj, bpy.context.scene, camera_object)
            f.write(f"{class_id} {min_x} {min_y} {max_x} {max_y}\n")
