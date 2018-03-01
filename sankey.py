import plotly.plotly
import urllib.request
import urllib, json

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
    plotly.offline.plot(fig,show_link=False, validate=False, filename=filename+".html")
'''
sankey constructor. Helper function for constructing sankey graphs in track.py
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
