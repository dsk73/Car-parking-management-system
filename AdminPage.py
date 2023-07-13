import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image
import datetime


class Car:
    def __init__(self, owner_name, car_number, car_color, status, entry_time):
        self.owner_name = owner_name
        self.car_number = car_number
        self.car_color = car_color
        self.status = status
        self.entry_time = entry_time
        self.exit_time = None
        self.parking_fee = 0.0

    def set_entry_time(self):
        self.entry_time = datetime.datetime.now()

    def set_exit_time(self):
        self.exit_time = datetime.datetime.now()



class ParkingLot:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Parking Lot")
        self.window.geometry('200x600')
        self.window.configure(bg='cyan')

        self.buttons = []  # Empty list to store buttons

        self.create_labels()
        self.create_image_objects()
        self.create_buttons()
        self.setup_button_handlers()

        self.occupied_slots_count = 0
        self.car_slot_empty = list(range(1, 51))
        self.car_slots = {}

        self.create_database()
        self.load_data_from_database()
        
        #self.current_status()

    def create_labels(self):
        label = tk.Label(self.window, text="Welcome to the parking lot", font=("Arial", 20, "bold"))
        label.grid(column=0, row=0, columnspan=21, pady=10)

        close_button = tk.Button(self.window, text="CLOSE", command=self.window.quit, font=("Arial", 14, "bold"),
                                 bg="red", fg="white")
        close_button.grid(column=21, row=0, pady=10)

        label_entry = tk.Label(self.window, text="ENTRY", width=8, height=5, font=("Arial", 14), bg="blue", fg="white")
        label_entry.grid(column=1, row=6)

        label_exit = tk.Label(self.window, text="EXIT", width=8, height=5, font=("Arial", 14), bg="blue", fg="white")
        label_exit.grid(column=12, row=6)
        #label_entry = tk.Label(self.window, text="ENTRY", width=8, height=5, font=("Arial", 14), bg="blue", fg="white")
        
        #label_currentStatus = tk.Label(self.window, text="CURRENT STATUS", width=8, height=5, font=("Arial", 14), bg="blue", fg="white")
        #label_currentStatus.grid(column=1, row=6)
        
    def create_buttons(self):
        slot_number = 1
        
        # Add 4 slots vertically in the first column starting from the second row
        for i in range(2, 6):
            button = tk.Button(
                self.window,
                text="Slot {}".format(slot_number),
                image=self.empty_image,
                compound=tk.TOP,  # Set text to be displayed above the image
                command=lambda idx=slot_number: self.handle_button_click(idx)
            )
            button.grid(row=i, column=0, padx=5, pady=5)
            self.buttons.append(button)
            slot_number += 1

            
        # Add 11 slots horizontally in the first row starting from the second column
        for i in range(0, 12):
            button = tk.Button(
                self.window,
                text="Slot {}".format(slot_number),
                image=self.empty_image,
                compound=tk.TOP,  # Set text to be displayed above the image
                command=lambda idx=slot_number: self.handle_button_click(idx)
            )
            button.grid(row=1, column=i + 1, padx=5, pady=5)
            self.buttons.append(button)
            slot_number += 1

        # Add 4 slots vertically in the fourteenth column starting from the second row
        for i in range(2, 6):
            button = tk.Button(
                self.window,
                text="Slot {}".format(slot_number),
                image=self.empty_image,
                compound=tk.TOP,  # Set text to be displayed above the image
                command=lambda idx=slot_number: self.handle_button_click(idx)
            )
            button.grid(row=i, column=13, padx=5, pady=5)
            self.buttons.append(button)
            slot_number += 1

        # Add 10 slots horizontally in the third row starting from the third column
        for i in range(1, 11):
            button = tk.Button(
                self.window,
                text="Slot {}".format(slot_number),
                image=self.empty_image,
                compound=tk.TOP,  # Set text to be displayed above the image
                command=lambda idx=slot_number: self.handle_button_click(idx)
            )
            button.grid(row=3, column=i + 1, padx=5, pady=5)
            self.buttons.append(button)
            slot_number += 1

        # Add 10 slots horizontally in the fourth row starting from the third column
        for i in range(1, 11):
            button = tk.Button(
                self.window,
                text="Slot {}".format(slot_number),
                image=self.empty_image,
                compound=tk.TOP,  # Set text to be displayed above the image
                command=lambda idx=slot_number: self.handle_button_click(idx)
            )
            button.grid(row=4, column=i + 1, padx=5, pady=5)
            self.buttons.append(button)
            slot_number += 1

        # Add 11 slots horizontally in the fifth row starting from the second column
        for i in range(1, 11):
            button = tk.Button(
                self.window,
                text="Slot {}".format(slot_number),
                image=self.empty_image,
                compound=tk.TOP,  # Set text to be displayed above the image
                command=lambda idx=slot_number: self.handle_button_click(idx)
            )
            button.grid(row=6, column=i+1, padx=5, pady=5)
            self.buttons.append(button)
            slot_number += 1

        remove_button = tk.Button(self.window, text="Remove Car", command=self.handle_remove_car,
                                  font=("Arial", 14, "bold"), bg="red", fg="white")
        remove_button.grid(column=0, row=7, columnspan=10, pady=10)

        availability_button = tk.Button(self.window, text="Check Availability", command=self.display_status,
                                        font=("Arial", 14, "bold"), bg="green", fg="white")
        availability_button.grid(column=10, row=7, columnspan=10, pady=10)
        
        currentStatus_button = tk.Button(self.window, text="CURRENT STATUS", command=self.current_status,
                                        font=("Arial", 14, "bold"), bg="blue", fg="white")
        currentStatus_button.grid(column=13, row=7, columnspan=10, pady=10)

    def create_image_objects(self):
        self.empty_image = self.load_image('empty_slot.png', (100, 130))
        self.red_car_image = self.load_image('red_car.png', (100, 130))
        self.blue_car_image = self.load_image('blue_car.png', (100, 130))
        self.green_car_image = self.load_image('green_car.png', (100, 130))
        self.black_car_image = self.load_image('black_car.png', (100, 130))
        self.white_car_image = self.load_image('white_car.png', (100, 130))
        self.grey_car_image = self.load_image('grey_car.png', (100, 130))
        self.orange_car_image = self.load_image('orange_car.png', (100, 130))
        self.yellow_car_image = self.load_image('yellow_car.png', (100, 130))
        self.default_car_image = self.load_image('default_car.png', (100, 130))

    def load_image(self, filename, size):
        image = Image.open(filename)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def setup_button_handlers(self):
        for i, button in enumerate(self.buttons):
            button.configure(command=lambda idx=i+1: self.handle_button_click(idx))

    def handle_button_click(self, index):
        if self.occupied_slots_count < 20:
            self.assign_parking_slot(index)
        else:
            messagebox.showerror("Parking Allotment", "The parking lot is full. Please try again later.")

    def assign_parking_slot(self, index):
        slot_number = index
        if slot_number not in self.car_slot_empty:
            car = self.car_slots[slot_number]
            messagebox.showinfo("Parking Allotment",
                                "Slot {} is already occupied.\n\nOwner's Name: {}\nCar Number: {}\nCar Color: {}\nStatus: {}\nEntry Time: {}".format(
                                    slot_number, car.owner_name, car.car_number, car.car_color, car.status, car.entry_time))
        else:
            owner_name = simpledialog.askstring("Car Information", "Enter owner's name:")
            car_number = simpledialog.askstring("Car Information", "Enter car number:")
            if owner_name and car_number:
                car_color = self.get_car_color()
                entry_time = datetime.datetime.now()  # Get the current time as the entry time
                car = Car(owner_name, car_number, car_color, "Reserved", entry_time)  # Pass entry_time parameter
                self.car_slots[slot_number] = car
                self.buttons[index-1].configure(image=self.get_car_image(car_color))
                self.car_slot_empty.remove(slot_number)
                self.occupied_slots_count += 1
                self.insert_car_into_database(slot_number, car)
                messagebox.showinfo("Welcome to the Parking Lot", "Slot {} is assigned to you.".format(slot_number))


    def remove_car(self, slot_number):
        if slot_number in self.car_slot_empty:
            messagebox.showinfo("Parking Allotment", "Slot {} is already empty.".format(slot_number))
        else:
            car = self.car_slots[slot_number]
            entry_time = car.entry_time
            exit_time = datetime.datetime.now()  # Assuming current time is the exit time

            duration = exit_time - entry_time
            hours = duration.total_seconds() / 3600  # Convert duration to hours

            parking_fee = self.calculate_parking_fee(hours)
            car.parking_fee = parking_fee  # Assign the parking fee to the car

            messagebox.showinfo("Parking Allotment","Parking Duration: {}\nParking Fee: ${:.2f}".format(duration, parking_fee))

            del self.car_slots[slot_number]
            self.buttons[slot_number - 1].configure(image=self.empty_image)
            self.car_slot_empty.append(slot_number)
            self.car_slot_empty.sort()
            self.occupied_slots_count -= 1
            self.delete_car_from_database(slot_number)  # Add this method call

            

    def handle_car_exit(self, slot_number):
        if slot_number in self.car_slot_empty:
            messagebox.showinfo("Parking Allotment", "Slot {} is already empty.".format(slot_number))
        else:
            car = self.car_slots[slot_number]
            car.set_exit_time()  # Set the exit time for the car

            entry_time = car.entry_time
            exit_time = car.exit_time

            duration = exit_time - entry_time
            hours = duration.total_seconds() / 3600  # Convert duration to hours

            parking_fee = self.calculate_parking_fee(hours)
            car.parking_fee = parking_fee  # Assign the parking fee to the car

            self.remove_car(slot_number)

            messagebox.showinfo("Parking Allotment", "Slot {} is now available.".format(slot_number))

    def calculate_parking_fee(self, hours):
        
        fee_per_hour = 50
        return hours * fee_per_hour



    def handle_remove_car(self):
        slot_number = simpledialog.askinteger("Remove Car", "Enter slot number to remove car from:")
        if slot_number:
            self.handle_car_exit(slot_number)

    def display_status(self):
        messagebox.showinfo("Parking Allotment", "{} cars are parked. {} slots are free.".format(
            self.occupied_slots_count, 50 - self.occupied_slots_count))

    def get_car_color(self):
        colors = ["red", "blue", "green", "black", "white","grey","orange","yellow"]
        color = simpledialog.askstring("Car Color", "Enter car color (red, blue, green, black, white, grey, orange, yellow):")
        if color in colors:
            return color
        else:
            return "default"

    def get_car_image(self, car_color):
        if car_color == "red":
            return self.red_car_image
        elif car_color == "blue":
            return self.blue_car_image
        elif car_color == "green":
            return self.green_car_image
        elif car_color == "black":
            return self.black_car_image
        elif car_color == "white":
            return self.white_car_image
        elif car_color == "grey":
            return self.grey_car_image
        elif car_color == "orange":
            return self.orange_car_image
        elif car_color == "yellow":
            return self.yellow_car_image
        else:
            return self.default_car_image

    def create_database(self):
        conn = sqlite3.connect('parking_lot.db')
        c = conn.cursor()

        # Create table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS cars
                      (slot_number INT, owner_name TEXT, car_number TEXT, car_color TEXT, status TEXT,
                      entry_time TEXT, exit_time TEXT)''')

        # Create a separate table for removed cars
        c.execute('''CREATE TABLE IF NOT EXISTS removed_cars
                      (slot_number INT, owner_name TEXT, car_number TEXT, car_color TEXT,
                      entry_time TEXT, exit_time TEXT)''')

        conn.commit()
        conn.close()


    def insert_car_into_database(self, slot_number, car):
        conn = sqlite3.connect('parking_lot.db')
        c = conn.cursor()

        c.execute("INSERT INTO cars (slot_number, owner_name, car_number, car_color, status,entry_time) VALUES (?, ?, ?, ?, ?, ?)",
                  (slot_number, car.owner_name, car.car_number, car.car_color, car.status, car.entry_time))

        conn.commit()
        conn.close()



    def delete_car_from_database(self, slot_number):
        conn = sqlite3.connect('parking_lot.db')
        c = conn.cursor()

        # Get the car data before deleting
        c.execute("SELECT * FROM cars WHERE slot_number=?", (slot_number,))
        row = c.fetchone()

        if row:
            # Insert the removed car data into the removed_cars table
            c.execute("INSERT INTO removed_cars (slot_number, owner_name, car_number, car_color, entry_time, exit_time) VALUES (?, ?, ?, ?, ?, ?)",
                      (row[0], row[1], row[2], row[3], row[5], row[6]))

        # Delete the car from the cars table
        c.execute("DELETE FROM cars WHERE slot_number=?", (slot_number,))

        conn.commit()
        conn.close()


    def load_data_from_database(self):
        conn = sqlite3.connect('parking_lot.db')
        c = conn.cursor()

        c.execute("SELECT * FROM cars")
        rows = c.fetchall()

        for row in rows:
            slot_number, owner_name, car_number, car_color, status, *_ = row
            entry_time = datetime.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S.%f")  # Parse the entry time string with milliseconds
            car = Car(owner_name, car_number, car_color, status, entry_time)
            self.car_slots[slot_number] = car
            self.buttons[slot_number - 1].configure(image=self.get_car_image(car_color))
            self.car_slot_empty.remove(slot_number)
            self.occupied_slots_count += 1
            
        conn.close()

        
    def load_data(self):
        conn = sqlite3.connect('parking_lot.db')
        c = conn.cursor()

        c.execute("SELECT * FROM cars")
        rows = c.fetchall()

        conn.close()
        
	
        return rows

    def current_status(self):
        # Load data from the database
        rows = self.load_data()

        # Create a new window for displaying the history
        history_window = tk.Toplevel(self.window)
        history_window.title("current status")

        # Create a Treeview widget to display the history
        tree = ttk.Treeview(history_window)
        tree["columns"] = ("Slot Number", "Owner Name", "Car Number", "Car Color", "status","Entry Time")

        # Configure column headings style
        tree.heading("#0", text="Serial Number", anchor=tk.CENTER)
        tree.heading("Slot Number", text="Slot Number", anchor=tk.CENTER)
        tree.heading("Owner Name", text="Owner Name", anchor=tk.CENTER)
        tree.heading("Car Number", text="Car Number", anchor=tk.CENTER)
        tree.heading("Car Color", text="Car Color", anchor=tk.CENTER)
        tree.heading("status", text="Status", anchor=tk.CENTER)
        tree.heading("Entry Time", text="Entry Time", anchor=tk.CENTER)
    

        # Configure column cells style
        tree.column("#0", width=100, anchor=tk.CENTER)
        tree.column("Slot Number", width=100, anchor=tk.CENTER)
        tree.column("Owner Name", width=150, anchor=tk.CENTER)
        tree.column("Car Number", width=100, anchor=tk.CENTER)
        tree.column("Car Color", width=100, anchor=tk.CENTER)
        tree.column("status", width=100, anchor=tk.CENTER)
        tree.column("Entry Time", width=150, anchor=tk.CENTER)
        

        for i, row in enumerate(rows, start=1):
            tree.insert("", tk.END, iid=str(i), text=str(i), values=row)

        tree.pack(pady=10, padx=10)

        # Apply a custom style to the Treeview widget
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25, show="tree headings")
        style.configure("Treeview.Tree", background="#FFFFFF")
        style.configure("Treeview.Cell", borderwidth=1, relief="solid")


        # Configure column lines
        #style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'))
        #style.configure("Treeview", font=('Helvetica', 12), rowheight=25, show="tree")
        #style.configure("Treeview.Treeview", background="white", foreground="black")

        # Add lines between columns
        #style.layout("Treeview.Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove default border
        #style.layout("Treeview.Cell", [('Treeview.Cell.border', {'sticky': 'nswe', 'children':
        #                       [('Treeview.Cell.padding', {'sticky': 'nswe', 'children':
        #                        [('Treeview.Cell.cell', {'sticky': 'nswe'})]})]})])

        # Add lines between rows
        #style.map("Treeview.Treeview", background=[('selected', '#1E90FF')], foreground=[('selected', 'white')])
        #style.configure("Treeview.Treeview", fieldbackground="white", highlightthickness=1,
        #               highlightcolor="#D3D3D3", highlightbackground="#D3D3D3")

        history_window.mainloop()
    def run(self):
        self.window.mainloop()

parking_lot = ParkingLot()
parking_lot.run()
