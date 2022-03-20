# -*- coding: utf-8 -*-
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table as dt
from dash.dependencies import ClientsideFunction, Input, Output, State
# from dash.exceptions import PreventUpdate
from pymongo import MongoClient as MC
from alienkbd import greek_kbd, metric_kbd
import json as j
import bson.json_util as bj
import re
from datetime import datetime as dtm
import uploadfile as uf 


volMenuKeyAndValues={
    'volTotum':'Totum',
    'volHipponax':'Hipponax',
    'volSappho':'Sappho...'
    }

zoneMenuKeyAndValues={
    'titleChoice':'Заголовок',
    'subtitleChoice':'Подзаголовок',
    'schemeChoice':'Схема',
    'rithmChoice':'Ритм',
    'srcChoice':'Оригинал',
    'transChoice':'Перевод'
}



preQueryKeyAndValues={
    'Totum':'totum',
    'Hipponax':'hipponax',
    'Sappho...':'sappho',
    'Заголовок':'titles',
    'Подзаголовок':'subtitles',
    'Схема':'scheme',
    'Ритм':'verse.rhythm',
    'Оригинал':'verse.src',
    'Перевод':'verse.trans.text',
    'Все':'all_pauses',
    'Жесткие':'hard_pauses',
    'Нет':'no_pauses',
    'Совпадение':'coinside',
    'Текст':'text',
    'Включение':'include',
    'any_condition':'$and',
    'some_condition':'$or',
    'number_list':'list',
    'define_formula':'formula',
    'all_zones':'content.markdown',
    'some_zones':'form_list_of_zones',
    'number_only':'count',
    'group_data':'group',
    'titleCheck':'titles',
    'subtitleCheck':'subtitles',
    'schemeCheck':'scheme',
    'rithmCheck':'verse.rhythm',
    'srcCheck':'verse.src',
    'transCheck':'verse.trans.text',
    '':'',
}


Greek_Letters_And_Diacritics={
    'Ι':'[ΙἼ]',
    'α':'[αάἀἂἄἆὰάᾶ]',
    'ε':'[εέἐἑἒἔὲέ]',
    'η':'[ηήἠἢἤἦὴήῆ]',
    'ι':'[ιίϊἰἴἶὶίῐΐῖ]',
    'ο':'[οόὀὂὄὸό]',
    'ρ':'[ρῤ]',
    'υ':'[υϋύὐὔὖὺύῦΰ]',
    'ω':'[ωὠὢὤὦὼώῶ]',
}


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.FONT_AWESOME,dbc.icons.BOOTSTRAP])

server=app.server

app.title="Древнейшие стихоложения мира"
app.config.suppress_callback_exceptions=True

Main_footer=html.Footer(children='Работа над проектом поддержана грантом РНФ № 18-18-00503 «Древнейшие стихосложения мира: от шумеров к грекам».',
        style={'width':'90%','height':'2%','color':'royalblue','font-size':'1.2em', 'font-style':'italic',
        'align-items': 'bottom','margin-left':'auto','margin-right':'auto','margin-top':'2em', 
        'margin-bottom':'2em'})


def This_project():
    mc=MC()
    db=mc['sumer_2_greek']
    col=db['doc_md']
    d1=col.find_one({'id_doc':'site_docs_0000'})
    About_the_project=d1['text']
    mc.close()
    return html.Div(children=[
        dcc.Markdown(id="This_project",children=About_the_project,
        style={'width':'90%','margin-left':'auto','margin-right':'auto'}), Main_footer
    ])


def The_report():
    mc=MC()
    db=mc['sumer_2_greek']
    col=db['doc_md']
    d2=col.find_one({'id_doc':"site_docs_0001"})
    About_the_site=d2['text']
    mc.close()
    return html.Div(children=[
        dcc.Markdown(id="This_project",children=About_the_site,
        style={'width':'90%','margin-left':'auto','margin-right':'auto'}), Main_footer
    ])


def The_pubs():
    return html.Div(children=[
        html.Div(
        html.H1("Публикации за 2019 год"),
        style={'width':'90%','margin-left':'auto','margin-right':'auto'}), Main_footer
    ])


def Search_wizard():
    return html.Div(
        id='searchWizard',
        children=[
            dbc.Alert(
                id='volChoice',
                color='primary',
                children=[
                    html.Div(
                        id='1stRow',
                        children=[
                            html.Div(
                                id='zonevolContainer',
                                children=[
                                    html.Div(
                                        id='volContainer',
                                        children=[
                                            dbc.Select(
                                                id='volChoiceMenu',
                                                size='md',
                                                style={'width':'12em'},
                                                options=[
                                                    {'value':'volTotum', 'label':'Totum'},
                                                    {'value':'volHipponax', 'label':'Hipponax','disabled':True},
                                                    {'value':'volSappho','label':'Sappho...','disabled':True}
                                                ],
                                                placeholder='Коллекция', 
                                            )
                                        ],
                                        style={'padding-left':'4pt','margin-right':'20pt','margin-bottom':'5pt'}
                                    ),
                                    html.Div(
                                        id='zoneContainer',
                                        children=[
                                            dbc.Select(
                                                id='zoneChoiceMenu',
                                                size='md',
                                                style={'width':'12em'},
                                                options=[
                                                    {'value':'titleChoice', 'label':'Заголовок'},
                                                    {'value':'subtitleChoice', 'label':'Подзаголовок'},
                                                    {'value':'schemeChoice', 'label':'Схема'},
                                                    {'value':'rithmChoice', 'label':'Ритм строки'},
                                                    {'value':'srcChoice', 'label':'Оригинал'},
                                                    {'value':'transChoice', 'label':'Перевод'},
                                                ],
                                                placeholder='Зона поиска', 
                                            )
                                        ],
                                        style={'padding-left':'4pt','margin-right':'20pt'}
                                    ),
                                ],
                                style={'display':'flex','flex-direction':'column','justify-content':'flex-start','align-items':'stretch'}
                            ),
                            html.Div(
                                id='hiddenContainer',
                                children=[
                                    dbc.Input(id="inputmode",value="lowercase",type="hidden"),
                                    dbc.Input(id="lastkeyid",value="",type="hidden"),
                                    dbc.Input(id="searchmode",value="regex",type="hidden"),
                                    dbc.Input(id='currentCondition',value="0",type="hidden"),
                                    dbc.Input(id='OkErrorSwith',value='',type='hidden'),
                                    dbc.Input(id='lastOueryType',value='',type='hidden'),
                                    dbc.Input(id='queryRusultSize',value='0',type='hidden'),
                                ],
                                style={'display':'none'}
                            ),
                            html.Div(
                                id='twoButtonRowsContainer',
                                children=[
                                    html.Div(
                                        id='zoneButtonContainer01',
                                        children=[
                                            dbc.ButtonGroup(
                                                id='searchControlGroup01',
                                                children=[
                                                    dbc.Button(id='virtualKeyBoardButton',children=[html.I(className='fa fa-keyboard text-white')],color='primary',n_clicks=0,disabled=True,style={'font-family':'monospace','width':'3em'}),
                                                    dbc.Button(id='magicButton',children=[html.I(className='fa fa-magic text-white')],color='primary',n_clicks=0,disabled=True,style={'font-family':'sans-serif','width':'3em'}),
                                                    dbc.Button(
                                                        id='allWordSection',
                                                        children='',
                                                        color='info',
                                                        n_clicks=0,
                                                        disabled=True,
                                                        style={
                                                            'background-image':'url("assets/all_breaks_test.svg")',
                                                            'background-repeat':'no-repeat', 
                                                            'background-position':'center',
                                                            'background-size':'22%',
                                                            'width':'3em'
                                                        },
                                                    ),
                                                    dbc.Button(
                                                        id='softWordSectionFree',
                                                        children='',
                                                        color='primary',
                                                        n_clicks=0,
                                                        disabled=True,
                                                        style={
                                                            'background-image':'url("assets/strong_breaks_test.svg")',
                                                            'background-repeat':'no-repeat', 
                                                            'background-position':'center',
                                                            'background-size':'8%',
                                                            'width':'3em'
                                                        },
                                                    ),
                                                    dbc.Button(
                                                        id='wordSectionFree',
                                                        children='',
                                                        color='primary',
                                                        n_clicks=0,
                                                        disabled=True,
                                                        style={
                                                            'background-image':'url("assets/no_breaks_test.svg")',
                                                            'background-repeat':'no-repeat', 
                                                            'background-position':'center 80%',
                                                            'background-size':'55%',
                                                            'width':'3em'
                                                        },
                                                    ),
                                                    dbc.Button(id='helpButton', children=[html.I(className='fa fa-question text-white')],color='primary', disabled=False,n_clicks=0,style={'font-family':'serif','width':'3em'}),
                                                ],
                                            ),
                                            dbc.Tooltip('Виртуальная клавиатура',target='virtualKeyBoardButton',placement='bottom'),
                                            dbc.Tooltip('"Волшебная палочка": "превращение" макрокодов в греческие буквы или метрические символы',target='magicButton',placement='bottom'),
                                            dbc.Tooltip('Учитываются все словоразделы',target='allWordSection',placement='bottom'),
                                            dbc.Tooltip('Учтываются только жесткие словоразделы',target='softWordSectionFree',placement='bottom'),
                                            dbc.Tooltip('Поиск без всех словоразделов',target='wordSectionFree',placement='bottom'),
                                            dbc.Tooltip('Справка по макрокодам',target='helpButton',placement='bottom'),
                                        ],
                                        style={'margin-bottom':'5pt'}
                                    ),
                                    html.Div(
                                        id='zoneButtonContainer02',
                                        children=[
                                            dbc.ButtonGroup(
                                                id='searchControlGroup02',
                                                children=[
                                                    dbc.Button(
                                                        id='exactSearch',
                                                        children=[html.I(className='fa fa-equals text-white')],
                                                        color='primary',
                                                        n_clicks=0,
                                                        disabled=False,
                                                        style={'font-family':'monospace','width':'3em'}
                                                    ),
                                                    dbc.Button(
                                                        id='textSearch',
                                                        children='',
                                                        color='primary',
                                                        n_clicks=0,
                                                        disabled=True,
                                                        style={
                                                            'background-image':'url("assets/text_test.svg")',
                                                            'background-repeat':'no-repeat', 
                                                            'background-position':'center',
                                                            'background-size':'70%',
                                                            'width':'3em',
                                                        },
                                                    ),
                                                    dbc.Button(id='addCondition',children=[html.I(className='fa fa-edit text-white')],color='primary',n_clicks=0, disabled=True,style={'font-family':'monospace','width':'3em'}),
                                                    dbc.Button(id='execQuery', children=[html.I(className='fa fa-search text-white')],color='primary', disabled=True,n_clicks=0,style={'font-family':'monospace','width':'3em'}),
                                                    dbc.Button(id='saveQueryButton', children=[html.I(className='fa fa-save text-white')],color='primary',disabled=True,n_clicks=0,style={'font-family':'monospace','width':'3em'}),
                                                    dbc.Button(id='openQueryButton', children=[html.I(className='fa fa-folder-open text-white')],color='primary',disabled=True,n_clicks=0,style={'font-family':'monospace','width':'3em'}),
                                                ],
                                            ),
                                            dbc.Tooltip('Поиск по точному совпадению',target='exactSearch',placement='bottom'),
                                            dbc.Tooltip('Полнотекстовый поиск',target='textSearch',placement='bottom'),
                                            dbc.Tooltip('Записать условие поиска',target='addCondition',placement='bottom'),
                                            dbc.Tooltip('Искать (выполнить запрос)',target='execQuery',placement='bottom'),
                                            dbc.Tooltip('Открыть запрос',target='openQueryButton',placement='bottom'),
                                            dbc.Tooltip('Сохранить запрос',target='saveQueryButton',placement='bottom'),
                                        ],
                                    ),
                                ],
                                style={'display':'flex','flex-direction':'column','justify-content':'flex-start','align-items':'stretch'}
                            )
                        ],
                        style={'display':'flex','flex-direction':'row','justify-content':'space-between','align-items':'flex-start','margin-bottom':'10pt'}
                    ),
                    html.Div(
                        id='2ndRow',
                        children=[
                            html.Div(
                                id='zonesearchContainer',
                                children=[
                                    dbc.Input(
                                        id="main_input",
                                        placeholder="Шаблон поиска...",
                                        type="search",
                                        autoFocus=True,
                                        value="", 
                                        size="md",
                                        html_size=46,
                                        style={"height":"2em","fontFamily":"monospace"}
                                    ),
                                    html.Div(
                                        id='zone_greek_keyboard',
                                        children=greek_kbd(),
                                        style={'display':'none'}
                                    ),
                                    html.Div(
                                        id='zone_metric_keyboard',
                                        children=metric_kbd(),
                                        style={'display':'none'}
                                    )
                                ],
                                style={'display':'block'}
                            ),

                        ],
                        style={'display':'flex','flex-direction':'row','justify-content':'center','align-items':'flex-start'}
                    )
                ],
                style={'display':'flex','flex-direction':'column','justify-content':'center'},
            ),
            dbc.Accordion(
                id='conditionStore',
                children=[
                    dbc.AccordionItem(
                        id='conditionStoreContent',
                        children=[
                            dt.DataTable(
                                id='conditionStoreDT',
                                columns=[
                                    {"name": 'Номер', "id":'id' },
                                    {"name": 'Коллекция', "id":'col_name' },
                                    {"name": 'Зона', "id":'zone_name' },
                                    {"name": 'Шаблон', "id":'pattern' },
                                    {"name": 'Словоразделы', "id":'word_section' },
                                    {"name": 'Поиск', "id":'compare_mode' },
                                ],
                                data=[
                                ],
                                style_cell={'text-align': 'center','padding-left':'1em','padding-right':'1em'},
                                style_header={
                                    'font-weight': 'bold',
                                },
                                cell_selectable=False,
                                style_cell_conditional=[
                                    {
                                        'if': {'column_id': 'id'},
                                        'text-align': 'right',
                                        'width':'6%',
                                    },
                                    {
                                        'if': {'column_id': 'col_name'},
                                        'width':'12%',
                                    },
                                    {
                                        'if': {'column_id': 'zone_name'},
                                        'width':'12%',
                                    },
                                    {
                                        'if': {'column_id': 'word_section'},
                                        'width':'12%',
                                    },
                                    {
                                        'if': {'column_id': 'compare_mode'},
                                        'width':'12%',
                                    },                                      
                                ],
                                row_deletable=True,
                            ),
                            html.Div(
                                id='buttonClearConditionListContainer',
                                children=[
                                    dbc.Button(
                                        id='buttonClearConditionList',
                                        children='Очистить список и обнулить счетчик условий',
                                        size='sm',
                                    ),                                    
                                ],
                                style={'display':'none'},                               
                            ),
                            html.Div(
                                id='viewFormatContainer',
                                children=[
                                    html.Div(
                                        id='AllSomeNumber',
                                        children='Выполнены все условия:',
                                        style={'margin-right':'2em'}
                                    ),
                                    html.Div(
                                        id='ZoneModeView',
                                        children='Все зоны:',
                                        style={}
                                    ),
                                    html.Div(
                                        id='GroupOrNo',
                                        children='',
                                        style={}
                                    ),
                                    html.Div(
                                        id='ZonesView',
                                        children='',
                                        style={}
                                    ),
                                ],
                                style={'display':'flex','flex-direction':'row','justify-content':'center','margin-top':'1em'},
                            )
                        ],
                        title='Сохраненные условия поиска:',
                    ),
                    dbc.AccordionItem(
                        id='outputForm',
                        title='Определение формата вывода данных',
                        children=[
                            html.Div(
                                id='outputFormContainer',
                                children=[
                                    html.Div(
                                        id='outputConditionCoiceContainer',
                                        children=[
                                            dbc.Label('Вывод данных'),
                                            dbc.RadioItems(
                                                id='outputСonditionChoice',
                                                options=[
                                                    {'label':'Выполнены все условия','value':'any_condition'},
                                                    {'label':'Выполнено хотя бы одно условие','value':'some_condition'},
                                                    {'label':'Список чисел','value':'number_list','disabled':True},
                                                    {'label':'Задать формулу','value':'define_formula','disabled':True},
                                                ],
                                                value='any_condition',
                                            )
                                        ],
                                        style={'border':'1px solid lightgray','border-radius':'3pt','margin':'5pt','padding':'10pt'},
                                    ),
                                    html.Div(
                                        id='outputZoneModeChoiceContainer',
                                        children=[
                                            dbc.Label('Выбор режима вывода зон'),
                                            dbc.RadioItems(
                                                id='outputZoneModeChoice',
                                                options=[
                                                    {'label':'Все зоны','value':'all_zones'},
                                                    {'label':'Выборочно','value':'some_zones','disabled':True},
                                                    {'label':'Количество','value':'number_only'},
                                                ],
                                                value='all_zones',
                                            ),
                                            dbc.Checklist(
                                                id='outputGroupCheckList',
                                                options=[
                                                    {'label':'Группировать','value':'group_data','disabled':True},
                                                ],
                                                value=[],
                                                switch=True,
                                            )
                                        ],
                                        style={'border':'1px solid lightgray','border-radius':'3pt','margin':'5pt','padding':'10pt'},
                                    ),
                                    html.Div(
                                        id='outputZoneChoiceContainer',
                                        children=[
                                            dbc.Label('Зоны для вывода'),
                                            dbc.Checklist(
                                                id='outputZoneChoice',
                                                options=[
                                                    {'label':'Заголовок','value':'titleCheck','disabled':True},
                                                    {'label':'Подзаголовок','value':'subtitleCheck','disabled':True},
                                                    {'label':'Схема','value':'schemeCheck','disabled':True},
                                                    {'label':'Ритм строки','value':'rithmCheck','disabled':True},
                                                    {'label':'Оригинал','value':'srcCheck','disabled':True},
                                                    {'label':'Перевод','value':'transCheck','disabled':True},
                                                ],
                                                value=[],
                                            )
                                        ],
                                        style={'border':'1px solid lightgray','border-radius':'3pt','margin':'5pt','padding':'10pt'},
                                    )
                                ],
                                style={'display':'flex','flex-direction':'row','justify-content':'center','align-items':'stretch'}    
                            )
                        ],
                    ),
                    dbc.AccordionItem(
                        id='queryResultList',
                        title='Результаты запроса',
                        children=[
                            html.Div(
                                id='saveResultsContainer',
                                children=[
                                    dbc.Button(
                                        id='saveQueryResults',
                                        children='Сохранить все результаты запроса', 
                                        n_clicks=0, 
                                        size='md', 
                                        color='primary', 
                                        style={'margin-right':'5pt','margin-bottom':'10pt'},
                                    ),
                                    dbc.Button(
                                        id='saveResultPage',
                                        children='Сохранить текущую страницу результатов', 
                                        n_clicks=0, 
                                        size='md', 
                                        color='primary',
                                        disabled=False,
                                        style={'margin-left':'5pt','margin-bottom':'10pt'},
                                    ),
                                    # dbc.Tooltip('Сохранить все результаты запроса',target='saveQueryResults',placement='top'),
                                    # dbc.Tooltip('Сохранить текущую страницу результатов',target='saveResultPage',placement='top'),
                                ],
                                style={'display':'none'},
                            ),

                            dcc.Download(id="downloadQueryResults"),
                            dcc.Download(id="downloadCurrentPage"),
                            dbc.Pagination(
                                id='showPage',
                                first_last=True,
                                fully_expanded=False,
                                max_value=1,
                                active_page=1,
                                previous_next=True,
                                # size='sm',
                                style={'display':'none'},
                            ),
                            html.Div(
                                id='queryResultsContainer',
                                children=[
                                    html.H4(id='place4number',children='',style={'dispay':'none'}),
                                    html.H5(id='place4list',children='',style={'display':'none'}),
                                    dbc.ListGroup(
                                        id='listForOnePage',
                                        children=[
                                        ],
                                    ),
                                ],
                            ),
                            dbc.Modal(
                                id='queryOK',
                                children=[
                                    dbc.ModalHeader(dbc.ModalTitle('Запрос успешно выполнен')),
                                    dbc.ModalBody('Можно посмотреть результаты выполнения запроса'),
                                    dbc.ModalFooter(dbc.Button('Ok',id='OkButton')),
                                ],
                                is_open=False
                            ),
                            dbc.Modal(
                                id='queryERROR',
                                children=[
                                    dbc.ModalHeader(dbc.ModalTitle('При выполнении запроса произошла ошибка')),
                                    dbc.ModalBody('Можно попробовать обновить страницу'),
                                    dbc.ModalFooter(dbc.Button('Закрыть',id='ErrorButton')),
                                ],
                                is_open=False
                            ),
                            
                        ]
                    )
                ],
                start_collapsed=True,
            ),
            dbc.Offcanvas(
                id='helpPlace',
                children=[
                    html.Div(
                        children=[
                            html.H6('Макрокоды для метрических символов',),
                            dbc.Button(
                                id='metricSymbolsCollapse', 
                                children='Показать', 
                                n_clicks=0, 
                                outline=False, 
                                color='primary',
                                size='sm',
                                style={'width':'6em'},
                            ),
                        ],
                        style={
                            'margin-bottom':'1em',
                            'display':'flex',
                            'flex-direction':'row',
                            'justify-content':'space-between',
                            'align-items':'flex-start',
                        },
                    ),
                    dbc.Collapse(
                        children=[
                            dt.DataTable(
                                id='charTable01',
                                columns=[
                                    {"name": 'Номер', "id":'id' },
                                    {"name": 'Код', "id":'macro_code' },
                                    {"name": 'Символ', "id":'char_image' },
                                ],
                                data=[
                                    {'id':'1','macro_code':'U+U_','char_image':'⏕'},
                                    {'id':'2','macro_code':'U+U!','char_image':'⏔'},
                                    {'id':'3','macro_code':'U+U','char_image':'⏖'},
                                    {'id':'4','macro_code':'U_','char_image':'⏓'},
                                    {'id':'5','macro_code':'U!','char_image':'⏒'},
                                    {'id':'6','macro_code':'U','char_image':'⏑'},
                                    {'id':'7','macro_code':'1','char_image':'¹'},
                                    {'id':'8','macro_code':'2','char_image':'²'},
                                    {'id':'9','macro_code':'3','char_image':'³'},
                                    {'id':'10','macro_code':'4','char_image':'⁴'},
                                    {'id':'11','macro_code':'5','char_image':'⁵'},
                                    {'id':'12','macro_code':'6','char_image':'⁶'},
                                    {'id':'13','macro_code':'|_','char_image':'┋'},
                                    {'id':'14','macro_code':'|.','char_image':'⋮'},
                                    {'id':'15','macro_code':'|||','char_image':'⦀'},
                                    {'id':'16','macro_code':'||','char_image':'‖'},                                    
                                    {'id':'17','macro_code':'X','char_image':'⨯'},
                                    {'id':'18','macro_code':'O','char_image':'⚬'},
                                ],
                                style_cell={'text-align': 'center','padding-left':'1em','padding-right':'1em'},
                                style_header={
                                    'font-weight': 'bold',
                                },
                                cell_selectable=False,
                                style_cell_conditional=[
                                    {
                                        'if': {'column_id': 'id'},
                                        'text-align': 'right',
                                        'width':'20%',
                                    },
                                    {
                                        'if': {'column_id': 'macro_code'},
                                        'width':'40%',
                                    },
                                    {
                                        'if': {'column_id': 'char_image'},
                                        'width':'40%',
                                    },
                                ],
                                row_deletable=False,
                            ),
                        ],
                        id='charTableCollapse01',
                        is_open=False,
                    ),
                    html.Div(
                        children=[
                            html.H6('Макрокоды для греческих букв',),
                            dbc.Button(
                                id='greekLettersCollapse', 
                                children='Показать', 
                                n_clicks=0, 
                                outline=False, 
                                color='primary',
                                size='sm',
                                style={'width':'6em'},
                            ),
                        ],
                        style={
                            'margin-bottom':'1em', 
                            'margin-top':'2em', 
                            'display':'flex',
                            'flex-direction':'row',
                            'justify-content':'space-between',
                            'align-items':'flex-start',
                        },
                    ),
                    dbc.Collapse(
                        children=[
                            dt.DataTable(
                                id='charTable02',
                                columns=[
                                    {"name": 'Номер', "id":'id' },
                                    {"name": 'Код', "id":'macro_code' },
                                    {"name": 'Символ', "id":'char_image' },
                                ],
                                data=[
                                    {'id':'1','macro_code':'A','char_image':'Α'},
                                    {'id':'2','macro_code':'B','char_image':'Β'},
                                    {'id':'3','macro_code':'G','char_image':'Γ'},
                                    {'id':'4','macro_code':'D','char_image':'Δ'},
                                    {'id':'5','macro_code':'E','char_image':'Ε'},
                                    {'id':'6','macro_code':'Z','char_image':'Ζ'},
                                    {'id':'7','macro_code':'H','char_image':'Η'},
                                    {'id':'8','macro_code':'Q','char_image':'Θ'},
                                    {'id':'9','macro_code':'I','char_image':'Ι'},
                                    {'id':'10','macro_code':'K','char_image':'Κ'},
                                    {'id':'11','macro_code':'L','char_image':'Λ'},
                                    {'id':'12','macro_code':'M','char_image':'Μ'},
                                    {'id':'13','macro_code':'N','char_image':'Ν'},
                                    {'id':'14','macro_code':'J','char_image':'Ξ'},
                                    {'id':'15','macro_code':'O','char_image':'Ο'},
                                    {'id':'16','macro_code':'P','char_image':'Π'},                                    
                                    {'id':'17','macro_code':'R','char_image':'Ρ'},
                                    {'id':'18','macro_code':'S','char_image':'Σ'},
                                    {'id':'19','macro_code':'T','char_image':'Τ'},
                                    {'id':'20','macro_code':'Y','char_image':'Υ'},
                                    {'id':'21','macro_code':'F','char_image':'Φ'},
                                    {'id':'22','macro_code':'X','char_image':'Χ'},
                                    {'id':'23','macro_code':'C','char_image':'Ψ'},
                                    {'id':'24','macro_code':'W','char_image':'Ω'},
                                    {'id':'25','macro_code':'a','char_image':'α'},
                                    {'id':'26','macro_code':'b','char_image':'β'},
                                    {'id':'27','macro_code':'g','char_image':'γ'},
                                    {'id':'28','macro_code':'d','char_image':'δ'},
                                    {'id':'29','macro_code':'e','char_image':'ε'},
                                    {'id':'30','macro_code':'z','char_image':'ζ'},
                                    {'id':'31','macro_code':'h','char_image':'η'},
                                    {'id':'32','macro_code':'q','char_image':'θ'},
                                    {'id':'33','macro_code':'i','char_image':'ι'},
                                    {'id':'34','macro_code':'k','char_image':'κ'},
                                    {'id':'35','macro_code':'l','char_image':'λ'},
                                    {'id':'36','macro_code':'m','char_image':'μ'},
                                    {'id':'37','macro_code':'n','char_image':'ν'},
                                    {'id':'38','macro_code':'j','char_image':'ξ'},
                                    {'id':'39','macro_code':'o','char_image':'ο'},
                                    {'id':'40','macro_code':'p','char_image':'π'},
                                    {'id':'41','macro_code':'r','char_image':'ρ'},
                                    {'id':'42','macro_code':'s','char_image':'σ'},
                                    {'id':'43','macro_code':'t','char_image':'τ'},
                                    {'id':'44','macro_code':'y','char_image':'υ'},
                                    {'id':'45','macro_code':'f','char_image':'φ'},
                                    {'id':'46','macro_code':'x','char_image':'χ'},
                                    {'id':'47','macro_code':'c','char_image':'ψ'},
                                    {'id':'48','macro_code':'w','char_image':'ω'},
                                    {'id':'49','macro_code':'$','char_image':'ς'},
                                ],
                                style_cell={'text-align': 'center','padding-left':'1em','padding-right':'1em'},
                                style_header={
                                    'font-weight': 'bold',
                                },
                                cell_selectable=False,
                                style_cell_conditional=[
                                    {
                                        'if': {'column_id': 'id'},
                                        'text-align': 'right',
                                        'width':'20%',
                                    },
                                    {
                                        'if': {'column_id': 'macro_code'},
                                        'width':'40%',
                                    },
                                    {
                                        'if': {'column_id': 'char_image'},
                                        'width':'40%',
                                    },
                                ],
                                row_deletable=False,
                            ),                
                        ],
                        id='charTableCollapse02',
                        is_open=False,
                    ),
                ],
                placement='start',
                is_open=False,
            ),
            # html.Div(
            #     id='debugging_place',
            #     children=[
            #         html.H4('Debug'),
            #         dcc.Markdown(
            #             id='debug_text',
            #             children='',
            #         )
            #     ],
            #     style={'margin':'10pt','padding':'10pt'}
            # )
        ]
    )

def Under_construction(t):
    return dbc.Alert(
        children=[
            html.Div(
                children=[
                    html.H1(t+' находится в стадии разработки!'),
                    html.Div(
                        children=[
                            html.Img(src=app.get_asset_url('images/under_construction.png')),
                        ],
                        style={'margin-top':'30pt','margin-bottom':'30pt'}
                    ),  
                ],
            ),                     
        ],
        color='primary',
    )


def Some_utility():
    return html.Div(
        id='some_utility_view',
        children=[
            dbc.Accordion(
                id='various_utility',
                children=[
                    dbc.AccordionItem(
                        id='browse_md_file',
                        title='Просмотр файла .MD',
                        children=[
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dcc.Upload(
                                                html.Div(
                                                    dbc.Button(
                                                        [html.I(className='fa fa-folder-open text-white')], 
                                                        color="primary",
                                                        id='open_md_file',
                                                        n_clicks=0,
                                                        style={'font-family':'monospace','font-weight':'bold',}
                                                    ),
                                                ),
                                                id='my_md_file',
                                            ),
                                            # dbc.Spinner(
                                            #     id='load_md_spinner',
                                            #     color='primary',
                                            #     size='md',
                                            #     spinner_style={'display':'none'}
                                            # ),
                                            dbc.Button(
                                                        [html.I(className='fa fa-folder text-white')], 
                                                        color="primary",
                                                        id='close_md_file',
                                                        n_clicks=0,
                                                        style={'font-family':'monospace','font-weight':'bold',},
                                            ),
                                        ],
                                        style={'display':'flex','flex-direction':'row','justify-content':'space-between'}
                                    ),
                                    dcc.Markdown(
                                        children='',
                                        id='md_file_for_browsing', 
                                        dangerously_allow_html=True,
                                        style={"margin-top":"10pt","margin-left":"20pt","margin-right":"20pt","margin-bottom":"10pt"},
                                    ),
                                    dbc.Tooltip('Открыть файл .MD', target='open_md_file', placement='right'),
                                    dbc.Tooltip('Закрыть файл .MD', target='close_md_file', placement='left'), 
                                ],
                            )                       
                        ],
                    ),
                    dbc.AccordionItem(
                        id='edit_json',
                        title='Просмотр и редактирование файла .JSON',
                        children=[
                            html.Div(
                                id='edit_json_button_container',
                                children=[
                                    html.Div(
                                        children=[
                                            dcc.Upload(
                                                dbc.Button(
                                                    id='open_JSON', 
                                                    children=[html.I(className='fa fa-folder-open text-white')],
                                                    color='primary',
                                                    disabled=False,
                                                    n_clicks=0,
                                                ), 
                                                id='my_JSON_file', 
                                                accept='application/json',
                                            ),
                                            dbc.Button(
                                                id='close_JSON',
                                                children=[html.I(className='fa fa-folder text-white')],
                                                color='primary',
                                                disabled=False,
                                                n_clicks=0,
                                                style={'margin-left':'4px'},
                                            ),
                                        ],
                                        style={
                                            'display':'flex',
                                            'flex-direction':'row',
                                            'justify-content':'flex-start',
                                        },
                                    ),
                                    dbc.Button(
                                        id='save_JSON',
                                        children=[html.I(className='fa fa-save text-white')],
                                        color='primary',
                                        disabled=False,
                                        n_clicks=0,
                                    ),
                                ],
                                style={'display':'flex','flex-direction':'row','justify-content':'space-between'},
                            ),
                            dbc.Tooltip('Открыть файл .JSON',target='open_JSON',placement='bottom'),
                            dbc.Tooltip('Закрыть файл .JSON',target='close_JSON',placement='bottom'),
                            dbc.Tooltip('Сохранить файл .JSON',target='save_JSON',placement='left'),
                            html.Div(
                                children=[
                                    dbc.Textarea(
                                        id='my_JSON_area',
                                        value='',
                                        placeholder='JSON...',
                                        wrap='hard',
                                        size='md',
                                        style={'height': '20em', 'margin-top':'1em', 'overflow':'auto'},
                                    )
                                ],
                                style={'display':'flex','justify-content':'center'},
                            ),
                            dcc.Download(id='download_JSON'),
                        ],
                    ),
                    dbc.AccordionItem(
                        id='edit_DB',
                        title='Редактирование базы данных',
                        children=[
                            Under_construction('Раздел "Редактирование базы данных"'),
                        ],
                    ),
                ],
                start_collapsed=True,
            ),
        ],
        style={'margin':'10pt'},
    )


app.layout = html.Div(
    children=[
        dcc.Store(id='storeForQueryResults',storage_type='local'),
        dbc.Tabs(
            id="main_tabs", 
            active_tab='this_project',
            children=[
                dbc.Tab(
                    label='О проекте', 
                    tab_id='this_project',
                ),
                dbc.Tab(
                    label='Ранние греческие тексты', 
                    tab_id='search_wizard',
                ),
                dbc.Tab(
                    label='Утилиты',
                    tab_id='utility',
                ),
            ],
            style={'cursor':'pointer'}
        ),
        html.Div(
            id='tabs_content',
            children=[
                html.Div(
                    id='project_page',
                    children=[
                        This_project(),
                    ],
                    style={'display':'block'}
                ),
                html.Div(
                    id='search_page',
                    children=[
                        Search_wizard(),
                    ],
                    style={'display':'none'}
                ),
                html.Div(
                    id='utility_page',
                    children=[
                        Some_utility(),
                    ],
                    style={'display':'none'}
                ),
            ]
        )
    ]
)

def Get_Tr_Element(tr,k):
    return tr['props']['children'][k]['props']['children']

'''
@app.callback(
    Output('md_file_for_browsing','children'),
    [
        Input('open_md_file','n_clicks'),
        Input('close_md_file','n_clicks'),
        Input('my_md_file','contents'),
    ],
    [
        State('md_file_for_browsing','children'),
    ],
)
def render_md_content(n_open, n_close, c, ch):
    dcct=dash.callback_context.triggered
    if dcct is None:
        keyid=''
    else:
        keyid=dcct[0]['prop_id'].split('.')[0]
    if keyid=='open_md_file' or keyid=='my_md_file':
        return uf.loadUTF8(c)
    elif keyid=='close_md_file':
        return ''
    else:
        return ch
'''
@app.callback(
    Output('my_JSON_area','value'),
    [
        Input('open_JSON','n_clicks'),
        Input('close_JSON','n_clicks'),
        Input('my_JSON_file','contents'),
    ],
    [
        State('my_JSON_area','value'),
    ],
)
def render_JSON_content(n_open, n_close, c, ch):
    d={}
    dcct=dash.callback_context.triggered
    if dcct is None:
        keyid=''
    else:
        keyid=dcct[0]['prop_id'].split('.')[0]
    if keyid=='my_JSON_file':
        d,  cont = uf.loadJSON(c)
        return cont
    elif keyid=='close_JSON':
        return ''
    else:
        return ch

'''
def load_JSON_from_file(c):
    d={}
    if c is not None and c!='':
        d, cont = uf.loadJSON(c)
        return cont
    else:
        return ''
'''

@app.callback(
    Output('download_JSON','data'),
    [Input('save_JSON','n_clicks')],
    [State('my_JSON_area','value')],
)
def Save_JSON_file_to_local_comp(n,v):
    if n:
        return dict(content=v, filename="JSON_file_"+re.sub('[-:. ]','_',str(dtm.now()))+".json")



@app.callback(
    Output('md_file_for_browsing','children'),
    [
        Input('open_md_file','n_clicks'),
        Input('close_md_file','n_clicks'),
        Input('my_md_file','contents'),
        Input('my_md_file','filename'),
    ],
    [
        State('md_file_for_browsing','children'),
    ],
)
def render_md_content(n_open, n_close, c, fn, ch):
    dcct=dash.callback_context.triggered
    if dcct is None:
        keyid=''
    else:
        keyid=dcct[0]['prop_id'].split('.')[0]
    if keyid=='my_md_file':
            cont = uf.loadUTF8(c)
            if fn[-3:].lower()=='.md':
                return cont
            else:
                return fn+': It is not a markdown file!'
    elif keyid=='close_md_file':
        return ''
    # else:
    #     return ch

# @app.callback(
#     [
#         Output('md_file_for_browsing','children'),
#         Output('load_md_spinner','spinner_style'),
#     ],
#     [
#         Input('open_md_file','n_clicks'),
#         Input('close_md_file','n_clicks'),
#         Input('my_md_file','contents'),
#     ],
#     [
#         State('my_md_file','loading_state'),
#         State('md_file_for_browsing','children'),
#         State('load_md_spinner','spinner_style'),
#     ],
# )
# def render_md_content(n_open,n_close,c,ls, ch, ss):
#     dcct=dash.callback_context.triggered
#     if dcct is None:
#         keyid=''
#     else:
#         keyid=dcct[0]['prop_id'].split('.')[0]
#     if keyid=='open_md_file' or keyid=='my_md_file':
#         return [uf.loadUTF8(c), {'display':'block'} if ls is not None and ls['is_loaded'] else {'display':'none'}]
#     elif keyid=='close_md_file':
#         return ['',{'display':'none'}]
#     else:
#         return [ch,ls]


# @app.callback(
#     Output('md_file_for_browsing','children'),
#     [
#         Input('my_md_file','contents'),
#         Input('close_md_file','n_clicks'),
#     ],
#     [
#         State('md_file_for_browsing','children'),
#     ],
# )
# def render_md_content(c,n,ch):
#     dcct=dash.callback_context.triggered
#     if dcct is None:
#         keyid=''
#     else:
#         keyid=dcct[0]['prop_id'].split('.')[0]
#     if keyid=='my_md_file':
#         return uf.loadUTF8(c)
#     elif keyid=='close_md_file':
#         return ''
#     else:
#         return ch
    


@app.callback(
    Output('downloadQueryResults','data'),
    [Input('saveQueryResults','n_clicks')],
    [
        State('place4number','children'),
        State('place4list','children'),
        State('listForOnePage','children'),
        State('storeForQueryResults','data'),
    ]
)
def SaveQueryResultsToLocalComp(n, p4n, p4l, l1p, d):
    if n:
        if p4n!='':
            out_number='#### '+p4n+'\n\n'
            out_list=''
        elif p4l!='':
            out_list='#### '+p4l+'\n\n'
            out_number=''
        if l1p==[]:
            out_md=''
        else:
            l=bj.loads(d)
            out_md='\n\n'.join(['###### '+str(i+1)+'\n'+l[i] for i in range(len(l))])
        return dict(content=out_number+out_list+out_md, filename="query_results_"+re.sub('[-:. ]','_',str(dtm.now()))+".md")


@app.callback(
    Output('downloadCurrentPage','data'),
    [Input('saveResultPage','n_clicks')],
    [
        State('place4number','children'),
        State('place4list','children'),
        State('listForOnePage','children'),
        State('storeForQueryResults','data'),
        State('showPage','active_page'),
        State('queryRusultSize','value'),
    ]
)
def SaveResultPageToLocalComp(n, p4n, p4l, l1p, d, ap, sz):
    if n:
        if p4n!='':
            out_number='#### '+p4n+'\n\n'
            out_list=''
        elif p4l!='':
            out_list='#### '+p4l+'\n\n'
            out_number=''
        if l1p==[]:
            out_md=''
        else:
            b=(ap-1)*5
            e=min(int(sz),ap*5)
            l=bj.loads(d)[b:e]
            out_md='\n\n'.join(['###### '+str(b+i+1)+'\n'+l[i] for i in range(len(l))])
        return dict(content=out_number+out_list+out_md, filename="current_page_"+re.sub('[-:. ]','_',str(dtm.now()))+".md")


@app.callback(
    [Output('charTableCollapse01','is_open'),Output('metricSymbolsCollapse','children')],
    [Input('metricSymbolsCollapse','n_clicks')],
    [State('charTableCollapse01','is_open'),State('metricSymbolsCollapse','children')],
)
def ToggleCollapse001(n, is_open,ch):
    if n:
        if is_open:
            return [False, 'Показать']
        else:
            return [True, 'Скрыть']
    else:
        return [is_open, ch]

@app.callback(
    [Output('charTableCollapse02','is_open'),Output('greekLettersCollapse','children')],
    [Input('greekLettersCollapse','n_clicks')],
    [State('charTableCollapse02','is_open'), State('greekLettersCollapse','children')],
)
def ToggleCollapse002(n, is_open,ch):
    if n:
        if is_open:
            return [False, 'Показать']
        else:
            return [True, 'Скрыть']
    else:
        return [is_open, ch]

@app.callback(
    Output('helpPlace','is_open'),
    [Input('helpButton','n_clicks')]
)
def ShowHelp(n):
    if n is not None and n>0:
        return True


formatOptionsKeysAndValues={
    'titleCheck':'Заголовок',
    'subtitleCheck':'Подзаголовок',
    'schemeCheck':'Схема',
    'rithmCheck':'Ритм строки',
    'srcCheck':'Оригинал',
    'transCheck':'Перевод',
    'all_zones':'Все зоны',
    'some_zones':'Выборочно',
    'number_only':'Количество',
    'any_condition':'Выполнены все условия',
    'some_condition':'Выполнено хотя бы одно условие',
    'number_list':'Список чисел',
    'define_formula':'Формула',
    'group_data':'Группировать',
    '':'',
}

@app.callback(
    [Output('ZonesView','children'),Output('ZonesView','style')],
    [Input('outputZoneChoice','value')]
)
def ChangeZonesView(v):
    if v==[]:
        return ['',{}]
    else:
        s=', '.join([formatOptionsKeysAndValues[v[i]] for i in range(len(v))])
        return [s,{'margim-left':'2em'}]



@app.callback(
    [Output('GroupOrNo','children'),Output('GroupOrNo','style')],
    [Input('outputGroupCheckList','value')]
)
def ChangeGroupOrNo(v):
    if v==[]:
        return ['',{}]
    else:
        return ['Группировать:',{'margim-left':'2em'}]



@app.callback(
    Output('ZoneModeView','children'),
    [Input('outputZoneModeChoice','value')]
)
def ChangeZoneModeView(v):
    return formatOptionsKeysAndValues[v]+':'

@app.callback(
    Output('AllSomeNumber','children'),
    [Input('outputСonditionChoice','value')]
)
def ChangeAllSomeNumber(v):
    return formatOptionsKeysAndValues[v]+':'




@app.callback(
    Output('buttonClearConditionListContainer','style'),
    [Input('currentCondition','value')]
)
def ChangeClearButtonStyle(v):
    if v=='0':
        return {'display':'none'}
    else:
        return {'display':'flex','flex-direction':'row','justify-content':'center','margin-top':'1em'}

            # md_style={'max-height':'20em','overflow-y':'auto','margin':'10pt','padding':'10pt','border':'1px solid lightgray','border-radius':'3pt'}

            # pq=max(1, sz//5 + (1 if sz%5>0 else 0))
            # k=min(sz,5)
            # if ap is not None:
            #     b=(ap-1)*5
            #     e=min(sz,ap*5)
            #     l=list(result_content[1].clone()[b:e])
            # else:
            #     l=list(result_content[1].clone()[:k])
            # li=dbc.ListGroupItem(
            #     children=[
            #         dcc.Markdown(children='###### '+str((ap-1)*5+i+1)+'\n'+l[i]['content']['markdown'],style=md_style)
            #         for i in range(len(l))
            #     ]
            # )

                # [li],{'display':'block'} if sz>0 else {'display':'none'},
                # pq, {'display':'flex', 'flex-direction':'row','justify-content':'center'} if pq>1 else {'display':'none'},


        ###########################################
        # Output('listForOnePage','children'), 
        # Output('listForOnePage','style'),
        ###########################################
        # Output('showPage','max_value'), 
        # Output('showPage','style'),
        ###########################################

        # Input('showPage','active_page'),

                # [], {'display':'none'},
                # 1, {'display':'none'},

                # [li],{'display':'block'} if sz>0 else {'display':'none'},
                # pq, {'display':'flex', 'flex-direction':'row','justify-content':'center'} if pq>1 else {'display':'none'},


@app.callback(
    [
        Output('queryOK','is_open'),
        Output('queryERROR','is_open'),
        ##########################################
        Output('listForOnePage','children'), 
        Output('listForOnePage','style'),
        ##########################################
        Output('showPage','max_value'), 
        Output('showPage','style'),
        ##########################################
        Output('saveResultsContainer','style'),
    ],
    [
        Input('OkButton','n_clicks'),
        Input('ErrorButton','n_clicks'), 
        Input('OkErrorSwith','value'), 
        Input('showPage','active_page'),
    ],
    [
        State('storeForQueryResults','data'),
        State('lastOueryType','value'),
        State('queryRusultSize','value'),
        ##########################################
        State('listForOnePage','children'), 
        State('listForOnePage','style'),
        ##########################################
        State('showPage','max_value'), 
        State('showPage','style'),
        ##########################################
        State('saveResultsContainer','style'),
    ]
)
def OpenCloseQueryModal(n_Ok,n_Error, v,ap,data_list,q_type,q_size,l_ch,l_st,sp_mv,sp_st, sqr_st):
    sz=int(q_size)
    pq=max(1, sz//5 + (1 if sz%5>0 else 0))
    md_style={
        'max-height':'20em',
        'overflow-y':'auto',
        'margin':'10pt',
        'padding':'10pt',
        'border':'1px solid lightgray',
        'border-radius':'3pt',
    }    
    dcct=dash.callback_context.triggered
    if dcct is None:
        keyid=''
    else:
        keyid=dcct[0]['prop_id'].split('.')[0]
    if keyid=='ErrorButton':
        return [
            False, False,
            [], {'display':'none'},
            1, {'display':'none'},
            {'display':'none'},
        ]
    elif keyid=='OkButton':
        if q_type=='number' or q_type=='list':
            return [
                False, False,
                [], {'display':'none'},
                1, {'display':'none'},
                {'display':'none'},
            ]
        elif q_type=='cursor':
            k=min(sz,5)
            l=bj.loads(data_list)[:k]
            li=dbc.ListGroupItem(
                children=[
                    ##############################################
                    # VERY IMPORTANT                             #
                    ##############################################
                    # dcc.Markdown(children='###### '+str(i+1)+'\n'+l[i]['content']['markdown'],style=md_style)
                    dcc.Markdown(children='###### '+str(i+1)+'\n'+l[i], style=md_style)
                    for i in range(len(l))
                ]
            )
            return [
                False, False,
                [li],{'display':'block'} if sz>0 else {'display':'none'},
                pq, {'display':'flex', 'flex-direction':'row','justify-content':'center'} if pq>1 else {'display':'none'},
                {'display':'flex','flex-direction':'row','justify-content':'space-between','align-items':'stretch','margin-bottom':'5pt'},
            ]
    elif keyid=='OkErrorSwith':
        if v=='Ok':
            return [
                True,False,
                [], {'display':'none'},
                1, {'display':'none'},
                {'display':'none'},
            ]
        elif v=='Error':
            return [
                False,True,
                [], {'display':'none'},
                1, {'display':'none'},
                {'display':'none'},
            ]
        else:
            return [
                False,False,
                [], {'display':'none'},
                1, {'display':'none'},
                {'display':'none'},
            ]
    elif keyid=='showPage':
        b=(ap-1)*5
        e=min(sz,ap*5)
        l=bj.loads(data_list)[b:e]
        li=dbc.ListGroupItem(
            children=[
                #######################################################
                # VERY IMPORTANT                                      #
                #######################################################
                # dcc.Markdown(children='###### '+str((ap-1)*5+i+1)+'\n'+l[i]['content']['markdown'],style=md_style)
                dcc.Markdown(
                    children='###### '+str((ap-1)*5+i+1)+'\n'+l[i], 
                    style=md_style,
                )
                for i in range(len(l))
            ]
        )
        return [
            False, False,
            [li],{'display':'block'} if sz>0 else {'display':'none'},
            pq, {'display':'flex', 'flex-direction':'row','justify-content':'center'} if pq>1 else {'display':'none'},
            {'display':'flex','flex-direction':'row','justify-content':'space-between','align-items':'stretch','margin-bottom':'5pt'},
        ]
    else:
        return [
            False,False,
            l_ch,l_st,
            sp_mv,sp_st,
            sqr_st,
        ]






@app.callback(
    [
        Output('place4number','children'), 
        Output('place4number','style'), 
        ###########################################
        Output('place4list','children'), 
        Output('place4list','style'),
        ###########################################
        # Output('listForOnePage','children'), 
        # Output('listForOnePage','style'),
        ###########################################
        # Output('showPage','max_value'), 
        # Output('showPage','style'),
        ###########################################
        Output('OkErrorSwith','value'),
        Output('storeForQueryResults','data'),
        Output('lastOueryType','value'),
        Output('queryRusultSize','value'),
    ],
    [
        Input('execQuery','n_clicks'),
        # Input('showPage','active_page'),
    ],
    [
        State('conditionStoreDT','data'),
        State('outputСonditionChoice','value'),
        State('outputZoneModeChoice','value'),
        State('outputGroupCheckList','value'),
        State('outputZoneChoice','value'),
    ]
)
def Render_Query_ResultsWithErrorMessage(
    n,
    # ap, 
    ch,
    oper,
    zone_mode,
    must_group,
    zones,
):
    try:
        return Render_Query_Results(
            n,
            # ap, 
            ch,
            oper,
            zone_mode,
            must_group,
            zones,
        )
    except:
        return [
                '', {'display':'none'},
                '', {'display':'none'},
                # [], {'display':'none'},
                # 1, {'display':'none'},
                'Error',
                [],
                '',
                '0',
            ]


def Render_Query_Results(
    n,
    # ap, 
    ch,
    oper,
    zone_mode,
    must_group,
    zones,
):
    mc=MC()
    db=mc['sumer_2_greek']
    if n is not None and n>0:
        dataOutputFormat={
            'dataOut':preQueryKeyAndValues[oper],
            'zoneForOutput':preQueryKeyAndValues[zone_mode],
            'group':[preQueryKeyAndValues[x] for x in must_group],
            'zones':[preQueryKeyAndValues[x] for x in zones],
        }
        preQuery={
            x['id']: {
                'col_name':preQueryKeyAndValues[x['col_name']],
                'zone_name':preQueryKeyAndValues[x['zone_name']],
                'pattern':x['pattern'], 
                'word_section':preQueryKeyAndValues[x['word_section']], 
                'compare_mode':preQueryKeyAndValues[x['compare_mode']],
            }
            for x in ch
        }
        a_query=Create_Multiple_Query(dataOutputFormat, preQuery)
        result_type, result_content = Get_Result_By_Query(a_query,db)
        if result_type=='number':
            mc.close()
            result_for_return = [
                'Количество найденных фрагментов: '+str(result_content),{'display':'block'},
                '', {'display':'none'},
                # [], {'display':'none'},
                # 1, {'display':'none'},
                'Ok',
                [],
                'number',
                '0',
            ]
        elif result_type=='list':
            mc.close()
            result_for_return = [
                '', {'display':'none'},
                'Список количеств найденных фрагментов: '+', '.join([str(x) for x in result_content]),{'display':'block'},
                # [], {'display':'none'},
                # 1, {'display':'none'},
                'Ok',
                [],
                'list',
                '0',
            ]
        elif result_type=='cursor':
            # md_style={'max-height':'20em','overflow-y':'auto','margin':'10pt','padding':'10pt','border':'1px solid lightgray','border-radius':'3pt'}
            sz=int(result_content[0])
            # pq=max(1, sz//5 + (1 if sz%5>0 else 0))
            # k=min(sz,5)
            # if ap is not None:
            #     b=(ap-1)*5
            #     e=min(sz,ap*5)
            #     l=list(result_content[1].clone()[b:e])
            # else:
            #     l=list(result_content[1].clone()[:k])
            # li=dbc.ListGroupItem(
            #     children=[
            #         dcc.Markdown(children='###### '+str((ap-1)*5+i+1)+'\n'+l[i]['content']['markdown'],style=md_style)
            #         for i in range(len(l))
            #     ]
            # )
            result_for_return = [
                'Количество найденных фрагментов: '+str(sz),{'display':'block'},
                '', {'display':'none'},
                # [li],{'display':'block'} if sz>0 else {'display':'none'},
                # pq, {'display':'flex', 'flex-direction':'row','justify-content':'center'} if pq>1 else {'display':'none'},
                ##########################################################
                # VERY IMPORTANT                                         #
                ##########################################################
                'Ok',
                # bj.dumps(list(result_content[1])),
                bj.dumps([x['content']['markdown'] for x in result_content[1]]),
                'cursor',
                str(sz),
            ]
    else:
        result_for_return = [
                '', {'display':'none'},
                '', {'display':'none'},
                # [], {'display':'none'},
                # 1, {'display':'none'},
                '',
                [],
                '',
                '0',
        ]
    mc.close()
    return result_for_return


def Get_Result_By_Query(a_query,db):
    result_content = None
    cols=[db[x] for x in a_query['cols']]
    result_type=a_query['flag']
    if result_type=='number':
        result_content=cols[0].count_documents(a_query['search'])
    elif result_type=='cursor':
        result_content=[cols[0].count_documents(a_query['search']), cols[0].find(a_query['search'],a_query['zones'])]
    elif result_type=='list':
        result_content=[cols[i].count_documents(a_query['search'][i]) for i in range(len(a_query['search']))]
    else:
        result_content=''
    return result_type, result_content

'''
        preQuery={
            x['id']: {
                'col_name':x['col_name'],
                'zone_name':x['zone_name'],
                'pattern':x['pattern'], 
                'word_section':x['word_section'], 
                'compare_mode':x['compare_mode'],
            }
            for x in ch
        }
'''

def Create_Multiple_Query(dataOutputFormat, preQuery):
    if dataOutputFormat['zoneForOutput']=='count':
        if dataOutputFormat['dataOut']=='list':
            flag='list'
        else:
            flag='number'
    else:
        flag='cursor' 
    singleQueries={
        x:Create_Single_Query(preQuery[x])
        for x in preQuery
    }
    singleQueryList=list(singleQueries.values())
    cols=[preQuery[x]['col_name'] for x in preQuery]

# Это условие возникновения ошибки  - временное. 
# После доработки новых режимов оно должно быть изменено 
    
    if (len(set(cols))>1) and (flag!='list'):
        return 'ERROR'
    elif len(singleQueryList)==1:
        search=singleQueryList[0]
    elif dataOutputFormat['dataOut'] in ['$and','$or']:
        search={dataOutputFormat['dataOut']: singleQueryList}
    elif dataOutputFormat['dataOut']=='list':
        search=singleQueryList
    else:
        return 'ERROR'

# Это временное условие 
# После доработки новых режимов оно должно быть изменено 

    if flag=='content':
        if dataOutputFormat['zoneForOutput'] not in ['form_list_of_zones','count']:
            zones={'_id':0, dataOutputFormat['zoneForOutput']:1}
        else:
            zones={'_id':0, 'title':1}
    else:
        zones=''    
    return {'flag':flag, 'cols':cols, 'search':search, 'zones':zones}


def Change_Metric_Pattern(pattern, word_section):
    if word_section=='all_pauses':
        p=re.sub('[|]','[|]',pattern)
    elif word_section=='hard_pauses':
        p=re.sub(r'[⋮┋]','',pattern)
        p=re.sub(r'([-⏑])',r'\1[⋮┋]?',p)
        p=re.sub('[|]','[|]',p)
    elif word_section=='no_pauses':
        p=re.sub(r'[⋮┋|‖⦀]','',pattern)
        p=re.sub(r'([-⏑])',r'\1[⋮┋|‖⦀]?',p)
    return p

##############################################
# Important
##############################################  

def Change_Greek_Pattern(pattern):
    global Greek_Letters_And_Diacritics
    p=pattern
    for x in Greek_Letters_And_Diacritics:
        p=re.sub(x,Greek_Letters_And_Diacritics[x],p)
    return p

'''
        preQuery={
            x['id']: {
                'col_name':x['col_name'],
                'zone_name':x['zone_name'],
                'pattern':x['pattern'], 
                'word_section':x['word_section'], 
                'compare_mode':x['compare_mode'],
            }
            for x in ch
        }
'''

def Change_Various_Pattern(pattern, zone_name, word_section):
    if zone_name not in ['scheme','verse.rhythm','verse.src']:
        return pattern
    elif zone_name in ['scheme','verse.rhythm']:
        return Change_Metric_Pattern(pattern, word_section)
    elif zone_name == 'verse.src':
        return Change_Greek_Pattern(pattern)


def Create_Single_Query(pre_query):
    zone_name=pre_query['zone_name']
    word_section=pre_query['word_section']
    compare_mode=pre_query['compare_mode']
    pattern=Change_Various_Pattern(pre_query['pattern'], zone_name, word_section)
    if compare_mode == 'coinside':
        if zone_name not in ['scheme','verse.rhythm','verse.src']:
            return {zone_name: pattern}
        else:
            return {zone_name: {"$regex":'^'+pattern+'$',"$options":"i"}}
    elif compare_mode == 'include':
        return {zone_name: {"$regex": pattern,"$options":"i"}}
    elif compare_mode == 'text':
        return {"$text":{"$search": pattern}}



#######################################
# Отладка                             #
#######################################


# def Translate_to_Code_block(s):
#     return '```\n'+s+'\n```'

# @app.callback(
#     Output('debug_text','children'),
#     [Input('execQuery','n_clicks')],
#     [
#         State('conditionStoreDT','data'),
#         State('outputСonditionChoice','value'),
#         State('outputZoneModeChoice','value'),
#         State('outputGroupCheckList','value'),
#         State('outputZoneChoice','value'),
#     ]
# )
# def Debug_Query(n,ch,oper,zone_mode,must_group,zones):
#     if n is not None and n>0:
#         dataOutputFormat={
#             'dataOut':preQueryKeyAndValues[oper],
#             'zoneForOutput':preQueryKeyAndValues[zone_mode],
#             'group':[preQueryKeyAndValues[x] for x in must_group],
#             'zones':[preQueryKeyAndValues[x] for x in zones],
#         }
#         preQuery={
#             Get_Tr_Element(x,0): {
#                 'col_name':preQueryKeyAndValues[Get_Tr_Element(x,1)],
#                 'zone_name':preQueryKeyAndValues[Get_Tr_Element(x,2)],
#                 'pattern':Get_Tr_Element(x,3), 
#                 'word_section':preQueryKeyAndValues[Get_Tr_Element(x,4)], 
#                 'compare_mode':preQueryKeyAndValues[Get_Tr_Element(x,5)],
#             }
#             for x in ch
#         }
#         debug_dict=Create_Multiple_Query(dataOutputFormat, preQuery)
#         debug_string=Translate_to_Code_block(j.dumps(debug_dict, indent=4, ensure_ascii=False))
#         return debug_string
#     else:
#         return ''




@app.callback(
    Output('outputСonditionChoice','value'),
    [Input('outputZoneModeChoice','value')],
    [State('outputСonditionChoice','value')]
)
def change_output_condition_mode(v,v1):
    if v!= 'number_only' and v1=='number_list':
        return 'any_condition'
    else:
        return v1


@app.callback(
    Output('outputСonditionChoice','options'),
    [Input('outputZoneModeChoice','value')],
    [State('outputСonditionChoice','options')],
)
def EnableNumberList(v,o):
    if v=='number_only':
        o[2]['disabled']=False
    else:
        o[2]['disabled']=True
    return o


@app.callback(
    Output('execQuery','disabled'),
    [Input('conditionStoreDT','data')]
)
def EnableExecuteButton(ch):
    if len(ch)>0:
        return False
    else:
        return True


@app.callback(
    [Output('outputGroupCheckList','options'),Output('outputZoneChoice','options')],
    [Input('outputZoneModeChoice','value')],
    [State('outputGroupCheckList','options'),State('outputZoneChoice','options')],    
)
def EnableOutputCheckboxes(v,o,o1):
    if v=='some_zones':
        o[0]['disabled']=False
        for i in range(len(o1)):
            o1[i]['disabled']=False
        # o1[1]['disabled']=True
    else:
        o[0]['disabled']=True
        for i in range(len(o1)):
            o1[i]['disabled']=True
    return [o, o1]


@app.callback(
    [
        Output('allWordSection','color'),
        Output('softWordSectionFree','color'),
        Output('wordSectionFree','color'),
        Output('exactSearch','color'),
        Output('textSearch','color'),
    ],
    [
        Input('allWordSection','n_clicks'),
        Input('softWordSectionFree','n_clicks'),
        Input('wordSectionFree','n_clicks'),
        Input('exactSearch','n_clicks'),
        Input('textSearch','n_clicks'),
        Input('zoneChoiceMenu','value')
    ],
    [
        State('allWordSection','color'),
        State('softWordSectionFree','color'),
        State('wordSectionFree','color'),
        State('exactSearch','color'),
        State('textSearch','color'),
    ]
)
def ChangeBlueColor(aw_S_n, sw_SF_n, w_SF_n, e_Sr_n, t_Sr_n, v, aw_S_c, sw_SF_c, w_SF_c, e_Sr_c, t_Sr_c):
    dcct=dash.callback_context.triggered
    if dcct is None:
        keyid=''
    else:
        keyid=dcct[0]['prop_id'].split('.')[0]
    if keyid=='allWordSection':
        return ['info','primary','primary', e_Sr_c, t_Sr_c]
    elif keyid=='softWordSectionFree':
        return ['primary','info','primary', e_Sr_c, t_Sr_c]
    elif keyid=='wordSectionFree':
        return ['primary','primary','info', e_Sr_c, t_Sr_c]
    elif keyid=='exactSearch':
        if e_Sr_c=='primary':
            return [aw_S_c, sw_SF_c, w_SF_c, 'info', 'primary']
        else:
            return [aw_S_c, sw_SF_c, w_SF_c, 'primary', t_Sr_c]
    elif keyid=='textSearch':
        if t_Sr_c=='primary':
            return [aw_S_c, sw_SF_c, w_SF_c, 'primary', 'info']
        else:
            return [aw_S_c, sw_SF_c, w_SF_c, e_Sr_c, 'primary']
    elif keyid=='zoneChoiceMenu':
        if v !='transChoice':
            return [aw_S_c, sw_SF_c, w_SF_c, e_Sr_c, 'primary']
        else:
            return [aw_S_c, sw_SF_c, w_SF_c, e_Sr_c, t_Sr_c]
    else:
        return [aw_S_c, sw_SF_c, w_SF_c, e_Sr_c, t_Sr_c]

        
def ExtractConditionRow(condition_row):
    return [Get_Tr_Element(condition_row,k) for k in range(1,len(condition_row['props']['children']))]


def ExtractConditionTable(condition_list):
    return [ExtractConditionRow(x) for x in condition_list]

@app.callback(
    [Output('conditionStoreDT','data'),Output('currentCondition','value')],
    [Input('addCondition','n_clicks'),Input('buttonClearConditionList','n_clicks')],
    [
        State('conditionStoreDT','data'),
        State('currentCondition','value'),State('volChoiceMenu','value'),
        State('zoneChoiceMenu','value'),State('main_input','value'),
        State('allWordSection','color'),State('softWordSectionFree','color'),State('wordSectionFree','color'),
        State('exactSearch','color'),State('textSearch','color'),
        State('allWordSection','disabled'),
    ]
)
def StoreCurrentCondition(n,n1,sc_ch, cc_n,v_l,z_l,v, aw_S_c, sw_SF_c, w_SF_c, e_Sr_c, t_Sr_c, aw_S_d):
    global volMenuKeyAndValues
    global zoneMenuKeyAndValues
    dcct=dash.callback_context.triggered
    if dcct is None:
        keyid=''
    else:
        keyid=dcct[0]['prop_id'].split('.')[0]
    if keyid=='addCondition':
        if aw_S_d:
            rem=''
        else:
            if aw_S_c=='info':
                rem='Все'
            elif sw_SF_c=='info':
                rem='Жесткие'
            elif w_SF_c=='info':
                rem='Нет'
            else:
                rem=''
        if e_Sr_c=='info':
            sr='Совпадение'
        elif t_Sr_c=='info':
            sr='Текст'
        else:
            sr='Включение'
        new_row={
            'id':str(int(cc_n)+1), 
            'col_name':volMenuKeyAndValues[v_l],
            'zone_name':zoneMenuKeyAndValues[z_l],
            'pattern':v,
            'word_section':rem,
            'compare_mode':sr,
        }
        return [sc_ch+[new_row],str(int(cc_n)+1)]
    elif keyid=='buttonClearConditionList':
        return [[],str(0)]
    else:
        return [sc_ch,cc_n]


@app.callback(
    [
        Output('virtualKeyBoardButton','disabled'),Output('magicButton','disabled'),
        Output('allWordSection','disabled'), 
        Output('softWordSectionFree','disabled'),Output('wordSectionFree','disabled'),
        Output('exactSearch','disabled'),Output('textSearch','disabled'),

    ],
    [Input('zoneChoiceMenu','value')]
)
def ChangeVirtualKbdButton(v):
    if v is not None and v in ['schemeChoice','rithmChoice','srcChoice']:
        if v=='srcChoice':
            return [False,False,True,True,True,False,True]
        else:     
            return [False,False,False,False,False,False,True]
    elif v=='transChoice':
        return [True,True,True,True,True,False,False]
    else:
        return [True,True,True,True,True,False,True] 

'''
def ChangeVirtualKbdButton(v):
    if v is not None and v in ['schemeChoice','rithmChoice','srcChoice']:
        if v=='srcChoice':
            return [False,False,True,True,True,False,True]
        else:     
            return [False,False,False,False,False,False,True]
    elif v=='transChoice':
        return [True,True,True,True,True,False,False]
    else:
        return [True,True,True,True,True,False,True] 

'''

@app.callback(
    Output('addCondition','disabled'),
    [Input('main_input','value'),Input('volChoiceMenu','value'),Input('zoneChoiceMenu','value')]
)
def WriteConditionButtonDisable(p_v, v_v, z_v):
    if v_v is not None and z_v is not None and p_v is not None and p_v != '':
        return False
    else:
        return True

@app.callback(
    [Output('zone_greek_keyboard','style'),Output('zone_metric_keyboard','style'), Output('virtualKeyBoardButton','color')],
    [Input('virtualKeyBoardButton','n_clicks'), Input('zoneChoiceMenu','value')],
    [State('virtualKeyBoardButton','color')]
)
def ButtonVirtualKbdClick(n, v, c):
    dcct=dash.callback_context.triggered
    if dcct is None:
        keyid=''
    else:
        keyid=dcct[0]['prop_id'].split('.')[0]
    if keyid=='zoneChoiceMenu':
        return [{'display':'none'},{'display':'none'},'primary']
    if n is not None and v is not None and n>0 and c=='primary':
        if v=='srcChoice':
            return [{'display':'block','padding':'10pt','margin-top':'4pt','background-color':'white','border-radius':'3pt','border':'1px solid lightgray'},{'display':'none'}, 'info']
        else:
            return [{'display':'none'},{'display':'block','padding':'10pt','margin-top':'4pt','background-color':'white','border-radius':'3pt','border':'1px solid lightgray'}, 'info']
    else:
        return [{'display':'none'},{'display':'none'},'primary']



@app.callback(
    [
        Output('project_page','style'),
        Output('search_page','style'),
        Output('utility_page','style',)
    ],
    [Input('main_tabs','active_tab')],
)
def render_content(tab):
    if tab=='this_project':
        return [{'display':'block'},{'display':'none'},{'display':'none'}]
    elif tab=='search_wizard':
        return [{'display':'none'},{'display':'block'},{'display':'none'}]
    elif tab=='utility':
        return [{'display':'none'},{'display':'none'},{'display':'block'}]

@app.callback(
    Output("lastkeyid","value"),
    [
        Input("alpha","n_clicks"),Input("beta","n_clicks"),
        Input("gamma","n_clicks"),Input("delta","n_clicks"),
        Input("epsilon","n_clicks"),Input("zeta","n_clicks"),
        Input("eta","n_clicks"),Input("theta","n_clicks"),
        Input("iota","n_clicks"),Input("kappa","n_clicks"),
        Input("lambda","n_clicks"),Input("mu","n_clicks"),
        Input("nu","n_clicks"),Input("xi","n_clicks"),
        Input("omicron","n_clicks"),Input("pi","n_clicks"),
        Input("rho","n_clicks"),Input("stigma","n_clicks"),
        Input("sigma","n_clicks"),Input("tau","n_clicks"),
        Input("upsilon","n_clicks"),Input("phi","n_clicks"),
        Input("chi","n_clicks"),Input("psi","n_clicks"),
        Input("omega","n_clicks"),
        Input("space","n_clicks"),
        Input("backspace","n_clicks"),
        Input('changecase','n_clicks'),
        Input("vector_or_cross_product","n_clicks"),
        Input("medium_small_white_circle","n_clicks"),
        Input("hyphen","n_clicks"),
        Input("metrical_breve","n_clicks"),
        Input("metrical_long_over_short","n_clicks"),
        Input("metrical_short_over_long","n_clicks"),
        Input("metrical_two_shorts_joined","n_clicks"),
        Input("metrical_long_over_two_shorts","n_clicks"),
        Input("metrical_two_shorts_over_long","n_clicks"),
        Input("accent","n_clicks"),
        Input("sup_1","n_clicks"),Input("sup_2","n_clicks"),Input("sup_3","n_clicks"),
        Input("sup_4","n_clicks"),Input("sup_5","n_clicks"),Input("sup_6","n_clicks"),
        Input("tilda","n_clicks"),
        Input("bar_1","n_clicks"),Input("bar_2","n_clicks"),Input("bar_3","n_clicks"),
        Input("dotted_bar","n_clicks"),Input("dashed_bar","n_clicks"),
        Input("mspace","n_clicks"),Input("mbackspace","n_clicks"),
        Input('magicButton','n_clicks'),
    ]
)

def SendDashParams(
    n_alpha,n_beta,n_gamma,n_delta,n_epsilon,n_zeta,n_eta,n_theta,n_iota,n_kappa,n_lambda,n_mu,
    n_nu,n_xi,n_omicron,n_pi,n_rho,n_stigma,n_sigma,n_tau,n_upsilon,n_phi,n_chi,n_psi,n_omega,
    n_spase,
    n_backspace,n_changecase,
    n_vector_or_cross_product,n_medium_small_white_circle,n_hyphen,
    n_metrical_breve,n_metrical_long_over_short,n_metrical_short_over_long,
    n_metrical_two_shorts_joined,n_metrical_long_over_two_shorts,
    n_metrical_two_shorts_over_long,
    n_accent,
    n_sup_1,n_sup_2,n_sup_3,n_sup_4,
    n_sup_5,n_sup_6,
    n_tilda,
    n_bar_1,n_bar_2,
    n_bar_3,n_dotted_bar,n_dashed_bar,
    n_mspase,
    n_mbackspace,
    n_magicButton    
    ):
    dcct=dash.callback_context.triggered
    if dcct is None:
        return ''
    else:
        keyid=dcct[0]['prop_id'].split('.')[0]
        return keyid

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='js_greek_input_line'
    ),
        Output("main_input","value"), 
        Output('changecase','children'),
        Output('alpha','children'),Output('beta','children'),
        Output('gamma','children'),Output('delta','children'),
        Output('epsilon','children'),Output('zeta','children'),
        Output('eta','children'),Output('theta','children'),
        Output('iota','children'),Output('kappa','children'),
        Output('lambda','children'),Output('mu','children'),
        Output('nu','children'),Output('xi','children'),
        Output('omicron','children'),Output('pi','children'),
        Output('rho','children'),Output('stigma','children'),
        Output('sigma','children'),Output('tau','children'),
        Output('upsilon','children'),Output('phi','children'),
        Output('chi','children'),Output('psi','children'),
        Output('omega','children'),
        Output('inputmode','value'), 
        Input('lastkeyid','value'), 
        State('inputmode','value'), 
        State("main_input","value"),
        State('zoneChoiceMenu','value'),
)


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_props_check=True)
