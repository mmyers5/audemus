import logging
import os
import pickle

import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from apps.whippet import utils

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_ID = '1R5xwxCPhslBOIaBtSOa8byA5DW4MQS9Wk570GZ4mR_k'
RANGE_NAME = 'Sheet1!A2:E'
SHEET_COLS = [
    'dex_num', 'specie', 'rarity', 'location', 'frequency'
]

RARITY_MAP = {
    '1': .80,
    '2': .60,
    '3': .30
}
FREQUENCY_MAP = {
    '1': .80,
    '2': .60,
    '3': .30,
    '4': .20
}

def get_service():
    creds = None
    if os.path.exists(utils.SHEETS_FLOW_TOKEN):
        with open(utils.SHEETS_FLOW_TOKEN, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                utils.SHEETS_CREDENTIALS, SCOPES
            )
            creds = flow.run_local_server()
        with open(utils.SHEETS_FLOW_TOKEN, 'wb') as token:
            pickle.dump(creds, token)
    return build('sheets', 'v4', credentials=creds)

def get_sheet_values():
    service = get_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SHEET_ID,
        range=RANGE_NAME
    )
    result = result.execute()
    values = result.get('values', [])
    if not values:
        logging.warning('No data found.')
    return values

def sheet_values_to_df(values):
    return pd.DataFrame(values, columns=SHEET_COLS)

def df_valid(df):
    return all(col in df for col in SHEET_COLS)

def df_at_location(df, location):
    if not df_valid(df):
        raise Exception(
            'Missing colums\nNeed:\n{need}\nHave:\n{have}'.format(
                need=SHEET_COLS, have=list(df.columns)
            )
        )
    location_mask = df.location == location
    return df[location_mask]

def calc_rarity(df):
    logging.info('Calculating rarity')
    rarity = [RARITY_MAP[r] for r in df.rarity]
    df = df.assign(rarity_frac=rarity)
    return df

def calc_frequency(df):
    logging.info('Calculating frequency')
    frequency = [FREQUENCY_MAP[f] for f in df.frequency]
    df = df.assign(frequency_frac=frequency)
    return df

def calc_encounter(df):
    cols = ['rarity_frac', 'frequency_frac']
    if not all(col in df for col in cols):
        df = calc_rarity(df)
        df = calc_frequency(df)
    logging.info('Calculating encounter chance')
    df = df.assign(
        encounter_percent=df.rarity_frac*df.frequency_frac*100
    )
    return df

def main(location):
    values = get_sheet_values()
    df = sheet_values_to_df(values)
    df = df_at_location(df, location)
    df = calc_encounter(df)
    return df.sample(1, weights='encounter_percent')
