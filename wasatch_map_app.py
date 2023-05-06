import dash as dash
import dash_leaflet.express as dlx
import dash_leaflet as dl
from dash_extensions.enrich import html

ind = []
image_bounds = []
urls = []

# the images extend slightly beyond the stated coordinate bounds, so overlap margins are identified to prevent repeating portions of images.
w_mrgn = 0.004
h_mrgn = 0.003

# aggregate map display info, including prediction maps, the coordinate bounds for each, and an index array for iteration
for i in range(144):
    ind.append(i)
    with open('mysite/assets/coordinates/' + str(i) + '.txt') as f:
        lines = f.readlines()
        co = lines[0].split(',')
        # [[S, W], [N, E]]
        image_bounds.append([[float(co[0])-h_mrgn,float(co[1])-w_mrgn],[float(co[2])+h_mrgn,float(co[3])+w_mrgn]])
    urls.append('/static/images/' + str(i) + '.jpg')

categories = ["Maple", "Aspen", "Oak", "Conifer", "Other", "None"]
colorscale = ['#FF0000', '#FFFF00', '#FFA500', '#006400', '#32CD32', '#F5F5DC']
colorbar = dlx.categorical_colorbar(categories=categories, colorscale=colorscale, width=300, height=30, position="bottomleft")

# create dash app
app = dash.Dash()

# create layout, including default tile layer as base map, overlay images, and colorbar legend
app.layout = html.Div(children=[
    html.H1(children='Wasatch Forests', style={'font-family': 'monospace'}),
    dl.Map(children=[
        dl.LayersControl(
            [dl.TileLayer()] +
            [dl.ImageOverlay(opacity=1.0, url=urls[i], bounds=image_bounds[i]) for i in ind]
        ), colorbar
    ], zoom=9, center=(40.75, -111.75)
)], style={'width': '95vw', 'height': '90vh', 'margin': "auto", "display": "block"})

if __name__ == '__main__':
    app.run_server()