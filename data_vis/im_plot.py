def plot_stack_barchart(df):
    from bokeh.core.properties import value
    from bokeh.io import output_notebook, show
    from bokeh.plotting import figure, ColumnDataSource
    from bokeh.models import HoverTool

    # set x axis
    x = list(df['Month'][1:])

    # set colors
    colors = ["#FC9D8A", "#F9CDAD", "#C8C8A9"]
    colors2 = ['salmon', 'darkseagreen', 'paleturquoise']

    depart_list = ['SAC', 'ICB', 'SPU']

    # 三组叠加的数据
    sac_list = list(df['SAC'])[1:]
    icb_list = list(df['ICB'])[1:]
    spu_list = list(df['SPU'])[1:]
    tot_list = list(df['TOTAL'])[1:]

    # 生成数据
    data = {
        'x': x,
        'SAC': sac_list,
        'ICB': icb_list,
        'SPU': spu_list,
        'tot': tot_list,
    }

    hover1 = HoverTool(tooltips=[("时间", '@x'),
                                 ("月总销售额", "@tot"),
                                 ("SAC", "@SAC"),
                                 ("ICB", "@ICB"),
                                 ("SPU", "@SPU")])

    p = figure(x_range=x, plot_height=500, plot_width=800,
               title="2017年各部门销售额",
               y_axis_label='销售额(万元)', x_axis_label='时间',
               toolbar_location='right', )
    p.add_tools(hover1)
    p.vbar_stack(depart_list, x='x', width=0.6, source=data, color=colors2)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    show(p)


def plot_grouped_barchart(df):
    from bokeh.models import FactorRange  # 设置x坐标轴
    from bokeh.models import LinearAxis, Range1d  # 设置双y轴
    from bokeh.io import output_notebook, show
    from bokeh.models import ColumnDataSource  # 整合数据
    from bokeh.transform import factor_cmap  # 颜色
    from bokeh.models import HoverTool
    from bokeh.plotting import figure, ColumnDataSource

    # x坐标轴坐标两个参数
    months = list(df['Month'][1:])
    depart_list = ['SAC', 'ICB', 'SPU']

    # y轴高度
    sac_list = list(df['SAC'])[1:]
    icb_list = list(df['ICB'])[1:]
    spu_list = list(df['SPU'])[1:]

    tot_target = df['TOTAL.1'][1:]
    tot_real = df['TOTAL.2'][1:]
    y2 = tot_real / tot_target * 100

    data = {
        'SAC': sac_list,
        'ICB': icb_list,
        'SPU': spu_list,
    }

    colors2 = ['salmon', 'darkseagreen', 'paleturquoise']

    # 设置x坐标轴
    x = [(month, dep) for month in months for dep in depart_list]
    # 设置竖直
    counts = sum(zip(data['SAC'], data['ICB'], data['SPU']), ())

    source = ColumnDataSource(data=dict(
        x=x,
        counts=counts,
    ))

    p = figure(x_range=FactorRange(*x), plot_height=450, plot_width=1000, title="2017年月度实际部门销售额度",
               y_axis_label='销售额(万元)', x_axis_label='时间/部门')

    p.vbar(x='x', top='counts', width=1, source=source, line_color='white',
           fill_color=factor_cmap('x', palette=colors2, factors=depart_list, start=1, end=2))

    # ["#FC9D9A", "#F9CDAD", "#C8C8A9"]

    p.extra_y_ranges = {"foo": Range1d(start=0, end=150)}

    p.line(months, y2, color='pink', y_range_name="foo")
    p.circle(months, y2, color='red', y_range_name="foo")

    p.add_layout(LinearAxis(y_range_name="foo"), "right")

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None

    # set hover function
    hover1 = HoverTool(tooltips=[("时间/部门", '@x'), ("销售额", "@counts" + "万元")],
                       mode='vline')
    p.add_tools(hover1)

    show(p)
