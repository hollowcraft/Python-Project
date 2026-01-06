from tkinter import Tk, filedialog
from PIL import Image

# Ouvrir une fenêtre de sélection de fichier
def choisir_image():
    root = Tk()
    root.withdraw()  # Cacher la fenêtre principale de Tkinter
    file_path = filedialog.askopenfilename(
        filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    root.destroy()
    return file_path

# Modifier l'image pour rendre les pixels noirs en noir et tous les autres en blanc
def traiter_image(chemin_image):
    image = Image.open(chemin_image).convert("RGB")
    largeur, hauteur = image.size
    nouvelle_image = Image.new("RGB", (largeur, hauteur), "white")
    
    for x in range(largeur):
        for y in range(hauteur):
            pixel = image.getpixel((x, y))
            # Vérifier si le pixel est noir
            if pixel == (0, 0, 0):
                nouvelle_image.putpixel((x, y), (0, 0, 0))
            else:
                nouvelle_image.putpixel((x, y), (255, 255, 255))
    
    # Sauvegarder la nouvelle image
    chemin_sortie = chemin_image.replace(".", "_noir_blanc.")
    nouvelle_image.save(chemin_sortie)
    print(f"Image traitée enregistrée sous : {chemin_sortie}")

# Choisir l'image et la traiter
chemin_image = choisir_image()
if chemin_image:
    traiter_image(chemin_image)
else:
    print("Aucune image sélectionnée.")
