
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


mkbKeysAndValues={
    'vector_or_cross_product':'⨯','medium_small_white_circle':'⚬','hyphen':'-',
    'metrical_breve':'⏑','metrical_long_over_short':'⏒','metrical_short_over_long':'⏓',
    'metrical_two_shorts_joined':'⏖','theta':'θ','metrical_long_over_two_shorts':'⏔',
    'metrical_two_shorts_over_long':'⏕','sup_1':'¹','sup_2':'²','sup_3':'³','sup_4':'⁴',
    'sup_5':'⁵','sup_6':'⁶','bar_1':'|','bar_2':'‖',
    'bar_3':'⦀','dotted_bar':'⋮','dashed_bar':'┋'
}


def greek_kbd():
    return  [
            html.Div(id='kbFirstLine',children=[
            dbc.Button(id="theta",children="θ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="omega",children="ω", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="epsilon",children="ε", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="rho",children="ρ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="tau",children="τ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="psi",children="ψ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="upsilon",children="υ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="omicron",children="ο", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="iota",children="ι", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="pi",children="π", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="backspace",children="⌫", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"})
            ],
            style={"paddingTop":"3pt",'display':'flex', 'flex-direction':'row','justify-content':'center'}),
        html.Div(id='kbSecondLine',children=[
            dbc.Button(id="alpha",children="α", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="sigma",children="σ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="delta",children="δ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="phi",children="φ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="gamma",children="γ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="eta",children="η", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="stigma",children="ς", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="kappa",children="κ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="lambda",children="λ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"})
        ],style={"paddingTop":"3pt",'display':'flex', 'flex-direction':'row','justify-content':'center'}),
        html.Div(id='kbThirdLine',children=[
            dbc.Button(id="zeta",children="ζ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="chi",children="χ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="xi",children="ξ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="beta",children="β", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="nu",children="ν", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="mu",children="μ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"})
    ],style={"paddingTop":"3pt",'display':'flex', 'flex-direction':'row','justify-content':'center'}),
        html.Div(id='specsymb',children=[
            dbc.Button(id="space",children=" ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace","width":"12em"}),
            dbc.Button(id="changecase",children='⇧', color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"})
        ],style={"paddingTop":"3pt",'display':'flex', 'flex-direction':'row','justify-content':'center'})
    ]

def metric_kbd():
    return  [
            html.Div(id='mkbFirstLine',children=[
            dbc.Button(id="vector_or_cross_product",children="⨯", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="medium_small_white_circle",children="⚬", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="hyphen",children="-", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="metrical_breve",children="⏑", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="metrical_long_over_short",children="⏒", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="metrical_short_over_long",children="⏓", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="metrical_two_shorts_joined",children="⏖", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="metrical_long_over_two_shorts",children="⏔", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="metrical_two_shorts_over_long",children="⏕", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="mbackspace",children="⌫", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"})
            ],
            style={"paddingTop":"3pt",'display':'flex', 'flex-direction':'row','justify-content':'center'}),
        html.Div(id='mkbSecondLine',children=[
            dbc.Button(id="accent",children="´", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="sup_1",children="¹", color="dark", outline=True, size="md", className="me-md-1",style={'text-decoration':'underline',"fontFamily": "monospace"}),
            dbc.Button(id="sup_2",children="²", color="dark", outline=True, size="md", className="me-md-1",style={'text-decoration':'underline',"fontFamily": "monospace"}),
            dbc.Button(id="sup_3",children="³", color="dark", outline=True, size="md", className="me-md-1",style={'text-decoration':'underline',"fontFamily": "monospace"}),
            dbc.Button(id="sup_4",children="⁴", color="dark", outline=True, size="md", className="me-md-1",style={'text-decoration':'underline',"fontFamily": "monospace"}),
            dbc.Button(id="sup_5",children="⁵", color="dark", outline=True, size="md", className="me-md-1",style={'text-decoration':'underline',"fontFamily": "monospace"}),
            dbc.Button(id="sup_6",children="⁶", color="dark", outline=True, size="md", className="me-md-1",style={'text-decoration':'underline',"fontFamily": "monospace"}),
            dbc.Button(id="tilda",children="~", color="dark", outline=True, size="md", className="me-md-1",style={'text-decoration':'underline',"fontFamily": "monospace"})
        ],style={"paddingTop":"3pt",'display':'flex', 'flex-direction':'row','justify-content':'center'}),
        html.Div(id='mkbThirdLine',children=[
            dbc.Button(id="bar_1",children="|", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="bar_2",children="‖", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace"}),
            dbc.Button(id="bar_3",children="⦀", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace", "width":"2.2em"}),
            dbc.Button(id="dotted_bar",children="⋮", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace", "width":"2.2em"}),
            dbc.Button(id="dashed_bar",children="┋", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace", "width":"2.3em"})
    ],style={"paddingTop":"3pt",'display':'flex', 'flex-direction':'row','justify-content':'center'}),
        html.Div(id='mspecsymb',children=[
            dbc.Button(id="mspace",children=" ", color="dark", outline=True, size="md", className="me-md-1", style={"fontFamily": "monospace", "width":"12em", "height":"2.25em"})
        ], style={"paddingTop":"3pt",'display':'flex', 'flex-direction':'row','justify-content':'center'})
    ]

