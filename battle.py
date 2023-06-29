"""
    Main Battle System
"""

from time import sleep

from AI import AI
from Error import *
from heros import *

DEBUG = True  # Don't mess with this
if DEBUG:
    Hero1 = Hero("Froggy", 1000, 250, 100, level=1, base_attack_stat="normal",
                 rank_2_skill_info={"name": "Whirlpool", "type": "sing. damage"},
                 rank_1_skill_info={"name": "Up and Away", "type": "all heal"})

    Hero2 = Hero("Sludge", 1000, 250, 100, level=1, base_attack_stat="magic",
                 rank_2_skill_info={"name": "Air Bound", "type": "self shield"},
                 rank_1_skill_info={"name": "Shatter", "type": "all damage"})
    Hero3 = Hero("A1", 1500, 350, 100, level=1,
                 rank_2_skill_info={"name": "Downfall", "type": "self heal"},
                 rank_1_skill_info={"name": "Broken Heart", "type": "all heal"})
    Hero4 = Hero("Dars", 1000, 150, 100, level=1, base_attack_stat="magic",
                 rank_2_skill_info={"name": "Flower of the Earth", "type": "sing. damage"},
                 rank_1_skill_info={"name": "Fallen", "type": "all damage"})

    Hero1.energy += 10000
    Hero2.energy += 10000
    enemy1 = Hero("asdf", 10, 200, 100, level=1, rank_2_skill_info={"name": "Downfall", "type": "damage"})

    enemy2 = Hero("ddge", 10, 150, 100, level=1, base_attack_stat="normal",
                  rank_2_skill_info={"name": "Flower of the Earth", "type": "self heal"})
    enemy3 = Hero("sge", 50, 150, 100, level=1, base_attack_stat="magic",
                  rank_2_skill_info={"name": "Flower of the Earth", "type": "self heal"})
    h = [Hero1, Hero2, Hero3, Hero4]
    e = [enemy1, enemy2, enemy3]
    e1 = [enemy1]
    e2 = [enemy2]
    e3 = [enemy3]


def battle_over_class(hero_list, enemy_list):
    if all(hero.permissions == "dead" for hero in hero_list):
        return 1
    elif all(enemy.permissions == "dead" for enemy in enemy_list):
        return 1
    else:
        return 0


def full_battle_over_check(enemy_list, heros, battle_round=None, round_max=None):
    t = []
    for li in enemy_list:
        if all(enemy.permissions == "dead" for enemy in enemy_list):
            t.append(True)
        else:
            t.append(False)
    if battle_round is None:
        if all(t):
            print("You won!")
            sleep(1)
            for hero in heros:
                hero.exp += 100
                print(f"{hero.name} got 100 exp!")
                sleep(0.5)
                while True:
                    if hero.exp >= hero.limit:
                        hero.level += 1
                        hero.exp -= hero.limit
                        hero.limit = round(hero.limit * 1.75)
                        sleep(0.5)
                        print(f"{hero.name} leveled up to level {hero.level}! {hero.exp} left!")
                    else:
                        break
        else:
            print("You lose.")
    else:
        if round_max is None:
            print("ERROR: ROUND MAX NOT DEFINED")
            return
        if all(t):
            print(f"You won round {battle_round}!")
            sleep(0.5)
            if battle_round < round_max:
                print(f"{round_max - battle_round} round(s) left.")
                return 1
            elif battle_round <= 0 or battle_round > round_max:
                raise InvalidInputError("Round Number Invalid")
            elif battle_round == round_max:
                print("You Win!")
                sleep(1)
                for hero in heros:
                    hero.exp += 100
                    print(f"{hero.name} got 100 exp!")
                    sleep(0.5)
                    while True:
                        if hero.exp >= hero.limit:
                            hero.level += 1
                            hero.exp -= hero.limit
                            hero.limit = round(hero.limit * 1.75)
                            sleep(0.5)
                            print(f"{hero.name} leveled up to level {hero.level}! {hero.exp} left!")
                        else:
                            break
        else:
            print("You lose.")


class Battle:
    def __init__(self, watchers, enemies, round=False, round_max=None):
        self.watchers = watchers
        self.enemies = enemies
        self.round = round
        self.round_max = round_max
        if isinstance(self.watchers, list) and len(self.watchers) == 0:
            raise InitError("Watcher List Empty", Battle)
        if isinstance(self.enemies, list) and len(self.enemies) == 0:
            raise InitError("Enemy List Empty", Battle)

    def list_check(self):
        # Checks if all lists are made of singular and elements from the class Hero. If not, print Error
        for item in self.watchers:
            type_ = type(item)
            if type_ != "<class 'heros.Hero'>":
                if type_ == "<class 'list'>":
                    for i in item:
                        self.list_check(item)
                else:
                    raise TypeError("List Check Function Failed")
            else:
                continue

    def battle(self):
        over = 0
        MAIN_AI = AI(self.watchers, self.watchers[1], self.enemies)

        for e in self.enemies:
            if e.AI:
                print(f"{e.name} is not AI, but is in ENEMY (Error)")

        # Making Sure that All Lists are not over 5
        if len(self.watchers) > 5:
            print("Go to feedback and report \"Battle Failed\"")

        while over == 0:
            for hero in self.watchers:
                if hero.health <= 0:
                    continue
                else:
                    hero.decision = ""
                    hero.enemy_decision: str = ""
                    while hero.decision == "":
                        print(f"Choose one action for {hero.name}:")
                        sleep(0.5)
                        print("(1): Base Attack")
                        sleep(0.5)
                        print("(2): Rank 2 Skill")
                        sleep(0.5)
                        print("(3): Rank 1 Skill")
                        sleep(0.5)
                        print("(4): Pass")
                        sleep(0.5)
                        hero.decision = input("Choose: ")
                        if hero.decision == "1":
                            print("Which Enemy Are You Going To Attack?")
                            sleep(0.1)
                            for index, enemy in enumerate(self.enemies, start=1):
                                if enemy.health > 0:
                                    sleep(0.5)
                                    if enemy.shield > 0:
                                        print(f"({index}): {enemy.name} [SHIELDED]")
                                    else:
                                        print(f"({index}): {enemy.name}")
                                else:
                                    continue
                            hero.enemy_decision = input("Choice: ")
                            moved = 0
                            while moved == 0:
                                if hero.enemy_decision.isdigit() and int(hero.enemy_decision) <= len(
                                        self.enemies) and not self.enemies[int(hero.enemy_decision) - 1].health <= 0:
                                    hero.base_attack(self.enemies[int(hero.enemy_decision) - 1])
                                    moved += 1
                                else:
                                    hero.enemy_decision = ""
                                    print("Retry. Unknown String Typed")
                                    hero.enemy_decision = input("Choice: ")
                                    sleep(1)
                                    continue

                            # Green Skill
                        elif hero.decision == "2":
                            type = hero.rank_2_skill_info["type"]
                            if hero.energy >= 20:
                                if type == "sing. damage":
                                    for index, enemy in enumerate(self.enemies, start=1):
                                        if enemy.health > 0:
                                            sleep(0.5)
                                            if enemy.shield > 0:
                                                print(f"({index}): {enemy.name} [SHIELDED]")
                                            else:
                                                print(f"({index}): {enemy.name}")
                                        else:
                                            continue
                                    hero.enemy_decision = input("Choose: ")
                                    moved = 0
                                    while moved == 0:
                                        if hero.enemy_decision.isdigit() and int(hero.enemy_decision) <= len(
                                                self.enemies) and not self.enemies[
                                                                          int(hero.enemy_decision) - 1].health <= 0:
                                            hero.rank_2_skill(self.enemies[int(hero.enemy_decision) - 1])
                                            moved += 1
                                        else:
                                            hero.enemy_decision = ""
                                            hero.enemy_decision = input("Choice: ")
                                            sleep(1)

                                elif type == "self heal":
                                    if hero.health != hero.max_health:
                                        print("Locked. You are already at max health!")
                                        hero.decision = ""
                                        hero.enemy_decision = ""
                                        continue
                                    else:
                                        hero.rank_2_skill()
                                        hero.decision = ""
                                        hero.enemy_decision = ""
                                        continue

                                elif type == "self shield":
                                    hero.rank_2_skill()
                            else:
                                hero.decision = ""
                                print("Not enough energy.")
                        elif hero.decision == "3":
                            if hero.energy >= 150:
                                hero.rank_1_skill(enemies=self.enemies, allies=self.watchers)
                            else:
                                hero.decision = ""
                                hero.enemy_decision = ""
                                print("Energy level not high enough")
                        elif hero.decision == "4":
                            print("Passing to the next hero. . .")
                            hero.energy += 30
                            sleep(1)
                            break
                        else:
                            hero.decision = ""
                            print("Try again")
                    hero.enemy_decision = ""
                    hero.decision = ""
                    print("Action Done")
                print("leaving current loop. . .")
                i = battle_over_class(self.watchers, self.enemies)
                over += i
                if over != 0:
                    break
            for enemy in self.enemies:
                if enemy.health <= 0:
                    continue
                else:
                    MAIN_AI.hero = enemy
                    MAIN_AI.decide()
                    over = battle_over_class(self.watchers, self.enemies)
        result = full_battle_over_check(self.enemies, self.watchers, self.round, self.round_max)
        if isinstance(result, int):
            self.round += full_battle_over_check(self.enemies, self.watchers, self.round, self.round_max)
        else:
            return 1
        print("hi")

    def reset(self):
        for hero in self.watchers:
            hero.reset()
        for enemy in self.enemies:
            enemy.reset()


def standard_battle(heros, enemy_set1, enemy_set2, enemy_set3):
    battle = Battle(heros, enemy_set1, round=1, round_max=3)
    battle.battle()
    battle.enemies = enemy_set2
    battle.battle()
    battle.enemies = enemy_set3
    battle.battle()
    battle.reset()


def sing_round_battle(heros, enemies):
    battle = Battle(heros, enemies)
    battle.battle()
    battle.reset()


if __name__ == "__main__":
    stuff = 2
    if stuff == 1:
        sing_round_battle(h, e)
    elif stuff == 2:
        standard_battle(h, e1, e2, e3)

 # standard_battle(h, e1, e2, e3)
