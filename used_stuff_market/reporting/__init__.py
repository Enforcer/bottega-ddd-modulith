import csv
from io import StringIO

from used_stuff_market.reporting import data


class CsvCashflowReport:
    def generate(self) -> None:
        buffer = StringIO()
        writer = csv.DictWriter(
            f=buffer, fieldnames=["item_id", "currency", "price", "fee"]
        )
        rows = data.fetch()
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "item_id": row[0],
                    "currency": row[1].currency.iso_code,
                    "price": f"{row[1].amount:.2f}",
                    "fee": f"{row[2].amount:.2f}",
                }
            )

        buffer.seek(0)
        line = buffer.readline()
        while line:
            print(line, end="")
            line = buffer.readline()


class JsonCashflowReport:
    pass


if __name__ == "__main__":
    CsvCashflowReport().generate()
