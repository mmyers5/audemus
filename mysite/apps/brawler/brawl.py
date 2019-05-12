import random

from apps.brawler.info import DefenseType, Move, Specie


class Brawl:
    def __init__(self, attacker, attacker_level, attack,
                 defender, defender_level):
        self.attacker = Specie(attacker, attacker_level)
        self.defender = Specie(defender, defender_level)
        self.attack = Move(attack)

    @property
    def damage_dealt(self):
        return int(
            self.base_damage
            * self.random_modifier
            * self.stab_modifier
            * self.type_modifier
        )

    @property
    def effective_defense(self):
        effective_stats = {
            'special': 'special-defense',
            'physical': 'defense'
        }
        effective_stat = effective_stats[self.attack.damage_class]
        return self.defender.leveled_stats[effective_stat]

    @property
    def effective_attack(self):
        effective_stats = {
            'special': 'special-attack',
            'physical': 'attack'
        }
        effective_stat = effective_stats[self.attack.damage_class]
        return self.attacker.leveled_stats[effective_stat]

    @property
    def type_modifier(self):
        modifier = 1.
        modifiers = {
            'double_damage_from': 2.,
            'half_damage_from': 1/2.,
            'no_damage_from': 0.
        }
        attack_type = self.attack.attack_type
        defense_types = self.defender.types
        for m in modifiers:
            for t in defense_types:
                defense_type = DefenseType(t)
                if attack_type in getattr(defense_type, m):
                    modifier *= modifiers[m]
        return modifier

    @property
    def base_damage(self):
        return (
            (
                (
                    (
                        (
                            (2. * self.attacker.level)
                            / 5.
                        )
                        + 2
                    )
                    * self.attack.power
                    * (
                        self.effective_attack
                        / self.effective_defense
                    )
                )
                / 50
            )
            + 2
        )

    @property
    def random_modifier(self):
        return 0.85
        return random.uniform(0.85, 1.00)

    @property
    def stab_modifier(self):
        modifier = 1
        if self.attack.attack_type in self.attacker.types:
            modifier *= 1.5
        return modifier

    @property
    def printout(self):
        return '\n'.join([
            'Attacker Type(s): {attacker_types}'.format(
                attacker_types=', '.join(self.attacker.types)
            ),
            'Defender Type(s): {defender_types}'.format(
                defender_types=', '.join(self.defender.types)
            ),
            'Attack Type: {attack_type}'.format(
                attack_type=self.attack.attack_type
            ),
            'Pct Damage Dealt: {pct:.2f}%'.format(
                pct=self.damage_dealt/self.defender.hp
            )
        ])
