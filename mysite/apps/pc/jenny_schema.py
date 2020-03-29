from apps.pc.exceptions import InvalidInputException


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
    VALID_INPUTS = [
        '⚲', '♀', '♂'
    ]
    DEFAULT_INPUT = '⚲'


class Ball(BaseInput):
    VALID_INPUTS = [
        'Ball', 'Poke Ball', 'Cherish Ball', 'Dive Ball', 'Dream Ball', 'Dusk Ball', 'Fast Ball', 'Friend Ball', 'Great Ball',
        'Heal Ball', 'Heavy Ball', 'Level Ball', 'Love Ball', 'Lure Ball', 'Luxury Ball', 'Moon Ball', 'Nest Ball',
        'Net Ball', 'Quick Ball', 'Repeat Ball', 'Timer Ball', 'Ultra Ball'
    ]
    DEFAULT_INPUT = 'Ball'

    @property
    def link_output(self):
        formatted_input = self._input.replace(' ', '_').lower()
        return (
            '' if self._input == self.DEFAULT_INPUT
            else 'https://files.jcink.net/uploads/pokemonaudemus/Shop_Items/{}.png'.format(
                formatted_input
            )
        )


class Item(BaseInput):
    VALID_INPUTS = [
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
    ]
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
    VALID_INPUTS = [
        'Type', 'Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass',
        'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water'
    ]
    DEFAULT_INPUT = 'Type'

    @property
    def input(self):
        return (
            '' if self._input == self.DEFAULT_INPUT
            else self._input
        )

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
    VALID_INPUTS = ['False', 'True']
    DEFAULT_INPUT = 'False'

    @property
    def output(self):
        return self._input == 'True'


class Form(BaseInput):
    VALID_INPUTS = [
        'Form', 'Alola', 'Archipelago', 'Blade', 'Blue', 'Blue Striped', 'Bug', 'Busted', 'Continental', 'Dandy',
        'Dark', 'Debutante', 'Diamond', 'Dragon', 'Dusk', 'East', 'Electric', 'Elegant', 'Fairy', 'Fall', 'Fan',
        'Fancy', 'Female', 'Fighting', 'Fire', 'Flying', 'Frost', 'Galar', 'Galar Zen', 'Garden', 'Ghost', 'Grass',
        'Green', 'Ground', 'Heart', 'Heat', 'High Plains', 'Ice', 'Icy Snow', 'Indigo', 'Jungle', 'Kabuki', 'La Reine',
        'Large', 'Low Key', 'Marine', 'Matron', 'Meadow', 'Meteor', 'Midnight', 'Modern', 'Monsoon', 'Mow', 'Ocean',
        'Orange', 'Pau', 'Pharaoh', 'Poison', 'Pokeball', 'Polar', 'Pompom', 'Psychic', 'Rainy', 'Red', 'River',
        'Rock', 'Sandstorm', 'Sandy', 'Savanna', 'School', 'Sensu', 'Small', 'Snowy', 'Star', 'Steel', 'Summer', 'Sun',
        'Sunny', 'Sunshine', 'Super', 'Trash', 'Tundra', 'Violet', 'Wash', 'Water', 'White', 'Winter', 'Yellow', 'Zen'
    ]
    DEFAULT_INPUT = 'Form'

    @property
    def output(self):
        return self._input != self.DEFAULT_INPUT


class Specie(BaseInput):
    def __init__(self, input=None, specie_type_1=None, specie_type_2=None, shiny=None, specie_form=None):
        self._input = input if input is not None else self.DEFAULT_INPUT
        self.specie_type_1 = specie_type_1 if specie_type_1 is not None else SpecieType()
        self.specie_type_2 = specie_type_2 if specie_type_2 is not None else SpecieType()
        self.shiny = shiny if shiny is not None else Shiny()
        self.specie_form = specie_form if specie_form is not None else Form()

    @property
    def link_output(self):
        if self._input == self.DEFAULT_INPUT:
            return ''
        unformatted_url = (
            'https://files.jcink.net/uploads/pokemonaudemus/pokemon/{}.gif' if not self.shiny.output
            else 'https://files.jcink.net/uploads/pokemonaudemus/pokemon/shiny/{}.gif'
        )
        formatted_input = self._input.replace(' ', '_').lower()
        if self.specie_form.output:
            formatted_input = '{}_{}'.format(
                formatted_input,
                'f' if self.specie_form._input == 'Female'
                else self.specie_form._input.replace(' ', '_').lower()
            )
        return unformatted_url.format(formatted_input)

    @property
    def specie_type(self):
        if self.specie_type_1._input == SpecieType.DEFAULT_INPUT:
            return ''
        elif self.specie_type_2._input == SpecieType.DEFAULT_INPUT:
            return ' :{}: '.format(self.specie_type_1._input.lower())
        else:
            return ' :{}: / :{}: '.format(
                self.specie_type_1._input.lower(),
                self.specie_type_2._input.lower()
            )


class Move(BaseInput):
    def __init__(self, input=None, move_type=None):
        self._input = input if input is not None else self.DEFAULT_INPUT
        self.move_type = move_type if move_type is not None else SpecieType()

    @property
    def link_output(self):
        unformatted_url = 'https://bulbapedia.bulbagarden.net/wiki/{}_(move)'
        formatted_input = self.output.replace(' ', '_')
        return unformatted_url.format(formatted_input)


class Ability(BaseInput):
    @property
    def link_output(self):
        unformatted_url = 'https://bulbapedia.bulbagarden.net/wiki/{}_(Ability)'
        formatted_input = self.output.replace(' ', '_')
        return unformatted_url.format(formatted_input)


class Bond(BaseInput):
    @property
    def output(self):
        try:
            return '{:.0f} %'.format(float(self._input))
        except ValueError:
            return ''
