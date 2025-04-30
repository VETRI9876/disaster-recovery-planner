import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px


default_data = pd.DataFrame({
    'System': ['Database', 'Web Server', 'Application Server', 'File Storage'],
    'RTO (hrs)': [2, 1, 3, 4],
    'RPO (hrs)': [1, 1, 2, 3],
    'Status': ['Ready', 'Ready', 'In Progress', 'Not Ready']
})


app = dash.Dash(__name__)
app.title = "Disaster Recovery Planner"

app.layout = html.Div([
    html.H1("Disaster Recovery & Data Resilience Planner", style={'textAlign': 'center', 'color': '#003366'}),

    html.Div([
        dcc.Input(id="system-name", type="text", placeholder="System Name", style={'margin': '5px', 'width': '200px'}),
        dcc.Input(id="rto", type="number", placeholder="RTO (hrs)", style={'margin': '5px', 'width': '200px'}),
        dcc.Input(id="rpo", type="number", placeholder="RPO (hrs)", style={'margin': '5px', 'width': '200px'}),
        dcc.Dropdown(
            id='status',
            options=[{'label': s, 'value': s} for s in ['Ready', 'In Progress', 'Not Ready']],
            placeholder="Status",
            style={'width': '200px', 'margin': '5px'}
        ),
        html.Button('Add System', id='add-button', n_clicks=0, style={'margin': '10px', 'padding': '10px', 'background-color': '#007bff', 'color': 'white', 'border': 'none', 'border-radius': '5px'})
    ], style={'display': 'flex', 'justify-content': 'center', 'flex-wrap': 'wrap', 'gap': '10px'}),

    html.Div(id='error-message', style={'color': 'red', 'textAlign': 'center', 'marginTop': '10px'}),

    html.H2("DR Plan Table", style={'marginTop': '20px', 'color': '#003366'}),
    html.Div(id='table-container'),

    html.H2("Status Overview", style={'marginTop': '20px', 'color': '#003366'}),
    dcc.Graph(id='status-chart', style={'height': '400px', 'marginTop': '10px'})
])


data_store = default_data.copy()

@app.callback(
    [Output('table-container', 'children'),
     Output('status-chart', 'figure'),
     Output('error-message', 'children')],
    Input('add-button', 'n_clicks'),
    State('system-name', 'value'),
    State('rto', 'value'),
    State('rpo', 'value'),
    State('status', 'value')
)
def update_output(n_clicks, name, rto, rpo, status):
    global data_store
    error_message = ''

    if n_clicks > 0:
        if not name or rto is None or rpo is None or not status:
            error_message = "Please fill in all the fields before adding a system."
        else:
            new_row = pd.DataFrame([{
                'System': name,
                'RTO (hrs)': rto,
                'RPO (hrs)': rpo,
                'Status': status
            }])
            data_store = pd.concat([data_store, new_row], ignore_index=True)

            name, rto, rpo, status = '', None, None, None
            error_message = ''

    table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in data_store.columns])),
        html.Tbody([
            html.Tr([html.Td(data_store.iloc[i][col]) for col in data_store.columns])
            for i in range(len(data_store))
        ])
    ], style={'width': '100%', 'border': '1px solid #ddd', 'textAlign': 'center', 'border-radius': '5px', 'marginTop': '20px'})

    fig = px.pie(data_store, names='Status', title='System Readiness Status')

    return table, fig, error_message

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8085)
