from flask import Flask, request, render_template

import apps.pc.jenny_schema as jenny_schema

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return 'Sup, bitch.'


@app.route('/pc', methods=['GET', 'POST'])
def pc_jenny():
    FORM_FIELDS = {
        'specie', 'specie_type', 'shiny', 'gender', 'ball_name', 'name', 'item_name', 'level', 'bond', 'ability'
    }
    FORM_FIELDS.update({'move_name_0{}'.format(n + 1) for n in range(6)})
    FORM_FIELDS.update({'move_type_0{}'.format(n + 1) for n in range(6)})

    def parse_pc_form(raw_form):
        form = {
            **{f: None for f in FORM_FIELDS},
            **{'description': ''},
            **raw_form
        }
        return {
            'specie': jenny_schema.Specie(
                input=form['specie'],
                specie_type=jenny_schema.SpecieType(input=form['specie_type']),
                shiny=jenny_schema.Shiny(input=form['shiny'])
            ),
            'gender': jenny_schema.Gender(input=form['gender']),
            'ball': jenny_schema.Ball(input=form['ball_name']),
            'name': jenny_schema.BaseInput(input=form['name']),
            'moves': {
                n + 1: jenny_schema.Move(
                    input=form['move_name_0{}'.format(n + 1)],
                    move_type=jenny_schema.SpecieType(
                        input=form['move_type_0{}'.format(n + 1)],
                        validate=True
                    )
                ) for n in range(6)
            },
            'item': jenny_schema.Item(input=form['item_name']),
            'level': jenny_schema.Level(input=form['level']),
            'bond': jenny_schema.Bond(input=form['bond']),
            'ability': jenny_schema.BaseInput(input=form['ability']),
            'description': form['description']
        }

    if request.method == 'GET':
        return render_template(
            'pc.html',
            form_data=parse_pc_form({}),
            genders=jenny_schema.Gender.VALID_INPUTS,
            balls=jenny_schema.Ball.VALID_INPUTS,
            move_types=jenny_schema.SpecieType.VALID_INPUTS,
            held_items=jenny_schema.Item.VALID_INPUTS
        )
    return render_template(
        'pc.html',
        form_data=parse_pc_form(request.form),
        genders=jenny_schema.Gender.VALID_INPUTS,
        balls=jenny_schema.Ball.VALID_INPUTS,
        move_types=jenny_schema.SpecieType.VALID_INPUTS,
        held_items = jenny_schema.Item.VALID_INPUTS
    )


if __name__ == '__main__':
    app.run()