import os
import re

from marshmallow import fields, Schema

from apps.pc.exceptions import InvalidInputException

BULBA_URL = 'https://bulbapedia.bulbagarden.net/wiki/'
SPRITE_SHINY_URL = 'https://play.pokemonshowdown.com/sprites/xyani-shiny/'
SPRITE_CONVENTIONAL_URL = 'https://play.pokemonshowdown.com/sprites/xyani/'


class MoveSchema(Schema):
    move_type = fields.String()
    move_name = fields.String()


class MoveSetSchema(Schema):
    move_01 = fields.Nested(MoveSchema)
    move_02 = fields.Nested(MoveSchema)
    move_03 = fields.Nested(MoveSchema)
    move_04 = fields.Nested(MoveSchema)
    move_05 = fields.Nested(MoveSchema)
    move_06 = fields.Nested(MoveSchema)


class PcSchema(Schema):
    name = fields.String()
    gender = fields.String()
    specie_name = fields.String()
    specie_type = fields.String()
    ball_name = fields.String()
    item_name = fields.String()
    ability_name = fields.String()
    level = fields.Integer()
    bond = fields.Decimal()
    moves = fields.Nested(MoveSetSchema)
    description = fields.String()


class BaseInput:
    VALID_INPUTS = {''}
    DEFAULT_INPUT = ''

    def __init__(self, input=None, validate=False):
        self._input = input if input is not None else self.DEFAULT_INPUT
        if validate:
            self.validate()

    def validate(self):
        if self._input not in self.VALID_INPUTS:
            raise InvalidInputException(
                f'Input {self._input} not accepted. Allowed values are {self.VALID_INPUTS}'
            )

    @property
    def output(self):
        return self._input.title()

class Gender(BaseInput):
    VALID_INPUTS = {
        '⚲', '♀', '♂'
    }
    DEFAULT_INPUT = '⚲'


class Ball(BaseInput):
    VALID_INPUTS = {
        'Cherish Ball', 'Dive Ball', 'Dream Ball', 'Dusk Ball', 'Fast Ball', 'Friend Ball', 'Great Ball', 'Heal Ball',
        'Heavy Ball', 'Level Ball', 'Love Ball', 'Lure Ball', 'Luxury Ball', 'Moon Ball', 'Nest Ball', 'Net Ball',
        'Poke Ball', 'Quick Ball', 'Repeat Ball', 'Timer Ball', 'Ultra Ball'
    }
    DEFAULT_INPUT = 'Poke Ball'

    @property
    def link_output(self):
        formatted_input = self._input.replace(' ', '_').lower()
        return 'https://files.jcink.net/uploads/pokemonaudemus/Shop_Items/{}.png'.format(
            formatted_input
        )


class Item(BaseInput):
    VALID_INPUTS = {
        'Item', 'Air Balloon', 'Amulet Coin', 'Assault Vest', 'Big Root', 'Binding Band', 'Black Belt', 'Black Glasses',
        'Black Sludge', 'Bright Powder', 'Bug Memory', 'Charcoal', 'Choice Band', 'Choice Scarf', 'Choice Specs',
        'Cleanse Tag', 'Damp Rock', 'Dark Memory', 'Deep Sea Scale', 'Deep Sea Tooth', 'Destiny Knot', 'Dragon Fang',
        'Dragon Memory', 'Electric Memory', 'Everstone', 'Eviolite', 'Expert Belt', 'Fairy Memory', 'Fighting Memory',
        'Fire Memory', 'Flame Orb', 'Float Stone', 'Flying Memory', 'Focus Band', 'Focus Sash', 'Full Incense',
        'Ghost Memory', 'Go Goggles', 'Grass Memory', 'Green Scarf', 'Grip Claw', 'Ground Memory', 'Hard Stone',
        'Heat Rock', 'Ice Memory', 'Icy Rock', 'Iron Ball', 'Kings Rock', 'Lagging Tail', 'Lax Incense', 'Leftovers',
        'Life Orb', 'Light Ball', 'Light Clay', 'Lucky Egg', 'Lucky Punch', 'Macho Brace', 'Magnet', 'Metal Coat',
        'Metal Powder', 'Metronome', 'Miracle Seed', 'Muscle Band', 'Mystic Water', 'Never-Melt Ice', 'Odd Incense',
        'Pink Scarf', 'Poison Barb', 'Poison Memory', 'Protective Pads', 'Psychic Memory', 'Quick Claw', 'Razor Claw',
        'Razor Fang', 'Red Card', 'Red Scarf', 'Ring Target', 'Rock Incense', 'Rock Memory', 'Rocky Helmet',
        'Rose Incense', 'Safety Goggles', 'Scope Lens', 'Sea Incense', 'Sharp Beak', 'Shed Shell', 'Shell Bell',
        'Shiny Charm', 'Silk Scarf', 'Silver Powder', 'Smooth Rock', 'Snowball', 'Soft Sand', 'Soothe Bell',
        'Spell Tag', 'Steel Memory', 'Stick', 'Sticky Barb', 'Terrain Extender', 'Thick Club', 'Toxic Orb',
        'Twisted Spoon', 'Water Memory', 'Wave Incense', 'Wide Lens', 'Wise Glasses', 'Yellow Scarf', 'Zoom Lens'
    }
    DEFAULT_INPUT = 'Item'

    @property
    def link_output(self):
        if self._input == self.DEFAULT_INPUT:
            return ''
        formatted_input = self._input.replace(' ', '_').lower()
        return 'https://files.jcink.net/uploads/pokemonaudemus/Shop_Items/{}.png'.format(
            formatted_input
        )


class SpecieType(BaseInput):
    VALID_INPUTS = {
        'Type', 'Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass',
        'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water'
    }
    DEFAULT_INPUT = 'Type'

    @property
    def input(self):
        if self._input == 'Type':
            return ''
        return self._input

    @property
    def bkg_output(self):
        output_dict = {
            'Type': '#fff',
            'Bug': '#A8B820',
            'Dark': '#705848',
            'Dragon': '#7038F8',
            'Electric': '#F8D030',
            'Fairy': '#EE99AC',
            'Fighting': '#C03028',
            'Fire': '#F08030',
            'Flying': '#A890F0',
            'Ghost': '#705898',
            'Grass': '#78C850',
            'Ground': '#E0C068',
            'Ice': '#98D8D8',
            'Normal': '#A8A878',
            'Poison': '#A040A0',
            'Psychic': '#F85888',
            'Rock': '#B8A038',
            'Steel': '#B8B8D0',
            'Water': '#6890F0'
        }
        return output_dict[self._input]


class Shiny(BaseInput):
    VALID_INPUTS = {'True', 'False'}
    DEFAULT_INPUT = 'False'

    @property
    def output(self):
        return self._input == 'True'


class Specie(BaseInput):
    def __init__(self, input=None, specie_type=None, shiny=None):
        self._input = input if input is not None else self.DEFAULT_INPUT
        self.specie_type = specie_type if specie_type is not None else SpecieType()
        self.shiny = shiny if shiny is not None else Shiny()

    @property
    def link_output(self):
        if self._input == self.DEFAULT_INPUT:
            return ''
        unformatted_url = (
            'https://files.jcink.net/uploads/pokemonaudemus/pokemon/{}.gif' if self.shiny.output
            else 'https://files.jcink.net/uploads/pokemonaudemus/pokemon/shiny/{}.gif'
        )
        formatted_input = self._input.replace(' ', '_').lower()
        return unformatted_url.format(formatted_input)


class Move(BaseInput):
    def __init__(self, input=None, move_type=None):
        self._input = input if input is not None else self.DEFAULT_INPUT
        self.move_type = move_type if move_type is not None else SpecieType()

    def link_output(self):
        unformatted_url = 'https://bulbapedia.bulbagarden.net/wiki/{}_(move)'
        formatted_input = self.output.replace(' ', '_')
        return unformatted_url.format(formatted_input)


class Level(BaseInput):
    @property
    def output(self):
        try:
            return '{:.0f}'.format(int(self._input))
        except ValueError:
            return ''


class Bond(BaseInput):
    @property
    def output(self):
        try:
            return '{:.2f}'.format(float(self._input))
        except ValueError:
            return ''
