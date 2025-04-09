from tkinter import * # acest import nu gaseste toate modulele mereu
from tkinter import messagebox # unele module sunt separate ca messagebox
from random import choice,shuffle,randint
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_symbols + password_letters +password_numbers
    shuffle(password_list)

    password = ''.join(password_list)
    password_entry.delete(0,END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    passw = password_entry.get()

    line = f'{website}:{username}:{passw}'

    print(len(website), len(username), len(passw))
    if len(website)==0 or len(username)==0 or len(passw)==0:
        messagebox.showinfo('Error',f'Please dont leave any fields empty')

    else:
        is_ok = messagebox.showinfo('data', f'Website:{website}\nUser:{username}\nIs it ok to save?')
        if is_ok:

            with open('data.txt','a') as file:
                file.write(f'{line}\n')
            website_entry.delete(0,END)
            password_entry.delete(0,END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20,pady=20)

canvas = Canvas(width=180, height=180)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0,column=1)

#Labels
website_label = Label(text='Website:')
website_label.grid(row=1,column=0)

username_label = Label(text='Email/Username:')
username_label.grid(row=2,column=0)

password_label = Label(text='Password:')
password_label.grid(row=3,column=0)

#Entries
username_entry = Entry(width=40)
username_entry.grid(row=2,column=1,columnspan=2)
username_entry.insert(0,'dan@gmail.com')

website_entry = Entry(width=35)
website_entry.grid(row=1,column=1,columnspan=2)
website_entry.focus()

password_entry = Entry(width=21)
password_entry.grid(row=3,column=1)

#Buttons
generate_button = Button(text='Generate Password',command=generate_password)
generate_button.grid(row=3,column=2)

add_button = Button(text='Add',width=36,command=save)
add_button.grid(row=4,column=1,columnspan=2)



window.mainloop()