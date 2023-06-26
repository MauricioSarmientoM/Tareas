from typing import Self
from enum import Enum
from time import sleep
from os import system, name
from pkm import Trainer, Pokemon
class MenuState(Enum):
    MainMenu = 0
    MainMenuExitMessage = 1
    MainMenuStart = 2
    PlayLobby = 3
    Team = 4
    Settings = 5
class Window():
    def __init__(self, haveBorder : bool = True, state : MenuState = MenuState(0)) -> None:
        self.asciiMap = [[' ' for j in range(140)] for i in range(35)]
        self.haveBorder = haveBorder
        self.state = state
    def __str__(self) -> str:
        system('cls' if name == 'nt' else 'clear')
        if self.haveBorder: self.DrawBox(textBox = True)
        string = '\n'.join([''.join(i) for i in self.asciiMap])
        return string
    def Render(self) -> Self:
        print(self.__str__())
        return self
    def DrawBox(self, width : int = 140, height : int = 35, offsetX : int = 0, offsetY : int = 0, textBox : bool = False, solidBG : bool = False, solidBorder: bool = True) -> Self:
        if solidBG:
            for i in range(height):
                for j in range(width):
                    self.asciiMap[i + offsetY][j + offsetX] = ' '
        if solidBorder:
            for i in range(height):
                if i == 0:
                    for j in range(width):
                        self.asciiMap[0 + offsetY][j + offsetX] = '█'
                        if textBox: self.asciiMap[height - 3 + offsetY][j + offsetX] = '█'
                        self.asciiMap[height - 1 + offsetY][j + offsetX] = '█'
                self.asciiMap[i + offsetY][0 + offsetX] = '█'
                self.asciiMap[i + offsetY][width - 1 + offsetX] = '█'
        return self
    def DrawText(self, offsetX : int = 0, offsetY : int = 0, text = '') -> Self:
        for i, j in enumerate(text): self.asciiMap[offsetY][i + offsetX] = j
        return self
    def Menu(self, option : str, trainer1 : Trainer, trainer2 : Trainer) -> bool:
        match [option, self.state]:
            case ['start' | 'begin' | 'iniciar' | 'play', MenuState.MainMenu]:
                self.state = MenuState.MainMenuStart
                self.MainMenuStart()
            case ['quit' | 'exit' | 'salir', MenuState.MainMenu]:
                self.state = MenuState.MainMenuExitMessage
                self.MainMenu()
            case ['quit' | 'exit' | 'salir' | 'si' | 'yes' | 'y', MenuState.MainMenuExitMessage]:
                return False
            case ['cancel' | 'no' | 'n', MenuState.MainMenuExitMessage]:
                self.state = MenuState.MainMenu
                self.MainMenu()
            case ['back' | 'cancel' | 'exit' | 'salir' | 'atras' | 'quit', MenuState.MainMenuStart]:
                self.state = MenuState.MainMenu
                self.MainMenu()
            case ['play' | 'play!' | 'start' | 'begin', MenuState.MainMenuStart]:
                self.state = MenuState.PlayLobby
                self.PlayLobby(trainer1, trainer2)
            case ['team' | 'teams', MenuState.MainMenuStart]:
                self.state = MenuState.Team
                #self.Team(trainer1, trainer2)
                self.MainMenuStart()
            case ['settings', MenuState.MainMenuStart]:
                self.state = MenuState.Settings
                #self.Settings(trainer1, trainer2)
                self.MainMenuStart()
            case _: pass
        return True
    def MainMenu(self) -> Self:
        self.DrawBox(solidBG = True, solidBorder = False) #clear asciiBox
        title = ['⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀', '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠟⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀', '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢀⣀⠀⠀⠀⠀⠀⣠⣾⡿⠃⢀⣠⣽⠧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀', '⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣶⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣶⡾⢿⣿⣿⡿⣷⣄⠀⠀⣴⣿⣿⣴⣾⣟⣉⠀⠀⢀⣤⣤⣤⣤⣴⣿⡿⠿⠿⣿⡀⠀⠀⠀⠀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀', '⠀⠀⠀⠀⣀⣴⡾⠟⠛⠉⠉⠀⠀⠀⠀⠀⠉⠛⢿⣦⠀⠀⠀⠀⣿⣿⢉⡉⠀⠀⢸⣿⠟⠀⠈⠙⢷⣤⣼⡿⠟⠛⠛⠛⠛⠿⣦⣾⣿⡇⠀⠀⠀⢻⠇⠀⠀⢸⡇⠀⠀⠀⠘⣿⣿⠛⠛⠿⠶⣶⣦⣠⣄⣀⡀⠀⠀⠀⠀⠀', '⠀⠀⢠⣾⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣧⠀⠀⠀⣿⣿⣿⡇⠀⠀⠘⠋⠀⠀⠀⢀⣼⡿⠋⠀⣠⣴⣦⡄⠀⢀⣼⣿⣿⠁⠀⠀⠀⢸⠀⠀⠀⠸⣷⠀⠀⣀⣀⣿⣿⣷⠀⠀⠀⠀⣿⣿⡏⠙⠛⠻⣷⡆⠀⠀', '⠀⠀⠀⢻⣿⣿⣆⠀⡀⠀⠀⠀⠀⠸⣿⠻⣦⠀⠀⢸⣿⣀⣤⡶⠶⢿⣿⣇⠀⠀⠀⠀⠀⢀⣴⡿⣿⠃⠀⠰⡏⣰⠟⠀⣴⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡶⠟⢛⠉⠙⠻⣿⡀⠀⠀⠀⢹⣿⠁⠀⠀⢰⡿⠀⠀⠀', '⠀⠀⠀⠀⠹⣿⣿⣿⣿⡄⠀⠀⠀⠀⢻⣀⡿⠀⢀⣾⡿⠋⢁⡄⠀⠀⠈⠻⣆⠀⠀⠀⠀⠻⢿⣦⣿⡆⠀⠀⠛⠁⠀⠚⠋⠀⠉⢻⣷⡄⠀⠀⠀⠀⠀⠀⠀⣼⠏⠀⣾⣇⠀⠀⡀⠈⣿⠀⠀⠀⠘⡏⠀⠀⢀⣿⠃⠀⠀⠀', '⠀⠀⠀⠀⠀⠙⠋⢿⣿⣿⡀⠀⠀⠀⠘⠋⠀⣠⣾⡟⠀⠀⣿⣧⣄⣤⠆⠀⢿⠀⠀⢀⠀⠀⠀⠀⠉⢿⣦⡀⠀⠀⠀⠀⢀⣀⣴⣿⠋⠀⠀⢰⣆⠀⢠⠀⢸⡏⠀⠀⠹⢿⣿⠟⠁⠀⣼⠁⠀⠀⠀⠁⠀⠀⣸⡏⠀⠀⠀⠀', '⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣷⡀⠀⠀⠀⢰⣾⣿⣿⠀⠀⠀⠈⠛⠛⠉⠀⢀⣿⠀⠀⢸⣿⣶⣤⣀⠀⠀⠉⠛⠿⢷⣾⣿⡿⢿⣿⣿⠀⠀⠀⣸⣿⣆⣾⡇⠘⣧⠀⠀⠀⠀⠀⠀⠀⣴⠟⠀⡀⠀⠀⠀⠀⢠⡿⠀⠀⠀⠀⠀', '⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣧⠀⠀⠀⠀⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⣠⣾⡇⠀⠀⢸⡟⠻⢿⣿⣿⣶⣤⣀⠀⢸⡇⠀⠀⠼⢿⣿⣿⣿⣷⣿⣿⣿⣿⣇⠀⠙⢷⣤⣀⣀⣠⣴⣾⠋⠀⠀⣇⠀⠀⠀⠀⣾⠃⠀⠀⠀⠀⠀', '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣧⠀⠀⠀⢸⣿⢿⣿⣿⣶⣤⣤⣶⡾⣿⣿⣧⣤⣤⣾⡇⠀⠀⠈⠙⠻⢿⣿⣿⣾⡇⠀⠀⠀⠀⠀⠀⠈⠉⠀⠛⢻⣿⣿⣶⣶⣤⣼⣿⠛⢹⣿⣿⣤⣄⣰⣿⠀⠀⠀⣸⡟⠀⠀⠀⠀⠀⠀', '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣇⠀⠀⢀⣿⡄⠈⠙⠛⠛⠋⠉⠀⠙⠛⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠛⠻⠛⠀⠘⠛⠛⠻⢿⣿⣿⡀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀', '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣶⣾⡿⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀', ' ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀']
        for i, j in enumerate(title):
            for k, l in enumerate(j): self.asciiMap[i + 5][k + 30] = l
        if self.state.value == 1: self.DrawBox(width = 60, height = 10, offsetX = 40, offsetY = 13, solidBG = True).DrawText(67, 17, 'Sure?').DrawText(2, 33, 'Write "Exit" again to leave or "Cancel" to return to the main menu.')
        else: self.DrawText(60, 20, '---World Champion---').DrawText(2, 33, 'Write "Start" to continue or "Exit" to leave the app.')
        return self
    def MainMenuStart(self) -> Self:
        self.DrawBox(solidBG = True, solidBorder = False) #clear asciiBox
        self.DrawBox(width = 30, height = 7).DrawText(12, 3, 'Play!').DrawBox(width = 110, height = 7, offsetX = 30).DrawText(56, 2, 'Fight along your friends to show them who\'s the best!').DrawText(57, 3, 'You have to choose a team or build one by yourself.')
        self.DrawBox(width = 30, height = 7, offsetY = 6).DrawText(9, 9, 'Build Team').DrawBox(width = 110, height = 7, offsetX = 30, offsetY = 6).DrawText(57, 8, 'Build a custom team with your favorite pokemons or').DrawText(65, 9, '<Error>NotImolemented</Error>')#.DrawText(62, 9, 'choose one of many prefabricated teams!')
        #self.DrawBox(width = 30, height = 7, offsetY = 12).DrawText(10, 15, 'Settings').DrawBox(width = 110, height = 7, offsetX = 30, offsetY = 12).DrawText(61, 14, 'Change some options or load saved data from the').DrawText(61, 15, 'local disk, you can even see the raking tables!')
        if self.state.value == 4 or self.state.value == 5:
            self.DrawBox(width = 60, height = 10, offsetX = 40, offsetY = 13, solidBG = True).DrawText(55, 17, '<Error>NotImolemented</Error>').DrawText(2, 33, 'Too Fast, Too Soon.').Render()
            sleep(1.5)
            self.state = MenuState.MainMenuStart
            self.MainMenuStart()
        else: self.DrawText(2, 33, 'Write "Play", "Team", "Settings" or "Back" to continue.')
        return self
    def PlayLobby(self, trainer1 : Trainer, trainer2 : Trainer) -> Self:
        self.DrawBox(solidBG = True, solidBorder = False) #clear asciiBox
        self.DrawBox(width = 40, height = 25, offsetX = 6, offsetY = 3).DrawBox(width = 40, height = 4, offsetX = 6, offsetY = 3).DrawText(offsetX = 22, offsetY = 4, text = 'PLAYER 1')
        self.DrawBox(width = 40, height = 25, offsetX = 94, offsetY = 3).DrawBox(width = 40, height = 4, offsetX = 94, offsetY = 3).DrawText(offsetX = 110, offsetY = 4, text = 'PLAYER 2')
        self.DrawText(2, 33, 'Write "Play" to continue if both players are ready! Use "Back" to cancel.')
        return self
    def Team(self, trainer1 : Trainer, trainer2 : Trainer) -> Self:
        pass
    def Settings(self, trainer1 : Trainer, trainer2 : Trainer) -> Self:
        pass
