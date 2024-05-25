from API_manager import runFlask
from SQL_manager import SqlConnector


def main():
    sql = SqlConnector("139.59.156.48", "mind", "oparolarandom", "MindClear")

    runFlask(sql)


main()