# -*- coding: utf-8 -*-

import dash

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=['/assets/style.css'],
                title='DASH APP',
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=0.5"}]
)
server = app.server
