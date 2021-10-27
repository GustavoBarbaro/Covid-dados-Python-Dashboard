import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input


#lendo o dataset
data = pd.read_csv("owid-covid-data.csv")

#lendo as datas da maneira correta
data["date"] = pd.to_datetime(data["date"], format="%Y/%m/%d")
data.sort_values("date", inplace=True)

#definindo a fonte
#CSS rules - font-family: 'Oswald', sans-serif;
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Oswald:wght@300&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Dados da COVID-19"


app = dash.Dash(__name__)

#definindo o layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Dados da COVID-19", className="header-title"
                ),
                html.P(
                    children="Analisa os casos de COVID-19 no mundo no período de 20/01/2020 a 18/08/2021",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        #inserindo as caixas de filtro
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="País", className="menu-title"),
                        dcc.Dropdown(
                            id="filtro_pais",
                            options=[
                                {"label": location, "value": location}
                                for location in np.sort(data.location.unique())
                            ],
                            value="Brazil",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Range de data",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.date.min().date(),
                            max_date_allowed=data.date.max().date(),
                            start_date=data.date.min().date(),
                            end_date=data.date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="total_de_casos", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="casos_por_dia", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    [Output("total_de_casos", "figure"), Output("casos_por_dia", "figure")],
    [
        Input("filtro_pais", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(location, start_date, end_date):
    mask = (
        (data.location == location)
        & (data.date >= start_date)
        & (data.date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    covid_total = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["total_cases"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Total de casos de COVID-19",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#ff3333"],
        },
    }

    covid_por_dia = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["new_cases"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {"text": "Novos casos por dia", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#3333ff"],
        },
    }
    return covid_total, covid_por_dia



if __name__ == "__main__":
    app.run_server(debug=False)

server = app.server