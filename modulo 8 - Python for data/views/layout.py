from dash import html, dcc, dash_table
from models.data_model import load_data
from controllers import eda_controller as ec


def _metric_card(title: str, value: str):
    return html.Div(
        className="metric-card",
        children=[
            html.Div(className="metric-title", children=title),
            html.Div(className="metric-value", children=value),
        ],
    )


def serve_layout():
    df = load_data()

    # Numéricas (Matplotlib / Seaborn)
    age_img, age_txt = ec.get_age_distribution_image(df)
    income_img, income_txt = ec.get_income_distribution_image(df)
    numweb_img, numweb_txt = ec.get_numwebvisits_distribution_image(df)
    kidteen_img, kidteen_txt = ec.get_kidteen_distribution_image(df)

    # Categóricas / financieras (Plotly)
    fig_marital, marital_txt = ec.get_marital_distribution_figure(df)
    fig_job, job_txt = ec.get_job_distribution_figure(df)
    fig_education, edu_txt = ec.get_education_distribution_figure(df)

    fig_housing, housing_txt = ec.get_binary_financial_figure(
        df, "housing", "Situación hipotecaria de los clientes"
    )
    fig_loan, loan_txt = ec.get_binary_financial_figure(
        df, "loan", "Clientes con préstamo personal"
    )
    fig_default, default_txt = ec.get_binary_financial_figure(
        df, "default", "Historial de impago (default)"
    )

    fig_y, y_txt = ec.get_target_distribution_figure(df)

    # Mapa geográfico
    fig_geo, geo_txt = ec.get_geo_density_figure(df)

    # Métricas globales, info y tabla descriptiva
    metrics = ec.generate_summary_metrics(df)
    dataset_info_md = ec.generate_dataset_info_text(df)
    conclusions_md = ec.generate_conclusions_text(df)
    desc_df = ec.get_descriptive_table(df)

    desc_table = dash_table.DataTable(
        data=desc_df.to_dict("records"),
        columns=[{"name": c, "id": c, "presentation": "markdown"} for c in desc_df.columns],
        page_size=7,
        fixed_rows={"headers": True},
        style_table={
            "overflowX": "auto",
            "maxHeight": "420px",
            "minWidth": "100%",
        },
        style_header={
            "backgroundColor": "#f3f4f6",
            "fontWeight": "600",
            "fontSize": 13,
            "whiteSpace": "normal",
            "height": "auto",
        },
        style_cell={
            "padding": "6px 10px",
            "fontSize": 12,
            "whiteSpace": "normal",
            "height": "auto",
            "textAlign": "center",
            "minWidth": "90px",
            "maxWidth": "200px",
        },
        style_cell_conditional=[
            {
                "if": {"column_id": "Estadístico"},
                "textAlign": "left",
                "minWidth": "130px",
                "fontWeight": "600",
            }
        ],
    )


    graph_style = {
        "height": "310px",   # o la altura que estés usando
        "width": "100%",     # importante para que respete el ancho de la tarjeta
    }
    graph_config = {"responsive": True, "displayModeBar": False}

    graph_config = {"responsive": False, "displayModeBar": False}

    def img_block(img_b64, alt_txt, insight):
        if img_b64 is None:
            return html.Div(insight, className="graph-insight")
        return html.Div(
            className="img-card",
            children=[
                html.Img(
                    src=f"data:image/png;base64,{img_b64}",
                    alt=alt_txt,
                    className="img-plot",
                ),
                html.P(insight, className="graph-insight"),
            ],
        )

    def graph_block(fig, insight):
        return html.Div(
            className="graph-with-text",
            children=[
                dcc.Graph(
                    figure=fig,
                    className="graph-card",
                    style=graph_style,
                    config=graph_config,
                ),
                html.P(insight, className="graph-insight"),
            ],
        )

    return html.Div(
        className="page-container",
        children=[
            html.Header(
                className="header",
                children=[
                    html.H1("EDA – Campaña de Depósitos a Plazo", className="title"),
                    html.P(
                        "Dashboard descriptivo profesional del dataset fusionado de clientes y campaña.",
                        className="subtitle",
                    ),
                ],
            ),
            dcc.Tabs(
                value="tab-resumen",
                children=[
                    dcc.Tab(
                        label="1. Resumen e información general",
                        value="tab-resumen",
                        children=[
                            html.Section(
                                className="section metrics-section",
                                children=[
                                    html.H2(
                                        "1. Información general del dataset",
                                        className="section-title",
                                    ),
                                    html.Div(
                                        className="metrics-grid",
                                        children=[
                                            _metric_card(
                                                "Total registros",
                                                f"{metrics['total_registros']:,}",
                                            ),
                                            _metric_card(
                                                "Total variables",
                                                f"{metrics['total_variables']}",
                                            ),
                                            _metric_card(
                                                "Tasa de conversión (y = yes)",
                                                f"{metrics['tasa_conversion']:.2f} %"
                                                if metrics["tasa_conversion"] is not None
                                                else "N/D",
                                            ),
                                            _metric_card(
                                                "Edad media",
                                                f"{metrics['edad_media']:.1f} años"
                                                if metrics["edad_media"] is not None
                                                else "N/D",
                                            ),
                                            _metric_card(
                                                "Ingreso medio",
                                                f"{metrics['ingreso_medio']:,.0f}"
                                                if metrics["ingreso_medio"] is not None
                                                else "N/D",
                                            ),
                                            _metric_card(
                                                "% con hipoteca",
                                                f"{metrics['porc_housing_yes']:.1f} %"
                                                if metrics["porc_housing_yes"] is not None
                                                else "N/D",
                                            ),
                                            _metric_card(
                                                "% con préstamo personal",
                                                f"{metrics['porc_loan_yes']:.1f} %"
                                                if metrics["porc_loan_yes"] is not None
                                                else "N/D",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            html.Section(
                                className="section",
                                children=[
                                    html.H2(
                                        "2. Estadísticos descriptivos globales",
                                        className="section-title",
                                    ),
                                    html.P(
                                        "Tabla de media, desviación estándar, mínimos, máximos y percentiles "
                                        "para las principales variables numéricas.",
                                        className="subtitle",
                                    ),
                                    desc_table,
                                ],
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label="2. Variables numéricas (Niños/Adolescentes)",
                        value="tab-numericas",
                        children=[
                            html.Section(
                                className="section",
                                children=[
                                    html.H2(
                                        "4. Análisis descriptivo de variables numéricas clave",
                                        className="section-title",
                                    ),
                                    html.Div(
                                        className="grid-2",
                                        children=[
                                            img_block(
                                                age_img,
                                                "Distribución de la edad",
                                                age_txt,
                                            ),
                                            img_block(
                                                income_img,
                                                "Distribución del ingreso",
                                                income_txt,
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="grid-2",
                                        children=[
                                            img_block(
                                                numweb_img,
                                                "Visitas web mensuales",
                                                numweb_txt,
                                            ),
                                            img_block(
                                                kidteen_img,
                                                "Menores en el hogar",
                                                kidteen_txt,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label="3. Variables categóricas",
                        value="tab-categoricas",
                        children=[
                            html.Section(
                                className="section",
                                children=[
                                    html.H2(
                                        "5. Análisis descriptivo de variables categóricas",
                                        className="section-title",
                                    ),
                                    html.Div(
                                        className="grid-2",
                                        children=[
                                            graph_block(fig_marital, marital_txt),
                                            graph_block(fig_job, job_txt),
                                        ],
                                    ),
                                    html.Div(
                                        className="grid-2",
                                        children=[
                                            graph_block(fig_education, edu_txt),
                                            graph_block(fig_y, y_txt),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label="4. Variables financieras y objetivo",
                        value="tab-financieras",
                        children=[
                            html.Section(
                                className="section",
                                children=[
                                    html.H2(
                                        "5.4 Variables financieras (hipoteca, préstamo, impago)",
                                        className="section-title",
                                    ),
                                    html.Div(
                                        className="grid-3",
                                        children=[
                                            graph_block(fig_housing, housing_txt),
                                            graph_block(fig_loan, loan_txt),
                                            graph_block(fig_default, default_txt),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label="5. Coordenadas geográficas",
                        value="tab-geo",
                        children=[
                            html.Section(
                                className="section",
                                children=[
                                    html.H2(
                                        "8. Dispersión de coordenadas de los clientes",
                                        className="section-title",
                                    ),
                                    html.P(
                                        "Diagrama de dispersión de las coordenadas (longitud, latitud). "
                                        "Cada punto corresponde a un cliente.",
                                        className="subtitle",
                                    ),
                                    html.Div(
                                        className="graph-with-text",
                                        children=[
                                            dcc.Graph(
                                                figure=fig_geo,
                                                className="graph-card",
                                                style={"height": "520px", "width": "100%"},
                                                config={"responsive": True, "displayModeBar": False},
                                            )
                                            if fig_geo is not None
                                            else html.Div(
                                                "No se ha podido generar el gráfico de dispersión de coordenadas.",
                                                className="graph-insight",
                                            ),
                                            html.P(geo_txt, className="graph-insight"),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
