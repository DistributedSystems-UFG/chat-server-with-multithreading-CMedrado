import zmq
from constPS import HOST, PORT

context = zmq.Context()

# Socket to receive messages on
subscriber = context.socket(zmq.SUB)
subscriber.bind(f"tcp://{HOST}:{PORT}")

while True:
    # Ask for the type of message
    print("Enter 'i' for individual message or 't' for topic message:")
    msg_type = input()

    # Handle individual message
    if msg_type == "i":
        # Wait for next message from publisher
        topic_filter = ""
        subscriber.setsockopt_string(zmq.SUBSCRIBE, topic_filter)
        message = subscriber.recv()
        print(f"Received message: {message}")

    # Handle topic message
    elif msg_type == "t":
        # Subscribe to a topic
        print("Enter a topic to subscribe to:")
        topic_filter = input()
        subscriber.setsockopt_string(zmq.SUBSCRIBE, topic_filter)

        # Wait for next message from publisher on that topic
        message = subscriber.recv()
        print(f"Received message on topic {topic_filter}: {message}")

    # Invalid input
    else:
        print("Invalid input. Please enter 'i' or 't'.")
