from donnees_pwm import *
import random
from pathlib import Path
import pickle


def new_alpha(alphabet, chiffres, symbols):
    """retourne une nouvelle liste de caractères"""
    new_list_char = alphabet + chiffres + symbols
    random.shuffle(new_list_char)
    return new_list_char


def recup_bases():
    """retourne ou crée la base de caractères en dictionnaire associé à un mot code"""
    chemin_base = Path(NOM_FICHIER_BASES)
    if chemin_base.exists():
        with chemin_base.open("rb") as fichier_bases:
            mon_depickler = pickle.Unpickler(fichier_bases)
            base_char = mon_depickler.load()
    else:
        base_char = {}
    return base_char


def enregistrer_codes(base_char):
    """enregistre la base de caractère associé au mot code dans le dictionnaire"""
    with open(NOM_FICHIER_BASES, "wb") as fichier_bases:
        mon_pickler = pickle.Pickler(fichier_bases)
        mon_pickler.dump(base_char)


def caesar(text, shift, direction, base_char):
    """demande une chaîne de caractère;
    puis demande le 'shift';
    puis encode ou décode la chaîne de cractère entrée;
    et finalement retourne le résultat"""
    final_text = ""
    for letter in text:
        if letter not in base_char:
            final_text += letter
        else:
            x = base_char.index(letter)
            if direction == "encode":
                if x + shift >= len(base_char):
                    z = (x + shift) - len(base_char)
                    y = base_char[z]
                else:
                    y = base_char[x + shift]
            elif direction == "decode":
                if x - shift < 0:
                    z = (x - shift) + len(base_char)
                    y = base_char[z]
                else:
                    y = base_char[x - shift]
            final_text += y
    return final_text
