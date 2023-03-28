import dash
from dash import dash, html, dcc, Input, Output
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.io as pio
import pickle
import re

file = open('data/sous_nutr_info.pkl', 'rb')
data_sous_nutr = pickle.load(file)
file.close()

file = open('data/dispo_alim.pkl', 'rb')
data_dispo_alim = pickle.load(file)
file.close()

df_pop = pd.read_csv("data/population.csv")
df_sous_nutr = pd.read_csv("data/sous_nutrition.csv")
df_dispo_alim = pd.read_csv("data/dispo_alimentaire.csv")
df_aide_alim = pd.read_csv("data/aide_alimentaire.csv")
pop_by_year = pd.read_csv("data/pop_by_year.csv")


df_sous_nutr.Valeur = df_sous_nutr.Valeur.replace({"<0.1": "0.05"}).fillna(0).astype(float)
df_sous_nutr.Année = df_sous_nutr.Année.replace({
    "2012-2014" : 2013,
    "2013-2015" : 2014,
    "2014-2016" : 2015,
    "2015-2017" : 2016,
    "2016-2018" : 2017,
    "2017-2019" : 2018,
})

df_pie = df_aide_alim.groupby(by="Pays bénéficiaire").sum().reset_index().sort_values(by="Valeur", ascending=False)
value_other = df_pie.tail(-5).Valeur.sum()
df_pie_head = df_pie.head(5)
df_pie_head.loc[5] = ["Others", 0, value_other]




pio.templates.default = "plotly_dark"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

dropdown_col = data_sous_nutr.Zone
dropdown_col2 = df_pop.Année.unique()



#############################----COMPONENTS----#################################


droplist = html.Div(
    [
    dcc.Dropdown(dropdown_col,id="dropdown",value=list(data_sous_nutr.Zone)[0], clearable=False,
                 style={
                "color": "black",
                "text-align": "center",
                'margin-top': '40px',
                'margin-bottom': '40px',
                'width': '100%',
                })
    ],
)

droplist2 = html.Div(
    [
    dcc.Dropdown(dropdown_col2,id="dropdown2",value=2017, clearable=False,
                 style={
                "color": "black",
                "text-align": "center",
                'margin-top': '40px',
                'margin-bottom': '40px',
                'width': '100%',
                })
    ],
)

card2 = dbc.Card(
    [
        dbc.CardHeader("", style={"height": "3.3rem"}),
        dbc.CardBody(
            [
                html.H3("Équivalent à"),
                html.H3(className="card-text", id="textcard2"),
                html.P("% des habitants")
            ]
        ),
    ],
    style={"width": "20rem"},
)

card = dbc.Card(
    [
        dbc.CardHeader("Info sous-nutrition"),
        dbc.CardBody(
            [
                html.H4(className="card-title", id="titlecard"),
                html.H2(className="card-text", id="textcard"),
                html.P("d'habitants en sous nutrition")
            ]
        ),
    ],
    style={"width": "19.5rem"},
)

card3 = dbc.Card(
    [
        dbc.CardHeader("Dans le monde : "),
        dbc.CardBody(
            [
                html.H2(id="textcard3"),
                html.P("d'habitants en sous nutrition en l'an"),
                html.H4(id="titlecard3")
            ]
        ),
    ],
    style={"width": "18.4rem", "height": "15.5rem"},
)

card4 = dbc.Card(
    [
        dbc.CardHeader("", style={"height": "3.3rem"}),
        dbc.CardBody(
            [
                html.H2(id="textcard4"),
                html.P("% des êtres humains qui sont en sous nutrition"),
            ]
        ),
    ],
    style={"width": "18.4rem", "height": "15.5rem"},
)

pie_chart = px.pie(df_pie_head, values="Valeur", names="Pays bénéficiaire", hole=.4, title="Pays bénficiants le plus d'aides alimentaire")

######################################----CALLBACKS----#####################################

@app.callback(

        Output('titlecard','children'),
        Input('dropdown', 'value')
    )
def change_title(value):
    return value

@app.callback(

        Output("textcard", "children"),
        Input('dropdown', 'value')
    )
def change_card_text(value):
    return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % (data_sous_nutr.loc[data_sous_nutr["Zone"] == value]["sous_nutr(Mhab)"] * 1000000))

@app.callback(

        Output('textcard2','children'),
        Input('dropdown', 'value')
    )
def change_title(value):
    return data_sous_nutr.loc[data_sous_nutr["Zone"] == value]["pct_sous_nutr"].round(2)



@app.callback(
        Output('textcard3','children'),
        Input('dropdown2', 'value')
    )
def change_year(value):
    pop_sous_nutr = df_sous_nutr.loc[df_sous_nutr['Année'] == value].Valeur.sum().round(2)

    return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % (pop_sous_nutr * 1000000))


@app.callback(
        Output('textcard4','children'),
        Input('dropdown2', 'value')
    )
def change_year(value):
    pop_sous_nutr = df_sous_nutr.loc[df_sous_nutr['Année'] == value].Valeur.sum()
    return (100 * pop_sous_nutr / (pop_by_year.loc[pop_by_year['Année'] == value].Valeur / 1000)).round(2)

@app.callback(

        Output('titlecard3','children'),
        Input('dropdown2', 'value')
    )
def change_title(value):
    return value

###################################----ROWS----#####################################

title_row = dbc.Row(html.H1('Analyse de la situation alimentaire dans le monde', style={'textAlign': 'center'}))

subtitle_row = dbc.Row(
    [
        dbc.Col("",width=2),
        dbc.Col(html.H4("Choisissez une année :"),width=2, style={"margin-left": "25px"}),
        dbc.Col("",width=4),
        dbc.Col(html.H4("Choisissez un pays:"),width=2, style={"margin-left": "5px"}),
        dbc.Col("",width=2),
    ])

row_dropdown = dbc.Row(
    [
        dbc.Col("",width=2),
        dbc.Col(html.Div(droplist2),width=2),
        dbc.Col("",width=4),
        dbc.Col(html.Div(droplist),width=2),
        dbc.Col("",width=2),
        html.Hr(style={'borderWidth': "0.3vh", "width": "100%", "color": "#FFFFFF"}),
    ])

card_row =dbc.Row(
    [
        dbc.Col("",width=1),
        dbc.Col(html.Div(card3),width=2),
        dbc.Col(html.Div(card4),width=2),
        dbc.Col("",width=2),
        dbc.Col(html.Div(card),width=2),
        dbc.Col(html.Div(card2),width=2),
        dbc.Col("",width=1),
    ])

graph_row = dbc.Row([
    dbc.Col("",width=4),
    dbc.Col(dcc.Graph(id= "graph1",figure = pie_chart), width=4),
    dbc.Col("",width=4)
])


#################################----LAYOUT----#####################################

app.layout = \
html.Div([
    html.Br(),
    title_row,
    html.Hr(style={'borderWidth': "0.3vh", "width": "100%", "color": "#FFFFFF"}),
    subtitle_row,
    row_dropdown,
    html.Br(),
    card_row,
    html.Br(),
    graph_row
    ])




if __name__ == '__main__':
    app.run_server(debug=True)
