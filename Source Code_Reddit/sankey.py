import plotly.plotly
import plotly.graph_objs as go

'''
sankey constructor. Helper function for constructing sankey graphs in track.py
'''
def sankey(name, sources, targets, values, labels, filename):
    data_trace = dict(
        type='sankey',
        width=1118,
        height=772,
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        ),
        orientation="h",
        valueformat=".2f",
        valuesuffix="% movement",
        node=dict(
            pad=15,
            thickness=15,
            line=dict(
                color="black",
                width=0.5
            ),
            label=labels,
            # color=data['data'][0]['node']['color']
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            # label=data['data'][0]['link']['label']
        ))

    layout = dict(
        title=filename,
        font=dict(
            size=10
        )
    )

    fig = dict(data=[data_trace], layout=layout)
    plotly.offline.plot(fig, show_link=False, validate=False, filename=filename+".html")
'''
sankey constructor. Helper function for getting statistics in track.py
'''
def sanFlow(name, sources, targets, values, labels, filename):
    data_trace = dict(
        type='sankey',
        width=1118,
        height=772,
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        ),
        orientation="h",
        valueformat=".2f",
        valuesuffix="% movement",
        node=dict(
            pad=15,
            thickness=15,
            line=dict(
                color="black",
                width=0.5
            ),
            label=labels,
            # color=data['data'][0]['node']['color']
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            # label=data['data'][0]['link']['label']
        ))

    layout = dict(
        title=filename,
        font=dict(
            size=10
        )
    )

    fig = dict(data=[data_trace], layout=layout)
 
    return  fig['data'][0]['link'] 


def bar(x, y, filename, title):
    txt = [
        "%.2f" % d for d in y
    ]
    # Create a trace
    trace = go.Bar(
        x=x,
        y=y,
        text=txt,
        textposition='auto',
    )
    layout = go.Layout(
        title=title,

        xaxis=dict(
            title='interest continuity rate(%)',
            tickangle=-45,
            # ticks='',
            dtick=5,
        ),
        yaxis=dict(
            # type='log',
            title='probability(%)',
            # autorange=True,
            # exponentformat='e',
            # showexponent = 'All'
        )
    )

    fig = dict(data=[trace], layout=layout)
    plotly.offline.plot(fig, filename=filename, show_link=False, validate=False)
