class IMC:
    
    def __init__(self, _edad, _estatura, _peso):
        try:
            self.edad = int(_edad)
            if self.edad < 0:
                self.edad = 0
                print('La edad era negativa')
        except:
            self.edad = 0
            print('La edad estaba mala')
        try:
            self.estatura = float(_estatura)
            if self.estatura < 0:
                self.estatura = 0
                print('La estatura era negativa')
        except:
            self.estatura = 0
            print('La estatura estaba mala')
        try:
            self.peso = float(_peso)
            if self.peso < 0:
                self.peso = 0
                print('El peso era negativo')
        except:
            self.peso = 0
            print('El peso estaba malo')

    def __del__(self):
        pass

    def cambiar(self, _edad, _estatura, _peso):
        try:
            self.edad = int(_edad)
            if self.edad < 0:
                self.edad = 0
                print('La edad era negativa')
        except:
            self.edad = 0
            print('La edad estaba mala')
        try:
            self.estatura = float(_estatura)
            if self.estatura < 0:
                self.estatura = 0
                print('La estatura era negativa')
        except:
            self.estatura = 0
            print('La estatura estaba mala')
        try:
            self.peso = float(_peso)
            if self.peso < 0:
                self.peso = 0
                print('El peso era negativo')
        except:
            self.peso = 0
            print('El peso estaba mal')
    def calcular(self):
        if self.estatura > 0:
            return round(self.peso / pow(self.estatura, 2), 2)
        else:
            return 0
    def imprimir(self):
        print(self.__str__())
    def __str__(self) -> str:
        return f"{self.edad} / {self.estatura} / {self.peso} / {self.calcular()}"
    def __add__(self, _other):
        print("LA SUMA DE LAS EDADES ES")
        total = self.edad + _other.edad
        return (total)
    def __sub__(self, _other):
        if(self.estatura > _other.estatura):
            print("LA RESTA DE LAS ESTATURAS ES")
            return self.estatura - _other.estatura
        else:
            print("LA RESTA DE LAS ESTATURAS ES")
            return _other.estatura - self.estatura
    def __iadd__(self, _incremento):
        print("UN KILO MAS SERIA")
        self.pesoMas = self.peso + _incremento
        return self
    def __gt__(self, _other):
        return self.edad > _other.edad
    
    def __lt__(self, _other):
        return self.edad < _other.edad


imc = IMC(19, 1.75, 65)
imc2 = IMC(22, 1.73, 102)

validar = '0'

while validar == '0':
    edad = input("POR FAVOR INGRESE EDAD PERSONA 1\n")
    estatura = input("POR FAVOR INGRESE ESTATURA PERSONA 1\n")
    peso = input("POR FAVOR INGRESE PESO PERSONA 1\n")
    imc.cambiar(edad, estatura, peso)
    imc.imprimir()
    validar = input('LOS VALORES SON CORRECTOS?\n1: SI, CONTINUAR | 0: NO, REPETIR\n')

while validar == '0':
    edad = input("POR FAVOR INGRESE EDAD PERSONA 2\n")
    estatura = input("POR FAVOR INGRESE ESTATURA PERSONA 2\n")
    peso = input("POR FAVOR INGRESE PESO PERSONA 2\n")
    imc2.cambiar(edad, estatura, peso)
    imc2.imprimir()
    validar = input('LOS VALORES SON CORRECTOS?\n1: SI, CONTINUAR | 0: NO, REPETIR\n')

print(imc + imc2)
print(imc - imc2)
imc+=1
print (imc)
imc2+=1
print (imc2)
mayor = imc > imc2
print(mayor)
menor = imc < imc2
print(menor)