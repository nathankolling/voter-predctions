import dash
from dash import dcc
from dash import html
import numpy as np
from dash.dependencies import Output, Input
import os
from threading import Timer
import webbrowser
import plotly.graph_objects as go
from catboost import CatBoostClassifier

classifier = CatBoostClassifier()
classifier.load_model("catboost_classifier")

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "2016 Voter Predictions"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="2016 Voter Predictions", className="header-title"
                ),
                html.P(
                    ["Interactive US voting prediction map based off of user input. The predictive model used is a "
                     "CatBoostClassifier (gradient boosted decision trees), trained on data from ", html.A('The 2016 Cooperative '
                                                                                     'Congressional Election Study',
                                                                                     href="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi%3A10.7910/DVN/GDF6Z0"), ".", html.Br(), "Please fill in the responses as if you were responding before the 2016 election."],
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="What gender are you?", className="menu-title-short"),
                        dcc.Dropdown(
                            id="gender",
                            options=[
                                {"label": key, "value": [1, 2][['Male', 'Female'].index(key)]}
                                for key in ['Male', 'Female']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Age", className="menu-title-short"),
                        dcc.Dropdown(
                            id="age",
                            options=[
                                {"label": age, "value": age}
                                for age in np.arange(18, 100)
                            ],
                            value=18,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Education level", className="menu-title-short"),
                        dcc.Dropdown(
                            id="educ",
                            options=[
                                {"label": key, "value": np.arange(1, 7)[['No high school degree', 'High school graduate','Some college', '2-year', '4-year', 'Post-grad'].index(key)]}
                                for key in ['No high school degree', 'High school graduate','Some college', '2-year', '4-year', 'Post-grad']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Ethnicity", className="menu-title-short"),
                        dcc.Dropdown(
                            id="race",
                            options=[
                                {"label": key, "value": [1,2,3,4,5,8,6,7][['White', 'Black', 'Hispanic', 'Asian', 'Native American', 'Middle Eastern', 'Mixed', 'Other'].index(key)]}
                                for key in ['White', 'Black', 'Hispanic', 'Asian', 'Native American', 'Middle Eastern', 'Mixed', 'Other']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="How important is religion in your life?", className="menu-title"),
                        dcc.Dropdown(
                            id="religion_imp",
                            options=[
                                {"label": key, "value": [1,2,3,4][['Very important', 'Somewhat important', 'Not too important', 'Not at all important'].index(key)]}
                                for key in ['Very important', 'Somewhat important', 'Not too important', 'Not at all important']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Do you follow what’s going on in government and public affairs?", className="menu-title"),
                        dcc.Dropdown(
                            id="newsint",
                            options=[
                                {"label": key, "value": [1,2,3,4,7][['Most of the time','Some of the time', 'Only now and then','Hardly at all','Don\'t know'].index(key)]}
                                for key in ['Most of the time','Some of the time', 'Only now and then','Hardly at all','Don\'t know']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Would you repeal the Affordable Care Act (Obamacare)?", className="menu-title"),
                        dcc.Dropdown(
                            id="obama",
                            options=[
                                {"label": key, "value": [1,2][['Yes','No'].index(key)]}
                                for key in ['Yes','No']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Over the past year, the nation’s economy has ...?", className="menu-title"),
                        dcc.Dropdown(
                            id="nat_eco_dir",
                            options=[
                                {"label": key, "value": [1,2,3,4, 5, 6][['Gotten much better','Gotten better','Stayed about the same','Gotten worse','Gotten much worse','Not sure'].index(key)]}
                                for key in ['Gotten much better','Gotten better','Stayed about the same','Gotten worse','Gotten much worse','Not sure']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Should the government identify and deport illegal immigrants?", className="menu-title"),
                        dcc.Dropdown(
                            id="deport_imm",
                            options=[
                                {"label": key, "value": [1,2][['Yes', 'No'].index(key)]}
                                for key in ['Yes', 'No']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Do you support banning assault rifles?", className="menu-title"),
                        dcc.Dropdown(
                            id="ban_ar",
                            options=[
                                {"label": key, "value": [1, 2][['Yes', 'No'].index(key)]}
                                for key in ['Yes', 'No']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu2",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Should women always be allowed to obtain a legal abortion?", className="menu-title"),
                        dcc.Dropdown(
                            id="abortion",
                            options=[
                                {"label": key, "value": [1,2][['Yes', 'No'].index(key)]}
                                for key in ['Yes', 'No']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Should the minimum wage be increased (from $7.25/hr) by 2020?", className="menu-title"),
                        dcc.Dropdown(
                            id="min_wage",
                            options=[
                                {"label": key, "value": [1,2][['Yes', 'No'].index(key)]}
                                for key in ['Yes', 'No']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Do you support the legalization of gay marriage?", className="menu-title"),
                        dcc.Dropdown(
                            id="gay_marriage",
                            options=[
                                {"label": key, "value": [1,2][['Yes', 'No'].index(key)]}
                                for key in ['Yes', 'No']
                            ],
                            value=1,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu3",
        ),
        html.Div(
            children=dcc.Graph(
                id="prediction-map", config={"displayModeBar": False},
            ),
            className="wrapper",
        )
    ]
)

state_codes = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}


@app.callback(
    Output("prediction-map", "figure"),
    [
        Input("gender", "value"),
        Input("age", "value"),
        Input("educ", "value"),
        Input("race", "value"),
        Input("religion_imp", "value"),
        Input("newsint", "value"),
        Input("obama", "value"),
        Input("nat_eco_dir", "value"),
        Input("deport_imm", "value"),
        Input("ban_ar", "value"),
        Input("abortion", "value"),
        Input("min_wage", "value"),
        Input("gay_marriage", "value")
    ],
)

def update_state_figure(gender, age, educ,race,religion_imp, newsint, obama, nat_eco_dir, deport_imm, ban_ar, abortion, min_wage, gay_marriage):
    beg = [gender, age, educ, race]
    end = [religion_imp, newsint, obama, nat_eco_dir, deport_imm, ban_ar, abortion, min_wage, gay_marriage]
    probas = {}
    for key in [*state_codes]:
        probas[key] = return_probability(beg, state_codes[key], end)
    layout = go.Layout(
        margin=go.layout.Margin(l=0, r=0, b=10, t=10),
        autosize=False,
        width=1400,
        height=478
    )
    fig = go.Figure(data=go.Choropleth(
        locations=[*probas],
        z=[*probas.values()],
        locationmode='USA-states',
        colorscale=[[0, 'rgb(0,0,255)'], [0.3, 'rgb(140,140,255)'], [0.4, 'rgb(200,200,255)'], [0.5, 'rgb(255,255,255)'], [0.6, 'rgb(255,200,200)'],[0.7, 'rgb(255,140,140)'], [1, 'rgb(255,0,0)']],
        zmin=0,
        zmax=1,
        colorbar=dict(
            title="Voting Probability",
            titleside="top",
            tickmode="array",
            tickvals=[0.001, 0.125, 0.25, 0.375, 0.5, 0.635, 0.75, 0.875, 0.995],
            ticktext=["100%", '      Clinton', '75%','',"50%",'', '75%','      Trump', "100%"],
            ticks="outside",
        ),
        hoverinfo='text',
        hovertext=[key + '<br><br>' + f'Probability of voting for <br>Clinton: {np.round(1 - val, 4)}<br>Trump:   {val}' for key, val in probas.items()]
        ),
        layout=layout
    )
    fig.update_layout(
        geo_scope='usa'
    )
    return fig


def return_probability(beg, state, end):
    proba_predict = classifier.predict_proba(beg + [state] + end)
    return np.round(proba_predict[0], 4)


def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:8050/')

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=True, port=8050)

# if __name__ == "__main__":
#     app.run_server(debug=True)
