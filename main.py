from tkinter import *
from tkinter import messagebox
import random
# to enable clipping to clipboard
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # create ranges
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    password_symbol = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    # combining the three lists
    password_list = password_letter + password_numbers + password_symbol

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    # copy password to clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    web = website_entry.get()
    email = email_entry.get()
    password_ = password_entry.get()
    # create a dictionary
    new_data = {
        web: {
            "email": email,
            "password": password_,
        }
    }

    if len(web) == 0 or len(password_) == 0:
        field_empty = messagebox.showinfo(title=web, message="Please don't leave any field empty!")

    else:
        try:
            # if json file doesnt exist it should be tried and exception should be handled
            # exception handling will include creation of a json file
            with open("data.json", mode="r") as file:
                # read json and update it
                data = json.load(file)

        except FileNotFoundError:
            # create a new json file
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)

        else:
            # update old data with new data
            data.update(new_data)

            # save the updated data
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    web = website_entry.get()

    try:
        with open("data.json") as file:
            contents = json.load(file)
    except FileNotFoundError:
        # display that file doesnt exist
        messagebox.showinfo(title="Error!", message="File does not exist.")
    else:
        if web in contents:
            email = contents[web]["email"]
            password = contents[web]["password"]
            messagebox.showinfo(title=web, message=f"email: {email} \npassword: {password}")
        else:
            messagebox.showinfo(title="Error!", message=f"No details for {web} found.")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("My Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()

search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)
# to populate an email
email_entry.insert(0, "dummyemail@gmail.com")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
