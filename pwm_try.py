from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import json
from fonctions_pwm import *


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
               't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '%', '&', '+', 'é', 'ù', 'à', '-']

    pass_list1 = []
    pass_list2 = []
    pass_list3 = []
    password_list = [pass_list1, pass_list2, pass_list3]

    password_complet = ""
    for _ in password_list:
        pass_letters = [choice(letters) for _ in range(randint(2, 6))]
        pass_symbols = [choice(symbols) for _ in range(randint(1, 2))]
        pass_numbers = [choice(numbers) for _ in range(randint(1, 2))]
        pass_list = pass_letters + pass_symbols + pass_numbers
        shuffle(pass_list)

        password = "".join(pass_list)
        password_complet += (password + "-")
    password_complet = password_complet[:-1]

    passw_entry.insert(0, password_complet)


# ----------------------------- ENCODE ------------------------------------- #
def encode(text_to_encode, base_char, shift):
    shift %= 88
    return caesar(text_to_encode, shift, direction="encode", base_char=base_char)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    base_char = recup_bases()
    code = name_entry.get()
    if code not in base_char.keys():
        base_char[code] = new_alpha(alphabet, chiffres, symbols)
    enregistrer_codes(base_char)
    x = randint(5, 85)
    y = randint(95, 170)
    z = [x, y]
    shift = choice(z)

    web_entry_encode = encode(web_entry.get(), base_char[code], shift)
    email_encode = encode(user_entry.get(), base_char[code], shift)
    password_encode = encode(passw_entry.get(), base_char[code], shift)

    new_data = {
        name_entry.get(): {
            "shift": shift,
            "web_address": web_entry_encode,
            "email": email_encode,
            "password": password_encode
        }
    }

    if name_entry.get() == "" or user_entry.get() == "" or passw_entry.get() == "":
        messagebox.showinfo(title="Oups !", message="Ne laissez pas ces champs libres !")
    else:
        try:
            with open("save_pass.json", "r") as saved:
                data = json.load(saved)
        except FileNotFoundError:
            with open("save_pass.json", "w") as saved:
                json.dump(new_data, saved, indent=4)
        else:
            data.update(new_data)
            with open("save_pass.json", "w") as saved:
                json.dump(data, saved, indent=4)
        finally:
            messagebox.showinfo(title="Enregistré !", message="C'est bon, c'est emboîté !")


# ----------------------------- ENCODE --------------------------------------#
def decode(text_to_decode, base_char, shift):
    shift %= 88
    return caesar(text_to_decode, shift, direction="decode", base_char=base_char)


def find_password():
    base_char = recup_bases()
    user_code = name_entry.get()
    try:
        with open("save_pass.json", "r") as data_check:
            search_passw = json.load(data_check)
    except FileNotFoundError:
        messagebox.showinfo(title="Erreur de donnée !", message="La base n'existe pas encore !")
    else:
        if user_code in search_passw:
            web_ad = search_passw[user_code]["web_address"]
            email = search_passw[user_code]["email"]
            password = search_passw[user_code]["password"]
            shift = search_passw[user_code]["shift"]

            web_entry_decode = decode(web_ad, base_char[user_code], shift)
            email_decode = decode(email, base_char[user_code], shift)
            password_decode = decode(password, base_char[user_code], shift)

            web_entry.insert(0, web_entry_decode)
            user_entry.insert(0, email_decode)
            passw_entry.insert(0, password_decode)
            messagebox.showinfo(title=user_code, message=f"Web address : {web_entry_decode}"
                                                         f"\nEmail : {email_decode}"
                                                         f"\nPassword : {password_decode}")
        else:
            messagebox.showinfo(title="Erreur d'entrée !", message="Cette entrée n'existe pas dans votre base !")


def empty():
    name_entry.delete(0, END)
    web_entry.delete(0, END)
    user_entry.delete(0, END)
    passw_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("CoW Rodgers PWM")
window.config(padx=25, pady=25)

label0 = Label(text="Addresse Web :")
label0.grid(column=0, row=2, pady=5)

label1 = Label(text="Référence : ")
label1.grid(column=0, row=1, pady=5)

label2 = Label(text="Email OU nom d'utilisateur : ")
label2.grid(column=0, row=3, pady=5, padx=5)

label3 = Label(text="Mot de passe : ")
label3.grid(column=0, row=4, pady=5)

label4 = Label(text="@ Cow Rodgers", font=("Arial", 7, "italic"))
label4.grid(column=0, row=6, pady=15)

name_entry = Entry(width=36)
name_entry.grid(column=1, row=1)
name_entry.focus()

web_entry = Entry(width=62)
web_entry.grid(column=1, row=2, columnspan=2)

user_entry = Entry(width=62)
user_entry.grid(column=1, row=3, columnspan=2)

passw_entry = Entry(width=36)
passw_entry.grid(column=1, row=4)

search_button = Button(text="Rechercher", width=20, command=find_password)
search_button.grid(column=2, row=1)

generate_button = Button(text="Generer un mot de passe", width=20, command=generate_password)
generate_button.grid(column=2, row=4, padx=5)

add_button = Button(text="Ajouter", width=20, command=save)
add_button.grid(column=2, row=5, columnspan=2, pady=5)

free_button = Button(text="Vider tous les champs", width=30, command=empty)
free_button.grid(column=1, row=5)

window.mainloop()
