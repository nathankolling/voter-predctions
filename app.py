import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import os
from threading import Timer
import webbrowser
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go

data = pd.read_csv("avocado.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "2016 Voter Predictions"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="2016 Voter Predictions", className="header-title"
                ),
                html.P(
                    children="Responsive US voting prediction map based off of user input.\nPlease fill in the responses as if you were responding before the 2016 election.",
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
                                {"label": key, "value": np.arange(1, 7)[['No HS', 'High school graduate','Some college', '2-year', '4-year', 'Post-grad'].index(key)]}
                                for key in ['No HS', 'High school graduate','Some college', '2-year', '4-year', 'Post-grad']
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
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                )
            ],
            className="wrapper",
        ),
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

state_codes_reversed = {v: k for k, v in state_codes.items()}
temp_state_plotting = {key: 0.1 for key in state_codes.keys()}


@app.callback(
    Output("price-chart", "figure"),
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
    # playing = np.asarray([*{key: 0.5 for key in state_codes.keys()}.values()])
    # zz = (np.where(playing[:, 0] < 0.5, -playing[:, 1], playing[:, 0]) + 1) / 2
    fig = go.Figure(data=go.Choropleth(
        locations=[*temp_state_plotting],  # Spatial coordinates
        z=[*temp_state_plotting.values()],  # Data to be color-coded
        locationmode='USA-states',  # set of locations match entries in `locations`
        colorscale=[[0, 'rgb(0,0,255)'], [0.3, 'rgb(200,200,255)'], [0.4, 'rgb(230,230,255)'], [0.5, 'rgb(255,255,255)'], [0.6, 'rgb(255,230,230)'],[0.7, 'rgb(255,200,200)'], [1, 'rgb(255,0,0)']],
        zmin=0,
        zmax=1,
        # colorbar_title='Binary Cross-entropy',
        colorbar=dict(
            title="Voting Probability",
            titleside="top",
            tickmode="array",
            tickvals=[0.001, 0.25, 0.5, 0.75, 0.995],
            ticktext=["100%", '75%',"50%", '75%', "100%"],
            ticks="outside"
        )
    ))

    fig.update_layout(
        title_text=f"{gender}, {age}, {educ}, {race}, {religion_imp}, {newsint}, {obama}, {nat_eco_dir}, {deport_imm}, {ban_ar}, {abortion}, {min_wage}, {gay_marriage}",
        geo_scope='usa',  # limite map scope to USA
        # coloraxis_colorbar=dict(
        #     title="Population",
        #     tickvals=[0, 0.2, 0.6, 1],
        #     ticktext=["1M", "10M", "100M", "1B"])
    )
    return fig

# def update_charts(dum, age, educ,race,religion_imp, newsint, obama, nat_eco_dir, deport_imm, ban_ar, abortion, min_wage, gay_marriage):
#     mask = (
#         (data.region == "Albany")
#         & (data.type == 'organic')
#         & (data.Date >= data.Date.min().date())
#         & (data.Date <= data.Date.max().date())
#     )
#     filtered_data = data.loc[mask, :]
#     price_chart_figure = {
#         "data": [
#             {
#                 "x": filtered_data["Date"],
#                 "y": filtered_data["AveragePrice"],
#                 "type": "lines",
#                 "hovertemplate": "$%{y:.2f}<extra></extra>",
#             },
#         ],
#         "layout": {
#             "title": {
#                 "text": f"{dum}, {age}, {educ},{race},  {religion_imp} {newsint} {obama} {nat_eco_dir} {deport_imm} {ban_ar} {abortion} {min_wage} {gay_marriage}",
#                 "x": 0.05,
#                 "xanchor": "left",
#             },
#             "xaxis": {"fixedrange": True},
#             "yaxis": {"tickprefix": "$", "fixedrange": True},
#             "colorway": ["#17B897"],
#         },
#     }
#
#     volume_chart_figure = {
#         "data": [
#             {
#                 "x": filtered_data["Date"],
#                 "y": filtered_data["Total Volume"],
#                 "type": "lines",
#             },
#         ],
#         "layout": {
#             "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
#             "xaxis": {"fixedrange": True},
#             "yaxis": {"fixedrange": True},
#             "colorway": ["#E12D39"],
#         },
#     }
#     # return price_chart_figure
#     return price_chart_figure, volume_chart_figure
def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:8050/')

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=True, port=8050)

# if __name__ == "__main__":
#     app.run_server(debug=True)
