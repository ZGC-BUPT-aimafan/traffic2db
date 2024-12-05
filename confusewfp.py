import os
import time

from pypcaptools import PcapToDatabaseHandler
from wechat_bot_aimafan import wechat_send

from myutils.config import get_database_config

os_name = "debian12"


def action(origin_root, file):
    db_config = get_database_config()
    db_config["table"] = file
    for root, _, files in os.walk(origin_root):
        for file_name in files:
            if file_name.endswith(".pcap"):
                pcap_path = os.path.join(root, file_name)
                protocol, _, _, site, domain = os.path.splitext(file_name)[0].split("_")
                handler = PcapToDatabaseHandler(
                    db_config,
                    pcap_path,
                    protocol,
                    domain,
                    site + "_" + os_name,
                )
                handler.split_flow_to_database()


if __name__ == "__main__":
    root_path = "/home/fcr/Documents/traffic_datasets/ConfuseWFP/pcap"
    for file in os.listdir(root_path):
        origin_root = os.path.join(root_path, file)
        start_time = time.time()
        action(origin_root, file)
        end_time = time.time()
        elapsed_time = end_time - start_time
        wechat_send(f"{file}入库完成，入库共消耗{elapsed_time:.2f} seconds")
