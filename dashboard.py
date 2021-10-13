
import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as mat
from dash.dependencies import Input, Output

df = pd.read_csv('/Users/shanacheng/Documents/332_2020/datasets/lab2.csv')
df3 = pd.read_csv('/Users/shanacheng/Documents/332_2020/datasets/lab3.csv')


mapp = px.choropleth(data_frame=df3, title="Percent of Population That is White", locations=df3['States'], locationmode="USA-states", color=df3['percent_whitepop'], scope="usa", hover_name="States",
                     color_continuous_scale="Blues", height=680)

mapp.update_layout(margin={"t": 20})

xy = ["Percent of Pop Killed By Police", "State Population", "percent_republican",
      "percent_democrat", "percent_blackpop", "percent_whitepop", "Number of Deaths per State"]
# data = df3.loc[:, xy]
data = df3.reindex(columns = xy)
c = data.corr()
cfig = px.imshow(c, x=["Percent of Pop Killed By Police", "State Population", "percent_republican", "percent_democrat", "percent_blackpop", "percent_whitepop", "Number of Deaths per State"],
                 y=["Percent of Pop Killed By Police", "State Population", "percent_republican",
                     "percent_democrat", "percent_blackpop", "percent_whitepop", "Number of Deaths per State"],
                 height=700, width=700, color_continuous_scale=px.colors.diverging.RdBu)

cfig.update_layout(title_text='Correlation Matrix: Per State',
                   title_x=.58, title_y=.88)


app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1('Deaths by Police in the United States (2015)', style={
            "text-align": "center", "font-family": "helvetica", "color": "#473E3C"}),
    html.H4('Scatter Plot: x axis', style={
            "font-family": "helvetica", "color": "#473E3C", 'width': '45%', 'float': 'left', 'display': 'inline-block'}),

    html.Div(
        dcc.Dropdown(id='xcol', style={"font-family": "helvetica", "width": "50%"},
                     clearable=False, value='Number of Deaths per State', multi=False, options=[
            {'label': 'Death Count per State',
                'value': 'Number of Deaths per State'},
            {'label': 'Percent of Population: White',
             'value': 'Percent of Population in State: White'},
            {'label': 'Percent of Population: Black',
             'value': 'Percent of Population in State: Black'},
            {'label': 'Percent of Republicans/Republican Leaning',
             'value': 'Percent of Republican/Leaning Republicans per State'},
            {'label': 'Percent of Democrats/Democrat Leaning',
             'value': 'Percent of Democrats/Leaning Democrats per State'},
            {'label': 'State Political Lean per Death',
             'value': 'State Political Lean'},
            {'label': 'State', 'value': 'States'},
            {'label': 'Victim\'s Age', 'value': 'Ages of Victims'},
        ]),

    ),
    html.H4('Scatter Plot: y axis:', style={
            "font-family": "helvetica", "color": "#473E3C", 'width': '45%'}),
    html.Div(
        dcc.Dropdown(
            id='ycol', style={"font-family": "helvetica", "width": "50%"}, value='Number of Deaths per State',
            multi=False, clearable=False, options=[
                {'label': 'Death Count per State',
                    'value': 'Number of Deaths per State'},
                {'label': 'Percent of Population: White',
                    'value': 'Percent of Population in State: White'},
                {'label': 'Percent of Population: Black',
                    'value': 'Percent of Population in State: Black'},
                {'label': 'Percent of Republicans/Republican Leaning',
                 'value': 'Percent of Republican/Leaning Republicans per State'},
                {'label': 'Percent of Democrats/Democrat Leaning',
                 'value': 'Percent of Democrats/Leaning Democrats per State'},
                {'label': 'State Political Lean per Death',
                    'value': 'State Political Lean'},
                {'label': 'State', 'value': 'States'},

                {'label': 'Victim\'s Age', 'value': 'Ages of Victims'},
            ]
        )
    ),
    html.Div([
        dcc.Graph(id='scatterg')], style={'width': '35%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='parallel')], style={'display': 'inline-block', 'width': '60%'}),


    html.Div([dcc.Graph(id="mapp", figure=mapp)], style={'width': '58%', 'display': 'inline-block', 'float': 'left',
                                                         'padding': '10px 10px', 'backgroundColor': 'rgb(250, 250, 250)'}),
    html.Div([
        dcc.Graph(id="bar_graph"), dcc.Graph(id="scatterg2")], style={'display': 'inline-block',
                                                                      'padding': '10px 10px', 'backgroundColor': 'rgb(250, 250, 250)'},
    ),

    html.Div(
        dcc.Graph(id="correlation", figure=cfig)
    )


])


@app.callback(
    Output('scatterg', 'figure'),
    [Input('xcol', 'value'),
     Input('ycol', 'value')]
)
def scat(xcol, ycol):
    scatfig = px.scatter(df, x=xcol, y=ycol, title=xcol +
                         ' vs ' + ycol, hover_name="States")
    return scatfig


@app.callback(
    Output('parallel', 'figure'),
    [Input('scatterg', 'hoverData'),
     Input('ycol', 'value')]
)
def updateparallel(hoverData, ycol):
    c = 0
    if not hoverData:
        state = "AK"
        c = 738516
    else:
        val = hoverData['points'][0]['hovertext']
        state = val
        count = 0
        for i in df3.itertuples():
            if i[7] == val:
                c = i[17]
                break

    fig = go.Figure(data=go.Parcoords(line_color="red",
                                      dimensions=list([
                                          dict(label='% of State Pop: Republican',
                                               values=df3['percent_republican']),
                                          dict(label='% of State Pop: Democrat',
                                               values=df3['percent_democrat']),
                                          dict(label='% of State Pop: Black',
                                               values=df3['percent_blackpop']),
                                          dict(label='% of State Pop: White',
                                               values=df3['percent_whitepop']),
                                          dict(
                                              label='Number of Deaths', values=df3['Number of Deaths per State']),
                                          dict(constraintrange=[
                                               c, c+1], label='State Population', values=df3['State Population']),

                                      ])
                                      )
                    )
    fig.update_layout(title_text=state, title_x=.5, title_y=0, height=400)

    return fig


@app.callback(
    Output('bar_graph', 'figure'),
    Input('mapp', 'hoverData')
)
def updatebar(hoverData):
    colors = ['gray', ] * 50
    statearray = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
                  "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "SC", "SD", "TN",
                  "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]
    if not hoverData:
        colors = ['gray', ] * 50
    else:
        colors = ['gray', ] * 50
        val = hoverData['points'][0]['hovertext']
        for i in statearray:
            if i == val:
                index = statearray.index(i)
                colors[index] = 'blue'
    barfig = go.Figure(data=go.Histogram(x=df['States'], marker_color=colors,
                                         ))
    barfig.update_xaxes(categoryorder="category ascending")
    barfig.update_layout(width=540, height=300,
                         title_text="Number of Deaths per State")
    return barfig


@app.callback(
    Output('scatterg2', 'figure'),
    Input('mapp', 'hoverData')
)
def updatescatter2(hoverData):
    colors = ['white']*50
    starray = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
               "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "SC", "SD", "TN",
               "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]
    if not hoverData:
        colors = ['gray']*50
    else:
        colors = ['gray']*50
        val = hoverData['points'][0]['hovertext']
        for i in starray:
            if i == val:
                ind = starray.index(i)
                colors[ind] = 'blue'

    scatt = px.scatter(df3, x="Percent of Pop Killed By Police", y="Number of Deaths per State",
                       hover_name="States", color="States", color_discrete_sequence=colors)

    scatt.update_layout(width=550, height=300,
                        title_text="Percent of Population Killed By Police")
    return scatt


if __name__ == '__main__':
    app.run_server(debug=True)
