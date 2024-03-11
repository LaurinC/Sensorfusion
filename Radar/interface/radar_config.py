from serial import Serial

"""
Module for configurating radar

TODO:
- apply parametrized cfg instead of MWE
"""

def read_until_empty(conf : Serial, verbose : bool = False):
    while True:
        line = conf.readline()
        if line == b'': break
        if verbose: print(line)

def baudrate_data(conf : Serial):
    # config for data uart
    conf.write(b'configDataPort 921600 1\n')
    read_until_empty(conf)

def config_radar(conf : Serial, start : bool = False):
    # stop sensor before configuration
    stop_radar(conf, verbose = False)
    # config for MWE
    conf.write(b'flushCfg\n')
    read_until_empty(conf)
    conf.write(b'dfeDataOutputMode 1\n')
    read_until_empty(conf)
    conf.write(b'channelCfg 3 1 0\n')
    read_until_empty(conf)
    conf.write(b'adcCfg 2 1\n')
    read_until_empty(conf)
    conf.write(b'adcbufCfg -1 0 1 1 1\n')
    read_until_empty(conf)
    conf.write(b'profileCfg 0 60 1192 7 57.14 0 0 70 1 256 5209 0 0 158\n')
    read_until_empty(conf)
    conf.write(b'chirpCfg 0 0 0 0 0 0 0 1\n')
    read_until_empty(conf)
    conf.write(b'chirpCfg 1 1 0 0 0 0 0 0\n')
    read_until_empty(conf)
    conf.write(b'frameCfg 0 0 16 0 100 1 0\n')
    read_until_empty(conf)
    conf.write(b'lowPower 0 0\n')
    read_until_empty(conf)
    conf.write(b'guiMonitor -1 1 1 0 0 0 0\n')
    read_until_empty(conf)
    conf.write(b'cfarCfg -1 0 2 8 4 3 0 15 1\n')
    read_until_empty(conf)
    conf.write(b'cfarCfg -1 1 0 4 2 3 1 15 1\n')
    read_until_empty(conf)
    conf.write(b'multiObjBeamForming -1 1 0.5\n')
    read_until_empty(conf)
    conf.write(b'clutterRemoval -1 0\n')
    read_until_empty(conf)
    conf.write(b'calibDcRangeSig -1 0 -5 8 256\n')
    read_until_empty(conf)
    conf.write(b'extendedMaxVelocity -1 0\n')
    read_until_empty(conf)
    conf.write(b'bpmCfg -1 0 0 1\n')
    read_until_empty(conf)
    conf.write(b'lvdsStreamCfg -1 0 0 0\n')
    read_until_empty(conf)
    conf.write(b'compRangeBiasAndRxChanPhase 0.0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0\n')
    read_until_empty(conf)
    conf.write(b'measureRangeBiasAndRxChanPhase 0 1.5 0.2\n')
    read_until_empty(conf)
    conf.write(b'CQRxSatMonitor 0 3 5 121 0\n')
    read_until_empty(conf)
    conf.write(b'CQSigImgMonitor 0 127 4\n')
    read_until_empty(conf)
    conf.write(b'analogMonitor 0 0\n')
    read_until_empty(conf)
    conf.write(b'aoaFovCfg -1 -90 90 -90 90\n')
    read_until_empty(conf)
    conf.write(b'cfarFovCfg -1 0 0 8.92\n')
    read_until_empty(conf)
    conf.write(b'cfarFovCfg -1 1 -1 1.00\n')
    read_until_empty(conf)
    conf.write(b'calibData 0 0 0\n')
    read_until_empty(conf)
    if start: start_radar(conf, full_config = True)

def start_radar(conf : Serial, full_config : bool = False, verbose : bool = True):
    # start sensor
    if full_config: conf.write(b'sensorStart\n')
    else: conf.write(b'sensorStart 0\n')
    read_until_empty(conf, verbose = verbose)

def stop_radar(conf : Serial, verbose : bool = True):
    # stop radar
    conf.write(b'sensorStop\n')
    read_until_empty(conf, verbose = verbose)

if __name__ == '__main__':
    # test: configurate radar
    conf = Serial('COM4', baudrate = 115200, timeout=0.1)
    baudrate_data(conf)
    config_radar(conf)
    start_radar(conf)
    stop_radar(conf)
