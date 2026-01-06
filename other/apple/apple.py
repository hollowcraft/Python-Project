def count_apple_occurrences(filename):
    """Compte le nombre de fois où 'apple' apparaît dans un fichier"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            count = content.count('apple')
        return count
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{filename}' n'a pas été trouvé.")
        return 0

if __name__ == "__main__":
    filename = r"C:\Users\Adam\Desktop\Mes Projects\python\other\apple\apple.txt"
    occurrences = count_apple_occurrences(filename)
    print(f"Le mot 'apple' apparaît {occurrences} fois dans {filename}.")