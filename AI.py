from heros import Hero
from random import choice


class AI:
    healers = []
    least_energy = []
    least_health = []
    most_energy = []
    most_health = []

    def __init__(self, enemies, watcher, allies):
        self.enemies = enemies
        self.allies = allies
        self.hero = watcher

    def get_healers(self):
        self.healers = [enemy for enemy in self.enemies if enemy.rank_2_skill_info['type'] == "self heal"]

    def get_energy(self):
        if len(self.enemies) >= 3:
            self.least_energy = sorted(self.enemies, key=lambda x: x.energy)[:2]
            self.most_energy = sorted(self.enemies, key=lambda x: x.energy)[2:]
        else:
            self.least_energy = self.enemies
            self.most_energy = self.enemies

    def get_health(self):
        self.least_health = sorted(self.enemies, key=lambda x: x.health)[:3]
        self.most_health = sorted(self.enemies, key=lambda x: x.health)[3:]

    def reset(self):
        self.healers = []
        self.least_energy = []
        self.least_health = []
        self.most_energy = []
        self.most_health = []

    def decide(self):
        targets = {}
        allied = []
        self.get_health()
        self.get_energy()
        self.get_healers()

        for enemy in self.enemies:
            if (enemy.health < self.hero.attack) and (enemy in self.least_health):
                targets[enemy] = "ONE SHOT"
            elif (enemy in self.healers) and (enemy in self.least_energy):
                targets[enemy] = "UNABLE TO HEAL"
            elif (enemy in self.healers) and (enemy in self.least_energy) and (
                    enemy.health < self.hero.attack) and (
                    enemy in self.least_health):
                targets[enemy] = "KILL"
        if (self.hero.energy >= 150) and (self.hero.rank_1_skill_info["type"] == "all damage"):
            # get all enemies that can be killed using rank_1_skill
            targets.update({e: "KILL" for e in self.enemies if e.health <= (self.hero.attack + 500)})
            if targets:
                # use rank_1_skill on all enemies
                self.hero.rank_1_skill(enemies=self.enemies)
                return
        if (self.hero.energy >= 150) and (self.hero.rank_1_skill_info["type"] == "all heal"):
            for a in self.allies:
                if a.health - choice(self.enemies).attack:
                    allied.append(1)
            if len(allied) >= (len(self.allies) -2):
                self.hero.rank_1_skill(allies = self.allied)
                return
        if targets == {}:
            target = choice(self.enemies)
            if self.hero.energy >= 20 and "sing. damage" == self.hero.rank_1_skill_info[
                "type"] and self.hero.rank_2_skill_info is not None:
                self.hero.rank_2_skill(target)
            else:
                self.hero.base_atack(target)
            return
        else:
            if self.hero.health < choice(self.enemies).attack and self.hero.rank_2_skill_info["type"] == "self heal":
                self.hero.rank_2_skill(choice(list(targets.keys())))
                return
            else:
                kills_that_can_getaway = []
                for target, reason in targets.items():
                    if reason == "KILL":
                        kills_that_can_getaway.append(target)

                try:
                    target = choice(kills_that_can_getaway)
                except IndexError:
                    print("")
                self.hero.base_attack(target)

        self.reset()
