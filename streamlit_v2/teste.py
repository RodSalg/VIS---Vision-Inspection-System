import dash
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash_html_components import Button
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from PIL import Image, ImageDraw
import io
import base64

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Software de Marcação de Imagens"),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Arraste e solte ou ',
            html.A('selecione a imagem')
        ]),
        multiple=False
    ),
    html.Div([
        dcc.Graph(id='image-display', config={'editable': True, 'scrollZoom': False}),
    ]),
    dbc.Button("Limpar Marcações", id="clear-button", color="danger", className="mt-3"),
    html.Div(id='bounding-box-coordinates', className="mt-3"),
])

# Função para converter imagem em base64
def encode_image(image_path):
    img = Image.open(image_path)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"

def parse_contents(contents):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    image = Image.open(io.BytesIO(decoded))
    return image

@app.callback(
    Output('image-display', 'figure'),
    Output('bounding-box-coordinates', 'children'),
    Input('upload-image', 'contents'),
    State('image-display', 'relayoutData'),
)
def update_image(content, relayoutData):
    if content is None:
        raise PreventUpdate

    image = parse_contents(content)

    if relayoutData is not None and 'xaxis.range[0]' in relayoutData:
        x_range = [relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']]
        y_range = [relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']]
    else:
        x_range, y_range = [0, image.width], [0, image.height]

    fig = {
        'data': [],
        'layout': {
            'xaxis': {'range': x_range},
            'yaxis': {'range': y_range},
            'images': [{
                'x': 0,
                'y': image.height,
                'sizex': image.width,
                'sizey': image.height,
                'source': encode_image(image),
                'xref': 'x',
                'yref': 'y',
                'layer': 'below',
            }],
            'shapes': [],
        },
    }

    return fig, ""

# Callback para adicionar bounding box
@app.callback(
    Output('image-display', 'relayoutData'),
    Output('bounding-box-coordinates', 'children'),
    Input('image-display', 'relayoutData'),
    Input('clear-button', 'n_clicks'),
    prevent_initial_call=True,
)
def draw_bounding_box(relayoutData, clear_button_clicks):
    ctx = dash.callback_context

    if not ctx.triggered_id or 'clear-button' in ctx.triggered_id:
        raise PreventUpdate

    if 'shapes' not in relayoutData:
        relayoutData['shapes'] = []

    draw = ImageDraw.Draw(parse_contents(ctx.inputs['image-display.contents']))

    for shape in relayoutData['shapes']:
        if 'type' in shape and shape['type'] == 'rect':
            coords = shape['x0'], shape['y0'], shape['x1'], shape['y1']
            draw.rectangle(coords, outline='red', width=2)

    # Atualiza as coordenadas do bounding box
    bounding_box_coordinates = [f"{shape['x0']},{shape['y0']},{shape['x1']},{shape['y1']}" for shape in relayoutData['shapes'] if 'type' in shape and shape['type'] == 'rect']

    return relayoutData, f"Bounding Box Coordenadas: {', '.join(bounding_box_coordinates)}"

if __name__ == '__main__':
    
    app.run_server(debug=True)
