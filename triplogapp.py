"""
Triplog Desktop App with TkInter
"""
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk
from tkinter import messagebox
import dateutil.parser
import requests


class TripLogApp(tk.Tk):

    def __init__(self):
        super().__init__()

        """
        Window size and style.
        """
        self.geometry("800x500")
        self.wm_title("Triplog App")
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
        self.trip_view["columns"] = ("Type", "Date")
        self.trip_view.heading('#0', text="Trips")
        self.trip_view.heading('#1', text="Type")
        self.trip_view.heading('#2', text="Date")
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
        self.trip_window = None
        self.disconnect = True
        self.trip_window_open = False

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
            self.token = token.get("token")
            trips = self.get_trip_list()
            self.categories = self.get_categories()
            if trips is not None:
                self.display_trips(trips)
                # Bind tree view click.
                self.trip_view.bind("<Double-1>", self.open_trip_detail)
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
    Get trip detail
    """
    def get_trip_detail(self, id):
        api_url = self.api_root + "trips/" + id
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
    Get location detail
    """

    def get_location_detail(self, id):
        api_url = self.api_root + "locations/" + id
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
            trip_date_parse = dateutil.parser.parse(trip.get('trip_date'))
            trip_date = trip_date_parse.strftime("%Y-%m-%d %H:%I %p")
            self.trip_view.insert('', tk.END, "{}-{}".format("trip", trip.get('id')), text=trip.get('trip_name'), values=("Trip", trip_date))
            if trip['trip_location'] is not None:
                for location in trip['trip_location']:
                    location_date_parse = dateutil.parser.parse(location.get('location_date'))
                    location_date = location_date_parse.strftime("%Y-%m-%d %H:%I %p")
                    self.trip_view.insert("{}-{}".format("trip", trip.get('id')), tk.END,
                                          "{}-{}-{}-{}".format("loc", location.get('id'), "trip", trip.get('id')),
                                          text=location.get('location_name'), values=("Location",
                                                                                      location_date))

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
            self.display_trips(trips)
        else:
            showinfo('Error', "Unable to get token.")

    """
    Open trip detail on tree click.
    """
    def open_trip_detail(self, event):
        item = self.trip_view.identify('item', event.x, event.y)
        root_x = self.winfo_x()
        root_y = self.winfo_y()
        if item:
            if self.trip_window_open:
                self.trip_window.destroy()
                self.trip_window_open = False
            self.trip_window = tk.Toplevel()
            self.trip_window.geometry("%dx%d+%d+%d" % (400, 400, root_x + 50, root_y + 50))
            sel_item = item.split("-")
            # If trip selected.
            if sel_item[0] == "trip":
                trip = self.get_trip_detail(sel_item[1])
                if trip is not None:
                    self.trip_window.wm_title("Trip: " + self.trip_view.item(item, "text"))
                    self.trip_window_open = True
                    # Get locations.
                    location = []
                    for trip_loc in trip.get('trip_location'):
                        location.append(trip_loc.get('location_name'))
                    # Trip name.
                    trip_name_label = ttk.Label(self.trip_window, text="Trip Name")
                    trip_name_label.grid(row=0, column=0, sticky="W")
                    trip_name = ttk.Label(self.trip_window, text=": " + trip.get('trip_name'))
                    trip_name.grid(row=0, column=1, sticky="W")
                    # Trip category.
                    trip_category_label = ttk.Label(self.trip_window, text="Category")
                    trip_category_label.grid(row=1, column=0, sticky="W")
                    trip_category = ttk.Label(self.trip_window, text=": " +
                                                                     trip.get('trip_category').get("category_name"))
                    trip_category.grid(row=1, column=1, sticky="W")
                    # Trip body.
                    trip_body_label = ttk.Label(self.trip_window, text="Description")
                    trip_body_label.grid(row=2, column=0, sticky="W")
                    trip_body = ttk.Label(self.trip_window, text=": " + trip.get('trip_body'))
                    trip_body.grid(row=2, column=1, sticky="W")
                    # Trip location.
                    if location:
                        trip_locations_label = ttk.Label(self.trip_window, text="Locations")
                        trip_locations_label.grid(row=3, column=0, sticky="NW")
                        trip_locations = ttk.Label(self.trip_window, text=": " + "\n".join(location))
                        trip_locations.grid(row=3, column=1, sticky="W")
                    # Trip Date
                    trip_data_parse = dateutil.parser.parse(trip.get('trip_date'))
                    trip_date_text = trip_data_parse.strftime("%Y-%m-%d %H:%I %p")
                    trip_date_label = ttk.Label(self.trip_window, text="Date")
                    trip_date_label.grid(row=4, column=0, sticky="W")
                    trip_date = ttk.Label(self.trip_window, text=": " + trip_date_text)
                    trip_date.grid(row=4, column=1, sticky="W")

            # If location selected.
            if sel_item[0] == "loc":
                location = self.get_location_detail(sel_item[1])
                if location:
                    self.trip_window.wm_title("Location: " + self.trip_view.item(item, "text"))
                    self.trip_window_open = True
                    # Location name,
                    location_name_label = ttk.Label(self.trip_window, text="Location name")
                    location_name_label.grid(row=0, column=0, sticky="W")
                    location_name = ttk.Label(self.trip_window, text=": " + location.get('location_name'))
                    location_name.grid(row=0, column=1, sticky="W")
                    # Location body.
                    location_body_label = ttk.Label(self.trip_window, text="Description")
                    location_body_label.grid(row=1, column=0, sticky="W")
                    location_body = ttk.Label(self.trip_window, text=": " + location.get('location_body'))
                    location_body.grid(row=1, column=1, sticky="W")
                    # Location date.
                    location_data_parse = dateutil.parser.parse(location.get('location_date'))
                    location_date_text = location_data_parse.strftime("%Y-%m-%d %H:%I %p")
                    location_date_label = ttk.Label(self.trip_window, text="Date")
                    location_date_label.grid(row=2, column=0, sticky="W")
                    location_date = ttk.Label(self.trip_window, text=": " + location_date_text)
                    location_date.grid(row=2, column=1, sticky="W")

    """
    Quit app.
    """
    def quit_app(self):
        quit_app = messagebox.askquestion("Disconnect and quit", "Are you sure want to exit application", icon='warning')
        if quit_app == 'yes':
            self.destroy()


if __name__ == "__main__":
    trip_log_app = TripLogApp()
    trip_log_app.mainloop()
