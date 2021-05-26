import io
import math
from tkinter import messagebox

from PIL import Image, ImageFilter
import glob
import os
import json

# import CSVWorker
import file_uploader as fu
import random


def read_design_name(location: str) -> (str, str):
    filename = os.path.basename(location)
    name = filename[:-4]
    design_id, *design_name = name.split()
    design_name = " ".join(design_name)
    return design_id, design_name


def fit_to_size(image_size: (int, int), target_size: (int, int)) -> (int, int):
    width_ratio = image_size[0] / target_size[0]
    height_ratio = image_size[1] / target_size[1]
    if math.isclose(width_ratio, height_ratio):
        return target_size
    elif width_ratio > height_ratio:
        return target_size[0], int(image_size[1] / width_ratio)
    else:
        return int(image_size[0] / height_ratio), target_size[1]


class Merger:

    def __init__(self):

        self.access_token: str = ""
        self.output_append = "_applied"
        self.overwrite = True
        self.upload_location = "/designs/"
        self.load_settings()
        self.design_image = None
        self.design_image_resized = None
        self.main_images_names = None
        self.main_image_counter = 0
        self.main_image = None
        self.design_image_name = None
        self.rectangle = None
        # GUI options
        self.product_name = ""  # name taken from GUI
        self.merged_image = None
        self.offset = [0, 0]
        self.output_path = None
        self.display_image = None
        self.centre = [0, 0]
        self.ratio = 1.414196123147092
        self.set_size = (600, int(600 * self.ratio))
        self.opacity = 245
        self.folder = None
        self.filenames = []
        self.sort_by_alphabet = True
        self.IMAGE_TYPE = "png"

        self.get_rectangle()
        random.seed()

    # class MainImage:
    #     def __init__(self):
    #

    def error_log(self, text):
        print('!E!', text)

    def set_options(self, **options):
        self.__dict__.update(options)
        return

    def load_settings(self):
        try:
            settings = open("settings.json", 'r')
        except IOError:
            print("Settings file not found")
            # Create the settings file
            with open("settings.json", 'w') as settings_json:
                settings = {
                    "output_append": self.output_append,
                    "overwrite": self.overwrite,
                    "access_token": "YOUR_ACCESS_TOKEN",
                    "upload_location": "/designs/"
                }
                json.dump(settings, settings_json, indent=3)
        except:
            print("Something else wrong with file")
        else:
            try:
                settings_dict = json.loads(settings.read())
            except json.JSONDecodeError:
                print("Bad json format")
            except:
                print("Something else wrong with json")
            else:
                self.access_token = settings_dict['access_token']
                self.output_append = settings_dict['output_append']
                self.overwrite = settings_dict['overwrite']
                self.upload_location = settings_dict['upload_location']
                return
        return

    def set_main_image(self, location):
        try:
            self.main_image = Image.open(location)
        except IOError:
            print("error: can't set main image")
            return False

    def set_next_main_image(self):
        self.main_image_counter += 1
        self.main_image_counter %= len(self.main_images_names)
        print("Main image Nr:", self.main_image_counter)
        self.set_main_image(self.main_images_names[self.main_image_counter])

    def set_previous_main_image(self):
        self.main_image_counter -= 1
        self.main_image_counter %= len(self.main_images_names)
        print("Main image Nr:", self.main_image_counter)
        self.set_main_image(self.main_images_names[self.main_image_counter])

    def open_main_image_folder(self, folder_location):  # returns image_id and image name
        try:
            self.main_images_names = glob.glob(os.path.join(folder_location, '*.png'))
            if self.sort_by_alphabet:
                self.main_images_names.sort()
            self.main_image_counter = 0
            self.set_main_image(self.main_images_names[0])
        except:
            messagebox.showerror("Error","Couldn't read clothes photos from given folder. Check if folder contains 'png' files")

    def merge_current(self, centre=None, fit: bool=True) -> None:
        if self.design_image is not None and self.main_image is not None:
            if self.design_image_resized is None or not fit:
                self.resize_to_set_size(fit=fit)
            if centre is None:
                centre = self.find_centre()
            if self.offset != [0, 0]:
                centre = list(centre)
                centre[0] += self.offset[0]
                centre[1] += self.offset[1]
                centre = tuple(centre)
            self.merged_image = self.main_image.copy()
            self.merged_image.alpha_composite(self.design_image_resized, centre)
            self.display_image = None
        else:
            print("Error: images not set")
        return

    def read_designs(self, folder) -> None:
        try:
            self.filenames = glob.glob(os.path.join(folder, '*.png'))
        except Exception as err:
            self.error_log(err)
        if len(self.filenames) == 0:
            self.error_log("No designs found in this directory:", folder)
            return
        self.set_design_image(self.filenames[0])

    def set_design_folder(self, folder) -> None:
        self.folder = folder
        self.read_designs(folder)

    def merge_all(self, maxi=None) -> None:
        # ExcelEditor.init_excel()
        # self.update_emi(emi=emi)
        counter = 0
        uploader = fu.get_file_uploader(self.access_token)
        # check if token is set right
        if not uploader.check_connection():
            self.error_log("Bad connection to dropbox. Maybe your token is wrong.")
            return
        if maxi is not None and maxi != 0:
            total_amount = maxi
        else:
            total_amount = len(self.filenames)
        for filename in self.filenames:
            if total_amount and counter > total_amount:
                del uploader
                return
            # # clean memory for potential thrash
            # del self.design_image_resized
            # del self.design_image
            # del self.merged_image
            # del self.display_image
            if not self.design_image_name == filename:
                self.set_design_image(filename)
            self.resize_to_set_size()
            self.change_opacity()
            self.merge_current()
            # self.write_to_file(self.output_path)
            counter += 1
            design_id, design_name = read_design_name(self.design_image_name)
            # TODO add random str to filenames DONE
            # TODO create rectangle
            url = self.upload_image(uploader=uploader, design_id=design_id, design_name=design_name)
            # if csv:
            #     self.write_excel(emi=emi, url=url, design_name=design_name, design_id=design_id, csv_worker=csv_worker)
            print(counter, "/", total_amount, design_id, design_name)
        # csv_worker.convert = True
        self.set_next_main_image()
        self.merged_image = None
        self.set_design_image(self.filenames[0])
        del uploader
        return

    def upload_image(self, uploader: fu.FileUploader, design_id: str, design_name: str) -> str:
        binary_image = io.BytesIO()
        if self.merged_image is None:
            self.merge_current()
        self.merged_image.save(binary_image, self.IMAGE_TYPE)
        binary_image.seek(0)
        upload_filename = "{0}{1} {2} {3}-{4:05x}.{5}".format(self.upload_location, design_id.strip(),
                            design_name.strip(), self.product_name.strip(), random.randrange(0xfffff), self.IMAGE_TYPE)
        url = uploader.upload_image(binary_image, upload_filename)
        # url = url[:-1] + '1'  # change last digit (0 -> 1) to make id downloadable instantly
        print(url)
        return url

    def resize_to_set_size(self, size=None, quality=True, fit=True):
        if size is None:
            size = self.set_size
        if quality:
            filter_to_use = Image.LANCZOS
        else:
            filter_to_use = Image.NEAREST
        if self.design_image is None:
            print("Design image is not set")
        if self.main_image is None:
            print("Main image is not set")
        if fit:
            size = fit_to_size(self.design_image.size, size)
        self.design_image_resized = self.design_image.resize(size, filter_to_use)
        self.merged_image = None
        self.display_image = None

    def set_design_image(self, location) -> bool:
        try:
            self.design_image = Image.open(location).convert(mode="RGBA")
            self.design_image_name = os.path.basename(location)
            self.merged_image = None
            self.design_image_resized = None
        except IOError:
            print("Something very bad with design images")
            return False
        self.display_image = None
        return True

    def find_centre(self) -> (int, int):
        centre = (int((self.main_image.size[0] - self.design_image_resized.size[0]) / 2),
                  int((self.main_image.size[1] - self.design_image_resized.size[1]) / 2))
        return centre

    def set_rectangle(self):
        self.design_image = self.rectangle
        self.design_image_resized = None

    def get_rectangle(self, size=400):
        rectangle = Image.open("Resources/rectangle.png")
        self.rectangle = rectangle

    def get_display(self, size=(300, 400), rectangle=True) -> Image:
        if rectangle:
            self.set_rectangle()
            self.merge_current(fit=False)
        if self.merged_image is None:
            self.merge_current()
        if self.display_image is None:
            self.display_image = self.merged_image.resize(fit_to_size(self.merged_image.size, size))
        return self.display_image

    def set_output_path(self, path):
        self.output_path = path

    def write_to_file(self, path=None) -> None:
        if not os.path.exists(os.path.join(self.folder, "applied")):
            print("Creating folder for applied designs")
            try:
                os.mkdir(os.path.join(self.folder, "applied"))
            except OSError:
                print("Can't create a folder in your design folder: ", os.path.join(self.folder, "applied"))
                print("Please create a folder in your designs directory named: 'applied'")
                return
        if path is None:
            path = os.path.join(self.folder, "applied", os.path.splitext(self.design_image_name)[0] + self.output_append
                                + os.path.splitext(self.design_image_name)[1])
        else:
            path = os.path.join(path, os.path.splitext(self.design_image_name)[0] + self.output_append +
                                os.path.splitext(self.design_image_name)[1])
        if os.path.exists(path) and not self.overwrite:
            return
        if self.merged_image is None:
            self.merge_current()
        self.merged_image.save(path)

    def add_blur(self):
        self.merged_image = None
        self.display_image = None
        self.design_image_resized = self.design_image_resized.filter(ImageFilter.GaussianBlur(radius=1))
        return

    def change_opacity(self, opacity=None, redo=True):
        if opacity is not None:
            self.opacity = opacity
        if redo:
            self.resize_to_set_size()
        ratio = self.opacity / 255
        data = self.design_image_resized.getdata()  # you'll get a list of tuples
        new_data = []
        for a in data:
            b = a[:3]
            b = b + (int(a[3]*ratio) if a[3] != 0 else 0,)
            new_data.append(b)
        self.design_image_resized.putdata(new_data)
        self.merge_current()
        self.display_image = None
        return

    def move_up(self, step: int):
        self.offset[1] -= step
        self.merge_current()
        return

    def move_down(self, step: int):
        self.offset[1] += step
        self.merge_current()
        return

    def move_right(self, step: int):
        self.offset[0] += step
        self.merge_current()
        return

    def move_left(self, step: int):
        self.offset[0] -= step
        self.merge_current()
        return

    def increase_size(self, size):
        old_size = self.set_size[0]
        old_size += size
        if old_size > self.main_image.size[0] or int(old_size * self.ratio) > self.main_image.size[1]:
            print((old_size, int(old_size * self.ratio)), "<- new_size, main_image_size ->", self.main_image.size)
            print("Design can't be bigger than main image (in any dimensions)")
            return
        if (int(abs(self.offset[0]) * 2 + old_size) > self.main_image.size[0]) or \
                (int(abs(self.offset[1]) * 2 + old_size * self.ratio) > self.main_image.size[1]):
            print("Increased size of design does not fit in this place, try moving it closer to centre")
            return
        self.set_size = (old_size, int(old_size * self.ratio))
        self.resize_to_set_size()
        return

    def decrease_size(self, size):
        old_size = self.set_size[0]
        old_size -= size
        if old_size <= 0:
            print("Design size can't be less than 1, it is now:", self.set_size[0])
            return
        self.set_size = (old_size, int(old_size * self.ratio))
        self.resize_to_set_size()
        return

    def increase_height(self, amount: int) -> None:
        old_size = self.set_size[1]
        old_size += amount
        self.ratio = old_size / self.set_size[0]
        self.set_size = (int(old_size / self.ratio), old_size)
        self.resize_to_set_size()

    def decrease_height(self, amount: int) -> None:
        old_size = self.set_size[1]
        old_size -= amount
        self.ratio = old_size / self.set_size[0]
        self.set_size = (int(old_size / self.ratio), old_size)
        self.resize_to_set_size()

    # def write_excel(self, emi: EMI, url: str, design_name: str, design_id: str, csv_worker: CSVWorker):
    #     emi_dict = emi.__dict__.copy()
    #     product_names = [design_name + " " + pn for pn in emi_dict["product_names"]]
    #     seller_sku = design_id + " " + emi_dict['seller_sku']
    #     del emi_dict['seller_sku']
    #     del emi_dict["product_names"]
    #     csv_worker.add_job(dropbox_url=url, product_names=product_names, seller_sku=seller_sku, **emi_dict)
