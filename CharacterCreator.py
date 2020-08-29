# Name: Sergiy Ensary, Kyle Moses
# Date: October 31st
# Course: COSC 2316 Fall 2019 (Dr. Shebaro)
# Program Description: Character Creation

######### Algorithm/Psuedocode ########

# 1. Menu to let user create or load a character or exit
# 2. Method to ask for a player name
# 3. Method to ask for a player gender
# 4. Method to ask for a player class (With description)
# 5. Method to ask for a player race
# 6. Method to input player stats that are withing race bounds
# 7. Method to ask for a favored weapon
# 8. Method to allocate skill points
# 9. Method to write a character to file
# 10. Method to select a pre-made character file
# 11. Method to load a pre-made character from file


############# Python Code #############
import random
import os
from enum import Enum
from os import scandir


#   Race construction
class Race:
    race, age, weight, speed, height = None, None, None, None, None

    def __init__(self, race, age, height, weight, speed):
        self.age = age
        self.race = race.type.value
        self.height = height
        self.weight = weight
        self.speed = speed

    def display(self):
        print("Race: ", self.race,
              "\nAge: ", self.age,
              "\nHeight: ", self.height,
              "\nWeight: ", self.weight,
              "\nSpeed: ", self.speed)

    def formatForFile(self):
        formatedString = (str(self.race) + "\n"
                          + str(self.age) + "\n"
                          + str(self.height) + "\n"
                          + str(self.weight) + "\n"
                          + str(self.speed) + "\n")
        return formatedString


#   Human stat bounds
class Human(Enum):
    type = "Human"
    minAge, maxAge = 15, 90
    minHeight, maxHeight = 60, 80
    minWeight, maxWeight = 100, 200
    speed = 25


#   Elf stat bounds
class Elf(Enum):
    type = "Elf"
    minAge, maxAge = 15, 90
    minHeight, maxHeight = 60, 86
    minWeight, maxWeight = 100, 200
    speed = 30


#   Orc stat bounds
class Orc(Enum):
    type = "Orc"
    minAge, maxAge = 15, 90
    minHeight, maxHeight = 60, 90
    minWeight, maxWeight = 100, 225
    speed = 25


#   Ogre stat bounds
class Ogre(Enum):
    type = "Ogre"
    minAge, maxAge = 15, 90
    minHeight, maxHeight = 60, 95
    minWeight, maxWeight = 120, 250
    speed = 25


#   Vampire stat bounds
class Vampire(Enum):
    type = "Vampire"
    minAge, maxAge = 90, 190
    minHeight, maxHeight = 60, 86
    minWeight, maxWeight = 100, 200
    speed = 30


#   Dwarf stat bounds
class Dwarf(Enum):
    type = "Dwarf"
    minAge, maxAge = 15, 90
    minHeight, maxHeight = 40, 60
    minWeight, maxWeight = 80, 180
    speed = 25


#   Giant stat bounds
class Giant(Enum):
    type = "Giant"
    minAge, maxAge = 15, 200
    minHeight, maxHeight = 70, 120
    minWeight, maxWeight = 150, 400
    speed = 25


#   Gnome stat bounds
class Gnome(Enum):
    type = "Gnome"
    minAge, maxAge = 15, 60
    minHeight, maxHeight = 20, 50
    minWeight, maxWeight = 60, 180
    speed = 30


#   Halfling stat bounds
class Halfling(Enum):
    type = "Halfling"
    minAge, maxAge = 15, 90
    minHeight, maxHeight = 30, 50
    minWeight, maxWeight = 50, 150
    speed = 25


#   Description: Find out if integer value is within given bounds
#   Pre: all inputs are integers, minValue <= maxValue
#   Post: returns true or false if value is within bounds
def inRange(value, minValue, maxValue):
    return minValue <= value <= maxValue


#   Description: Pick a race that you want to make
#   Pre: call anytime
#   Post: returns a selected race
def selectRace():
    raceSelected = False
    while not raceSelected:
        print("\n" + "Please Select a Race from options below:\n")
        for index in range(len(listRaces)):
            print(index + 1, ". ", listRaces[index].type.value)
        try:
            race = int(input("\n>>>"))
            if inRange(race, 1, 9):
                race = listRaces[race - 1]
                raceSelected = True
        except ValueError:
            print("Invalid choice, try again\n")
    return race


#   Description: Lets you decide the stats of your character
#   Pre: value is a string (name of stat) min/max inputs are integers, min <= max
#   Post: returns stats for your character
def getParameters(min, max, value):
    validChoice = False
    while not validChoice:
        try:
            print("\nNow select your", value, " in the range provided:\nmin -", min, " max -", max)
            parameter = int(input("\n>>>"))
            if inRange(parameter, min, max):
                return parameter
            else:
                print("Invalid Value")
        except ValueError:
            print("Please enter a correct value")


def createPlayer():
    race = selectRace()
    age = getParameters(race.minAge.value, race.maxAge.value, "age")
    height = getParameters(race.minHeight.value, race.maxHeight.value, "height")
    weight = getParameters(race.minWeight.value, race.maxWeight.value, "weight")
    print("The speed of ", race.type.value, " race is ", race.speed.value)
    player = Race(race, age, height, weight, race.speed.value)
    return player


# Function Description: Formats a string with all attributes of the character that the user created
# Pre: the user has gone through all the steps of the character creation
# Post: returns a string that is the correct format of what should be written to the text file
def formatPlayer():
    string = ""
    string += playerList[0] + "\n"
    string += playerList[1] + "\n"
    string += playerList[2] + "\n"
    string += playerList[3].formatForFile()
    string += playerList[4] + "\n"
    for key, value in playerList[5].items():
        string += key + " " + str(value) + "\n"
    return string


# Function Description: Writes a new text file with the characters name as the file title
# Pre: runs when the character creation is finished
# Post: Writes a file with the title as the characters name, using the formatPlayer function
def writeFile():
    characterFile = open(str(playerList[0]).format() + ".txt", "w+")
    characterFile.write(formatPlayer())

    characterFile.close()


# Function Description:Takes all .txt files and lets you select the one you want to load
# Pre: called to load an existing character
# Post: returns a filepath to a selected .txt file
def getSelectedFile():
    dir_entries = scandir(os.getcwd())
    listOfTxtFiles = []
    for entry in dir_entries:
        ext = os.path.splitext(entry.name)[-1].lower()
        if ext == ".txt":
            listOfTxtFiles.append(entry)
    if len(listOfTxtFiles) < 1:
        print("There are no saved characters")
        menu()
    print("Available Characters:")
    for index in range(len(listOfTxtFiles)):
        print(str(index + 1) + ". " + listOfTxtFiles[index].name + "\n")
    fileNotChosen = True
    while fileNotChosen:
        try:
            userInput = int(input("Which file do you want to load:\n"))
            return listOfTxtFiles[userInput - 1].name
        except ValueError or UnboundLocalError:
            print("\nNot a Valid Input\n")


# Function Description: Reads a selected character file
# Pre: fileName is a valid file path
# Post: stores all values in the files into a player container
def readCharacterFromFile(fileName):
    characterFile = open(fileName, "r")
    lines = characterFile.readlines()

    playerList[0] = lines[0].rstrip()
    playerList[1] = lines[1].rstrip()
    playerList[2] = lines[2].rstrip()
    race = None
    for raceIndex in range(len(listRaces)):
        value = listRaces[raceIndex].type.value
        valueToSearch = str(lines[3].rstrip())
        if str(valueToSearch).format() == str(value).format():
            race = listRaces[raceIndex]
    playerList[3] = Race(race, int(lines[4]), int(lines[5]), int(lines[6]), int(lines[7]))

    playerList[4] = lines[8].rstrip()
    attributes = {}
    for line in range(6):
        attr = lines[line + 9].split()
        attributes.update({attr[0]: int(attr[1])})
    playerList[5] = attributes

# Algorithm:
# 1. Starts by creating a dictionary with all attributes and 0 as the value
# 2. Display attributes to the user and tell them they have 10 points to put into all attributes
# 3. goes through each key in dictionary, asking the user how many points they want to input into that attribute
# 4. if they have 0 points left to spend then skip through the rest of the attributes
# 5. return the dictionary and put it into the playerList global variable
# Function Description: This function has the user input their characters attribute stats
# Precondition: Runs as the last selection option
# Postcondition: Returns a dictionary with the specific stat and the number of points they inputted
def placeAttributes():
    attributes = {"Strength": 0, "Dexterity": 0, "Wisdom": 0, "Intelligence": 0, "Charisma": 0, "Constitution": 0}
    totalPoints = 10
    print("\n" + "***ATTRIBUTES***")
    print("These are the attributes... You have", totalPoints, "Attribute Points to start")
    print("1) Strength ")
    print("2) Dexterity  ")
    print("3) Wisdom ")
    print("4) Intelligence  ")
    print("5) Charisma  ")
    print("6) Constitution  ")

    for key in attributes.keys():
        catchBool = False
        while not catchBool:
            if totalPoints == 0:
                break
            try:
                selection = int(input("How many points would you like to put into " + key.upper() + ": "))
            except ValueError as e:
                selection = 100
            if totalPoints >= selection >= 0:
                attributes[key] += selection
                totalPoints -= selection
                print(selection, "points added to", key.upper())
                print("You have", totalPoints, "Attribute Points left")
                catchBool = True
            else:
                print("You cannot put ", selection, "of points in", key.upper())
    return attributes



# Algorithm:
# 1. have default name as UN-NAMED, ask the user to input a name
# 2. if the user enters nothing for their name, name is set to default
# 3. returns a string that is used as their file name and their character name, stored in global playerList
# Function Description: Asks the user what there name is, default value for name is "UN-NAMED"
# Pre: Recieves nothing and is run when the program starts
# Post: Returns the name as a string
def askCharacterName():
    characterName = "UN-NAMED"
    print("Please enter your character's name   (if no name entered, default name is: UN-NAMED")
    name = input("CHARACTER NAME: ")
    if len(name) != 0:
        characterName = name
    return characterName


# Algorithm:
# 1. create a list of strings with all class names
# 2. display class names to user, then ask them to select a number to see the class description
# 3. When number is selected, find that classes index and display the class description
# 4. Use confirm class function to ask the user if they are sure that this is the class they want
# 5. if they type Y or y, then the name of the class is returned as a string and stored in global playerList
# Function Description: This function asks the user to select a class from 8 individual choices
# Pre: Is run as the third thing from the start of the program
# Post: Returns the selected class as a string to be stored into the playerList
def selectClass():
    print("\n" + "***CLASS SELECTION***")
    classes = ["Fighter", "Wizard", "Archer", "Rogue", "Sorcerer", "Barbarian", "Paladin", "Monk"]
    # prints out classes in the list
    classNumber = 1
    for i in classes:
        print(classNumber, ") ", i)
        classNumber += 1

    # asks user to select a class from the list
    catchBool = False
    while not catchBool:
        try:
            classSelect = int(input("Enter Class Selection Number to See Class Description: "))
        except ValueError:
            classSelect = 100
        if len(classes) >= classSelect > 0:
            classChoice = classes[classSelect - 1]
            if classChoice == "Fighter":
                print("""Fighter Description: A fighter uses speed and agility to vanquish their foes.
                      The fighter is a versatile, weapons-oriented warrior who fights using skill, 
                      strategy, and tactics.""")
            elif classChoice == "Wizard":
                print("""Wizard Description: Wizards are magic users, able to cast spells upon both the enemies and their
                      friends. Their power can range from fire, ice, regeneration to even mind control.""")
            elif classChoice == "Archer":
                print("""Archer Description: The archer is crafty nibble and Nobel.  
                      The archer usually stalks their prey from range, hunting them patiently, but in a pinch, 
                      the hunter can quickly escape from their foe.""")
            elif classChoice == "Rogue":
                print("""Rogue Description: The rogue is a versatile character, 
                      capable of sneaky combat and nimble tricks. The rogue is stealthy and dexterous.""")
            elif classChoice == "Sorcerer":
                print("""Sorcerer Description: The sorcerer calls upon dark magic to cast their spells upon enemies. 
                      Dark and twisted, they are not afraid to trick friends or foes to get what they want""")
            elif classChoice == "Barbarian":
                print("""Barbarian Description: The barbarian is filled with rage and power. 
                      Their strength allows them to wield even the heaviest of weapons with great proficiency, 
                      tearing through their enemies.""")
            elif classChoice == "Paladin":
                print("""Paladin Description: The paladin is the holiest of warriors. 
                      In the name of justice and honor, the paladin casts holy magic spells""")
            else:
                print("""Monk Description: The monk is a master of martial arts and inner tranquility. 
                      The fight mostly with their fists and with their minds.""")
            # asks the user if they want to confirm there class or continue looking at descriptions
            if confirmClass():
                catchBool = True
        else:
            print("You did not enter a valid class number")
    return classChoice


# Function Description: selectClass helper method. asks the user to confirm if they want the selected class
# Pre: Run when the user selects a class
# Post: Returns true if the user inputs Y or y, and false if they input anything else
def confirmClass():
    print("Would you like to confirm this as your class?")
    try:
        confirmation = input("Type Y or N: ")
        confirmation = confirmation.upper()
        if confirmation == "Y":
            return True
        else:
            return False
    except:
        return False


# Algorithm:
# 1. create list of all weapon types as strings
# 2. iterate through list and display all names to user
# 3. ask the user to select number for weapon and find that weapons index
# 4. if option 11 is chosen, find a random value within the length of the list and use that for weapon
# 5. return a string of the weapon chosen by the user, that is then stored into the player list
# Function Description: This function asks the user select a weapon
# Pre: Runs during the program
# Post: returns a string of the weapon selection
def askWeaponType():
    print("\n" + "***WEAPON SELECTION***")
    # defualt selection
    weaponChoice = "Sword"
    # list of weapons
    weapons = ["Shortbow", "Longbow", "Pike", "Shortsword", "Longsword", "Staff", "Dagger", "BroadSword", "Crossbow",
               "Halbert", "RandomSelection"]

    # prints out weapons in the list
    weaponNumber = 1
    for i in weapons:
        print(weaponNumber, ") ", i)
        weaponNumber += 1

    # asks user to select a weapon from the list
    catchBool = False
    while not catchBool:
        try:
            weaponSelect = int(input("Enter Weapon Selection Number: "))
        except ValueError:
            weaponSelect = 100
        if weaponSelect <= len(weapons) and weaponSelect > 0:
            weaponChoice = weapons[weaponSelect - 1]
            if weaponChoice == "RandomSelection":
                weaponChoice = weapons[random.randrange(0, len(weapons) - 1)]
            catchBool = True
        else:
            print("You did not select a valid weapon number...")

    # returns the users weapon choice
    return weaponChoice


# Function Description: This function asks the user select a gender
# Pre: Runs during the program
# Post: returns a string of the input gender
def askGender():
    gender = ""
    print("Please enter your character's gender")
    try:
        inputGender = str(input("CHARACTER GENDER: "))
        gender = inputGender
        return gender
    except ValueError:
        print("Please enter your gender")
        askGender()


# Algorithm:
# 1. Use global playerList to display all choices made by user to the console after character creation is finished
# Function Description: prints out all the selections that the user made for their character
# Pre: Runs after the character creation is finished
# Post: prints out all selections to console
def outputToConsole():
    print("\n" + "***YOUR CHARACTER***" + "\n")
    print("Name:", playerList[0])
    print("Gender:", playerList[1])
    print("Class:", playerList[2])
    playerList[3].display()
    print("Weapon:", playerList[4])
    print("Attributes:", playerList[5])


# Function Description: Create or Load a character, or Exit program
# Pre: Starts the program
# Post: Lets you selected options in the program
def menu():
    print("\nDo you want to create or load a character:\n"
          "1. Create\n"
          "2. Load\n"
          "3. Exit\n")
    try:
        userInput = int(input(">>>"))
        if userInput == 1:
            createCharacter()

        if userInput == 2:
            file = getSelectedFile()
            readCharacterFromFile(file)

            for index in range(len(playerList)):
                if index == 3:
                    playerList[index].display()
                elif index == 5:
                    for key, value in playerList[index].items():
                        print(key + ": " + str(value))
                elif index == 0 or 1 or 2 or 4 or 6:
                    print(playerList[index])

            input("Press Enter to continue back to menu")
            menu()

        if userInput == 3:
            exit()
    except ValueError:
        print("Wrong input try again")
        menu()
    menu()


# Function Description: Create a new character
# Pre: Call to create a new character
# Post: Prints everything about your character, populates the player list
def createCharacter():
    playerList[0] = askCharacterName()
    playerList[1] = askGender()
    playerList[2] = selectClass()
    playerList[3] = createPlayer()
    playerList[4] = askWeaponType()
    playerList[5] = placeAttributes()
    formatPlayer()
    writeFile()
    outputToConsole()


# Global variable playerList -- used to store data from character
listRaces = [Human, Elf, Orc, Ogre, Vampire, Dwarf, Giant, Gnome, Halfling]
playerList = [0 for i in range(6)]

# ----------- Driver Program -----------
menu()
