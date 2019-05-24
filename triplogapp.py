from tkinter import *
from tkinter import messagebox
import requests


class TripLogApp:

    def __init__(self, master):
        self.triplog_login_form(master)

    def triplog_login_form(self, master):
        self.username_label = Label(master, text="Username")
        self.password_label = Label(master, text="Password")

        self.username_field = Entry(master)
        self.password_field = Entry(master, show="*")

        self.username_label.grid(row=0, sticky=W)
        self.password_label.grid(row=1, sticky=W)

        self.username_field.grid(row=0, column=1)
        self.password_field.grid(row=1, column=1)

        self.login_button = Button(master, text="Login")
        self.login_button.bind("<Button-1>", self.triplog_connect_server)
        self.login_button.grid(row=4, column=1, sticky=W)

    def triplog_connect_server(self, event):
        api_token_url = 'http://127.0.0.1:8000/api-auth-token/'
        username = self.username_field.get()
        password = self.password_field.get()
        print(username)
        print(password)
        data = {
            'username': username,
            'password': password,
        }
        headers = {
            'Accept': 'application/json'
        }
        response = requests.post(
            api_token_url,
            data=data,
            headers=headers
        )

        if response.status_code == 200:
            print(response.text)
        else:
            messagebox.showerror("Error", "Connection failed.")

    def test(self):
        print("test")

root = Tk()
menu = Menu(root)
triplogapp = TripLogApp(root)
sub_menu = Menu(menu)
menu.add_cascade(label="Triplog", menu=sub_menu)
sub_menu.add_command(label="Connect")
sub_menu.add_command(label="Categories")

root.config(menu=menu)
root.mainloop()




