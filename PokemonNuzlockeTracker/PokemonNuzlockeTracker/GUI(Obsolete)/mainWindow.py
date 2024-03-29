from tkinter import *
import os
from tkinter import ttk

from templateWindow import TemplateWindow
from encounterWindow import EncounterWindow
from trainer import Trainer

#TODO if there are no trainers, only display label

class MainWindow(TemplateWindow):
    _spriteFolder = os.path.join(os.path.dirname(os.getcwd()), f"images/sprites")
    _pokemonSpritesFolder = os.path.join(_spriteFolder, f"pokemon")
    
    def __init__(self, x, y, game, save, parent = None):
        super().__init__(x, y, parent) 
        #self._game is a gameObject  
        self._game = game
        #attempt x :str
        #update location of the savefile
        self._game.saveFile = save
        self._master.title(f"{self._game.gameName} {save}")
        #get all data from game and save file
        self._listOfAreas = self._game.retrieveGameData()

        self._trainerDict = {}
        self._itemDict = {}
        self._areaNames = []
        self.getAreaNames()

        self.currentArea = None #soon to be Area object

        """number of badges"""
        self._numberOfBadges = IntVar()
        self._numberOfBadges.set(self._game.badge)
        self._badgesMenu = OptionMenu(self._master, self._numberOfBadges, *list(range(0,9)), command = self.changeAreaList)
        self._badgesMenu.grid(row=0, column=0,rowspan=1, columnspan=1, sticky=NW) 

        """item frames"""
        self._itemFrame = Frame(self._master)
        self._itemFrame.grid(row=0, column=4,rowspan = 25, columnspan = 1, sticky = N)
        self._itemFrame.rowconfigure(0, weight = 2)
        self._itemFrame.columnconfigure(0, weight = 2)

        self._indivItemFrame = Frame(self._itemFrame, relief = SUNKEN)
        self._indivItemFrame.grid(row = 1, column = 0, columnspan = 4, sticky = N)
        self._indivItemFrame.rowconfigure(0, weight = 2)
        self._indivItemFrame.columnconfigure(0, weight = 2)
        self.createItemScrollbar()

        self._itemLabel = Label(self._itemFrame, text="Available Items", anchor = CENTER)
        self._itemLabel.grid(row=0,column=0,sticky=N)

        """item buttons"""
        self._addItemButton = Button(self._itemFrame, text = "add an item", bd = 3, font = self._font)#, command = self.addItem)
        self._addItemButton.grid(row = 25, column = 0, sticky = NSEW)
        
        self._deleteItemButton = Button(self._itemFrame, text = "delete an item", bd = 3, font = self._font)#, command = self.deleteItem)
        self._deleteItemButton.grid(row = 25, column = 1, sticky = NSEW)

        """trainer frames"""
        self._trainerFrame = Frame(self._master)
        self._trainerFrame.grid(row=0, column=1, rowspan=10, columnspan = 3, sticky = N)
        self._trainerFrame.rowconfigure(0, weight = 2)
        self._trainerFrame.columnconfigure(0, weight = 2)

        self._selectedTrainer = StringVar()
        self._selectedTrainer.set("which trainer do you want to see")
        #self._selectedTrainer.trace_add("write", self.getTrainerPokemon)
        self._trainerMenu = OptionMenu(self._trainerFrame, self._selectedTrainer, ())
        self._trainerMenu.grid(row=0, column = 0, columnspan = 3, sticky = "nwe")
        #self._trainerMenu.configure(postcommand = self.centerDropDownMenu(self._trainerMenu))

        self._indivTrainerFrame = Frame(self._trainerFrame)
        self._indivTrainerFrame.grid(row = 1, column = 0, columnspan = 3, sticky = N)
        self._indivTrainerFrame.rowconfigure(0, weight = 2)
        self._indivTrainerFrame.columnconfigure(0, weight = 2)

        """trainer buttons"""
        self._addTrainerButton = Button(self._trainerFrame, text = "add a trainer", bd = 3, font = self._font, command = self.addTrainer)
        self._addTrainerButton.grid(row = 8, column = 0, sticky = NSEW)

        self._editTrainerButton = Button(self._trainerFrame, text = "edit a trainer", bd = 3, font = self._font)#, command =self.editTrainer)
        self._editTrainerButton.grid(row = 8, column = 1, sticky = NSEW)

        self._deleteTrainerButton = Button(self._trainerFrame, text = "delete a trainer", bd = 3, font = self._font)#, command = self.deleteTrainer)
        self._deleteTrainerButton.grid(row = 8, column = 2, sticky = NSEW)

        """showdown buttons"""
        # self._exportToShowdownButton = Button(self._trainerFrame, text = "export current trainer to showdown", bd = 5, font = self._font)#, command = self.showdownExport)
        # self._exportToShowdownButton.grid(row = 9, column =0, columnspan = 3, sticky = NSEW)

        # self._exportAllToShowdownButton = Button(self._trainerFrame, text = "export all available trainer data to showdown", bd = 5, font = self._font)
        # self._exportAllToShowdownButton.grid(row = 10, column =0, columnspan = 3, sticky = NSEW)

        """selected Area"""
        self._areaFrame = Frame(self._master)
        self._areaFrame.grid(row = 0, column = 5, sticky = N)

        self._selectedArea = StringVar()
        self._selectedArea.set("choose an Area")
        #area is the _selectedArea variable
        self._areaMenu = ttk.Combobox(self._areaFrame, textvariable = self._selectedArea, values = self._areaNames)#, command = lambda area: [self.getTrainers(area), self.getItems(area)])
        self._areaMenu.grid(row=0, column=5, sticky=NSEW)
        self._areaMenu['state'] = 'readonly'
        self._areaMenu.bind("<<ComboboxSelected>>", lambda area = self._areaMenu.get(): self.updateCurrentArea(area))

        """Accessible updater"""
        self._currentAccessible = IntVar()
        self._accessibleFrame = Frame(self._areaFrame)
        self._accessibleFrame.grid(row = 1, column = 5, columnspan = 3, sticky = NSEW)

        self._currentAreaAccessibleLabel = Label(self._accessibleFrame, text = "badge needed:")
        self._currentAreaAccessibleLabel.grid(row = 0, column = 1, columnspan = 2)

        self._changeAccessibleMenu = OptionMenu(self._accessibleFrame, self._currentAccessible, *list(range(0,9)), command = self.updateCurrentAreaAccessible)
        self._changeAccessibleMenu.grid(row = 0, column = 3, sticky = NSEW)

        self._showWildEncounterButton = Button(self._areaFrame, text = "Encounters", command = self.showEncounters)
        self._showWildEncounterButton.grid(row = 2, column = 5, sticky = NSEW)

        """exit buttons and main loop"""
        self._exitButton = Button(self._master, text = "save & exit", command = self.saveAndExit)
        self._exitButton.grid(row=4, column = 0, sticky=SW)

        self._backButton = Button(self._master, text = "back", command = self.createGameMenu)
        self._backButton.grid(row=4, column=5, sticky=SE)

        # self._exportToShowdownButton.configure(state = DISABLED)
        #self.changeTrainerButtonState(DISABLED)
        #closing window saves the changes made
        """"""
        #self._master.protocol("WM_DELETE_WINDOW", self.saveAndExit)
        """"""

        #disable all the widgest in trainerframe and in the itemdisplay
        self.disableWidgetsStartup()
        self.update()
        self.run()
    
    def getAreaNames(self):
        """creates a list of areaNames based on the _listOfAreas"""
        for area in self._listOfAreas:
            self._areaNames.append(area.name)

    def showEncounters(self):
        """opens the encounterwindow and passes the correct area as parameter"""
        currentArea = self._areaMenu.get()
        for area in self._listOfAreas:
            if area.name == currentArea:
                EncounterWindow(self._master, area)
    
    def updateCurrentArea(self, event):
        """updates the current area based on the name of the area passed as the parameter, also updates the GUI lists connected to the area
        , updates all the widgets on screen aswell (trainermenu, itemdisplay, button colour)"""
        areaName = event.widget.get()
        for area in self._listOfAreas:
            if area.name == areaName:
                self.currentArea = area
                break
        else:
            print(f"ERROR: {areaName} could not be found")
        #update the lists to match the area object
        self._trainerDict = self.currentArea.trainers
        self._itemDict = self.currentArea.items

        self.updateTrainerMenu()
        self.updateItemDisplay()
        self.updateAccessibleMenu()
        self.changeCbbColor()
        self.enableWidgetsStartup()
    
    def updateTrainerMenu(self):
        """update the trainermenu with currentarea.trainers"""
        #TODO create the trainerframes 
        # pass
        # #remove the previous pokemon and hide the display
        self.deletePokemonDisplay()
        self._indivTrainerFrame.grid_remove()
        #remove all previous trainers from the optionmenu
        self._trainerMenu['menu'].delete(0, 'end')

        if len(self._trainerDict) == 0:
            #TODO create a label instead of an optionmenu otherwise create the optionmenu
            self._selectedTrainer.set("this route has no trainers, please add one with the add trainer button")
            pass
        else:
            self._selectedTrainer.set("select a trainer")
            menu = self._trainerMenu["menu"]
            #empty the optionmenu
            menu.delete(0, "end")
            for trainerName in self._trainerDict.keys():
                print(f"added {trainerName}")
                #set the label to the corect name and display the correct pokemon
                menu.add_command(label = trainerName, command = lambda trainerName = trainerName: [self._selectedTrainer.set(trainerName), self.getTrainerPokemon(trainerName)])

    def getTrainerPokemon(self, trainerName):
        """get the pokemon from a selected trainer"""
        #TODO use trainerpokemon frames
        #this trainer has pokemon, show the frame again
        self._indivTrainerFrame.grid()
        # self._exportToShowdownButton.configure(state = NORMAL)
        #print(self._listOfTrainers)
        if len(self._trainerDict) == 0:
            print("This trainer has no pokemon")
        else:
            trainer = self._trainerDict[trainerName] 
            self.deletePokemonDisplay()
            for index, pokemon in enumerate(trainer.pokemon):
                self.displayPokemon(pokemon, index)

    def deletePokemonDisplay(self):
        """delete all listboxs etc in indivtrainerframe"""
        for label in self._indivTrainerFrame.winfo_children():
            label.destroy()
        
    def displayPokemon(self, pokemon, index):
        """look for photo of the pokemon and add the pokemon to the gui"""
        photo = os.path.join(self._pokemonSpritesFolder, pokemon.name + '.png')
        #check if pokemon name is correct else display '?' png
        try:
            pokemonImg = PhotoImage(file = photo)
        except TclError:
            photo = os.path.join(self._pokemonSpritesFolder, '0.png')
            pokemonImg = PhotoImage(file = photo)
        
        #pokemonImg = ImageTk.PhotoImage(PIL.Image.open(photo))
        pokemonPhoto = Label(self._indivTrainerFrame, image = pokemonImg)
        pokemonPhoto.grid(row = index, column = 0, sticky = N)
        
        dataBox = Listbox(self._indivTrainerFrame, height = 4)
        dataBox.grid(row = index, column = 1, sticky = N)
        dataBox.insert(1, f"{pokemon._name} lvl {pokemon._level}")
        dataBox.insert(2, f"Ability: {pokemon._ability}")
        dataBox.insert(3, f"Item: {pokemon._heldItem}")
        dataBox.insert(4, f"Gender: {pokemon._gender}")

        moveBox = Listbox(self._indivTrainerFrame, height = 4)
        moveBox.grid(row = index, column = 2, sticky = N)
        for index, move in enumerate(pokemon.moves):
            moveBox.insert(index, move)
        #prevent garbage collection
        pokemonPhoto.image = pokemonImg
    
    def addTrainer(self):
        print("adding trainer")
        trainer = Trainer("Morty")
        self.currentArea.trainers[trainer.name] = trainer
        

    def updateItemDisplay(self):

        self.deleteItemDisplay()
        #remove
        if not len(self._itemDict):
            self._indivItemFrame.grid_remove()
        else:
            self._indivItemFrame.grid()
            self.displayItems()

    def deleteItemDisplay(self):
        self._itemBox.delete(0, "end")

    def itemBoxHeight(self):
        """returns the length the itembox should have"""
        itemDictLength = len(self._itemDict)
        return itemDictLength if itemDictLength < 10 else 10

    def createItemScrollbar(self):
        itemScrollbar = Scrollbar(self._indivItemFrame)
        itemScrollbar.grid(row = 0, column = 1, sticky = NS)
        self._itemBox = Listbox(self._indivItemFrame, yscrollcommand = itemScrollbar.set, height = self.itemBoxHeight())
        self._itemBox.grid(row = 0, column = 0)
        itemScrollbar.configure(command = self._itemBox.yview)


    def displayItems(self):
        """Displays the current items available in this area"""
        for itemName, itemObject in self._itemDict.items():
            self._itemBox.insert(END, itemName)
        

    def changeAreaList(self, *args):
        badges = self._numberOfBadges.get()
        #TODO sort list on number of badges
        pass

    def updateAccessibleMenu(self):
        """update the accessible value from the GUI to the one from the game object"""
        self._currentAccessible = self.currentArea.accessible
    
    def updateCurrentAreaAccessible(self, *args):
        """update accessible value belonging to the game object"""
        newAccessible = args[0]
        self.currentArea.accessible = newAccessible

    def changeCbbColor(self):
        """change the colour of the 'show encounters' button"""
        if self.currentArea.canCatchPokemon:
            self._showWildEncounterButton.config(background = "green")
        else:
            self._showWildEncounterButton.config(background = "red")

    def enableWidgetsStartup(self):
        frames = [self._trainerFrame, self._itemFrame, self._accessibleFrame]
        self.changeFrameWidgets(frames, 'normal') 
    
    def disableWidgetsStartup(self):
        """sets all the widgets inside of trainerframe and the itemdisplay to disabled until an area is selected"""
        frames = [self._trainerFrame, self._itemFrame, self._accessibleFrame]
        self.changeFrameWidgets(frames, "disabled")  
    
    def changeFrameWidgets(self, frames :list, state :str):
        """change the widgets of the given frames, list, to the state"""
        widgetList = []
        for frame in frames:
            #comprehension to weed out all the frame and Listbox objects
            widgetList.extend(widget for widget in frame.winfo_children() if not isinstance(widget, (Frame, Listbox)))
        self.updateWidgetState(widgetList, state)

    def updateWidgetState(self, widgets :list, state: str):
        """accepts a list of widgets which will be given the state"""
        for widget in widgets:
            widget.configure(state = state)

    def showdownExport(self):
        """grabs current trainer selected and converts its data to showdown format"""
        #not here
        chosenTrainer = self._selectedTrainer.get()
        for trainer in self._listOfTrainers:
            if chosenTrainer == trainer.name:
                with open('showdown.txt', 'w') as outputFile:
                    #TODO rewrite to showdown format
                    pass
                break

    def createGameMenu(self):
        """return to the first screen of the program"""
        from selectGameWindow import SelectGameWindow
        self.stop()
        self.exit()
        SelectGameWindow()

    def saveAndExit(self):
        self._game.writeToFile()
        self.exit()
