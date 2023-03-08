# perform the basic imports
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
import yfinance as yf
from datetime import datetime
from datetime import date, timedelta
import os
import pandas as pd
os.environ["IEX_API_KEY"] = "pk_698caadc6a2b40c28993dde175e64c3b"

# launch the application
app = dash.Dash()

# read a .csv file, make a dataframe, and build a list of Dropdown options
nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label': '{} {}'.format(
        tic, nsdq.loc[tic]['Name']), 'value': tic})

# create a Div to contain basic headers, an input box, and our graph
app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),

    html.Div([
        # add styles to enlarge the input box and make room for DatePickerRange
        # replace dcc.Input with dcc.Dropdown, set options=options
        html.H3('Select stock symbol: ', style={'paddingRight': '30px'}),
        dcc.Dropdown(
            id='my_ticker_symbol',
            options=options,
            value=[''],
            multi=True
        )
        # widen the Div to fit multiple inputs
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%'}),

    # add a Div to contain the DatePickerRange
    html.Div([
        html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2022, 12, 1),
            end_date=datetime.today()
        )
    ], style={'display': 'inline-block'}),

    # add a Button element
    html.Div([
        html.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            style={'fontSize': 24, 'marginLeft': '30px'}
        ),
    ], style={'display': 'inline-block'}),

    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1, 2], 'y':[3, 1]}
            ]
        }
    )
])


@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
     State('my_date_picker', 'start_date'),
     State('my_date_picker', 'end_date')]
)
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    # since stock_ticker is now a list of symbols, create a list of traces
    traces = []
    for tic in stock_ticker:
        df = yf.download(tic, start=start, end=end)
        # df = web.DataReader(tic, 'yahoo', start, end)
        traces.append({'x': df.index, 'y': df.Close, 'name': tic})
    fig = {
        # set data equal to traces
        'data': traces,
        # use string formattin to include all symbols in the chart title
        'layout': {'title': ','.join(stock_ticker)+' Closing Prices'}
    }
    return fig


# Add the server clause
if __name__ == '__main__':
    app.run_server()
