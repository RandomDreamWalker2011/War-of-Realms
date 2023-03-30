from time import sleep
from Error import *


def wait():
    sleep(1)


heroes_list = []


class Hero:
    permissions = "living"
    ATTACK_STATS = ["physical", "magic", "pure"]
    energy = 0
    decision = ""
    enemy_decision = ""

    def __init__(self, name, health, attack, level=1, base_attack_stat=0,
                 rank_2_skill_info: dict = False, rank_1_skill_info: dict = False, AI=False):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.level = level
        self.base_attack_stat = self.ATTACK_STATS[base_attack_stat]
        self.rank_2_skill_info = rank_2_skill_info
        self.rank_1_skill_info = rank_1_skill_info
        self.AI = AI
        self.shield = 0
        if self.max_health <= 0:
            raise InitError(f"Health/MaxHealth is 0 or less in Hero {name}", Hero)

    def __str__(self):
        return f"{self.name}, {self.permissions}, {self.health}"

    def base_attack(self, enemy, ally=None):
        if self.permissions == "dead":
            print(
                "PROBLEM HAS OCCURRED IN BATTLE.PY. PLEASE REPORT AS 'DEAD HERO TRIED TO ATTACK'")
            wait()
            return f"{self.name} tried to attack while dead."
        if enemy.permissions == "dead":
            print(f"Attacking failed. {enemy.name} is already dead!(SAY THE MESSAGE IN COMMENTS) ")
            wait()
            return f"{self.name} tried to attack a dead enemy."
        else:
            if enemy.shield > 0:
                enemy.shield -= self.attack
                if enemy.shield < 0:
                    print(f"{self.name} broke through {enemy.name}'s shield! {-enemy.shield} was dealt to {enemy.name}!")
                    enemy.health + enemy.shield
                    if enemy.health <= 0:
                        print(f"{enemy.name} was killed!")
                    enemy.shield = 0
                    enemy.permissions = "dead"
                    enemy.health = 0;
                    return
                elif enemy.shield == 0:
                    print(f"{self.name} managed to break {enemy.name}'s shield, but dealt no damage to {enemy.name}.")
                    return
                else:
                    print(f"{self.name} failed to break through {enemy.name}'s shield! {enemy.name}'s shield can "
                          f"still stand {enemy.shield} left.")
                    return


            if (enemy.health - self.attack) <= 0:
                print(f"{self.name} dealt {self.attack} {self.base_attack_stat} damage to {enemy.name}! \n \
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
                enemy.health = enemy.health - self.attack
                self.energy += 20
                return f"{self.name} dealt {self.attack} {self.base_attack_stat} damage to {enemy.name}. {enemy.name}'s health is {enemy.health} \n"

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
                                e.shield -= self.attack
                                if e.shield < 0:
                                    print(
                                        f"{self.name} broke through {e.name}'s shield! {-e.shield} was dealt to {e.name}!")
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
                            if (e.health - (self.attack + 500)) <= 0:
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
                                print(f"{a.name} got healed by {self.attack + 500}! {a.name}'s health is now at {a.health}")
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
                    enemy.shield -= (self.attack + 300)
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
                        print(f"{self.name} failed to break through {enemy.name}'s shield using the green skill {self.rank_2_skill_info['name']}! {enemy.name}'s shield can "
                              f"still stand {enemy.shield} left.")
                        return

                if (enemy.health - (self.attack + 300)) < 0:
                    print(
                        f"{self.name} used their green skill {self.rank_2_skill_info['name']} and dealt "
                        f"{(self.attack + 300) - enemy.health} damage to {enemy.name} \n"
                        f"{enemy.name} is dead.")
                    enemy.permissions = "dead"
                    enemy.health = 0
                else:
                    enemy.health -= (self.attack + 300)
                    print(
                        f"{self.name} used their green skill {self.rank_2_skill_info['name']} and dealt "
                        f"{self.attack + 300} damage to {enemy.name} \n"
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

    def reset(self):
        self.permissions = "living"
        self.health = self.max_health
        self.energy = 0


# testing_initerror = Hero("h", 0, 50)

DEBUG = False
if DEBUG:
    print("Handful of code")
