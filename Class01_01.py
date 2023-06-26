class Item:
    def __init__(self, name = 'Health Potion', typeItem = 'Potion') -> None:
        self.name = name
        self.typeItem = typeItem
    def UseItem(self):
        return self
class Weapon(Item):
    def __init__(self, name = '9mm Pistol', typeItem = 'Pistol', damage = 1, bullet = 'HitScan') -> None:
        super().__init__(name = name, typeItem = typeItem)
        self.damage = damage
        self.bullet = self.maxBullet = bullet
    def Shoot(self):
        if self.bullet > 0:
            self.bullet -= 1
        return self
class Entity:
    def __init__(self, name = 'Entity', health = 10, shield = 10) -> None:
        self.name = name
        self.health = self.maxHealth = health
        self.shield = self.maxShield = shield
    def TakeDamage(self, damage = 1):
        if self.shield > 0:
            self.shield = self.shield - damage if self.shield > damage else 0
        else:
            self.health = self.health - damage if self.health > damage else 0
        return self.Die()
    def Die(self):
        if self.health == 0:
            print(f'{self.name} has died!')
        return self
class Hero(Entity):
    def __init__(self, name = 'An Hero', health = 10, shield = 10, mainWeapon = Weapon(), secondaryWeapon = Weapon()) -> None:
        super().__init__(name = name, health = health, shield = shield)
        self.mainWeapon = mainWeapon
        self.secondaryWeapon = secondaryWeapon
        self.items = []
    def TakeItem(self, item = Item()):
        self.items.append(item)

class Enemy(Entity):
    def __init__(self, name = 'Entity', health = 10, shield = 10) -> None:
        super().__init__(name, health, shield)
    def Attack(self, target):
        pass

flamethrower = Weapon(name = 'Flamethrower', typeItem = 'Flamethrower')
axe = Weapon(name = 'Fireman Axe', typeItem = 'Melee')
guy = Hero(name = 'Guy Montag', mainWeapon = flamethrower, secondaryWeapon = axe)