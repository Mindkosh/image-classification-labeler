import sqlite3 as sq


class DatabaseHandler:
    def __init__(self, location):
        print("Initializing Database")

        # Load/create database:
        self.db = sq.connect(location)
        self.cursor = self.db.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS dataSets(id INTEGER NOT NULL PRIMARY KEY, dataSetName TEXT, dataSetPath TEXT UNIQUE)')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS images(id INTEGER NOT NULL PRIMARY KEY, dataSet_id INTEGER, imageName TEXT, imagePath TEXT UNIQUE, FOREIGN KEY(dataSet_id) REFERENCES dataSets(id))')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS categories(id INTEGER NOT NULL PRIMARY KEY, categoryName TEXT UNIQUE)')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS labels(category_id INTEGER, image_id INTEGER, FOREIGN KEY(category_id) REFERENCES categories(id), FOREIGN KEY(image_id) REFERENCES images(id))')
        self.db.commit()

    def addDataset(self, dataSetName,  dataSetPath):
        self.cursor.execute('INSERT OR IGNORE INTO dataSets(dataSetName, dataSetPath) VALUES(?, ?)', (
            dataSetName, dataSetPath))
        self.db.commit()

    def addImagesToDataset(self, datasetID, imageNames, imagePaths):
        for imagei in range(len(imageNames)):
            self.cursor.execute('INSERT OR IGNORE INTO images(dataSet_id, imageName, imagePath) VALUES(?, ?, ?)', (
                datasetID, imageNames[imagei], imagePaths[imagei]))
        self.db.commit()

    def addCategories(self, categories):
        for category in categories:
            self.cursor.execute(
                'INSERT OR IGNORE INTO categories(categoryName) VALUES(?)', (category,))
        self.db.commit()

    def getCategoryName(self, categoryID):
        self.cursor.execute(
            'SELECT categoryName FROM categories WHERE id = ?', (categoryID,))
        return self.cursor.fetchone()[0]

    def addImageCategory(self, imageID, categoryID):
        self.cursor.execute(
            'INSERT INTO labels(image_id, category_id) VALUES(?, ?)', (imageID, categoryID))
        self.db.commit()

    def getImageCategory(self, imageID):
        self.cursor.execute('SELECT category_id FROM labels WHERE image_id = ?',
                            (imageID,))
        return self.cursor.fetchall()

    def deleteImageLabels(self, imageID):
        self.cursor.execute(
            'DELETE FROM labels WHERE image_id = ?', (imageID,))
        self.db.commit()

    # Get Image ID from name
    def getImageID(self, imageName):
        self.cursor.execute(
            'SELECT id FROM images WHERE imagePath = ?', (imageName,))
        return self.cursor.fetchone()[0]

    def getAllCategories(self):
        self.cursor.execute('SELECT id, categoryName FROM categories')
        return self.cursor.fetchall()

    # Get category ID from name
    def getCategoryID(self, categoryName):
        self.cursor.execute(
            'SELECT id FROM categories WHERE categoryName = ?', (categoryName,))
        return self.cursor.fetchone()[0]

    # Get dataset ID from name
    def getDataSetID(self, datasetName):
        self.cursor.execute(
            'SELECT id FROM dataSets WHERE dataSetName = ?', (datasetName,))
        return self.cursor.fetchone()[0]

    # Find which images in a dataset are labeled
    def getImageLabelStatus(self, imageList, datasetID):
        unlabeledImages = len(imageList)
        imageHash = dict()

        # Save the index of each image
        for ind, i in enumerate(imageList):
            imageHash[i] = ind

        imageLabels = [False for i in range(unlabeledImages)]

        self.cursor.execute(
            'SELECT labels.category_id, images.imageName FROM labels JOIN images ON labels.image_id = images.id JOIN dataSets ON dataSets.id = images.dataSet_id WHERE images.dataSet_id="'+str(datasetID)+'"')
        labeledImages = self.cursor.fetchall()
        unlabeledImages = unlabeledImages - len(labeledImages)

        # Save which images are labeled
        for labeledImage in labeledImages:
            imageLabels[imageHash[labeledImage[1]]] = True
        return (unlabeledImages, imageLabels)

    def getParsedLabelName(self, labelName):
        if labelName[0] == "(":
            return labelName[3:].strip()
        return labelName

    def getLabeledImagesForExport(self, datasetID):
        allCategories = self.getAllCategories()
        categories = {}
        for category in allCategories:
            parsedLabel = self.getParsedLabelName(category[1])
            categories[category[0]] = parsedLabel

        # Get all labeled images and their categories for this dataset
        self.cursor.execute(
            'SELECT labels.category_id, images.imageName FROM labels JOIN images ON labels.image_id = images.id WHERE images.dataSet_id="'+str(datasetID)+'"')
        labeledImages = []
        for labeledImage in self.cursor.fetchall():
            labeledImages.append(labeledImage)

        exportData = dict()
        self.cursor.execute(
            'SELECT imageName FROM images WHERE images.dataSet_id="'+str(datasetID)+'"')

        # Initialize all images in the dataset
        for imageName in self.cursor.fetchall():
            exportData[imageName[0]] = []

        for labeledImage in labeledImages:
            exportData[labeledImage[1]].append(categories[labeledImage[0]])

        return exportData
