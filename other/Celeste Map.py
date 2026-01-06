import perlin_noise

# Définition de la taille de la room
room_width = 40  # en tiles
room_height = 30  # en tiles

# Initialisation de la grille de room avec des tiles vides
room = [[None for x in range(room_width)] for y in range(room_height)]

# Fonction pour générer des tiles avec un bruit de Perlin pour le sol
def generate_ground(room):
    noise = perlin_noise.PerlinNoise(octaves=3)
    for y in range(room_height):
        for x in range(room_width):
            value = noise([x / room_width, y / room_height])
            if value > 0.5:  # seuil pour générer un sol
                room[y][x] = "ground_tile"
            else:
                room[y][x] = "empty"
    return room

# Génération de la room avec les tiles de sol
room = generate_ground(room)

# Placement du player spawn
room[room_height - 1][2] = "player_spawn"

# Ajout d'entités comme les boosters
def place_boosters(room):
    room[room_height - 5][10] = "booster_red"
    return room

room = place_boosters(room)

# Fonction de conversion des tiles en binaire
def convert_tile_to_bin(tile):
    # Exemple simple : chaque type de tile est converti en un identifiant binaire
    tile_mapping = {
        "ground_tile": b'\x01',  # Représentation binaire pour un sol
        "empty": b'\x00',        # Représentation binaire pour une case vide
        "player_spawn": b'\x02', # Représentation binaire pour le spawn du joueur
        "booster_red": b'\x03'   # Représentation binaire pour un booster rouge
    }
    return tile_mapping.get(tile, b'\x00')  # Par défaut, retourne 'empty' si tile inconnue

# Export de la room en format utilisable pour Lönn
def export_to_bin(room):
    with open("custom_map.bin", "wb") as f:
        for row in room:
            for tile in row:
                # Convertir chaque tile en donnée binaire et écrire dans le fichier
                tile_data = convert_tile_to_bin(tile)
                f.write(tile_data)

# Appel de la fonction pour exporter la room en binaire
export_to_bin(room)
