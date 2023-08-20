import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = dash.Dash(__name__)

# Load sample data from a CSV file
csv_file = 'sample_data.csv'
data = pd.read_csv(csv_file)

# Available chart types
chart_types = ['Bar Chart', 'Scatter Plot', 'Line Chart', 'Pie Chart', 'Histogram', 'Box Plot', 'Violin Plot']

app.layout = html.Div([
    html.H1("Interactive Data Visualization Dashboard"),
    
    dcc.Dropdown(
        id='chart-type-dropdown',
        options=[{'label': chart_type, 'value': chart_type} for chart_type in chart_types],
        value='Bar Chart',
        multi=False,
        searchable=False
    ),
    
    dcc.Graph(id='selected-chart')
])

def update_data():
    global data
    data = pd.read_csv(csv_file)

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.csv'):
            update_data()

observer = Observer()
observer.schedule(FileChangeHandler(), path='.', recursive=False)
observer.start()

@app.callback(
    Output('selected-chart', 'figure'),
    [Input('chart-type-dropdown', 'value')]
)
def update_selected_chart(selected_chart_type):
    if selected_chart_type == 'Bar Chart':
        chart = px.bar(data, x='Category', y='Value', title='Bar Chart')
    elif selected_chart_type == 'Scatter Plot':
        chart = px.scatter(data, x='X', y='Y', title='Scatter Plot')
        chart.update_layout(
            xaxis_title='X',
            yaxis_title='Y',
            coloraxis_showscale=False  # Disable color scale to improve interactivity
        )
    elif selected_chart_type == 'Line Chart':
        chart = px.line(data, x='X', y='Value', title='Line Chart')
    elif selected_chart_type == 'Pie Chart':
        chart = px.pie(data, names='Category', values='Value', title='Pie Chart')
    elif selected_chart_type == 'Histogram':
        chart = px.histogram(data, x='Value', title='Histogram')
    elif selected_chart_type == 'Box Plot':
        chart = px.box(data, x='Category', y='Value', title='Box Plot')
    elif selected_chart_type == 'Violin Plot':
        chart = px.violin(data, x='Category', y='Value', title='Violin Plot')

    return chart

if __name__ == '__main__':
    app.run_server(debug=True)
