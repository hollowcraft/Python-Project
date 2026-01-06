from pymem import Pymem

# Charge le processus Minecraft
minecraft = Pymem("javaw.exe")

# Adresse trouvée via Cheat Engine pour l'angle de caméra (remplacer par la vraie adresse)
pitch_address = 0x602CB4078

# Définit des angles précis
def set_camera_angle(pitch):
    minecraft.write_float(pitch_address, pitch)

# Exemple : définit un angle de caméra
set_camera_angle(48.65645)
