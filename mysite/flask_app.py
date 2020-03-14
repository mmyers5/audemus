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

    def parse_pc_form(raw_form, N):
        form = {
            **{f'{f}_{N}': None for f in FORM_FIELDS},
            **{f'description_{N}': ''},
            **raw_form.to_dict()
        }
        return {
            'specie': jenny_schema.Specie(
                input=form[f'specie_{N}'],
                specie_type=jenny_schema.SpecieType(input=form[f'specie_type_{N}']),
                shiny=jenny_schema.Shiny(input=form[f'shiny_{N}'])
            ),
            'gender': jenny_schema.Gender(input=form[f'gender_{N}']),
            'ball': jenny_schema.Ball(input=form[f'ball_name_{N}']),
            'name': jenny_schema.BaseInput(input=form[f'name_{N}']),
            'moves': {
                n + 1: jenny_schema.Move(
                    input=form['move_name_0{}_{}'.format(n + 1, N)],
                    move_type=jenny_schema.SpecieType(
                        input=form['move_type_0{}_{}'.format(n + 1, N)],
                        validate=True
                    )
                ) for n in range(6)
            },
            'item': jenny_schema.Item(input=form[f'item_name_{N}']),
            'level': jenny_schema.Level(input=form[f'level_{N}']),
            'bond': jenny_schema.Bond(input=form[f'bond_{N}']),
            'ability': jenny_schema.Ability(input=form[f'ability_{N}']),
            'description': form[f'description_{N}']
        }

    def parse_multiple_pc_form(form, n_pcs):
        return [
            parse_pc_form(form, n) for n in range(n_pcs)
        ]

    if request.method == 'GET':
        n_pcs = 1
        return render_template(
            'pc.html',
            form_data=parse_multiple_pc_form(form={}, n_pcs=n_pcs),
            genders=jenny_schema.Gender.VALID_INPUTS,
            balls=jenny_schema.Ball.VALID_INPUTS,
            move_types=jenny_schema.SpecieType.VALID_INPUTS,
            held_items=jenny_schema.Item.VALID_INPUTS,
            n_pcs=n_pcs
        )
    n_pcs = int(request.form['n_pcs'])
    return render_template(
        'pc.html',
        form_data=parse_multiple_pc_form(form=request.form, n_pcs=n_pcs),
        genders=jenny_schema.Gender.VALID_INPUTS,
        balls=jenny_schema.Ball.VALID_INPUTS,
        move_types=jenny_schema.SpecieType.VALID_INPUTS,
        held_items=jenny_schema.Item.VALID_INPUTS,
        n_pcs=n_pcs
    )


if __name__ == '__main__':
    app.run()