from flask import Flask, request, render_template

from apps.pc.jenny import PcSchema

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return 'Sup, bitch.'


@app.route('/pc', methods=['GET', 'POST'])
def pc_jenny():
    if request.method == 'GET':
        return render_template(
            'pc.html',
            name=None, gender=None, specie_name=None,
            specie_type=None, ball_name=None, item_name=None,
            ability_name=None, level=None, bond=None, moves=None,
            description=None
        )
    body = request.get_json()
    schema = PcSchema()
    return schema.dump(body)


if __name__ == '__main__':
    app.run()