import threading
import time
import traceback
from tkinter import *
from tkinter import messagebox, font, filedialog

from PIL import ImageTk

import merger as mg

ENTRY_BG_COLOR = "#f7e6ad"
BG_COLOR = "#ffffff"


class ProgramInterface(Frame):
    def __init__(self):
        Frame.__init__(self)
        frame = Frame()
        merger = mg.Merger()
        sides = 80
        vertically = 80
        merger.move_down(vertically)
        merger.move_right(sides)
        # self.csv_worker = CSVWorker.CSVWorker()
        # self.csv_worker_thread = threading.Thread(target=self.csv_worker.main_loop, daemon=True)
        # self.csv_worker_thread.start()
        # GUI ico
        self.master.iconbitmap('Resources/shirt.ico')
        # GUI title
        self.master.title('Design applier')
        # GUI size
        self.master.geometry("610x565+500+200")
        # gui always-on-top
        self.master.wm_attributes("-topmost", 1)
        self.master.resizable(0, 0)
        # Background color
        frame.configure(bg=BG_COLOR)
        #  Font description
        font11 = font.Font(family="Roboto", size=11, weight='bold')
        #  Packing decision
        frame.pack(fill="both", expand=True)
        self.save_btn = PhotoImage(file='Resources/button_save.png')
        self.select_btn = PhotoImage(file='Resources/button_select.png')
        self.left_arrow_btn = PhotoImage(file='Resources/left_arrow_button.png')
        self.right_arrow_btn = PhotoImage(file='Resources/right_arrow_button.png')
        self.up_arrow_btn = PhotoImage(file='Resources/button_up.png')
        self.down_arrow_btn = PhotoImage(file='Resources/button_down.png')
        self.set_btn = PhotoImage(file='Resources/button_set.png')
        self.plus_btn = PhotoImage(file='Resources/button_plus.png')
        self.minus_btn = PhotoImage(file='Resources/button_minus.png')
        self.merge_all_btn = PhotoImage(file='Resources/button_merge-all.png')

        # Select cloths folder section:
        # Text label for cloth
        self.pict_cloth = Label(frame, text="Location of folder with clothing:", bg=BG_COLOR, font=font11, fg="#424c58")
        self.pict_cloth.place(x=20, y=20)

        # Entry for cloths folder
        self.pict_cloth_Entry = Entry(frame, width=34, bg=ENTRY_BG_COLOR)
        self.pict_cloth_Entry.place(x=266, y=23)

        # Function for clicking Save cloth
        def click_pick_cloth(event):
            try:
                hoodie_path = str(self.pict_cloth_Entry.get())
                merger.open_main_image_folder(hoodie_path)  # return
            except:
                messagebox.showerror("Error", "Mistake in directory to clothing png")
            return event

        # Button to confirm cloths folder
        self.pict_cloth_Button = Button(frame, image=self.save_btn, borderwidth=0, bg=BG_COLOR)
        self.pict_cloth_Button.bind("<ButtonRelease-1>", click_pick_cloth)
        self.pict_cloth_Button.place(x=540, y=17)

        # Function for button allowing to use OS selection for file
        def select_file_location(event):
            pic_file_name = filedialog.askdirectory(title="Select folder with pictures of clothing")
            # self.pict_cloth_Entry.config(text=pic_file_name)
            self.pict_cloth_Entry.delete(0, len(str(self.pict_cloth_Entry.get())))
            self.pict_cloth_Entry.insert(0, pic_file_name)
            return event

        # Button to select file location
        self.pict_cloth_file = Button(frame, image=self.select_btn, borderwidth=0, bg=BG_COLOR)
        self.pict_cloth_file.bind("<ButtonRelease-1>", select_file_location)
        self.pict_cloth_file.place(x=476, y=17)

        # End of select cloths folder section
        # --------------------=--------------------

        # Select designs folder section:
        # Text label for design
        self.fold_desi = Label(frame, text="Location of folder with designs", bg=BG_COLOR, font=font11, fg="#424c58")
        self.fold_desi.place(x=20, y=58)

        # Entry for design folder
        self.fold_desi_Entry = Entry(frame, width=34, bg=ENTRY_BG_COLOR)
        self.fold_desi_Entry.place(x=265, y=61)

        # Function which displays cloth and design on GUI
        def picture_in_gui():
            # try:
            self.img = ImageTk.PhotoImage(image=merger.get_display(size=(280, 365)))
            self.panel = Label(frame, image=self.img)
            self.panel.place(x=20, y=110)

        # Function which happens after clicking save design folder
        def click_fold_desi(event):
            try:
                design_path = str(self.fold_desi_Entry.get())
                merger.set_design_folder(design_path)
                merger.resize_to_set_size()
                picture_in_gui()
            except:
                messagebox.showerror("Error",
                                     "Couldn't read design photos from given folder. Check if folder contains 'png' files")
            return event

        # Button to save design folder
        self.fold_desi_Button = Button(frame, image=self.save_btn, borderwidth=0, bg=BG_COLOR)
        self.fold_desi_Button.bind("<ButtonRelease-1>", click_fold_desi)
        self.fold_desi_Button.place(x=540, y=53)

        # Function which happens after clicking select design folder
        def select_folder_location(event):
            pic_file_name = filedialog.askdirectory(title="Select folder with designs")
            self.fold_desi_Entry.delete(0, len(str(self.fold_desi_Entry.get())))
            self.fold_desi_Entry.insert(0, pic_file_name)
            return event

        # Button to select designs folder location
        self.pict_cloth_file = Button(frame, image=self.select_btn, borderwidth=0, bg=BG_COLOR)
        self.pict_cloth_file.bind("<ButtonRelease-1>", select_folder_location)
        self.pict_cloth_file.place(x=476, y=53)

        # End of select designs folder section
        # --------------------=--------------------

        # Set opacity section:
        # Function on button "Set"
        def opacity_set(event):
            try:
                merger.change_opacity(opacity=int(self.opacity_Entry.get()))
                picture_in_gui()
            except Exception as ex:
                print(ex)
                messagebox.showerror("Error", "Mistake in setting opacity")
            return event

        # Button for setting opacity
        self.opacity_Button = Button(frame, image=self.set_btn, borderwidth=0, bg=BG_COLOR)
        self.opacity_Button.bind("<ButtonRelease-1>", opacity_set)
        self.opacity_Button.place(x=461, y=245)

        # Opacity entry
        self.opacity_Entry = Entry(frame, width=3, bg=ENTRY_BG_COLOR)
        self.opacity_Entry.insert(END, str(merger.opacity))
        self.opacity_Entry.place(x=431, y=253)

        # Text label for setting opacity
        self.Info1 = Label(frame, text="Set opacity", bg=BG_COLOR, font=font11, fg="#424c58")
        self.Info1.place(x=421, y=283)

        # End of set opacity section
        # --------------------=--------------------

        def click_main_left_arrow(event):
            try:
                merger.set_previous_main_image()
                picture_in_gui()
            except:
                messagebox.showerror("Error", "Couldn't select previous main image")
            return event

        self.main_left_arrow_key = Button(frame, image=self.left_arrow_btn, borderwidth=0, bg=BG_COLOR)
        self.main_left_arrow_key.bind("<ButtonRelease-1>", click_main_left_arrow)
        self.main_left_arrow_key.place(x=20, y=470)

        def click_main_right_arrow(event):
            try:
                merger.set_next_main_image()
                picture_in_gui()
            except:
                messagebox.showerror("Error", "Couldn't select next main image")
            return event

        self.main_right_arrow_key = Button(frame, image=self.right_arrow_btn, borderwidth=0, bg=BG_COLOR)
        self.main_right_arrow_key.bind("<ButtonRelease-1>", click_main_right_arrow)
        self.main_right_arrow_key.place(x=286, y=475)

        # Move design section:
        # Arrows to move design on cloth
        def click_left_arrow(event):
            try:
                merger.move_left(int(self.Pix_move_Entry.get()))
                picture_in_gui()
            except:
                messagebox.showerror("Error", "Couldn't move design to the left")
            return event

        self.left_arrow_key = Button(frame, image=self.left_arrow_btn, borderwidth=0, bg=BG_COLOR)
        self.left_arrow_key.bind("<ButtonRelease-1>", click_left_arrow)
        self.left_arrow_key.place(x=415, y=140)

        def click_right_arrow(event):
            try:
                merger.move_right(int(self.Pix_move_Entry.get()))
                picture_in_gui()
            except:
                messagebox.showerror("Error", "Couldn't move design to the right")
            return event

        self.right_arrow_key = Button(frame, image=self.right_arrow_btn, borderwidth=0, bg=BG_COLOR)
        self.right_arrow_key.bind("<ButtonRelease-1>", click_right_arrow)
        self.right_arrow_key.place(x=475, y=140)

        def click_up_arrow(event):
            try:
                merger.move_up(int(self.Pix_move_Entry.get()))
                picture_in_gui()
            except:
                messagebox.showerror("Error", "Couldn't move design to the up")
            return event

        self.up_arrow_key = Button(frame, image=self.up_arrow_btn, borderwidth=0, bg=BG_COLOR)
        self.up_arrow_key.bind("<ButtonRelease-1>", click_up_arrow)
        self.up_arrow_key.place(x=441, y=120)

        def click_down_arrow(event):
            try:
                merger.move_down(int(self.Pix_move_Entry.get()))
                picture_in_gui()
            except:
                messagebox.showerror("Error", "Couldn't move design to the down")
            return event

        self.down_arrow_key = Button(frame, image=self.down_arrow_btn, borderwidth=0, bg=BG_COLOR)
        self.down_arrow_key.bind("<ButtonRelease-1>", click_down_arrow)
        self.down_arrow_key.place(x=441, y=170)

        # Default amount of pixels to move design
        self.Pix_move_Entry = Entry(frame, width=4, bg=ENTRY_BG_COLOR)
        self.Pix_move_Entry.insert(END, '100')
        self.Pix_move_Entry.place(x=445, y=147)

        # Text label for moving design
        self.Info = Label(frame, text="Move design", bg=BG_COLOR, font=font11, fg="#424c58")
        self.Info.place(x=411, y=200)

        # End of move design section
        # --------------------=--------------------

        # Design size section:
        # Buttons to increase/decrease design size
        def click_plus(event):
            try:
                merger.increase_size(size=int(self.Design_size_Entry.get()))
                picture_in_gui()
            except:
                messagebox.showerror("Error", "Couldn't increase design")
            return event

        self.plus_key = Button(frame, image=self.plus_btn, borderwidth=0, bg=BG_COLOR)
        self.plus_key.bind("<ButtonRelease-1>", click_plus)
        self.plus_key.place(x=421, y=323)

        def click_minus(event):
            try:
                merger.decrease_size(size=int(self.Design_size_Entry.get()))
                picture_in_gui()
            except:
                messagebox.showerror("Error", "Couldn't reduce design")
            return event

        self.minus_key = Button(frame, image=self.minus_btn, borderwidth=0, bg=BG_COLOR)
        self.minus_key.bind("<ButtonRelease-1>", click_minus)
        self.minus_key.place(x=482, y=323)

        # Default amount of pixels to increase/decrease design size
        self.Design_size_Entry = Entry(frame, width=4, bg=ENTRY_BG_COLOR)
        self.Design_size_Entry.insert(END, '50')
        self.Design_size_Entry.place(x=451, y=331)

        # Text label for increase/decrease design
        self.Info1 = Label(frame, text="Design width", bg=BG_COLOR, font=font11, fg="#424c58")
        self.Info1.place(x=416, y=363)

        # End of design size section
        # --------------------=--------------------
        # Begin of design height section
        # Buttons to increase/decrease design height
        def click_plus_height(event):
            try:
                merger.increase_height(amount=int(self.Design_height_entry.get()))
                picture_in_gui()
            except:
                messagebox.showerror("Error", "Couldn't increase height")
            return event

        self.plus_key_height = Button(frame, image=self.plus_btn, borderwidth=0, bg=BG_COLOR)
        self.plus_key_height.bind("<ButtonRelease-1>", click_plus_height)
        self.plus_key_height.place(x=421, y=403)

        def click_minus_height(event):
            try:
                merger.decrease_height(amount=int(self.Design_height_entry.get()))
                picture_in_gui()
            except:
                messagebox.showerror("Error", "Couldn't reduce height")
            return event

        self.minus_key_height = Button(frame, image=self.minus_btn, borderwidth=0, bg=BG_COLOR)
        self.minus_key_height.bind("<ButtonRelease-1>", click_minus_height)
        self.minus_key_height.place(x=482, y=403)

        # Default amount of pixels to increase/decrease design size
        self.Design_height_entry = Entry(frame, width=4, bg=ENTRY_BG_COLOR)
        self.Design_height_entry.insert(END, '50')
        self.Design_height_entry.place(x=451, y=411)

        # Text label for increase/decrease design
        self.Info1 = Label(frame, text="Design height", bg=BG_COLOR, font=font11,
                           fg="#424c58")
        self.Info1.place(x=416, y=443)

        # End of design height section
        # --------------------=--------------------
        def run_merger(event):
            try:
                start = time.time()
                print((time.time() - start))
                print("Merging all starts")
                start = time.time()
                merger.merge_all(maxi=0)
                print("{:.1f}".format(time.time() - start), "Seconds")
                picture_in_gui()
            except Exception:
                print(traceback.format_exc())
                messagebox.showerror("Error", "Couldn't start script (All)")
            return event

        self.up_arrow_key = Button(frame, image=self.merge_all_btn, borderwidth=0, bg=BG_COLOR)
        self.up_arrow_key.bind("<ButtonRelease-1>", run_merger)
        self.up_arrow_key.place(x=425, y=495)

        # # Text label for product name UK
        self.product_name_UK = Label(frame, text="Prod. name:", bg=BG_COLOR, font=font11, fg="#424c58")
        # self.product_name_UK.place(x=359, y=260)
        #
        # Entry for product name UK
        self.product_name_UK_Entry = Entry(frame, width=20, bg=ENTRY_BG_COLOR)
        # self.product_name_UK_Entry.place(x=475, y=264)
        #


def gui():
    ProgramInterface().mainloop()


def main():
    gui()


main()
