"""Määrittelee luokan GraphDrawer ja sen riippuvuudet"""

from matplotlib import pyplot

from .report_reader import ReportReader


class GraphDrawer:
    """Piirtää kuvaajia, jotka kuvaavat tietyn meno- tai kulukategorian arvoja viimeisimmän vuoden
    aikana"""

    def __init__(self, configs):
        self.x_values = list(range(1, 13))
        self.save_dir = configs.get_config("save_dir")

    def draw(self, start_date, category, end_date=None):
        """Piirtää kuvaajan kategorian category arvoista aikavälillä [start_date, end_date]. Jos
        endend_datea ei ole annettu, piirretään kuvaaja tuoreimpaan kategorian arvoon asti."""

        y_values = self._calculate_y(start_date, category, end_date)
        pyplot.plot(self.x_values, y_values)
        pyplot.xlabel("Kuukausi")
        pyplot.ylabel(category)
        pyplot.show()

    def _calculate_y(self, start_date, category, end_date):
        report_reader = ReportReader(self.save_dir)
        category_values = report_reader.get_category_values_in_time_period(
                start_date,
                category,
                end_date=end_date
                )
        return self._create_y_array(category_values)

    @staticmethod
    def _create_y_array(category_values):
        y_values = [0 for value in range(1, 13)]

        for i, category_value in enumerate(category_values):
            y_values[i] = category_value

        return y_values
