from pymoo.docs import parse_doc_string
from pymoo.model.plot import Plot
from pymoo.operators.default_operators import set_if_none


class Scatter(Plot):

    def __init__(self,
                 angle=None,
                 **kwargs):

        super().__init__(**kwargs)
        self.angle = angle

    def _do(self):

        is_2d = (self.n_dim == 2)
        is_3d = (self.n_dim == 3)
        more_than_3d = (self.n_dim > 3)

        # create the figure and axis objects
        if is_2d:
            self.init_figure()
        elif is_3d:
            self.init_figure(plot_3D=True)
        elif more_than_3d:
            self.init_figure(n_rows=self.n_dim, n_cols=self.n_dim)

        # now plot data points for each entry
        for k, (F, kwargs) in enumerate(self.to_plot):

            # copy the arguments and set the default color
            _kwargs = kwargs.copy()
            set_if_none(_kwargs, "color", self.colors[k])

            # determine the plotting type - scatter or line
            _type = _kwargs.get("plot_type")
            if "plot_type" in _kwargs:
                del _kwargs["plot_type"]

            if self.n_dim == 1:
                raise Exception("1D Interval not implemented yet.")

            elif is_2d:
                self.get_plot_func(self.ax, _type)(F[:, 0], F[:, 1], **_kwargs)
                self.set_labels(self.ax, self.get_labels(), False)
            elif is_3d:
                set_if_none(_kwargs, "alpha", 1.0)

                self.get_plot_func(self.ax, _type)(F[:, 0], F[:, 1], F[:, 2], **_kwargs)
                self.ax.xaxis.pane.fill = False
                self.ax.yaxis.pane.fill = False
                self.ax.zaxis.pane.fill = False

                self.set_labels(self.ax, self.get_labels(), True)

                if self.angle is not None:
                    self.ax.view_init(45, 45)

            else:
                labels = self.get_labels()

                for i in range(self.n_dim):
                    for j in range(self.n_dim):

                        ax = self.ax[i, j]

                        if i != j:
                            self.get_plot_func(ax, _type)(F[:, i], F[:, j], **_kwargs)
                            self.set_labels(ax, [labels[i], labels[j]], is_3d)
                        else:
                            ax.set_xticks([])
                            ax.set_yticks([])
                            ax.scatter(0, 0, s=1, color="white")
                            ax.text(0, 0, labels[i], ha='center', va='center', fontsize=20)

        return self

    def get_plot_func(self, ax, type):

        if type is None or type == "scatter":
            return ax.scatter
        else:
            return ax.plot

    def set_labels(self, ax, labels, is_3d):

        # set the labels for each axis
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])

        if is_3d:
            ax.set_zlabel(labels[2])


# =========================================================================================================
# Interface
# =========================================================================================================


def scatter(**kwargs):
    """

    Scatter Plot

    Parameters
    ----------------

    axis_style : {axis_style}
    endpoint_style : dict
        Endpoints are drawn at each extreme point of an objective. This style can be modified.
    labels : {labels}

    Other Parameters
    ----------------

    figsize : {figsize}
    title : {title}
    legend : {legend}
    tight_layout : {tight_layout}
    cmap : {cmap}


    Returns
    -------
    Scattr : :class:`~pymoo.model.analytics.visualization.scatter.Scatter`

    """

    return Scatter(**kwargs)


parse_doc_string(scatter)