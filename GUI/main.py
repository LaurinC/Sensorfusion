from dash import Dash, dcc, html, Input, Output, ctx, callback
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go 
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

@callback(
    [Output('image-graph', 'figure')],
    [Input('interval-component', 'n_intervals'), Input('switch-bbox','value')],
    prevent_initial_call = True
)
def update(n_intervals, switch_bbox):
    if ctx.triggered_id == 'switch-bbox':
        # TODO: control camera process
        raise PreventUpdate
    else:
        # TODO: get real data from camera/radar process
        img = np.random.randint(0, high = 255, size = (400, 800, 3), dtype = np.uint8)
        fig_img = px.imshow(img)
    # eventually there should be two graphs
    return [fig_img]

def config_app() -> Dash:
    # dash app
    app = Dash(__name__, external_stylesheets = [dbc.themes.QUARTZ])
    # list for graph controls
    controls = [
        dbc.Checklist(options=[{'label' : 'Object detection', 'value' : 1},], 
                    value = [0], 
                    id = 'switch-bbox', 
                    switch = True)
    ]
    # html layout
    app.layout = dbc.Container([
        html.Div(html.H1('Demo GUI'), style = {'margin-top' : 20}),
        dbc.Card(dbc.Row([dbc.Col(c) for c in controls]), body = True),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(id = 'image-graph')),
            dbc.Col(dcc.Graph(id = 'polarscatter-graph'))
        ]),
        dcc.Interval(
            id = 'interval-component',
            interval = 0.2 * 1000
        )
    ])
    return app

if __name__ == '__main__':
    # TODO: start other interfaces from here
    app = config_app()
    app.run(debug = True)