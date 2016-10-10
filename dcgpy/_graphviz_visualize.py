def _graphviz_visualize(self, erc = 0, draw_inactive = True):
    """
    ex.visualize(self, erc, draw_inactive)

    Visualizes the d-CGP expression

    Visualizes the graph of the d-CGP expression, by generating a png image and displaying it on Matplotlib axes

    Note:
        This method requires matplotlib and pygraphviz modules installed in your Python system

    Args:
        erc (an ``int``): number of ephemeral random consants in input
        draw_inactive (a ``Boolean``): indicates whether to draw inactive nodes

    Returns:
        The AxesImage of the displayed graph

    Raises:
        ImportError: if modules matplotlib or pygraphviz are not installed in your Python system

    Examples:
        >>> ex = dcgpy.expression_double(2,1,3,3,2,2,dcgpy.function_set_double(["sum","diff"])(),0)
        >>> img = ex.visualize(1, True)
    """

    try:
        import pygraphviz as pgv
    except ImportError:
        print("Failed to import the required module pygraphviz")
        raise

    try:
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
    except ImportError:
        print("Failed to import the required module matplotlib")
        raise


    x = self.get()
    n = self.get_n()
    m = self.get_m()
    r = self.get_rows()
    c = self.get_cols()
    f = self.get_f()
    arity = self.get_arity()
    active_nodes = self.get_active_nodes()

    # bool vector of active nodes
    is_active = [False] * (n + r * c)
    for i in range(len(active_nodes)):
        is_active[active_nodes[i]] = True

    G = pgv.AGraph(strict = False, directed = True, rankdir = 'LR')

    # force the nodes to be placed in the right ranks
    inputs = []
    for i in range(n):
        inputs.append('n' + str(i))
    G.add_subgraph(inputs, rank = 'same')
    for i in range(c):
        col = []
        for j in range(r):
            col.append('n' + str(n + (i * c) + j))
        G.add_subgraph(col, rank = 'same')
        if i == 0:
            for j in range(n):
                for k in range(r):
                    G.add_edge('n' + str(j),'n' + str(n + k), style = 'invis')
        else:
            for j in range(r):
                for k in range(r):
                    G.add_edge('n' + str(n + (i - 1) * r + j),'n' + str(n + i * r + k), style = 'invis')
    outputs = []
    for i in range(m):
        outputs.append('n' + str(n + r * c + i))
    G.add_subgraph(outputs, rank = 'same')
    for i in range(r):
        for j in range(m):
            G.add_edge('n' + str(n + (c - 1) * r + i),'n' + str(n + r * c + j), style = 'invis')

    # input nodes
    for i in range(n - erc):
        G.add_node('n' + str(i), label = '<x<sub>' + str(i) + '</sub>>', shape = 'circle', style = 'bold')

    # input constants
    for i in range(erc):
        G.add_node('n' + str(n - erc + i), label = '<c<sub>' + str(i) + '</sub>>', shape = 'circle', style = 'bold')

    # function nodes and connections
    for i in range(r * c):
        if is_active[n + i] or draw_inactive:
            if is_active[n + i]:
                nstyle = 'solid'
                estyle = 'solid'
                col = 'black'
            else:
                nstyle = 'dashed'
                estyle = 'dotted'
                col = 'grey70'
            op = str(f[x[i * (arity + 1)]])
            if op == 'sum':
                op = '+'
            elif op == 'diff':
                op = '-'
            elif op == 'mul':
                op = '*'
            elif op == 'div':
                op = '/'
            G.add_node('n' + str(n + i), label =  op, shape = 'circle', style = nstyle, color = col, fontcolor = col)
            for j in range(arity):
                if j == 0:
                    ah = 'lnormal'
                elif j == 1:
                    ah = 'rnormal'
                else:
                    ah = 'normal'
                G.add_edge('n' + str(x[i * (arity + 1) + j + 1]), 'n' + str(n + i), arrowhead = ah, style = estyle, color = col)

    # output nodes
    for i in range(m):
        G.add_node('n' + str(n + r * c + i), label = '<o<sub>' + str(i) + '</sub>>', shape = 'circle', style = 'bold')
        G.add_edge('n' + str(x[len(x) - m + i]), 'n' + str(n + r * c + i))

    # generate the graph and display it
    G.draw('cgp_graph.png', prog = 'dot')
    img = plt.imshow(mpimg.imread('cgp_graph.png'))
    plt.axis('off')
    plt.show()

    return img
