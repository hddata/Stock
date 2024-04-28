import asyncio
from aiohttp import TCPConnector, ClientSession

import pyecharts.options as opts
from pyecharts.charts import Graph

import json

"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://echarts.apache.org/examples/editor.html?c=graph-npm

目前无法实现的功能:

1、暂无
"""


async def get_json_data(url: str) -> dict:
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url=url) as response:
            return await response.json()


# 获取官方的数据
# data = asyncio.run(
#     get_json_data(
#         url="https://echarts.apache.org/examples/data/asset/data/npmdepgraph.min10.json"
#     )
# )

# loop = asyncio.get_event_loop()

# data = loop.run_until_complete(
#     get_json_data(
#         url="https://echarts.apache.org/examples/data/asset/data/npmdepgraph.min10.json"
#     )
# )

with open(r'C:\SoftwareZ\SProjects\PyProjects\Stock\data\npmdepgraph.min10.json', 'r') as f:
    data = json.load(f)

nodes = [
    {
        "x": node["x"],
        "y": node["y"],
        "id": node["id"],
        "name": node["label"],
        "symbolSize": node["size"],
        "itemStyle": {"normal": {"color": node["color"]}},
    }
    for node in data["nodes"]
]

# nodes = [
#     {
#         "x": node["x"],
#         "y": node["y"],
#         "id": node["id"],
#         "name": node["label"],
#         "symbolSize": node["size"],
#         "itemStyle": {"normal": {"color": node["color"]}},
#     }
#     for node in data["nodes"]
# ]

edges = [
    {"source": edge["sourceID"], "target": edge["targetID"]} for edge in data["edges"]
]


(
    Graph(init_opts=opts.InitOpts(width="1600px", height="800px"))
    .add(
        series_name="",
        nodes=nodes,
        links=edges,
        layout="none",
        is_roam=True,
        is_focusnode=True,
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(width=0.5, curve=0.3, opacity=0.7),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="NPM Dependencies"))
    .render("npm_dependencies1.html")
)
