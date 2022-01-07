'''
html.Img(src=app.get_asset_url('images/under_construction.png'),
'''

import dash
from dash import html
import dash_bootstrap_components as dbc


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.title="Сайт находится в стадии разработки"
app.config.suppress_callback_exceptions=True

app.layout = html.Div(children=[
    dbc.Alert(
        children=[
            html.Div(
                children=[
                    html.H1('Сайт находится в стадии разработки!'),
                    html.Div(
                        children=[
                        html.Img(src=app.get_asset_url('images/under_construction.png')),
                    ],
                    style={'margin-top':'30pt','margin-bottom':'30pt'}
                    )  
                ]
            )
                     
        ],
        color='primary',
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)

