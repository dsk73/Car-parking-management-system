import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image


class Car:
    def _init_(self, owner_name, car_number, car_color, status):
        self.owner_name = owner_name
        self.car_number = car_number
        self.car_color = car_color
        self.status = status


class CarIn:
    def _init_(self, parking_lot):
        self.parking_lot = parking_lot

    def handle_button_click(self, index):
        if self.parking_lot.occupied_slots_count < 20:
            self.assign_parking_slot(index)
        else:
            messagebox.showerror("Parking Allotment", "The parking lot is full. Please try again later.")

    def assign_parking_slot(self, index):
        slot_number = index + 1
        if slot_number not in self.parking_lot.car_slot_empty:
            car = self.parking_lot.car_slots[slot_number]
            messagebox.showinfo(
                "Parking Allotment",
                "Slot {} is already occupied.\n\nOwner's Name: {}\nCar Number: {}\nCar Color: {}\nStatus: {}".format(
                    slot_number, car.owner_name, car.car_number, car.car_color, car.status
                ),
            )
        else:
            owner_name = simpledialog.askstring("Car Information of Slot {}".format(slot_number), "Enter owner's name:")
            car_number = simpledialog.askstring("Car Information of Slot {}".format(slot_number), "Enter car number:")
            if owner_name and car_number:
                car_color = self.parking_lot.get_car_color()
                car = Car(owner_name, car_number, car_color, "Reserved")
                self.parking_lot.car_slots[slot_number] = car
                self.parking_lot.buttons[index].configure(image=self.parking_lot.get_car_image(car_color))
                self.parking_lot.car_slot_empty.remove(slot_number)
                self.parking_lot.occupied_slots_count += 1
                self.parking_lot.insert_car_into_database(slot_number, car)
                messagebox.showinfo("Welcome to the Parking Lot", "Slot {} is assigned to you.".format(slot_number))


class CarOut:
    def _init_(self, parking_lot):
        self.parking_lot = parking_lot

    def handle_remove_car(self):
        slot_number = simpledialog.askinteger("Remove Car", "Enter slot number to remove car from:")
        if slot_number:
            self.remove_car(slot_number)

    def remove_car(self, slot_number):
        if slot_number in self.parking_lot.car_slot_empty:
            messagebox.showinfo("Parking Allotment", "Slot {} is already empty.".format(slot_number))
        else:
            del self.parking_lot.car_slots[slot_number]
            self.parking_lot.buttons[slot_number - 1].configure(image=self.parking_lot.empty_image)
            self.parking_lot.car_slot_empty.append(slot_number)
            self.parking_lot.car_slot_empty.sort()
            self.parking_lot.occupied_slots_count -= 1
            self.parking_lot.delete_car_from_database(slot_number)
            messagebox.showinfo("Parking Allotment", "Slot {} is now available.".format(slot_number))


class ParkingLot:
    def _init_(self):
        self.window = tk.Tk()
        self.window.title("Parking Lot")
        self.window.geometry('1920x1080')
        self.window.configure(bg='gray')

        self.buttons = []  # Empty list to store buttons

        self.create_labels()
        self.create_image_objects()
        self.create_buttons()
        self.setup_button_handlers()

        self.occupied_slots_count