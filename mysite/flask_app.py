from flask import Flask, request, render_template

from apps.whippet import get_one
from apps.bran import scrape, doc_write
from apps.jeeves import scrape, score

import utils

app = Flask(__name__)

@app.route('/whippet/', methods=['GET', 'POST'])
def whippet():
    template = 'whippet.html'
    values = get_one.get_sheet_values()
    df = get_one.sheet_values_to_df(values)
    locations = sorted(df.location.unique())
    if request.method == 'GET':
        form = {
            'location': locations[0],
            'printout': ''
        }
    elif request.method == 'POST':
        location = request.form['location']
        location_df = get_one.df_at_location(df, location)
        location_df = get_one.calc_encounter(location_df)
        row_entry =  location_df.sample(1, weights='encounter_percent')
        specie = row_entry.specie.iloc[0]
        chance = row_entry.encounter_percent.iloc[0]
        form = {
            'location': location,
            'printout': '{specie} - {chance:.2f}%'.format(
                specie=specie, chance=chance
            )
        }
    return render_template(
        template,
        locations=locations,
        form=form
    )

@app.route('/bran/', methods=['GET', 'POST'])
def bran():
    template = 'bran.html'
    if request.method == 'GET':
        form = {
            'username': '',
            'thread_url': '',
            'printout': ''
        }
    elif request.method == 'POST':
        username = request.form['username']
        thread_url = request.form['thread_url']
        service = doc_write.get_service()
        thread = scrape.JcinkThread(thread_url)
        posts, users = thread.ordered_posts()
        filename = doc_write.filename(
            username, thread.title, thread.subtitle
        )
        doc = doc_write.write_file(filename, posts, users, service)
        doc_url = doc_write.doc_url(doc)

        form = {
            'username': username,
            'thread_url': thread_url,
            'printout': doc_url
        }
    return render_template(
        template,
        form=form
    )

@app.route('/jeeves/', methods=['GET', 'POST'])
def jeeves():
    template = 'jeeves.html'
    if request.method == 'GET':
        form = {
            'thread_url': '',
            'printout': ''
        }
    elif request.method == 'POST':
        thread_url = request.form['thread_url']
        page = scrape.JcinkPage(thread_url)
        users = page.users
        posts = page.posts
        thread_score = score.ThreadScore(users, posts)
        printout = thread_score.printout(
            words_per_level=utils.N_WORDS_LEVEL,
            words_per_dollar=utils.N_WORDS_DOLLAR
        )
        form = {
            'thread_url': thread_url,
            'printout': printout
        }
    return render_template(
        template,
        form=form
    )
