import plotly.plotly
import urllib.request
import urllib, json

'''
sankey constructor. Helper function for constructing sankey graphs in track.py
'''
def sankey(name, sources, targets, values, labels):
    data_trace = dict(
        type='sankey',
        width=1118,
        height=772,
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        ),
        orientation="h",
        valueformat=".0f",
        valuesuffix="TWh",
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
        title=name,
        font=dict(
            size=10
        )
    )

    fig = dict(data=[data_trace], layout=layout)
    plotly.offline.plot(fig, validate=False)

'''
example function that uses sankey for reference
'''
def example():
    url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    data_trace = dict(
        type='sankey',
        width=1118,
        height=772,
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        ),
        orientation="h",
        valueformat=".0f",
        valuesuffix="TWh",
        node=dict(
            pad=15,
            thickness=15,
            line=dict(
                color="black",
                width=0.5
            ),
            label=data['data'][0]['node']['label'],
            # color=data['data'][0]['node']['color']
        ),
        link=dict(
            source=data['data'][0]['link']['source'],
            target=data['data'][0]['link']['target'],
            value=data['data'][0]['link']['value'],
            # label=data['data'][0]['link']['label']
        ))

    layout = dict(
        title="Reddit",
        font=dict(
            size=10
        )
    )

    fig = dict(data=[data_trace], layout=layout)
    plotly.offline.plot(fig, validate=False)
