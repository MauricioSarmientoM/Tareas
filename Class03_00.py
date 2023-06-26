# Use Python 3.11 for correct functionality
# Also, for some reason, everything works kinda fine, but the price can't be modified, no idea why
from os import system, name
from json import dump, load
from typing import Self
class Media():
    def __init__(self, title = '', price = 0) -> None:
        self.__title = title
        self.__price = price

    @property
    def title(self) -> str: return self.__title
    @property
    def price(self) -> int: return self.__price
    @property
    def description(self) -> str: return f'{self.title} --- {self.price}[$]'
    def Modify(self, title = '', price = 0) -> Self:
        if title != '0': self.__title = title
        if price != 0: self__price = price
        return self
    @classmethod
    def CommandDescription(self) -> str: pass

class Book(Media):
    def __init__(self, title = '', price = 0, pages = 0, editorial = '') -> None:
        super().__init__(title, price)
        self.__pages = pages
        self.__editorial = editorial

    @property
    def pages(self) -> int: return self.__pages
    @property
    def editorial(self) -> str: return self.__editorial
    @editorial.setter
    def editorial(self, editorial = '') -> str:
        self.__editorial = editorial
        return self.__editorial
    @property
    def description(self) -> str: return 'Book) ' + super().description + f' --- {self.pages} pages --- Editorial {self.editorial}'
    def Modify(self, title = '', price = 0, pages = 0, editorial = '') -> Self:
        if pages != 0: self.__pages = pages
        if editorial != '0': self.__editorial = editorial
        return super().Modify(title, price)
    @property
    def toList(self) -> dict: return [self.title, self.price, self.pages, self.editorial]
    @classmethod
    def CommandDescription(self) -> str: return 'Usage: book [OPTIONS]... [DATA]...\nLet the user interact with the digital bookshelf.\n\t-a\t--add\t\t\tCreates a new book with NAME, PRICE and PAGES.\n\t-m\t--modify\t\t\tModify a book based on its position on the list. USAGE title=[OPTION] price=[OPTION] pages=[OPTION] editorial=[OPTION]\n\t-l <FLAGS>...\t\t\tLists all the created books.\n\t\t-A\t--asc\t\tSorts the books by ascendant id.\n\t\t-D\t--desc\t\tSorts the books by descendant id.\n\t-s\t--save\t\t\tSave the changes for books and cds in disk.\n\t--help\t\t\t\tdisplay this help\n'

class CD(Media):
    def __init__(self, title = '', price = 0, duration = 0, producer = '') -> None:
        super().__init__(title, price)
        self.__duration = duration
        self.__producer = producer

    @property
    def duration(self) -> int: return self.__duration
    @property
    def producer(self) -> str: return self.__producer
    @producer.setter
    def producer(self, producer = '') -> str:
        self.__producer = producer
        return self.__producer
    @property
    def description(self) -> str: return 'CD) ' + super().description + f' --- {self.duration} minutes --- Producer {self.producer}'
    def Modify(self, title = '', price = 0, duration = 0, producer = '') -> Self:
        if duration != 0: self.__duration = duration
        if producer != '0': self.__producer = producer
        return super().Modify(title, price)
    @property
    def toList(self) -> dict: return [self.title, self.price, self.duration, self.producer]
    @classmethod
    def CommandDescription(self) -> str: return 'Usage: comdisk [OPTIONS]... [DATA]...\nLet the user interact with the digital CD shelf.\n\t-a\t--add\t\t\tCreates a new book with NAME, PRICE and PAGES.\n\t-m\t--modify\t\t\tModify a CD based on its position on the list. USAGE title=[OPTION] price=[OPTION] duration=[OPTION] producer=[OPTION]\n\t-l <FLAGS>...\t\t\tLists all the created books.\n\t\t-A\t--asc\t\tSorts the books by ascendant id.\n\t\t-D\t--desc\t\tSorts the books by descendant id.\n\t-s\t--save\t\t\tSave the changes for books and cds in disk.\n\t--help\t\t\t\tdisplay this help\n'

def AddBook(books : list[Book], info : list[str]) -> None:
    if len(info) != 4: print(f'This command takes 4 positional arguments but {len(info)} were given.')
    else:
        try:
            obj = Book(info[0], int(info[1]), int(info[2]), info[3])
            books.append(obj)
            print(f'Book {info[0]} added successfully.'.replace('_', ' '))
        except ValueError as e: print(e)
def AddCD(cds : list[CD], info : list[str]) -> None:
    if len(info) != 4: print(f'This command takes 4 positional arguments but {len(info)} were given.')
    else:
        try:
            obj = CD(info[0], int(info[1]), int(info[2]), info[3])
            cds.append(obj)
            print(f'CD {info[0]} added successfully'.replace('_', ' '))
        except ValueError as e: print(e)
def ModifyMedia(media: list, info : list[str]) -> None:
    try:
        pos = int(info[0]) if int(info[0]) < len(media) else len(media) - 1
        info = [i for i in info if '=' in i]
        verify = {}
        for i in info:
            splitPairs = i.split('=')
            if len(splitPairs) == 2: verify[splitPairs[0].lower()] = splitPairs[1]
            else: print(f'"{i}"\nChanging an attribute takes 2 positional arguments but {len(splitPairs)} were given.')
        if len(verify) == 0: print('No valid arguments given to change.')
        else:
            for i in ['title', 'price', 'pages', 'editorial', 'duration', 'producer']:
                if not i in verify.keys(): verify[i] = '0'
            if isinstance(media[pos], Book): media[pos].Modify(title = verify['title'], price = int(verify['price']), pages = int(verify['pages']), editorial = verify['editorial'])
            elif isinstance(media[pos], CD): media[pos].Modify(title = verify['title'], price = int(verify['price']), duration = int(verify['duration']), producer = verify['producer'])
            else: print('Something is wrong...')
            print(f'{media[pos].title} was successully modified.'.replace('_', ' '))
    except: print(f'"{info[0]}" is not a valid book position.')
def ListMedia(media : list[Media], flags : list[str] = ['-a']) -> None:
    print('id\t|\tMedia\n_________________________________________________________________')
    if len(media) == 0:
        print('---\t|\tNo information able for the moment, add books with the command "book -a [DATA]"')
    else:
        if len(flags) != 1: print(f'This command takes 1 positional argument but {len(flags)} were given.')
        else:
            iterable : enumerate
            match flags:
                case ['-D' | '--desc']:
                    iterable = enumerate(media[::-1])
                case _:# | ['-A' | '--asc']:
                    iterable = enumerate(media)
            for i, j in iterable: print('{}\t|\t{}'.format(i, j.description.replace('_', ' ')))
def SaveData(books : list[Book], cds : list[CD]) -> None:
    try:
        jsonDict = {'book': {}, 'comdisk': {}}
        for i in books:
            listObj = i.toList
            jsonDict['book'][listObj[0]] = {'price': listObj[1], 'pages': listObj[2], 'editorial': listObj[3]}
        for i in cds:
            listObj = i.toList
            jsonDict['comdisk'][listObj[0]] = {'price': listObj[1], 'duration': listObj[2], 'producer': listObj[3]}
        with open('Class03_00.json', 'w') as writeFile: dump(jsonDict, writeFile)
        print('Data saved successfully!')
    except: print('Something went wrong...')
def LoadData(key : str) -> list[Media]:
    info = []
    try:
        with open('Class03_00.json', 'r') as openFile: data = load(openFile)
        if key == 'book': info = [Book(i, j['price'], j['pages'], j['editorial']) for i, j in data[key].items()]
        elif key == 'comdisk': info = [CD(i, j['price'], j['duration'], j['producer']) for i, j in data[key].items()]
    except: print('Something went wrong...')
    return info
def main():
    books = LoadData('book')
    cds = LoadData('comdisk')
    command = ''
    print('Introduce a command to continue.\n\tbook\t\tAcceed to the book database and interact with books.\n\tcomdisk\t\tAcceed to the CD database and interact with the CDs.\n\texit\t\tClose the program.\nFor more information, add the --help flag to the command.\n')
    while True:
        command = input('user@pystem:$ ')
        match command.split(' '):
            case ['book'] | ['book', '--help']:
                print(Book.CommandDescription())
            case ['book', '--add' | '-a', *info]:
                AddBook(books, info)
            case ['book', '-m' | '--modify', *info]:
                ModifyMedia(books, info)
            case ['book', '-l']:
                ListMedia(books)
            case ['book', '-l', *flags]:
                ListMedia(books, flags)
            case ['comdisk'] | ['comdisk', '--help']:
                print(CD.CommandDescription())
            case ['comdisk', '--add' | '-a', *info]:
                AddCD(cds, info)
            case ['comdisk', '-m' | '--modify', *info]:
                ModifyMedia(cds, info)
            case ['comdisk', '-l']:
                ListMedia(cds)
            case ['comdisk', '-l', *flags]:
                ListMedia(cds, flags)
            case ['comdisk' | 'book', '-s' | '--save']:
                SaveData(books, cds)
            case ['ls' | 'dir']:
                system('dir' if name == 'nt' else 'ls')
            case ['clear' | 'cls']:
                system('cls' if name == 'nt' else 'clear')
                print('Introduce a command to continue.\n\tbook\t\tAcceed to the book database and interact with books.\n\tcomdisk\t\tAcceed to the CD database and interact with the CDs.\n\texit\t\tClose the program.\nFor more information, add the --help flag to the command.\n')
            case ['exit' | 'close' | 'quit']:
                break
            case _:
                print('Introduce a command to continue.\n\tbook\t\tAcceed to the book database and interact with books.\n\tcomdisk\t\tAcceed to the CD database and interact with the CDs.\n\texit\t\tClose the program.\nFor more information, add the --help flag to the command.\n')

if __name__ == '__main__':
    main()
