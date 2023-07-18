from subprocess import PIPE, Popen

import rclpy
from rclpy.node import Node
from rione_interfaces.srv import TextToSpeech


class FestivalNode(Node):
    def __init__(self):
        super().__init__("festival_node")

        self._tts_srv = self.create_service(TextToSpeech, "tts", self.tts_callback)

        self.get_logger().info("festival_node is running")

    def tts_callback(self, request, response):
        self.get_logger().info(f"Generating voice: {request.text}")

        try:
            proc = Popen(["festival", "--tts"], stdin=PIPE)
            proc.stdin.write(f"{str(request.text)}".encode())
            proc.stdin.close()
            proc.wait()

            self.get_logger().info("Succecfully generated and played voice")

            response.result = True
        except Exception as e:
            self.get_logger().info("Failed to generate or play voice")
            print(e)

            response.result = False

        return response


def main():
    rclpy.init()

    festival_node = FestivalNode()

    try:
        rclpy.spin(festival_node)
    except KeyboardInterrupt:
        print("\nCtrl-c is pressed")
    finally:
        festival_node.destroy_node()

    rclpy.shutdown()
