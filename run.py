import os
import time
import csv
from PIL import Image, ImageTk
import tkinter as tk
from databaseHandler import DatabaseHandler


class ClassificationLabeler:

    def __init__(self, master):

        self.categoryConfigFile = "./config/categories.config"
        self.recentActivityConfigFile = "./config/recentActiviy.config"
        self.datasetConfigFile = "./config/datasets.config"

        if os.path.exists(self.recentActivityConfigFile):
            self.recentActivityConfig = open(
                self.recentActivityConfigFile).read().split(",")
        else:
            self.recentActivityConfig = []

        self.master = master
        self.default_size = (self.master.winfo_screenwidth(
        )-600, self.master.winfo_screenheight()-150)

        master.title("Classification Labeler v1.2")

        master.bind("<Key>", self.keyPressed)
        self.master.option_add("*Font", "aerial 15")

        master.wm_iconphoto(True, ImageTk.PhotoImage(file='favicon.png'))

        self.imageLabels = []
        # Create GUI elements:

        # BOTTOM "STATUS BAR" VVVVVVVVVVVVVVVVVVVVVVVVV

        self.statusBar = tk.Label(master, text="", relief=tk.RIDGE)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)

        self.initialize()

        # LEFT FRAME VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

        self.frameSeperator00 = tk.Frame(master, width=6, height=1)
        self.frameSeperator00.pack(side=tk.LEFT)

        self.frameLEFT = tk.Frame(master, bd=2)
        self.frameLEFT.pack(side=tk.LEFT, padx=(0, 0))

        self.datasetTitleLabel = tk.Label(
            self.frameLEFT, text="Data Set Selection:")
        self.datasetTitleLabel.pack()

        self.dataSetsListbox = tk.Listbox(
            self.frameLEFT, relief=tk.FLAT, exportselection=False, height=5)
        for item in self.dataSetsListStr:
            self.dataSetsListbox.insert(tk.END, item)
        self.dataSetsListbox.pack()

        self.loadDataSetButton = tk.Button(
            self.frameLEFT, text="Load Data Set", command=self.loadDataSet)
        self.loadDataSetButton.pack()

        # self.dataSetStatusLabel = tk.Label(self.frameLEFT, text="No Data Set Loaded!")
        # self.dataSetStatusLabel.pack()

        # -------------------

        self.categoriesLabel = tk.Label(self.frameLEFT, text="Categories:")
        self.categoriesLabel.pack(pady=(30, 0))

        # Add this to allow multiple selections
        # selectmode=tk.MULTIPLE
        self.categoriesListbox = tk.Listbox(
            self.frameLEFT, selectbackground='#119911', relief=tk.FLAT, bd=2, exportselection=False, height=8)
        for item in self.categories:
            self.categoriesListbox.insert(tk.END, item)
        self.categoriesListbox.pack()
        self.categoriesListbox.config(state=tk.DISABLED)

        # --------------------

        self.frameMIDDLEBUTTONS = tk.Frame(self.frameLEFT, bd=2)
        self.frameMIDDLEBUTTONS.pack(pady=(30, 0))

        self.prevImageButton = tk.Button(
            self.frameMIDDLEBUTTONS, text="<- Previous", command=self.prevImage, state=tk.DISABLED)
        self.prevImageButton.pack(side=tk.LEFT, padx=(0, 20))

        self.nextImageButton = tk.Button(
            self.frameMIDDLEBUTTONS, text="Next ->", command=self.nextImage, state=tk.DISABLED)
        self.nextImageButton.pack(side=tk.LEFT)

        self.frameAnnotatedImages = tk.Frame(self.frameLEFT, bd=2)
        self.frameAnnotatedImages.pack()

        self.checkButtonNavigateLabeledImages = tk.IntVar()
        self.navigateLabeledImages = tk.Checkbutton(
            self.frameAnnotatedImages,
            text="Show unlabeled images",
            variable=self.checkButtonNavigateLabeledImages,
            onvalue=1,
            offvalue=0)
        self.navigateLabeledImages.pack(side=tk.LEFT, pady=(5))

        self.numberOfLabeledImages = tk.Frame(self.frameLEFT, bd=2)
        self.numberOfLabeledImages.pack()
        self.unlabeledImagesLabel = tk.Label(
            self.numberOfLabeledImages, text="0 unlabeled")
        self.unlabeledImagesLabel.pack()

        self.frameMIDDLEIMGLABEL = tk.Frame(self.frameLEFT, bd=2)
        self.frameMIDDLEIMGLABEL.pack()

        self.imageNumberLabel = tk.Label(
            self.frameMIDDLEIMGLABEL, text="Image:")
        self.imageNumberLabel.pack(side=tk.LEFT)

        self.imageNumberInput = tk.Entry(self.frameMIDDLEIMGLABEL, width=10)
        self.imageNumberInput.pack(side=tk.LEFT)

        self.skipToImageButton = tk.Button(
            self.frameMIDDLEIMGLABEL, text="Go", command=self.skipToImage, state=tk.DISABLED)
        self.skipToImageButton.pack(side=tk.LEFT)

        self.frameMIDDLEIMGZOOM = tk.Frame(self.frameLEFT, bd=2)
        self.frameMIDDLEIMGZOOM.pack()

        self.imageZoomLabel = tk.Label(self.frameMIDDLEIMGZOOM, text="Zoom:")
        self.imageZoomLabel.pack(side=tk.LEFT, padx=(0, 5))

        self.zoomOutButton = tk.Button(
            self.frameMIDDLEIMGZOOM, text="-", command=self.zoomOut, state=tk.DISABLED)
        self.zoomOutButton.pack(side=tk.LEFT, padx=(0, 10))

        self.zoomInButton = tk.Button(
            self.frameMIDDLEIMGZOOM, text="+", command=self.zoomIn, state=tk.DISABLED)
        self.zoomInButton.pack(side=tk.LEFT)

        self.currentZoomLabel = tk.Label(
            self.frameMIDDLEIMGZOOM, text=' '+str(self.imgScaleFactor)+'X ')
        self.currentZoomLabel.pack(side=tk.LEFT)

        self.frameEXPORT = tk.Frame(self.frameLEFT, bd=2)
        self.frameEXPORT.pack()

        self.exportButton = tk.Button(
            self.frameEXPORT, text="Export labels", command=self.export)
        self.exportButton.pack(side=tk.LEFT, padx=(0, 5))

        # ----------------------
        self.frameSeperator01 = tk.Frame(master, width=100, height=1)
        self.frameSeperator01.pack(side=tk.LEFT)

        # RIGHT FRAME VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

        self.frameMIDDLE = tk.Frame(master, bd=2)
        self.frameMIDDLE.pack(side=tk.LEFT)

        self.imgStage = tk.Canvas(
            self.frameMIDDLE, height=self.default_size[1], width=self.default_size[0], background="#292826")
        self.imgStage.pack(expand=tk.YES, fill=tk.BOTH)

        self.imgFileName = tk.Label(self.frameMIDDLE, text="")
        self.imgFileName.pack()

        self.imgStage.bind("<MouseWheel>", lambda event: self.do_zoom(event))
        self.imgStage.bind("<Button-4>", lambda event: self.do_zoom(event))
        self.imgStage.bind("<Button-5>", lambda event: self.do_zoom(event))
        self.imgStage.bind(
            '<ButtonPress-1>', lambda event: self.imgStage.scan_mark(event.x, event.y))
        self.imgStage.bind(
            "<B1-Motion>", lambda event: self.imgStage.scan_dragto(event.x, event.y, gain=1))

        self.frameSeperator02 = tk.Frame(master, width=20, height=1)
        self.frameSeperator02.pack(side=tk.LEFT)

        self.select_defaults()

    def do_zoom(self, event):
        if event.num == 5 or event.delta < 0:
            self.zoomOut()
        elif event.num == 4 or event.delta > 0:
            self.zoomIn()

    def select_defaults(self):
        if len(self.recentActivityConfig) > 0:
            dataset_ii = int(self.recentActivityConfig[0])
            image_ii = int(self.recentActivityConfig[1])

            try:
                self.dataSetsListbox.selection_set(dataset_ii)
                self.loadDataSet(image_ii)
            except:
                self.dataSetsListbox.selection_set(0)
                self.loadDataSet()

        elif len(self.dataSetsListStr) == 1:
            self.dataSetsListbox.selection_set(0)
            self.loadDataSet()

    def initialize(self):
        self.imgScaleFactor = 1

        self.database = DatabaseHandler("storage.db")
        self.initializeDatasets()
        self.initializeCategories()

    def createDatasetName(self, datasetPath):
        datasetName = os.path.basename(os.path.abspath(os.path.join(
            datasetPath, os.pardir))) + "-" + os.path.basename(datasetPath)
        return datasetName

    def initializeDatasets(self):
        print("Initializing Datasets")

        # Get Datasets:
        dataset_dirs = []
        if os.path.exists(self.datasetConfigFile):
            with open(self.datasetConfigFile) as fin:
                fileContents = fin.read()
                for i in fileContents.splitlines():
                    if i.strip() == "":
                        continue
                    else:
                        dataset_dirs.append(i.strip())

        self.dataSetsListDir = dataset_dirs
        self.dataSetsListStr = [
            self.createDatasetName(i) for i in dataset_dirs]

        if len(self.dataSetsListDir) == 0:
            self.statusBar.config(text="ERROR! No datasets found.")
            print("ERROR! No datasets found.")

    def initializeCategories(self):
        print("Initializing Categories")

        if os.path.exists(self.categoryConfigFile):
            catFile = open(self.categoryConfigFile, 'r')
            self.categories = [o.strip() for o in catFile.readlines()]
            catFile.close()
        else:
            self.categories = []
            self.statusBar.config(text="ERROR! No categories found.")
            print("ERROR! No categories found.")

        if len(self.categories) == 0:
            self.statusBar.config(text="ERROR! No categories found.")
            print("ERROR! No categories found.")

        # Populate db table for categories:
        self.database.addCategories(self.categories)

        # Parse Categories, set ad-hoc category key bindings:
        self.keyBindings = []
        for keyi in self.categories:
            if keyi[0] == "(" and keyi[2] == ")":
                if keyi[1] in self.keyBindings:
                    self.statusBar.config(
                        text="ERROR! Multiple categories with the same key binding!")
                    print("ERROR! Multiple categories with the same key binding!")
                    exit()
                else:
                    self.keyBindings.append(keyi[1].lower())

    def keyPressed(self, key):
        if key.keysym == 'Left':
            self.prevImageButton.config(relief=tk.SUNKEN)
            self.prevImageButton.update_idletasks()
            self.prevImage()
            time.sleep(0.05)
            self.prevImageButton.config(relief=tk.RAISED)
        elif key.keysym == 'Right':
            self.nextImageButton.config(relief=tk.SUNKEN)
            self.nextImageButton.update_idletasks()
            self.nextImage()
            time.sleep(0.05)
            self.nextImageButton.config(relief=tk.RAISED)
        elif key.char == '+' or key.char == '=':
            self.zoomInButton.config(relief=tk.SUNKEN)
            self.zoomInButton.update_idletasks()
            self.zoomIn()
            time.sleep(0.05)
            self.zoomInButton.config(relief=tk.RAISED)
        elif key.char == '-':
            self.zoomOutButton.config(relief=tk.SUNKEN)
            self.zoomOutButton.update_idletasks()
            self.zoomOut()
            time.sleep(0.05)
            self.zoomOutButton.config(relief=tk.RAISED)
        else:
            # Check if this is an ad-hoc keybind for a category selection...
            try:
                if self.categoriesListbox.selection_includes(self.keyBindings.index(key.char.lower())):
                    self.categoriesListbox.selection_clear(
                        self.keyBindings.index(key.char.lower()))
                else:
                    self.categoriesListbox.selection_set(
                        self.keyBindings.index(key.char.lower()))
            except ValueError:
                pass

    # Go to previous image

    def prevImage(self):
        self.saveImageCategorization()
        navigateLabeled = bool(self.checkButtonNavigateLabeledImages.get())

        if self.imageSelection > 0:
            if navigateLabeled:
                moveTo = -1
                for i in reversed(range(0, self.imageSelection)):
                    if self.imageLabels[i] is False:
                        moveTo = i
                        break
                if moveTo != -1:
                    self.imageSelection = moveTo
                    self.imgScaleFactor = 1
                    self.imgScaleFactor = 1
                    self.loadImage(reset=True)
                else:
                    self.statusBar.config(
                        text="All images before this are labeled.")

            else:
                self.imageSelection -= 1
                self.imgScaleFactor = 1
                self.imgScaleFactor = 1
                self.loadImage(reset=True)
        else:
            self.statusBar.config(text="Already at first image.")

    # Go to next image

    def nextImage(self):
        self.saveImageCategorization()
        navigateLabeled = bool(self.checkButtonNavigateLabeledImages.get())

        if self.imageSelection < (len(self.imageListDir)-1):
            if navigateLabeled:
                moveTo = -1
                for i in range(self.imageSelection+1, len(self.imageListDir)):
                    if self.imageLabels[i] is False:
                        moveTo = i
                        break
                if moveTo != -1:
                    self.imageSelection = moveTo
                    self.imgScaleFactor = 1
                    self.imgScaleFactor = 1
                    self.loadImage(reset=True)
                else:
                    self.statusBar.config(
                        text="All images after this are labeled.")

            else:
                self.imageSelection += 1
                self.imgScaleFactor = 1
                self.imgScaleFactor = 1
                self.loadImage(reset=True)
        else:
            self.statusBar.config(text="Already at last image.")

    def loadImage(self, reset=False):
        imageFile = Image.open(self.imageListDir[self.imageSelection])

        imageFile.thumbnail(self.default_size, Image.LANCZOS)

        canvasImage = ImageTk.PhotoImage(imageFile.resize(
            (int(imageFile.size[0] * self.imgScaleFactor),
             int(imageFile.size[1] * self.imgScaleFactor)),
            Image.NEAREST))

        self.imgStage.create_image(0, 0, anchor=tk.NW, image=canvasImage)
        self.imgStage.image = canvasImage

        if reset:
            self.imgStage.xview_moveto(0)
            self.imgStage.yview_moveto(0)

        self.imgFileName.config(text=os.path.basename(
            str(self.imageListStr[self.imageSelection])))
        self.imageNumberInput.delete(0, tk.END)
        self.imageNumberInput.insert(
            0, str(self.imageSelection+1) + " / " + str(len(self.imageListDir)))
        self.statusBar.config(text="")

        # Read from db and update starting categories in listbox if data exists:
        self.categoriesListbox.selection_clear(0, len(self.categories))
        categories = self.database.getImageCategory(
            self.database.getImageID(self.imageListDir[self.imageSelection]))

        for category_id in categories:
            categoryName = self.database.getCategoryName(category_id[0])

            try:
                self.categoriesListbox.selection_set(
                    self.categories.index(categoryName))
            except ValueError:
                self.statusBar.config(
                    text="FATAL ERROR! Image is saved with invalid category.")
                print(
                    'FATAL ERROR! Image is saved with invalid category: '+str(categoryName))
                print('image Name: '+self.imageListStr[self.imageSelection])
                print('This category must be listed in the categories config file.')
                exit()

        with open(self.recentActivityConfigFile, "w") as fout:
            fout.write(",".join([
                str(self.dataSetSelection),
                str(self.imageSelection)
            ]))

    def saveImageCategorization(self):
        # Clear out existing category labels for the image...
        self.database.deleteImageLabels(self.database.getImageID(
            self.imageListDir[self.imageSelection]))

        # Insert new category labels for the image...
        labelSaved = False
        for cati in self.categoriesListbox.curselection():
            labelSaved = True
            self.database.addImageCategory(self.database.getImageID(
                self.imageListDir[self.imageSelection]), self.database.getCategoryID(self.categories[cati]))

        if labelSaved is True:
            if self.imageLabels[self.imageSelection] is False:
                self.unlabeledImages = self.unlabeledImages-1

            self.imageLabels[self.imageSelection] = True
        else:
            if self.imageLabels[self.imageSelection] is True:
                self.unlabeledImages = self.unlabeledImages+1

            self.imageLabels[self.imageSelection] = False

        self.unlabeledImagesLabel.config(
            text=str(self.unlabeledImages) + " unlabeled")

    def skipToImage(self, img_itr=None):
        try:
            if img_itr is not None:
                tryImageSelection = img_itr
            else:
                tryImageSelection = int(
                    self.imageNumberInput.get().split("/")[0].strip())-1

            if (tryImageSelection >= 0) and (tryImageSelection < len(self.imageListDir)):
                self.imageSelection = tryImageSelection
                self.imgScaleFactor = 1
                self.loadImage(reset=True)
            else:
                self.statusBar.config(text="ERROR! Image does not exist.")
                print("ERROR! Image does not exist.")
        except Exception as e:
            self.statusBar.config(text="ERROR! Invalid image selection.")
            print(e)

    def loadDataSet(self, img_itr=None):
        print("Load DataSet")

        # Check to see if selection has been made
        try:
            self.dataSetSelection = int(self.dataSetsListbox.curselection()[0])
        except IndexError:
            # self.dataSetStatusLabel.config(text='No selection!')
            self.dataSetSelection = -1

        # Check if a valid dataSet is selected
        if self.dataSetSelection >= 0:

            # Load images in dataset:
            d = self.dataSetsListDir[self.dataSetSelection]
            self.imageListDir = [os.path.join(d, o) for o in os.listdir(
                d) if os.path.isdir(os.path.join(d, o)) == False]
            self.imageListStr = [os.path.basename(
                i) for i in self.imageListDir]

            # Create db table entry for this dataSet:
            self.database.addDataset(
                self.dataSetsListStr[self.dataSetSelection], self.dataSetsListDir[self.dataSetSelection])

            # Populate db table entries for all images in this dataSet (this can take a few seconds if over ~2,000 images):
            self.dataSet_id = self.database.getDataSetID(
                self.dataSetsListStr[self.dataSetSelection])
            self.database.addImagesToDataset(
                self.dataSet_id, self.imageListStr, self.imageListDir)

            # Retrieve and save whether images are labeled
            self.unlabeledImages, self.imageLabels = self.database.getImageLabelStatus(
                self.imageListStr, self.dataSet_id)

            self.unlabeledImagesLabel.config(
                text=str(self.unlabeledImages) + " unlabeled")

            # Prepare image stage:
            self.imageNumberInput.delete(0, tk.END)
            self.imageNumberInput.insert(0, '1')
            self.prevImageButton.config(state=tk.NORMAL)
            self.nextImageButton.config(state=tk.NORMAL)
            self.skipToImageButton.config(state=tk.NORMAL)
            self.categoriesListbox.config(state=tk.NORMAL)
            self.zoomInButton.config(state=tk.NORMAL)
            self.zoomOutButton.config(state=tk.NORMAL)

            # Go to first image
            self.skipToImage(img_itr)

            self.statusBar.config(text='Dataset loaded: '+str(
                self.dataSetsListStr[self.dataSetSelection])+', Number of images: '+str(len(self.imageListDir)))
            print('Dataset loaded: ' +
                  str(self.dataSetsListStr[self.dataSetSelection])+', Number of images: '+str(len(self.imageListDir)))

    def zoomIn(self):
        self.imgScaleFactor += .2
        # Since anti-aliasing is NOT used, only integer zoom factors are permitted.
        self.currentZoomLabel.config(text=f' {self.imgScaleFactor:.2f}X ')
        self.loadImage()

    def zoomOut(self):
        # Since anti-aliasing is NOT used, only integer zoom factors are permitted.
        if self.imgScaleFactor > .2:
            self.imgScaleFactor -= .2
            self.currentZoomLabel.config(text=f' {self.imgScaleFactor:.2f}X ')
            self.loadImage()

    def export(self):
        if self.dataSet_id:
            exportData = self.database.getLabeledImagesForExport(
                self.dataSet_id)
            rows = [[key, ",".join(exportData[key])]
                    for key in exportData.keys()]
            fields = ['ImageName', 'Categories']

            # name of csv file
            filename = "exported_labels_dataset_" + \
                str(self.dataSet_id) + ".csv"

            # writing to csv file
            with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';')

                # Write the header
                csvwriter.writerow(fields)

                # Write data rows
                csvwriter.writerows(rows)
            print("Dataset exported to CSV with filename" + filename)
            self.statusBar.config(
                text='Dataset exported to CSV with filename: '+filename)


if __name__ == "__main__":
    root = tk.Tk()
    guiObject = ClassificationLabeler(root)
    root.mainloop()
