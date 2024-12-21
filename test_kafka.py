from confluent_kafka import Producer

KAFKA_BROKER = "localhost:9092"
producer = Producer({"bootstrap.servers": KAFKA_BROKER})

# Получение метаданных о топике
topic_name = "my_topic"
metadata = producer.list_topics(topic_name)

# Вывод информации о партициях
for partition in metadata.topics[topic_name].partitions.values():
    print(
        f"Partition: {partition.id}, Leader: {partition.leader}, Replicas: {partition.replicas}"
    )
