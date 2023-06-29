from time import sleep
from Error import *


def wait():
    sleep(1)


heroes_list = []


class Hero:
    """
        For Battles and Characters the Player Controls
    """

    permissions = "living"
    ATTACK_STATS = ["demonic", "magic", "pure", "elemental", "normal"]
    # Different Attack Stats for shields and crits.
    energy = 0
    decision = ""
    enemy_decision = ""
    crit_chance = 10
    status = {}

    def __init__(self, name, health, attack, defense, element=None, level=1, base_attack_stat="normal",
                 rank_3_skill_info: dict = False,
                 rank_2_skill_info: dict = False,
                 rank_1_skill_info: dict = False,
                 AI=False):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.base_attack_stat = base_attack_stat
        self.rank_2_skill_info = rank_2_skill_info
        self.rank_1_skill_info = rank_1_skill_info
        self.AI = AI
        self.shield = 0
        self.exp = 0
        self.limit = 50
        self.element = element
        if self.max_health <= 0:
            raise InitError(f"Health/MaxHealth is 0 or less in Hero {name}", Hero)
        if self.base_attack_stat not in self.ATTACK_STATS:
            raise InitError(f"Base Attack Stat isn' t one of the five. ", Hero)

    def __str__(self):
        return f"{self.name}, {self.permissions}, {self.health}"

    def get_duration(self):
        pass

    def damage_calculator(self, enemy, damage = None):
        # Apply defense reduction to attack
        if damage is not None:
            modified_attack = self.attack - (enemy.defense / 10)
        else:
            modified_attack = damage - enemy.defense / 10
        # Basic damage formula with level suppression
        base_damage = modified_attack

        # Level Difference Calculator
        level_difference = self.level - enemy.level

        if level_difference > 0:
            level_suppression = 0.40 * (0.75 ** (level_difference - 1))
        elif level_difference < 0:
            level_suppression = 1.6 * (1.25 ** abs(level_difference))
        else:
            level_suppression = 1.0  # No level difference, full damage

        suppressed_damage = base_damage * level_suppression
        damage = max(0, suppressed_damage)
        return round(damage)  # Round the damage to two decimal places

    @classmethod
    def damage_calculator(cls, hero, enemy, damage = None):
        # Apply defense reduction to attack
        if damage is not None:
            modified_attack = hero.attack - (enemy.defense / 10)
        else:
            modified_attack = damage - enemy.defense / 10
        # Basic damage formula with level suppression
        base_damage = modified_attack

        # Level Difference Calculator
        level_difference = hero.level - enemy.level

        if level_difference > 0:
            level_suppression = 0.40 * (0.75 ** (level_difference - 1))
        elif level_difference < 0:
            level_suppression = 1.6 * (1.25 ** abs(level_difference))
        else:
            level_suppression = 1.0  # No level difference, full damage

        suppressed_damage = base_damage * level_suppression
        damage = max(0, suppressed_damage)
        return round(damage)  # Round the damage to two decimal places

    def breakthrough(self):
        pass

    def base_attack(self, enemy, ally=None):
        if self.permissions == "dead":
            print(
                "PROBLEM HAS OCCURRED IN BATTLE.PY. ")
            wait()
            return f"{self.name} tried to attack while dead."
        if enemy.permissions == "dead":
            print(f"Attacking failed. {enemy.name} is already dead!")
            wait()
            return f"{self.name} tried to attack a dead enemy."
        else:
            if enemy.shield > 0:
                enemy.shield -= self.damage_calculator(enemy)
                if enemy.shield < 0:
                    print(
                        f"{self.name} broke through {enemy.name}'s shield! {-enemy.shield - enemy.defense} was dealt to {enemy.name}!")
                    if enemy.health <= 0:
                        print(f"{enemy.name} was killed!")
                    enemy.shield = 0
                    enemy.permissions = "dead"
                    enemy.health = 0
                    return
                elif enemy.shield == 0:
                    print(f"{self.name} managed to break {enemy.name}'s shield, but dealt no damage to {enemy.name}.")
                    return
                else:
                    print(f"{self.name} failed to break through {enemy.name}'s shield! {enemy.name}'s shield can "
                          f"still stand {enemy.shield} left.")
                    return

            if (enemy.health - self.damage_calculator(enemy, self.attack)) <= 0:
                print(f"{self.name} dealt {self.damage_calculator(enemy, damage = self.attack)} {self.base_attack_stat} damage to {enemy.name}! \n \
{enemy.name} is dead!")
                self.energy += 25
                enemy.permissions = "dead"
                enemy.health = 0
                wait()
                return f'{self.name} dealt {self.attack} {self.base_attack_stat} damage to {enemy.name}. {enemy.name} is dead. \n'
            else:
                print(f"{self.name} dealt {self.attack} {self.base_attack_stat} damage to {enemy.name}! \n \
{enemy.name} only has {enemy.health - self.attack} health left!")
                wait()
                enemy.health = enemy.health - self.damage_calculator(enemy, damage = self.attack)
                self.energy += 20
                return f"{self.name} dealt {self.damage_calculator(enemy, damage = self.attack)} {self.base_attack_stat} damage to {enemy.name}. {enemy.name}'s health is {enemy.health} \n"

    def rank_1_skill(self, enemies=None, allies=None, enemy=None, ally=None):
        if self.permissions == "dead":
            print(f"Stop it.")
            return None
        if not self.rank_1_skill_info:
            print(f"{self.name} doesn't have a Gray Skill Implemented Yet")
            return None
        if self.energy >= 150:
            self.energy -= 150
            if self.rank_1_skill_info["type"] == "all damage":
                print(f"{self.name} used their rank 1 skill {self.rank_1_skill_info['name']} on the enemies!")
                if enemies is not None:
                    for e in enemies:
                        if e.permissions != "dead":
                            if e.shield > 0:
                                e.shield -= self.damage_calculator(e, damage = (self.attack + 500))
                                if e.shield < 0:
                                    print(
                                        f"{self.name} broke through {e.name}'s shield! {-e.shield} was dealt to {e.name}!")
                                    e.health -= self.damage_calculator(e, damage = (-e.shield))
                                    if e.health <= 0:
                                        print(f"{e.name} is dead!")
                                        e.shield = 0
                                        e.permissions = "dead"
                                        e.health = 0
                                    e.shield = 0
                                    continue
                                elif e.shield == 0:
                                    print(
                                        f"{self.name} managed to break {e.name}'s shield, but dealt no damage to {e.name}.")
                                    continue
                                else:
                                    print(
                                        f"{self.name} failed to break through {e.name}'s shield! {e.name}'s shield can "
                                        f"still stand {e.shield} left.")
                                    continue
                            if (e.health - self.damage_calculator(self.attack + 500)) <= 0:
                                print(f"{e.name} is dead.")
                                e.health = 0
                                e.permissions = "dead"
                            else:
                                e.health -= (self.attack + 500)
                                print(
                                    f"{e.name} lost {self.attack + 500} and only has {e.health} health left.")
                        else:
                            continue
                else:
                    raise InputNotFoundError(f"Enemies not found in rank 1 skill of Hero {self.name}")
            elif self.rank_1_skill_info["type"] == "all heal":
                print(f"{self.name} used their gray skill {self.rank_1_skill_info['name']} on the allies!")
                if allies is not None:
                    for a in allies:
                        if a.permissions != "dead":
                            if (a.health + (self.attack + 500)) >= a.max_health:
                                if a.health == a.max_health:
                                    print(f"{a.name} is already at max health!")
                                if a.health > a.max_health:
                                    print("ERROR: ABOVE MAX HEALTH")
                                print(
                                    f"{a.name} got healed by {self.health + self.attack + 500 - a.max_health}! {a.name} is now at "
                                    "max health.")
                                a.health = a.max_health
                            else:
                                a.health += (self.attack + 500)
                                print(
                                    f"{a.name} got healed by {self.attack + 500}! {a.name}'s health is now at {a.health}")
                else:
                    raise InputNotFoundError(f"Allies not found in rank 1 skill of Hero {self.name}")
            else:
                print("Rank 1 Skill Type Not Found")
        else:
            return "'Energy level not high enough.' (ERROR)"

    def rank_2_skill(self, enemy=None):
        if self.permissions == "dead":
            print(f"Stop it.")
            return None
        if not self.rank_2_skill_info:
            print(f"{self.name} doesn't have a Green Skill Implemented Yet")
            return None

        if self.energy >= 20:
            self.energy -= 20
            if self.rank_2_skill_info['type'] == "sing. damage":
                if enemy.shield > 0:
                    enemy.shield -= self.damage_calculator(enemy, damage = self.attack + 300)
                    if enemy.shield < 0:
                        print(
                            f"{self.name} broke through {enemy.name}'s shield using the green skill {self.rank_2_skill_info['name']}! {-enemy.shield} was dealt to {enemy.name}!")
                        enemy.shield = 0
                        return
                    elif enemy.shield == 0:
                        print(
                            f"{self.name} managed to break {enemy.name}'s shield using the green skill {self.rank_2_skill_info['name']}, but dealt no damage to {enemy.name}.")
                        return
                    else:
                        print(
                            f"{self.name} failed to break through {enemy.name}'s shield using the green skill {self.rank_2_skill_info['name']}! {enemy.name}'s shield can "
                            f"still stand {enemy.shield} left.")
                        return

                if (enemy.health - self.damage_calculator(enemy, damage = self.attack + 300)) < 0:
                    print(
                        f"{self.name} used their green skill {self.rank_2_skill_info['name']} and dealt "
                        f"{self.damage_calculator(enemy, damage = self.attack + 300) - enemy.health} damage to {enemy.name} \n"
                        f"{enemy.name} is dead.")
                    enemy.permissions = "dead"
                    enemy.health = 0
                else:
                    enemy.health -= self.damage_calculator(self.attack + 300)
                    print(
                        f"{self.name} used their green skill {self.rank_2_skill_info['name']} and dealt "
                        f"{self.damage_calculator(enemy, damage = self.attack + 300)} damage to {enemy.name} \n"
                        f"{enemy.name} only has {enemy.health} health left.")
            if self.rank_2_skill_info['type'] == "self heal":
                if (self.health + 350) > self.max_health:
                    if self.health >= self.max_health:
                        print("You are already at max health! (ERROR)")
                        return
                    else:
                        print(
                            f"{self.name} used their green skill {self.rank_2_skill_info['name']} and healed themselves by "
                            f"{(self.health + 350) - self.max_health}. \n"
                            f"{self.name}'s health is now at {self.max_health}!")
                        self.health = self.max_health
                else:
                    self.health += 350
                    print(f"{self.name} used their green skill {self.rank_2_skill_info['name']} and healed by 350!" +
                          f"{self.name}'s health is now at {self.health}")
            if self.rank_2_skill_info['type'] == "self shield":
                self.shield += (300 + self.attack)
                print(
                    f"{self.name} used their rank 2 skill {self.rank_2_skill_info['name']} and cast a shield around themselves! Their shield can stand {self.shield} damage!")
        else:
            print(f"{self.name} Does Not Enough Energy")

    def rank_3_skill(self, target=None, is_in_battle = False):
        if self.rank_3_skill_info == False:
            print(f"Rank 3 Skill Info UNDEFINED for {self.name}")
            return None
        else:
            if is_in_battle is False:
                print("OWO what are you doing here? \n How did you evoke this?!? ERROR: NOT IN BATTLE?!?")
            elif is_in_battle is True:
                if self.rank_3_skill_info["type"] == "poison":
                    if target.permissions != "living":
                        print(f"Error: attacked dead enemy uwu")
                        return
                    else:
                        self.status["poison"] = [self.level + 1, self.get_duration()]
                        print(f"{self.name} attacked {target.name}! \n {target.name} is poisoned!")
                        return
                if self.rank_3_skill_info["type"] == "self regen.":
                    if target.permissions != "living":
                        print(f"Error: tried to cast regeneration on a dead ally uwu")
                        return
                    else:
                        self.status
            else:
                print("How did you get here?!?!?!?!? \n"
                      "ERROR! ERROR! "
                      "\nHUGE ERROR! NOT IN BATTLE AND NOT NOT IN THE BATTLE! (what did I set this to lol)")
                # Ridiculously simple


    def rank_4_skill(self):
        pass

    def special_passive(self, in_battle=False):
        pass

    def reset(self):
        self.permissions = "living"
        self.health = self.max_health
        self.energy = 0
        self.status = []


class Monster(Hero):
    pass


DEBUG = False
if DEBUG:
    print("Handful of code")
