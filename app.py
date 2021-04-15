import dash 
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.express as px 
import  pandas as pd
from dash.dependencies import  Input, Output



df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets = external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id = 'graph_with_slider'),
    dcc.Slider(
        id = 'year_slider',
        min=df['year'].min(),
        max = df['year'].max(),
        value = df['year'].min(),
        marks = {str(year):str(year) for year in df['year'].unique()},
        step =None
    ),
    html.H4(children='World GDP data'),
    generate_table(df)
])


@app.callback(
    Output('graph_with_slider', 'figure'),
    Input('year_slider', 'value')
)

def update_figure(year_selected):
    filtered_df = df[df.year == year_selected]

    fig = px.scatter(filtered_df,x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55,title = 'My Graph')
    fig.update_layout(transition_duration = 500) 
    return fig    
    
               


if __name__ == '__main__':
    app.run_server(debug=True)