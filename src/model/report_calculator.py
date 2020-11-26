from os.path import join

class ReportCalculator:

    @staticmethod
    def sum_reports(reports):
        values_by_category = reports[0]
        values_by_category.pop("timestamp")

        for i, report in enumerate(reports):
            if i == 0:
                continue

            report.pop("timestamp")

            for key, value in report.items():
                values_by_category[key] += value

        return values_by_category
