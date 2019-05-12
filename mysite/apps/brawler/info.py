import os
import requests

from apps.brawler import utils

IV = 31


class DefenseType:
    def __init__(self, name):
        self.name = name
        self.uri = os.path.join(
            utils.API_URI, utils.TYPE_ENDPOINT,
            self.name
        )
        self.raw_data = requests.get(self.uri).json()

    @property
    def double_damage_from(self):
        return [
            t['name'] for t in
            self.raw_data['damage_relations']['double_damage_from']
        ]

    @property
    def half_damage_from(self):
        return [
            t['name'] for t in
            self.raw_data['damage_relations']['half_damage_from']
        ]

    @property
    def no_damage_from(self):
        return [
            t['name'] for t in
            self.raw_data['damage_relations']['no_damage_from']
        ]


class Move:
    def __init__(self, name):
        self.name = name
        self.uri = os.path.join(
            utils.API_URI, utils.MOVE_ENDPOINT,
            self.name
        )
        self.raw_data = requests.get(self.uri).json()

    @property
    def accuracy(self):
        return self.raw_data['accuracy']

    @property
    def power(self):
        return self.raw_data['power']

    @property
    def attack_type(self):
        return self.raw_data['type']['name']

    @property
    def damage_class(self):
        return self.raw_data['damage_class']['name']


class Specie:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.uri = os.path.join(
            utils.API_URI, utils.PKMN_ENDPOINT,
            self.name
        )
        self.raw_data = requests.get(self.uri).json()

    @property
    def base_stats(self):
        raw_stats = self.raw_data['stats']
        return {
            r['stat']['name']: r['base_stat'] for r in raw_stats[::-1]
        }

    @property
    def leveled_stats(self):
        return {
            s: self.leveled_stat(s) for s in self.base_stats
        }

    @property
    def types(self):
        return [
            t['type']['name'] for t in self.raw_data['types']
        ]

    @property
    def hp(self):
        base = self.base_stats['hp']
        return (
            (
                (
                    (
                        (2 * base ) + IV
                    )
                    * self.level
                )
            / 100.
            )
            + self.level + 10
        )

    def leveled_stat(self, stat_name):
        if stat_name == 'hp':
            return self.hp
        base = self.base_stats[stat_name]
        return (
            (
                (
                    (
                        (2 * base ) + IV
                    )
                    * self.level
                )
            / 100.
            )
            + 5
        )
