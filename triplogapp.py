import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk
from tkinter import messagebox
import requests


class TripLogApp(tk.Tk):

    def __init__(self):
        super().__init__()

        """
        Window size and style.
        """
        self.geometry("300x500")
        style = ttk.Style(self)
        style.theme_use('aqua')

        """
        Layout
        """
        frame_top = tk.Frame(self)
        frame_top.pack()
        frame_mid = tk.Frame(self)
        frame_mid.pack(fill=tk.BOTH, expand=tk.YES)
        frame_bottom = tk.Frame(self)
        frame_bottom.pack(side=tk.BOTTOM, fill=tk.X)

        """
        Trip tree view
        """
        self.trip_view = ttk.Treeview(frame_mid)
        self.trip_view.heading('#0', text="Trips")
        self.trip_view.pack(fill=tk.BOTH, expand=tk.YES)

        """
        Refresh and add trip button.
        """
        self.refresh_button = ttk.Button(frame_mid, text="Refresh", command=self.reload_trips)
        self.refresh_button.config(state="disabled")
        self.refresh_button.pack(side=tk.LEFT)
        self.add_trip_button = ttk.Button(frame_mid, text="Add Trip", command=self.add_trip_window)
        self.add_trip_button.config(state="disabled")
        self.add_trip_button.pack(side=tk.RIGHT)

        """
        Connect button.
        """
        self.connect_button = ttk.Button(frame_top, text="Connect", command=self.connect_window)
        self.connect_button.pack()

        """
        Status bar.
        """
        self.status_bar = tk.Label(frame_bottom, text="Disconnected", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        """
        Connect windows
        """
        self.connect_window = None
        self.add_trip_window = None
        self.disconnect = True

        """
        Api Data and token.
        """
        self.api_auth = "http://127.0.0.1:8000/api-auth-token/"
        self.api_root = "http://127.0.0.1:8000/api/"
        self.token = None
        self.categories = None

    """
    Create connect window.
    """
    def connect_window(self):
        if self.disconnect:
            self.connect_window = tk.Toplevel()
            self.connect_window.wm_title("Connect to server")
            username_label = tk.Label(self.connect_window, text="Username")
            password_label = tk.Label(self.connect_window, text="Password")
            username_label.grid(row=0)
            password_label.grid(row=1)
            username_field = tk.Entry(self.connect_window)
            password_field = tk.Entry(self.connect_window, show="*")
            username_field.grid(row=0, column=1, columnspan=2)
            password_field.grid(row=1, column=1, columnspan=2)
            connect_button = ttk.Button(self.connect_window,
                                        text="Connect", command=lambda username=username_field, password=password_field:
                                        self.connect_server(username, password))
            connect_button.grid(row=2, column=1)
            connect_close_button = ttk.Button(self.connect_window, text="Close", command=self.connect_window.destroy)
            connect_close_button.grid(row=2, column=2)
        else:
            self.quit_app()

    """
    Add trip window.
    """
    def add_trip_window(self):
        if self.disconnect is False:
            self.add_trip_window = tk.Toplevel()


    """
    Connect to server.
    """
    def connect_server(self, username, password):
        data = {
            'username': username.get(),
            'password': password.get(),

        }

        connect = requests.post(self.api_auth, data=data)
        if connect.status_code == 200:
            token = connect.json()
            self.connect_button['text'] = "Quit"
            self.disconnect = False
            self.status_bar['text'] = "Connected"
            self.connect_window.destroy()
            self.refresh_button.config(state="enabled")
            self.add_trip_button.config(state="enabled")
            self.token = token["token"]
            trips = self.get_trip_list()
            self.categories = self.get_categories()
            if trips is not None:
                self.display_trips(trips)
        else:
            showinfo('Error', "Unable to login.")

    """
    Get categories.
    """
    def get_categories(self):
        api_url = self.api_root + "categories/"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token
        }

        connect = requests.get(api_url, headers=headers)
        if connect.status_code == 200:
            data = connect.json()
            return data
        else:
            showinfo('Error', "Unable to get request.")
            return None

    """
    Get data from server
    """
    def get_trip_list(self):
        api_url = self.api_root + "trips/"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token
        }

        connect = requests.get(api_url, headers=headers)
        if connect.status_code == 200:
            data = connect.json()
            return data
        else:
            showinfo('Error', "Unable to get request.")
            return None

    """
    Render result in TreeView.
    """
    def display_trips(self, data):
        for trip in data:
            self.trip_view.insert('', tk.END, "{}-{}".format("trip", trip['id']), text=trip['trip_name'])
            if trip['trip_location'] is not None:
                for location in trip['trip_location']:
                    self.trip_view.insert("{}-{}".format("trip", trip['id']), tk.END,
                                          "{}-{}-{}-{}".format("trip", trip['id'], "loc", location['id']), text=location['location_name'])

    """
    Reload trips display.
    """
    def reload_trips(self):

        # Clean all items
        children = self.trip_view.get_children()
        for child in children:
            self.trip_view.delete(child)

        # Recreate all items.
        if self.token is not None:
            trips = self.get_trip_list()
            print(trips)
            self.display_trips(trips)
        else:
            showinfo('Error', "Unable to get token.")

    """
    Quit app.
    """
    def quit_app(self):
        quit_app = messagebox.askquestion("Disconnect and quit", "Are you sure want to exit application", icon='warning')
        if quit_app == 'yes':
            self.destroy()


if __name__ == "__main__":
    triplog_app = TripLogApp()
    triplog_app.mainloop()
