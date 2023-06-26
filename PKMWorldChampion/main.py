from ui import Window
from pkm import Trainer, PKMN
def main():
    loop = True
    trainer1 = Trainer(name = 'Violet', team = [PKMN['spearow'], PKMN['weedle'], PKMN['bulbasaur']])
    trainer2 = Trainer(name = 'Blue', team = [PKMN['rattata'], PKMN['caterpie'], PKMN['charmander']])
    window = Window()
    window.MainMenu()
    while loop: loop = window.Render().Menu(input('\n█ > '), trainer1, trainer2)

if __name__ == '__main__':
    main()
