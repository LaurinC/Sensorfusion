import serial
import threading
from queue import Queue
from collections import deque
import struct
from radar_config import config_radar, stop_radar, baudrate_data
import time
from utility import intify, q_to_db

class Radar:
    def __init__(self, com):
        self.conf = serial.Serial(com['conf_port'], baudrate=com['conf_baud'], timeout=com['conf_to'])
        self.data = serial.Serial(com['data_port'], baudrate=com['data_baud'], timeout=1)
        baudrate_data(self.conf)
        config_radar(self.conf, start=True)
        
        self.magic_word = b'\x02\x01\x04\x03\x06\x05\x08\x07'
        self.data_queue = Queue()
        self.latest_data = None
        self.active = threading.Event()
        self.active.set()  # Initially active
        
        self.process_thread = threading.Thread(target=self.data_processor)
        self.data_thread = threading.Thread(target=self.data_reader)
        self.process_thread.start()
        self.data_thread.start()

    def sync_stream(self):
        sync_buffer = deque(maxlen=len(self.magic_word))
        while self.active.is_set():
            byte = self.data.read(1)
            if byte:
                sync_buffer.append(byte)
                # Correctly convert a deque of bytes to a single bytes object
                buffered_bytes = b''.join(sync_buffer)
                if buffered_bytes == self.magic_word:
                    print("Synchronization achieved.")
                    return
            else:
                # Optional: Handle the case where no byte is read
                print("No data read; possibly due to timeout or disconnection.")
                break

    def data_reader(self):
        while self.active.is_set():
            self.sync_stream()
            data = self.data.read(1024)
            self.data_queue.put(data)

    def data_processor(self):
        while self.active.is_set():
            data = self.data_queue.get()
            if data:
                self.latest_data = self.parse(data)

    def parse(self):
        buffer = self.input['buffer']
        offset = 0  # Use offset instead of slicing buffer repeatedly

        def head(data, n = 40):
            return struct.unpack('8sIIIIIIII', data)

        def read_format(fmt, offset):
            size = struct.calcsize(fmt)
            if len(buffer) - offset < size:
                raise ValueError("Insufficient data for expected format")
            return struct.unpack_from(fmt, buffer, offset), offset + size

        # Parse the header
        header_fmt = '8sIIIIIIII'
        try:
            header, offset = read_format(header_fmt, offset)
            (magic, version, length, platform, number, time, objects, blocks, subframe) = header
            self.output['header'] = {
                'magic': magic, 'version': version, 'length': length, 'platform': platform,
                'number': number, 'time': time, 'objects': objects, 'blocks': blocks, 'subframe': subframe
            }
        except ValueError as e:
            print(f"Error parsing header: {e}")
            return

        # Process each TLV block
        while blocks > 0:
            try:
                tlv_header_fmt = 'II'
                tlv_header, offset = read_format(tlv_header_fmt, offset)
                tlv_type, tlv_length = tlv_header
                blocks -= 1

                data_block = buffer[offset:offset + tlv_length]
                offset += tlv_length

                # Handle different types of data based on TLV type
                if tlv_type == 1:  # Example type for detected points
                    self.output['detected_points'] = self.parse_detected_points(data_block, self.output['header']['objects'])
                # Example elif blocks for additional TLV types
                elif tlv_type == 2:  # Range Profile
                    while values > 0:
                        n, v = profile(buffer)
                        progress(n, self.indices[address], q_to_db(v))

                elif tlv_type == 3:  # Noise Floor Profile
                    while values > 0:
                        n, v = profile(buffer)
                        progress(n, self.indices[address], q_to_db(v))

                elif tlv_type == 4:  # Azimuth Static Heatmap
                    while values > 0:
                        n, v = heatmap(buffer, False)  # Assuming non-signed values for heatmap
                        progress(n, self.indices[address], v)

                elif tlv_type == 5:  # Range-Doppler Heatmap
                    while values > 0:
                        n, v = heatmap(buffer, False)
                        progress(n, self.indices[address], v)

                elif tlv_type == 6:  # Statistics
                    n, stats = extract_stats(buffer)
                    progress(n, self.indices[address], stats)

                elif tlv_type == 7:  # Side Info for Detected Points
                    for i in range(self.output['header']['objects']):
                        n, snr, noise = side_info(buffer)
                        progress(n, self.indices[address], (f'{i},{i}', {'snr': snr, 'noise': noise}))


            except ValueError as e:
                print(f"Error parsing block type {tlv_type}: {e}")
                continue  # Skip this block or handle error
    
    def parse_detected_points(self, data, count):
        point_fmt = 'ffff'
        point_size = struct.calcsize(point_fmt)
        points = []
        offset = 0
        for _ in range(count):
            if len(data) - offset < point_size:
                raise ValueError("Insufficient data for detected points")
            point = struct.unpack_from(point_fmt, data, offset)
            points.append({
                'x': point[0],
                'y': point[1],
                'z': point[2],
                'velocity': point[3]
            })
            offset += point_size
        return points

    def get_latest_data(self):
        return self.latest_data

    def stop_radar(self):
        self.active.clear()  # This will stop the threads
        stop_radar(self.conf)
        self.conf.close()
        self.data.close()

    def pause(self):
        self.active.clear()

    def resume(self):
        self.active.set()

    def __call__(self):
        return self.get_latest_data()

# Adjusted __main__ usage if needed
if __name__ == '__main__':
    com_settings = {
        'conf_port': 'COM4',
        'conf_baud': 115200,
        'conf_to': 0.01,
        'data_port': 'COM3',
        'data_baud': 921600,
    }
    radar = Radar(com_settings)
    try:
        while True:
            if radar.latest_data:
                current_time = time.time()
                if hasattr(radar, 'last_call_time'):
                    time_since_last_call = current_time - radar.last_call_time
                    print(f"Time since last call: {time_since_last_call} seconds")
                radar.last_call_time = current_time
    except KeyboardInterrupt:
        radar.stop_radar()
