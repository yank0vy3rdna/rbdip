import time
from threading import Thread

from clickhouse_driver import Client

from app.read_conf import config


class ClickHouse:
    def __init__(self):
        self.queue = []
        try:
            self.client = Client(
                host=config.clickhouse.host,
                database=config.clickhouse.database,
                user=config.clickhouse.user,
                port=config.clickhouse.port,
                password=config.clickhouse.password
            )
            self.client.execute("""CREATE TABLE IF NOT EXISTS photo_actions(
                                    id UUID,
                                    user_id Int64,
                                    photo_size Int64,
                                    action_type String,
                                    processing_time Int64,
                                    timestamp DEFAULT now()
                                    )ENGINE MergeTree ORDER BY timestamp""")
        except Exception as e:
            print(e)

    def requests(self, ):
        while True:
            if len(self.queue) != 0:
                queue = self.queue.copy()
                self.queue.clear()
                try:
                    self.client.execute(
                        'INSERT INTO photo_actions (user_id, photo_size, action_type, processing_time) VALUES', queue)
                except Exception as e:
                    print(e)
            time.sleep(3)

    def record(self, statistic_information: dict):
        data = (
            int(statistic_information["user_id"]),
            int(statistic_information["photo_size"]),
            statistic_information["action_type"],
            int(statistic_information["processing_time"])
        )
        self.queue.append(data)


def process(clickhouse_instance):
    clickhouse_instance.requests()


clickhouse = ClickHouse()
dbThread = Thread(target=process, args=(clickhouse,))
dbThread.start()
