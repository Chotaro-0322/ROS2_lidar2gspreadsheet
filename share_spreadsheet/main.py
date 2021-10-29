import rclpy
import threading

from .share_spreadsheet import Lidar_Import

def main(args=None):
    rclpy.init(args=args)
    try:
        Lidar_import = Lidar_Import()
        run_threading = threading.Thread(target=Lidar_import.run)
        run_threading.start()
        while True:
            rclpy.spin(Lidar_import)
    finally:
        Lidar_import.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
