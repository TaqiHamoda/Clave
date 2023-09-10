import io, csv

class DataUtilities:
    @staticmethod
    def DictToCSV(data: list[dict]) -> str:
        if len(data) == 0:
            return ''

        csv_buffer = io.StringIO()
        csv_writer = csv.DictWriter(csv_buffer, fieldnames=list(data[0].keys()))

        csv_writer.writeheader()
        csv_writer.writerows(data)

        csv_data = csv_buffer.getvalue()
        csv_buffer.close()

        return csv_data

    @staticmethod
    def CSVToDict(data: str | bytes) -> list[dict]:
        csv_buffer = None

        if data is str:
            csv_buffer = io.StringIO(data)
        elif data is bytes:
            csv_buffer = io.BytesIO(data)
        else:
            raise Exception("Unknown type for data given.")

        csv_reader = csv.DictReader(csv_buffer)

        dict_data = [row for row in csv_reader]
        csv_buffer.close()
        
        return dict_data