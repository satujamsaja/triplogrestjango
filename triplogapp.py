"""
Triplog Desktop App with TkInter
"""
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk
from tkinter import messagebox
import dateutil.parser
import requests
import json


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
        self.trip_view.column('#0', minwidth=0)
        self.trip_view.column('#1', width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.trip_view.column('#2', width=150, stretch=tk.NO, anchor=tk.CENTER)
        self.trip_view.pack(fill=tk.BOTH, expand=tk.YES)

        """
        Refresh and add trip button.
        """
        self.refresh_button = ttk.Button(frame_mid, text="Refresh", command=self.reload_trips)
        self.refresh_button.config(state="disabled")
        self.refresh_button.pack(side=tk.LEFT)
        self.add_trip_button = ttk.Button(frame_mid, text="Add Trip", command=self.add_trip_popup)
        self.add_trip_button.config(state="disabled")
        self.add_trip_button.pack(side=tk.RIGHT)

        """
        Connect button.
        """
        self.username_label = tk.Label(frame_top, text="Username")
        self.username_label.pack(side=tk.LEFT)
        self.username_field = tk.Entry(frame_top)
        self.username_field.pack(side=tk.LEFT)
        self.password_label = tk.Label(frame_top, text="Password")
        self.password_label.pack(side=tk.LEFT)
        self.password_field = tk.Entry(frame_top, show="*")
        self.password_field.pack(side=tk.LEFT)
        self.connect_button = ttk.Button(frame_top, text="Connect", command=self.connect_window)
        self.connect_button.pack()

        """
        Status bar.
        """
        self.status_bar = tk.Label(frame_bottom, text="Disconnected", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        """
        Windows
        """
        self.connect_window = None
        self.add_trip_window = None
        self.edit_trip_window = None
        self.add_location_window = None
        self.edit_location_window = None
        self.trip_window = None
        self.disconnect = True
        self.trip_window_open = False

        """
        Api Data and token.
        """
        self.api_auth = "http://127.0.0.1:8000/api-auth-token/"
        self.api_root = "http://127.0.0.1:8000/api/"
        self.token = None
        self.user_id = None
        self.categories = None
        self.categories_opts = None

    """
    Create connect window.
    """
    def connect_window(self):
        if self.disconnect:
            self.connect_server(self.username_field, self.password_field)
        else:
            self.quit_app()

    """
    Add trip window.
    """
    def add_trip_popup(self):
        if self.disconnect is False:
            self.add_trip_window = tk.Toplevel()
            self.add_trip_window.wm_title("Add trip")
            trip_name_label = ttk.Label(self.add_trip_window, text="Trip name: ")
            trip_name_label.grid(row=0, column=0, sticky="W")
            trip_name_field = ttk.Entry(self.add_trip_window)
            trip_name_field.grid(row=0, column=1, sticky="W")

            # Fetch categories.
            if self.categories is None:
                self.categories = self.get_categories()

            if self.categories:
                # Generate category opts.
                tk_var = tk.StringVar()
                if not self.categories_opts:
                    default_categories = {'Select category': 0}
                    db_categories = {category.get('category_name'): category.get('id') for category in self.categories}
                    self.categories_opts = default_categories.copy()
                    self.categories_opts.update(db_categories)

                # Trip category.
                trip_category_label = ttk.Label(self.add_trip_window, text="Category: ")
                trip_category_label.grid(row=1, column=0, sticky="W")
                trip_category_option = ttk.OptionMenu(self.add_trip_window, tk_var, *self.categories_opts.keys())
                trip_category_option.grid(row=1, column=1, sticky="W")
                # Trip body.
                trip_body_label = ttk.Label(self.add_trip_window, text="Description")
                trip_body_label.grid(row=2, column=0, sticky="NW")
                trip_body = tk.Text(self.add_trip_window, height=10, width=25)
                trip_body.grid(row=2, column=1, sticky="W")
                # Save button.
                trip_save_button = ttk.Button(self.add_trip_window, text="Save",
                                              command=lambda trip_name_data=trip_name_field,
                                                             trip_category_data=tk_var,
                                                             trip_body_data=trip_body:
                                              self.save_trip(trip_name_data, trip_category_data, trip_body_data))

                trip_save_button.grid(row=3, column=1, sticky="W")

    """
    Add location window.
    """
    def add_location_popup(self, trip_id):
        if self.disconnect is False:
            self.add_location_window = tk.Toplevel()
            self.add_location_window.wm_title("Add location")
            self.trip_window.destroy()
            # Location name.
            location_name_label = ttk.Label(self.add_location_window, text="Location name")
            location_name_label.grid(row=0, column=0, sticky="W")
            location_name_field = tk.Entry(self.add_location_window)
            location_name_field.grid(row=0, column=1, sticky="W")
            # Location description
            location_body_label = ttk.Label(self.add_location_window, text="Description")
            location_body_label.grid(row=1, column=0, sticky="NW")
            location_body_field = tk.Text(self.add_location_window, height=10, width=25)
            location_body_field.grid(row=1, column=1, sticky="W")
            # Save button
            location_save_button = ttk.Button(self.add_location_window, text="Save",
                                                command=lambda location_name_data=location_name_field,
                                                location_body_data=location_body_field,
                                                trip_id_data=trip_id:
                                                self.save_location(location_name_data, location_body_data, trip_id_data))
            location_save_button.grid(row=2, column=1, sticky="W")

    """
    Edit trip window.
    """
    def edit_trip_popup(self, trip_id):
        if self.disconnect is False:
            self.edit_trip_window = tk.Toplevel()
            self.edit_trip_window.wm_title("Edit trip id:" + "{}".format(trip_id))
            self.trip_window.destroy()
            # Get trip data.
            trip = self.get_trip_detail(trip_id)
            if trip:
                # Trip name field.
                trip_name_label = tk.Label(self.edit_trip_window, text="Location name")
                trip_name_label.grid(row=0, column=0, sticky="W")
                trip_name_field = tk.Entry(self.edit_trip_window)
                trip_name_field.grid(row=0, column=1, sticky="W")
                trip_name_field.insert(0, trip.get('trip_name'))
                trip_name_field.focus_set()

                # Generate category opts.
                tk_var = tk.StringVar()
                trip_category = 'Select category'
                for category in self.categories:
                    if category.get('id') == trip.get('trip_category'):
                        trip_category = category.get('category_name')
                if not self.categories_opts:
                    default_categories = {'Select category': 0}
                    db_categories = {category.get('category_name'): category.get('id') for category in self.categories}
                    self.categories_opts = default_categories.copy()
                    self.categories_opts.update(db_categories)
                # Trip category.
                trip_category_label = ttk.Label(self.edit_trip_window, text="Category: ")
                trip_category_label.grid(row=1, column=0, sticky="W")
                trip_category_option = ttk.OptionMenu(self.edit_trip_window, tk_var, *self.categories_opts.keys())
                tk_var.set(trip_category)
                trip_category_option.grid(row=1, column=1, sticky="W")
                # Trip body field.
                trip_body_label = tk.Label(self.edit_trip_window, text="Description")
                trip_body_label.grid(row=2, column=0, sticky="NW")
                trip_body_field = tk.Text(self.edit_trip_window, height=10, width=25)
                trip_body_field.grid(row=2, column=1, sticky="W")
                trip_body_field.insert(tk.END, trip.get('trip_body'))
                # Update button.
                trip_update_button = ttk.Button(self.edit_trip_window, text="Update",
                                                command=lambda trip_name_data=trip_name_field,
                                                trip_body_data=trip_body_field, trip_category_data=tk_var, trip_id_data=trip.get('id'):
                                                self.update_trip(trip_name_data, trip_category_data, trip_body_data, trip_id_data))
                trip_update_button.grid(row=3, column=1, sticky="W")

    """
    Edit location window.
    """
    def edit_location_popup(self, location_id):
        if self.disconnect is False:
            self.edit_location_window = tk.Toplevel()
            self.edit_location_window.wm_title("Edit location id" + "{}".format(location_id))
            self.trip_window.destroy()
            # Get location data.
            location = self.get_location_detail(location_id)
            if location:
                # Location name.
                location_name_label = ttk.Label(self.edit_location_window, text="Location name")
                location_name_label.grid(row=0, column=0, sticky="W")
                location_name_field = tk.Entry(self.edit_location_window)
                location_name_field.grid(row=0, column=1, sticky="W")
                location_name_field.insert(0, location.get('location_name'))
                # Location description
                location_body_label = ttk.Label(self.edit_location_window, text="Description")
                location_body_label.grid(row=1, column=0, sticky="NW")
                location_body_field = tk.Text(self.edit_location_window, height=10, width=25)
                location_body_field.grid(row=1, column=1, sticky="W")
                location_body_field.insert(tk.END, location.get('location_body'))
                # Save button
                location_save_button = ttk.Button(self.edit_location_window, text="Update",
                                                  command=lambda location_name_data=location_name_field,
                                                                 location_body_data=location_body_field,
                                                                 location_id_data=location_id:
                                                  self.update_location(location_name_data, location_body_data, location_id_data))
                location_save_button.grid(row=2, column=1, sticky="W")

    """
    Connect to server.
    """
    def connect_server(self, username, password):
        data = {
            'username': username.get(),
            'password': password.get(),
        }

        if username.get() and password.get():
            try:
                connect = requests.post(self.api_auth, data=data)
                if connect.status_code == 200:
                    token = connect.json()
                    self.connect_button['text'] = "Quit"
                    self.disconnect = False
                    self.status_bar['text'] = "Connected"
                    self.refresh_button.config(state=tk.NORMAL)
                    self.add_trip_button.config(state=tk.NORMAL)
                    self.username_field.config(state=tk.DISABLED)
                    self.password_field.config(state=tk.DISABLED)
                    self.token = token.get("token")
                    self.user_id = token.get('id')
                    trips = self.get_trip_list()
                    self.categories = self.get_categories()
                    if trips is not None:
                        self.display_trips(trips)
                        # Bind tree view click.
                        self.trip_view.bind("<Double-1>", self.open_trip_detail)
                else:
                    showinfo("Error", "Unable to login.")
            except requests.exceptions.ConnectionError as e:
                showinfo("Connection error", e)
        else:
            showinfo("Error", "Please enter required fields.")

    """
    Get categories.
    """
    def get_categories(self):
        api_url = self.api_root + "categories/"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token
        }

        try:
            connect = requests.get(api_url, headers=headers)
            if connect.status_code == 200:
                data = connect.json()
                return data
            else:
                showinfo("Error", "Unable to get request.")
                return None
        except requests.exceptions.ConnectionError as e:
            showinfo("Connection error", e)

    """
    Get data from server
    """
    def get_trip_list(self):
        api_url = self.api_root + "trips/"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token
        }

        try:
            connect = requests.get(api_url, headers=headers)
            if connect.status_code == 200:
                data = connect.json()
                return data
            else:
                showinfo("Error", "Unable to get request.")
                return None
        except requests.exceptions.ConnectionError as e:
            showinfo("Connection error", e)

    """
    Get trip detail
    """
    def get_trip_detail(self, trip_id):
        api_url = self.api_root + "trips/" + "{}".format(trip_id)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token,
        }

        try:
            connect = requests.get(api_url, headers=headers)
            if connect.status_code == 200:
                data = connect.json()
                return data
            else:
                showinfo("Error", "Unable to get request.")
                return None
        except requests.exceptions.ConnectionError as e:
            showinfo("Connection error", e)

    """
    Get location detail
    """
    def get_location_detail(self, location_id):
        api_url = self.api_root + "locations/" + "{}".format(location_id)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token
        }

        try:
            connect = requests.get(api_url, headers=headers)
            if connect.status_code == 200:
                data = connect.json()
                return data
            else:
                showinfo("Error", "Unable to get request.")
                return None
        except requests.exceptions.ConnectionError as e:
            showinfo("Connection error", e)

    """
    Get category detail
    """
    def get_category_detail(self, category_id):
        api_url = self.api_root + "categories/" + "{}".format(category_id)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token
        }

        try:
            connect = requests.get(api_url, headers=headers)
            if connect.status_code == 200:
                data = connect.json()
                return data
            else:
                showinfo("Error", "Unable to get request.")
                return None
        except requests.exceptions.ConnectionError as e:
            showinfo("Connection error", e)

    """
    Save trip
    """
    def save_trip(self, trip_name_data, trip_category_data, trip_body_data):
        api_url = self.api_root + "trips/"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token,
        }

        if trip_name_data.get() and trip_category_data.get() != "Select category" and \
                len(trip_body_data.get("1.0", tk.END)) > 1:
            trip_category = self.categories_opts[trip_category_data.get()]

            data = {
                'trip_name': trip_name_data.get(),
                'trip_category': trip_category,
                'trip_body': trip_body_data.get("1.0", tk.END),
                'trip_user': self.user_id,
            }

            try:
                connect = requests.post(api_url, headers=headers, data=json.dumps(data))
                if connect.status_code == 201:
                    self.add_trip_window.destroy()
                    self.reload_trips()
            except requests.exceptions.ConnectionError as e:
                showinfo("Connection error", e)
        else:
            showinfo("Require fields", "Please fill required fields.")

    """
    Update trip.
    """
    def update_trip(self, trip_name_data, trip_category_data, trip_body_data, trip_id_data):
        api_url = self.api_root + "trips/" + "{}/".format(trip_id_data)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token,
        }

        if trip_name_data.get() and trip_category_data.get() != "Select category" and \
                len(trip_body_data.get("1.0", tk.END)) > 1:
            trip_category = self.categories_opts[trip_category_data.get()]

            data = {
                'trip_name': trip_name_data.get(),
                'trip_category': trip_category,
                'trip_body': trip_body_data.get("1.0", tk.END),
                'trip_user': self.user_id,
            }

            try:
                connect = requests.patch(api_url, headers=headers, data=json.dumps(data))
                if connect.status_code == 200:
                    self.edit_trip_window.destroy()
                    self.reload_trips()
            except requests.exceptions.ConnectionError as e:
                showinfo("Connection error", e)

        else:
            showinfo("Require fields", "Please fill required fields.")

    """
    Save location.
    """
    def save_location(self, location_name_data, location_body_data, trip_id_data):
        api_url = self.api_root + "locations/"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token,
        }

        if location_name_data.get() and len(location_body_data.get("1.0", tk.END)) > 1:

            data = {
                'location_name': location_name_data.get(),
                'location_body': location_body_data.get("1.0", tk.END),
            }

            try:
                connect = requests.post(api_url, headers=headers, data=json.dumps(data))
                if connect.status_code == 201:
                    response = connect.json()
                    if response:
                        trip = self.get_trip_detail(trip_id_data)
                        if trip:
                            trip_location = trip.get('trip_location')
                            # Add new trip to trip location.
                            trip_location.append(response.get('id'))

                            # Construct data.
                            data_trip = {
                                'trip_location': trip_location
                            }
                            # Request patch to trip.
                            try:
                                api_trip_url = self.api_root + "trips/" + "{}/".format(trip_id_data)
                                connect_trip = requests.patch(api_trip_url, headers=headers, data=json.dumps(data_trip))
                                if connect_trip.status_code == 200:
                                    self.add_location_window.destroy()
                                    self.reload_trips()
                            except requests.exceptions.ConnectionError as e:
                                showinfo("Connection error", e)

            except requests.exceptions.ConnectionError as e:
                showinfo("Connection error", e)
        else:
            showinfo("Require fields", "Please fill required fields.")

    """
    Update location.
    """
    def update_location(self, location_name_data, location_body_data, location_id_data):
        api_url = self.api_root + "locations/" + "{}/".format(location_id_data)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token,
        }

        if location_name_data.get() and len(location_body_data.get("1.0", tk.END)) > 1:

            data = {
                'location_name': location_name_data.get(),
                'location_body': location_body_data.get("1.0", tk.END),
            }

            try:
                connect = requests.patch(api_url, headers=headers, data=json.dumps(data))
                if connect.status_code == 200:
                    response = connect.json()
                    if response:
                        self.edit_location_window.destroy()
                        self.reload_trips()
            except requests.exceptions.ConnectionError as e:
                showinfo("Connection error", e)
        else:
            showinfo("Require fields", "Please fill required fields.")

    """
    Render result in TreeView.
    """
    def display_trips(self, data):
        for trip in data:
            trip_date_parse = dateutil.parser.parse(trip.get('trip_date'))
            trip_date = trip_date_parse.strftime("%Y-%m-%d %H:%I %p")
            self.trip_view.insert('', tk.END, "{}-{}".format("trip", trip.get('id')), text=trip.get('trip_name'),
                                  values=("Trip", trip_date))
            if trip['trip_location'] is not None:
                for location_id in trip['trip_location']:
                    location = self.get_location_detail(location_id)
                    if location:
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
            showinfo("Error", "Unable to get token.")

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
            self.trip_window.geometry("+%d+%d" % (root_x + 50, root_y + 50))
            sel_item = item.split("-")
            # If trip selected.
            if sel_item[0] == "trip":
                trip = self.get_trip_detail(sel_item[1])
                if trip is not None:
                    self.trip_window.wm_title("Trip: " + self.trip_view.item(item, "text"))
                    self.trip_window_open = True
                    # Get locations.
                    location = []
                    for trip_loc_id in trip.get('trip_location'):
                        trip_loc = self.get_location_detail(trip_loc_id)
                        if trip_loc:
                            location.append(trip_loc.get('location_name'))
                    # Trip name.
                    trip_name_label = ttk.Label(self.trip_window, text="Trip Name")
                    trip_name_label.grid(row=0, column=0, sticky="W")
                    trip_name = ttk.Label(self.trip_window, text=": " + trip.get('trip_name'))
                    trip_name.grid(row=0, column=1, sticky="W")
                    # Trip category.
                    category = self.get_category_detail(trip.get('trip_category'))
                    if category:
                        trip_category_label = ttk.Label(self.trip_window, text="Category")
                        trip_category_label.grid(row=1, column=0, sticky="W")
                        trip_category = ttk.Label(self.trip_window, text=": " + category.get('category_name'))
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
                    # Edit and delete button add trip.
                    trip_delete_button = ttk.Button(self.trip_window, text="Delete trip",
                                                    command=lambda trip_id=trip.get('id'): self.trip_delete(trip_id))
                    trip_delete_button.grid(row=5, column=1, sticky="W")
                    trip_edit_button = ttk.Button(self.trip_window, text="Edit trip",
                                                  command=lambda trip_id=trip.get('id'): self.edit_trip_popup(trip_id))
                    trip_edit_button.grid(row=6, column=1, sticky="W")
                    location_add_button = ttk.Button(self.trip_window, text="Add location",
                                                     command=lambda trip_id=trip.get('id'):
                                                     self.add_location_popup(trip_id))
                    location_add_button.grid(row=7, column=1, sticky="W")

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
                    # Edit and delete location
                    location_delete_button = ttk.Button(self.trip_window, text="Delete location",
                                                        command=lambda location_id=location.get('id'):
                                                        self.location_delete(location_id))
                    location_delete_button.grid(row=3, column=1, sticky="W")
                    location_edit_button = ttk.Button(self.trip_window, text="Edit location",
                                                      command=lambda location_id=location.get('id'):
                                                      self.edit_location_popup(location_id))
                    location_edit_button.grid(row=4, column=1, sticky="W")

    """
    Delete trip.
    """
    def trip_delete(self, trip_id):
        api_url = self.api_root + "trips/" + "{}".format(trip_id)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token,
        }

        delete_trip = messagebox.askquestion("Delete trip", "Are you sure want to delete trip?")

        if delete_trip == 'yes':
            try:
                connect = requests.delete(api_url, headers=headers)
                if connect.status_code == 204:
                    showinfo("Success", "Trip successfully deleted.")
                    self.trip_window.destroy()
                    self.reload_trips()
            except requests.ConnectionError as e:
                showinfo("Connection error", e)

    """
    Delete location.
    """
    def location_delete(self, location_id):
        api_url = self.api_root + "locations/" + "{}".format(location_id)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + self.token,
        }

        delete_location = messagebox.askquestion("Delete location", "Are you sure want to delete location?")

        if delete_location == 'yes':
            try:
                connect = requests.delete(api_url, headers=headers)
                if connect.status_code == 204:
                    showinfo("Success", "Location successfully deleted.")
                    self.trip_window.destroy()
                    self.reload_trips()
            except requests.ConnectionError as e:
                showinfo("Connection error", e)

    """
    Quit app.
    """
    def quit_app(self):
        quit_app = messagebox.askquestion("Disconnect and quit", "Are you sure want to exit application",
                                          icon='warning')
        if quit_app == 'yes':
            self.destroy()


if __name__ == "__main__":
    trip_log_app = TripLogApp()
    trip_log_app.mainloop()
