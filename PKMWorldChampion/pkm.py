from typing import Self
from enum import Enum
from random import randint
#Useful functions
def Clamp(value : int | float, minimum : int | float, maximum : int | float):
    if value < minimum: return minimum
    elif value > maximum: return maximum
    return value
#Useful enums
class Type(Enum):
    Normal = 0
    Fighting = 1
    Flying = 2
    Poison = 3
    Ground = 4
    Rock = 5
    Bug = 6
    Ghost = 7
    Steel = 8
    Fire = 9
    Water = 10
    Grass = 11
    Electric = 12
    Psychic = 13
    Ice = 14
    Dragon = 15
    Dark = 16
    Fairy = 17
    NoneType = 18
class DamageType(Enum):
    ContactPhysical = 0
    DistantPhysical = 1
    Special = 2
    Status = 3
#Big pokemon class with all the useful and generic stuff for later
class Pokemon():
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        self.name = name
        self.species = species
        self.level = 1
        self.types = Type(18), secondaryType            #Based on the main games, a pokemon can only have two types, saved on this tuple
        self.typeRel = []                               #The relationship of this type with the others, weakness and strength are here
        self.moves = moves
        #Setting genes for the pokemon
        self.genPS = randint(0, 31)
        self.genPP = randint(0, 31)
        self.genPrecision = randint(0, 31)
        self.genEvasion = randint(0, 31)
        self.genSpeed = randint(0, 31)
        self.genDefense = randint(0, 31)
        self.genResistance = randint(0, 31)
        self.genAttack = randint(0, 31)
        self.genSpecial = randint(0, 31)
        #Setting basic stats
        self.baseMaxPs = ps
        self.maxPs = self.ps = self.genPS + self.baseMaxPs
        self.baseMaxPp = pp
        self.maxPp = self.pp = self.genPP + self.baseMaxPp
        self.baseAttack = self.attack = attack
        self.baseDefense = self.defense = defense
        self.baseSpecial = self.special = special
        self.baseResistance = self.resistance = resistance
        self.basePrecision = self.precision = precision
        self.baseEvasion = self.evasion = evasion
        self.baseSpeed = self.speed = speed
        #Multipliers
        self.attackMultiplier = 1
        self.defenseMultiplier = 1
        self.specialMultiplier = 1
        self.resistanceMultiplier = 1
        self.speedMultiplier = 1
        self.precisionMultiplier = 1
        self.evasionMultiplier = 1
        #Status effect
        self.flinch = False
        self.burn = False
        self.freeze = False
        self.paralyzis = False
        self.poison = False
        self.toxic = False
        self.sleep = False
        self.confusion = False
        self.seeded = False
        self.splinters = False
        #
        self.gainPs = 0
        self.gainPp = 0
        self.damageRecived = 0
        self.damageStatus = 0
        self.lastUsedMove = None
    @property
    def Attack(self) -> int: return round((self.attack + self.genAttack) * self.attackMultiplier * (.5 if self.burn else 1))
    @property
    def Defense(self) -> int: return round((self.defense + self.genDefense) * self.defenseMultiplier)
    @property
    def Special(self) -> int: return round((self.special + self.genSpecial) * self.specialMultiplier * (.5 if self.toxic else 1))
    @property
    def Resistance(self) -> int: return round((self.resistance + self.genResistance) * self.resistanceMultiplier * (.5 if self.sleep else 1))
    @property
    def Speed(self) -> int: return round((self.speed + self.genSpeed) * self.speedMultiplier * (.5 if self.paralyzis else 1))
    @property
    def Precision(self) -> int: return round((self.precision + self.genPrecision) * self.precisionMultiplier)
    @property
    def Evasion(self) -> int: return round((self.evasion + self.genEvasion) * self.evasionMultiplier)
    def UseMove(self, move : int, other : Self) -> Self:
        if not (move < 0 or move > 4): 
            if not self.flinch and not self.freeze and self.paralyzis:
                if self.moves[move].ppUsage <= self.pp: self.moves[move].Execute(self, other)
            else: self.flinch = False
        return self
    def TakeDamage(self, damage) -> Self:
        self.damageRecived = damage
        self.ps = Clamp(self.ps - self.damageRecived, 0, self.maxPs)
        return self
    def ModifyVitals(self, addPS : int = 0, addPercentajePS : int = 0, addPP : int = 0, addPercentajePP : int = 0) -> Self:
        self.gainPs = Clamp(addPS + int(self.maxPs * addPercentajePS / 100), 0, self.maxPs)
        self.gainPp = Clamp(addPP + int(self.maxPp * addPercentajePP / 100), 0, self.maxPp)
        self.ps += self.gainPs
        self.pp += self.gainPp
        return self
    def StartTurn(self, other : Self) -> Self:
        self.damageStatus = 0
        if self.burn:
            damage = round(self.maxPs / 8)
            self.damageStatus += damage
            self.ps = Clamp(self.ps - damage, 0, self.maxPs)
            if randint(0, 100) < (67 if self.types[0] == Type(9) or self.types[1] == Type(9) else 5): self.burn = False
        if self.freeze and randint(0, 100) < 67 if self.types[0] == Type(14) or self.types[1] == Type(14) else 10: self.freeze = False
        if self.poison:
            damage = round(self.maxPs / 8)
            self.damageStatus += damage
            self.ps = Clamp(self.ps - damage, 1, self.maxPs)
        if self.toxic:
            damage = round(self.maxPs / 16)
            self.damageStatus += damage
            self.ps = Clamp(self.ps - damage, 1, self.maxPs)
        if self.sleep and randint(0, 100) < 20: self.sleep = False
        if self.seeded:
            damage = round(self.maxPs / 16) if self.types[0] == Type(11) or self.types[1] == Type(11) else round(self.maxPs / 8)
            self.damageStatus += damage
            self.ps = Clamp(self.ps - damage, 0, self.maxPs)
            other.ModifyVitals(addPS = damage)
        if self.splinters:
            CRITICAL = 1.5 if randint(0, 101) > self.critChance else 1
            relation = 1
            for i in self.types: relation = Clamp(relation * self.typeRel[i.value], 1, 8)
            damage = round((((25 / self.defense) + 2)  * CRITICAL * relation) + self.ps / 16)
            self.damageStatus += damage
            self.ps = Clamp(self.ps - damage, 0, self.maxPs)
            if randint(0, 100) < (80 if self.types[0] == Type(6) or self.types[1] == Type(6) else 20): self.burn = False
        return self
#Children from pokemon, kind of redundant, but that's what the profe asked
class NormalType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(0), secondaryType
        self.typeRel = [1, 1, 1, 1, 1, .5, 1, 0, .5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
class FightingType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(1), secondaryType
        self.typeRel = [2, 1, .5, .5, 1, 2, .5, 0, 2, 1, 1, 1, 1, .5, 2, 1, 2, .5, 1]
class FlyingType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(2), secondaryType
        self.typeRel = [1, 2, 1, 1, 1, .5, 2, 1, .5, 1, 1, 2, .5, 1, 1, 1, 1, 1, 1]
class PoisonType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(3), secondaryType
        self.typeRel = [1, 1, 1, .5, .5, .5, 1, .5, 0, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1]
class GroundType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(4), secondaryType
        self.typeRel = [1, 1, 0, 2, 1, 2, .5, 1, 2, 2, 1, .5, 2, 1, 1, 1, 1, 1, 1]
class RockType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(5), secondaryType
        self.typeRel = [1, .5, 2, 1, .5, 1, 2, 1, .5, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1]
class BugType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(6), secondaryType
        self.typeRel = [1, .5, .5, .5, 1, 1, 1, .5, .5, .5, 1, 2, 1, 2, 1, 1, 2, .5, 1]
class GhostType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(7), secondaryType
        self.typeRel = [0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, .5, 1, 1]
class SteelType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(8), secondaryType
        self.typeRel = [1, 1, 1, 1, 1, 2, 1, 1, .5, .5, .5, 1, .5, 1, 2, 1, 1, 2, 1]
class FireType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(9), secondaryType
        self.typeRel = [1, 1, 1, 1, 1, .5, 2, 1, 2, .5, .5, 2, 1, 1, 2, .5, 1, 1, 1]
class WaterType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(10), secondaryType
        self.typeRel = [1, 1, 1, 1, 2, 2, 1, 1, 1, 2, .5, .5, 1, 1, 1, .5, 1, 1, 1]
class GrassType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(11), secondaryType
        self.typeRel = [1, 1, .5, .5, 2, 2, .5, 1, .5, .5, 2, .5, 1, 1, 1, .5, 1, 1, 1]
class ElectricType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(12), secondaryType
        self.typeRel = [1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 2, .5, .5, 1, 1, .5, 1, 1, 1]
class PsychicType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(13), secondaryType
        self.typeRel = [1, 2, 1, 2, 1, 1, 1, 1, .5, 1, 1, 1, 1, .5, 1, 1, 0, 1, 1]
class IceType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(14), secondaryType
        self.typeRel = [1, 1, 2, 1, 2, 1, 1, 1, .5, 2, .5, 2, 1, 1, .5, 2, 1, 1, 1]
class DragonType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(15), secondaryType
        self.typeRel = [1, 1, 1, 1, 1, 1, 1, 1, .5, 1, 1, 1, 1, 1, 1, 2, 1, 0, 1]
class DarkType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(16), secondaryType
        self.typeRel = [1, .5, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, .5, .5, 1]
class FairyType(Pokemon):
    def __init__(self, name : str = "", species : str = "", ps : int = 10, pp : int = 10, attack : int = 10, defense : int = 10, special : int = 10, resistance : int = 10, precision : int = 10, evasion : int = 10, speed : int = 10, secondaryType : Type = Type(18), moves : list = []):
        super().__init__(name, species, ps, pp, attack, defense, special, resistance, precision, evasion, speed, secondaryType, moves)
        self.types = Type(17), secondaryType
        self.typeRel = [1, 2, 1, .5, 1, 1, 1, 1, .5, .5, 1, 1, 1, 2, 1, 1, 2, 2, 1]
# MOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVESMOVES
class Move():
    def __init__(self, elementType : Type, name : str = '', description : str = '', damageType : DamageType = DamageType(0), power : int = 0, precision : int = 100, critChance : int = 4, affectUserPercentage : int = 0, healPercentage : int = 0, ppUsage : int = 1, flinchChance : int = 0, burnChance : int = 0, freezeChance : int = 0, paralyzisChance : int = 0, poisonChance : int = 0, toxicChance : int = 0, sleepChance : int = 0, confusionChance : int = 0, seededChance : int = 0, splintersChance : int = 0, hasPriority : bool = False, modUserChance : int = 0, modTargetChance : int = 0, modUserAttack : int = 0, modUserDefense : int = 0, modUserSpecial : int = 0, modUserResistance : int = 0, modUserSpeed : int = 0, modUserPrecision : int = 0, modUserEvasion : int = 0, modTargetAttack : int = 0, modTargetDefense : int = 0, modTargetSpecial : int = 0, modTargetResistance : int = 0, modTargetSpeed : int = 0, modTargetPrecision : int = 0, modTargetEvasion : int = 0):
        self.elementType = elementType
        self.name = name
        self.description = description
        self.damageType = damageType
        self.power = power
        self.precision = precision
        self.critChance = critChance
        self.affectUserPercentage = affectUserPercentage
        self.healPercentage = healPercentage
        self.ppUsage = ppUsage
        #Status effects
        self.flinchChance = flinchChance
        self.burnChance = burnChance
        self.freezeChance = freezeChance
        self.paralyzisChance = paralyzisChance
        self.poisonChance = poisonChance
        self.toxicChance = toxicChance
        self.sleepChance = sleepChance
        self.confusionChance = confusionChance
        self.seededChance = seededChance
        self.splintersChance = splintersChance
        #This allow quick moves
        self.hasPriority = hasPriority
        #Stats gaem
        self.modUserChance = modUserChance
        self.modTargetChance = modTargetChance
        self.modUserAttack = modUserAttack
        self.modUserDefense = modUserDefense
        self.modUserSpecial = modUserSpecial
        self.modUserResistance = modUserResistance
        self.modUserSpeed = modUserSpeed
        self.modUserPrecision = modUserPrecision
        self.modUserEvasion = modUserEvasion
        self.modTargetAttack = modTargetAttack
        self.modTargetDefense = modTargetDefense
        self.modTargetSpecial = modTargetSpecial
        self.modTargetResistance = modTargetResistance
        self.modTargetSpeed = modTargetSpeed
        self.modTargetPrecision = modTargetPrecision
        self.modTargetEvasion = modTargetEvasion
    def Execute(self, user : Pokemon, target : Pokemon):
        CRITICAL = 1.5 if randint(0, 101) > self.critChance else 1
        userAttack = target.Attack if self.damageType != DamageType(2) else target.Special
        targetDefense = target.Defense if self.damageType != DamageType(2) else target.Resistance
        userPrecision = randint(user.level + (user.Precision / 2), user.Precision)
        targetEvasion = randint(target.level + (target.Evasion / 2), target.Evasion)
        STAB = 1.5 if user.types[0] == self.elementType or user.types[1] == self.elementType else 1
        relation = 1
        for i in target.types: relation *= target.typeRel[i.value]
        damage = round(((((((2 * user.level) / 5) + 2) * self.power * userAttack / targetDefense) / 50) + 2)  * (userPrecision / targetEvasion) * CRITICAL * STAB * relation)
        if damage != 0:
            target.TakeDamage(damage)
            user.ModifyVitals(addPS = damage * self.healPercentage)
            user.TakeDamage(round(damage * self.affectUserPercentage / 100))
#Player as trainer stuff
class Trainer():
    def __init__(self, name : str = 'Trainer', team : list[Pokemon] = []):
        self.name = name
        self.team = team
    @property
    def hasTeam(self) -> bool: return len(self.team) > 0
    def ChangePkmn(self, pkmn : Pokemon, position : int) -> bool:
        pass

MOVE : dict[Move] = {
    'absorb' : Move(Type(11), 'Absorb', 'A nutrient-draining attack. The user\'s HP is restored by up to half the damage taken by the target.', damageType = DamageType(2), power = 20, precision = 100, healPercentage = 50, ppUsage = 4),
    'acid': Move(Type(3), 'Acid', 'Opposing Pokémon are attacked with a spray of harsh acid. This may also lower their Sp. Def stats.', damageType = DamageType(2), power = 40, precision = 100, ppUsage = 3, modTargetChance = 10, modTargetResistance = -1),
    'agility': Move(Type(13), 'Agility', 'The user relaxes and lightens its body to move faster. This sharply boosts its Speed stat.', damageType = DamageType(3), precision = 100, critChance = 0, modUserChance = 100, modUserSpeed = 2),
    'bite' : Move(Type(16), 'Bite', 'The target is bitten with viciously sharp fangs. This may also make the target flinch.', damageType = DamageType(0), power = 60, precision = 100, ppUsage = 4, flinchChance = 30),
    'doubleteam' : Move(Type(0), 'Double Team', '	By moving rapidly, the user makes illusory copies of itself to boost its evasiveness.', damageType = DamageType(3), precision = 100, critChance = 0, ppUsage = 2, modUserChance = 100, modUserEvasion = 1),
    'ember' : Move(Type(9), 'Ember', 'The target is attacked with small flames. This may also leave the target with a burn.', damageType = DamageType(2), power = 40, precision = 100, ppUsage = 4, burnChance = 10),
    'flamethrower' : Move(Type(9), 'Flamethrower', 'The target is scorched with an intense blast of fire. This may also leave the target with a burn.', damageType = DamageType(2), power = 90, precision = 100, ppUsage = 10, burnChance = 10),
    'glare' : Move(Type(0), 'Glare', 'The user gives opposing Pokémon an intimidating glare that lowers their Defense stats.', damageType = DamageType(3), precision = 100, critChance = 0, ppUsage = 3, modTargetChance = 100, modTargetDefense = -1),
    'growl' : Move(Type(0), 'Growl', 'The user growls in an endearing way, making opposing Pokémon less wary. This lowers their Attack stats.', damageType = DamageType(3), precision = 100, critChance = 0, ppUsage = 2, modTargetChance = 100, modTargetAttack = -1),
    'gust' : Move(Type(2), 'Gust', 'A gust of wind is whipped up by wings and launched at the target to inflict damage.', damageType = DamageType(2), power = 40, precision = 100, ppUsage = 3),
    'harden' : Move(Type(0), 'Harden', 'The user stiffens all the muscles in its body to boost its Defense stat.', damageType = DamageType(3), precision = 100, critChance = 0, ppUsage = 2, modUserChance = 100, modUserDefense = 1),
    'hydropump' : Move(Type(10), 'Hydro Pump', 'The target is blasted by a huge volume of water launched under great pressure.', damageType = DamageType(2), power = 120, precision = 80, ppUsage = 20),
    'icebeam' : Move(Type(14), 'Ice Beam', 'The target is struck with an icy-cold beam of energy. This may also leave the target frozen.', damageType = DamageType(2), power = 90, precision = 100, ppUsage = 10, freezeChance = 10),
    'leechseed' : Move(Type(11), 'Leech Seed', 'A seed is planted on the target. It steals some HP from the target every turn.', damageType = DamageType(3), precision = 90, critChance = 0, ppUsage = 10, seededChance = 10),
    'liquify' : Move(Type(3), 'Liquify', 'The user alters its cellular structure to liquefy itself, boosting its Defense stat and Evasion.', damageType = DamageType(3), precision = 100, critChance = 0, ppUsage = 5, modUserChance = 100, modUserDefense = 1, modUserEvasion = 1),
    'peek' : Move(Type(2), 'Peek', 'The target is jabbed with a sharply pointed beak or horn to inflict damage. ', damageType = DamageType(0), power = 35, precision = 100, ppUsage = 3),
    'pinmissile' : Move(Type(6), 'Pin Missile', 'Sharp spikes are shot at the target. Spike splinters left behind by this attack continue to damage the target for several turns.', damageType = DamageType(1), power = 40, precision = 100, ppUsage = 5, splintersChance = 100),
    'poisonpowder' : Move(Type(3), 'Poison Powder', 'The user scatters a cloud of poisonous dust that poisons the target.', damageType = DamageType(3), precision = 75, critChance = 0, ppUsage = 3, poisonChance = 100),
    'poisonsting' : Move(Type(3), 'The user stabs the target with a poisonous stinger to inflict damage. This may also poison the target.', damageType = DamageType(3), power = 25, precision = 100, critChance = 4, ppUsage = 2, poisonChance = 30),
    'quickattack' : Move(Type(0), 'Quick Attack', 'he user lunges at the target to inflict damage, moving at blinding speed. This move always goes first.', damageType = DamageType(0), power = 40, precision = 100, ppUsage = 3, hasPriority = True),
    'razorleaf' : Move(Type(11), 'Razor Leaf', 'Sharp-edged leaves are launched to slash at opposing Pokémon. This move has a heightened chance of landing a critical hit.', damageType = DamageType(2), power = 40,  precision = 100, critChance = 10, ppUsage = 4),
    'sandattack' : Move(Type(4), 'Ground', 'Sand is hurled in the target\'s face, lowering the target\'s accuracy.', damageType = DamageType(3), precision = 100, critChance = 0, ppUsage = 7, modTargetChance = 100, modTargetPrecision = -1),
    'scratch' : Move(Type(0), 'Scratch', 'Hard, pointed, sharp claws rake the target to inflict damage.', damageType = DamageType(0), power = 40, precision = 100, ppUsage = 3),
    'slash' : Move(Type(0), 'Slash', 'The target is attacked with a slash of claws, scythes, or the like. This move has a heightened chance of landing a critical hit.', damageType = DamageType(0), power = 70, precision = 100, ppUsage = 6, critChance = 15),
    'sleeppowder' : Move(Type(11), 'Sleep Powder', 'The user scatters a cloud of soporific dust that puts the target to sleep.', damageType = DamageType(3), precision = 75, critChance = 0, ppUsage = 7, sleepChance = 100),
    'strength' : Move(Type(1), 'Strengh', 'The target is slugged with a punch thrown at maximum power.', damageType = DamageType(0), power = 80, precision = 100, ppUsage = 7),
    'stringshot' : Move(Type(6), 'String Shot', 'The user blows silk from its mouth that binds opposing Pokémon and harshly lowers their Speed stats.', damageType = DamageType(3), precision = 95, critChance = 0, ppUsage = 2, modTargetChance = 100, modTargetSpeed = -1),
    'stunspore' : Move(Type(3), 'Stun Spore', 'The user scatters a cloud of numbing powder that paralyzes the target.', damageType = DamageType(3), precision = 75, critChance = 0, ppUsage = 3, sleepChance = 100),
    'tackle' : Move(Type(0), 'Tackle', 'A physical attack in which the user charges and slams into the target with its whole body.', damageType = DamageType(0), power = 40, precision = 100, ppUsage = 3),
    'tailwhip' : Move(Type(0), 'Tail Whip', 'The user wags its tail cutely, making opposing Pokémon less wary. This lowers their Defense stats.', damageType = DamageType(3), precision = 100, critChance = 0, ppUsage = 3, modTargetChance = 100, modTargetDefense = -1),
    'vinewhip' : Move(Type(11), 'Vine Whip', 'The target is struck with slender, whiplike vines to inflict damage.', damageType = DamageType(0), power = 45, precision = 100, ppUsage = 4),
    'withdraw' : Move(Type(10), 'Withdraw', 'The user withdraws its body into its hard shell, boosting its Defense stat.', damageType = DamageType(3), precision = 100, critChance = 0, ppUsage = 2, modUserChance = 100, modUserDefense = 1)
}

PKMN : dict[Pokemon] = {
    'bulbasaur': GrassType(species = 'Bulbasaur', ps = 45, attack = 49, defense = 49, special = 65, resistance = 65, speed = 45, secondaryType = Type(3), moves = [MOVE['tackle'], MOVE['poisonpowder'], MOVE['razorleaf'], MOVE['leechseed']]), #318
    'charmander' : FireType(species = 'Charmander', ps = 39, attack = 52, defense = 43, special = 60, resistance = 50, speed = 65, secondaryType = Type(18), moves = [MOVE['scratch'], MOVE['glare'], MOVE['ember'], MOVE['strength']]), #309
    'squirtle' : WaterType(species = 'Squirtle', ps = 44, attack = 48, defense = 65, special = 50, resistance = 64, speed = 43, secondaryType = Type(18), moves = [MOVE['tackle'], MOVE['withdraw'], MOVE['hydropump'], MOVE['icebeam']]), #314
    'caterpie' : BugType(species = 'Caterpie', ps = 45, attack = 50, defense = 35, special = 50, resistance = 20, speed = 45, secondaryType = Type(0), moves = [MOVE['tackle'], MOVE['stringshot'], MOVE['harden'], MOVE['sleeppowder']]), #245
    'weedle' : BugType(species = 'Weedle', ps = 40, attack = 35, defense = 30, special = 55, resistance = 20, speed = 65, secondaryType = Type(3), moves = [MOVE['poisonsting'], MOVE['stringshot'], MOVE['harden'], MOVE['pinmissile']]), #245
    'pidgey' : NormalType(species = 'Pidgey', ps = 50, attack = 45, defense = 40, special = 35, resistance = 35, speed = 56, secondaryType = Type(2), moves = [MOVE['quickattack'], MOVE['gust'], MOVE['sandattack'], MOVE['agility']]),
    'rattata' : NormalType(species = 'Rattata', ps = 30, attack = 56, defense = 35, special = 25, resistance = 35, speed = 72, secondaryType = Type(18), moves = [MOVE['bite'], MOVE['quickattack'], MOVE['tailwhip'], MOVE['doubleteam']]),
    'spearow' : NormalType(species = 'Spearow', ps = 40, attack = 60, defense = 30, special = 31, resistance = 31, speed = 70, secondaryType = Type(2), moves = [MOVE['tackle'], MOVE['peek'], MOVE['growl'], MOVE['glare']]),
}
