from serial import Serial
from struct import unpack
from .radar_config import stop_radar, config_radar, baudrate_data
from .utils import intify, q_to_db

"""
Main class for interface

TODO:
- increase processing speed (process parallel to reading, tricky)
- adjust output data format for specific needs

Suggested changes:

- streamline parsing process: 
    pre-determining the size and structure of each block type based on the header 
    can allow for more targeted parsing without inspecting each byte individually

- use Struct for Binary Data:
    instead of manually slicing and converting bytes, use the struct module more 
    extensively to unpack data based on expected formats
"""

class Radar():
    def __init__(self, com : dict):
        # connect config ports
        self.conf = Serial(com['conf_port'], baudrate = com['conf_baud'], timeout = com['conf_to'])
        # configurate sensor
        baudrate_data(self.conf)
        config_radar(self.conf, start = True)
        # connect to data port
        self.data = Serial(com['data_port'], baudrate = com['data_baud'])
        # sync word
        self.magic_word = b'\x02\x01\x04\x03\x06\x05\x08\x07'
        # tracks sync of uart
        self.sync = False
        # buffer for bytestream
        self.input = {'buffer' : b''}
        # ?
        self.output = {}
        # chunk size for reading bytestream
        self.size = 32
        # dict for tlv types
        self.indices={
            1: 'detected_points', 
            2: 'range_profile', 
            3: 'noise_profile',
            4: 'azimuth_static', 
            5: 'range_doppler', 
            6: 'stats', 
            7: 'side_info'
        }

    def has_data(self):
        return self.data.inWaiting() > 0

    def close(self):
        # stop radar, close serial
        stop_radar(self.conf)
        self.conf.close()
        self.data.close()

    def __del__(self):
        # close on destruction
        self.close()
        
    def read_uart(self):
        # create buffer for sliding window
        last8 = [b'\x00'] * 8
        # synchronize
        while (b''.join(last8) != self.magic_word):
            # read new byte
            byte = self.data.read(1)
            # slide window, append new byte
            last8[:7] = last8[1:]
            last8[7] = byte
        # add magic word to buffer
        self.input['buffer'] = b''.join(last8)
        # 8 bytes for version + frame length
        self.input['buffer'] += self.data.read(8)
        # convert length to int
        length = int.from_bytes(self.input['buffer'][-4:], 'little')
        # read rest of frame
        self.input['buffer'] += self.data.read(length - 16)
        # reset for parsing
        self.output = {}
        # parse
        self.parse()
        
    def parse(self):
        buffer = self.input['buffer']
        address = 0

        def head(dat, n = 40):
            """
            Extract header meta data from buffer
            """
            return n, \
            {
                'magic' : dat[:8],
                'version' : intify(dat[8:12], 10),
                'length' : int.from_bytes(dat[12:16],'little'),
                'platform' : intify(dat[16:20], 10),
                'number' : int.from_bytes(dat[20:24],'little'),
                'time' : int.from_bytes(dat[24:28],'little'),
                'objects' :  int.from_bytes(dat[28:32],'little'),
                'blocks' : int.from_bytes(dat[32:36],'little'),
                'subframe' : int.from_bytes(dat[36:n],'little')
            }
        
        def structure(data, n = 8):
            """
            Check structure of TLV Packet
            """
            t = int.from_bytes(data[:4], 'little')
            l = int.from_bytes(data[4:n], 'little')
            # t = intify(data[:4])
            # l = intify(data[4:n])
            return n, t, l

        def progress(n, block, value):
            nonlocal buffer, values, address
            buffer = buffer[n:]
            values -= n
            if values == 0: address = 0
            try: 
                self.output[block].append(value)
            except:
                try:
                    self.output[block][value[0]] = value[1]
                except:
                    self.output[block] = value

        def det_object(data, n = 16):
            # convert from bytes to float
            x = unpack('f',data[0:4])[0]
            y = unpack('f',data[4:8])[0]
            z = unpack('f',data[8:12])[0]
            p = unpack('f',data[12:n])[0]
            """
            x = intify(data[:4])
            y = intify(data[4:8])
            z = intify(data[8:12])
            p = intify(data[12:16])
            if x > 32767: x -= 65536
            if y > 32767: y -= 65536
            if z > 32767: z -= 65536
            qfrac = 0
            if 'qfrac' in oth: qfrac = oth['qfrac']
            x = q_to_dec(x, qfrac)
            y = q_to_dec(y, qfrac)
            z = q_to_dec(z, qfrac)
            """
            return n, p, x, y, z
        
        def profile(data, n = 2):
            v = int.from_bytes(data[:n], 'little')
            # v = intify(data[:n])
            return n,v
        
        def heatmap(data, sgn, n = 2):
            if sgn: v = int.from_bytes(data[:n], 'little', signed = True)
            else: v = int.from_bytes(data[:n], 'little')
            # v = intify(data[:n])
            # if sgn and v > 32767: v -= 65536
            return n,v
        
        def info(data, n = 24):
            ifpt = int.from_bytes(data[:4], 'little')
            tot = int.from_bytes(data[4:8], 'little')
            ifpm = int.from_bytes(data[8:12], 'little')
            icpm = int.from_bytes(data[12:16], 'little')
            afpl = int.from_bytes(data[16:20], 'little')
            ifpl = int.from_bytes(data[20:n], 'little')
            # ifpt = intify(data[:4])
            # tot  = intify(data[4:8])
            # ifpm = intify(data[8:12])
            # icpm = intify(data[12:16])
            # afpl = intify(data[16:20])
            # ifpl = intify(data[20:n])
            return n, ifpt, tot, ifpm, icpm, afpl, ifpl
        
        def side_info(data, n = 4):
            snr = int.from_bytes(data[:2], 'little')
            noise = int.from_bytes(data[2:n], 'little')
            # snr = intify(data[:2])
            # noise = intify(data[2:n])
            return n, snr, noise
        
        # process header 
        n, self.output['header'] = head(buffer)
        buffer = buffer[n:]
        blocks = self.output['header']['blocks']
        
        for block in range(blocks):
            # 0) get block type and length
            if address == 0:
                n, address, values = structure(buffer)
                buffer = buffer[n:]
                blocks -= 1
                if address in (1, 7):
                    self.output[self.indices[address]] = {}
                elif address in (2,3,4,5):
                    self.output[self.indices[address]] = []
                elif address in (6,):
                    self.output[self.indices[address]] = None
            
            # 1) point cloud
            if address == 1:
                for i in range(self.output['header']['objects']):
                    n, p, x, y, z = det_object(buffer)
                    progress(n, self.indices[address], (f'{i},{i}', {'v' : p, 'x' : x, 'y' : y, 'z' : z}))

            # 2) log mag range fft
            if address == 2:
                while values > 0:
                    n, v = profile(buffer)
                    progress(n, self.indices[address], q_to_db(v))

            # 3) noise array
            if address == 3:
                while values > 0:
                    n, v = profile(buffer)
                    progress(n, self.indices[address], q_to_db(v))

            # 4) range-azimuth heatmap
            if address == 4:
                while values > 0:
                    n, v = heatmap(buffer, True)
                    progress(n, self.indices[address], v)

            # 5) range-doppler heatmap
            if address == 5:
                while values > 0:
                    n, v = heatmap(buffer, True)
                    progress(n, self.indices[address], v)

            # 6) statistics
            if address == 6:
                n, ifpt, tot, ifpm, icpm, afpl, ifpl = info(buffer)
                progress(n, self.indices[address], {
                    'interframe_processing' : ifpt,
                    'transmit_output': tot,
                    'processing_margin': {
                        'interframe': ifpm,
                        'interchirp': icpm},
                    'cpu_load': {
                        'active_frame': afpl,
                        'interframe': ifpl}
                })
            
            # 7) detected points side info
            if address == 7:
                for i in range(self.output['header']['objects']):
                    n, snr, noise = side_info(buffer)
                    progress(n, self.indices[address], (f'{i},{i}', {'snr' : snr, 'noise' : noise}))
                             
    def __call__(self):
        # generate new output
        self.read_uart()
        return self.output



