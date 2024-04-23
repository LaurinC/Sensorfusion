from serial import Serial

"""
Module for configuring radar.

This module provides functions to configure and control a radar sensor using a serial connection.

TODO:
- apply parametrized cfg instead of MWE

Functions:
- read_until_empty(conf: Serial, verbose: bool = False) -> None:
    Reads lines from the serial connection until an empty line is encountered.

- baudrate_data(conf: Serial) -> None:
    Configures the data UART baudrate for the radar sensor.

- config_radar(conf: Serial, start: bool = False) -> None:
    Configures the radar sensor with the desired parameters.
    If 'start' is True, the sensor is started after configuration.

- start_radar(conf: Serial, full_config: bool = False, verbose: bool = True) -> None:
    Starts the radar sensor.
    If 'full_config' is True, the sensor is started with full configuration.
    If 'verbose' is True, the function prints the received lines from the sensor.

- stop_radar(conf: Serial, verbose: bool = True) -> None:
    Stops the radar sensor.
    If 'verbose' is True, the function prints the received lines from the sensor.
"""

def read_until_empty(conf: Serial, verbose: bool = False) -> None:
    """
    Reads lines from the serial connection until an empty line is encountered.

    Args:
    - conf: Serial - The serial connection object.
    - verbose: bool - If True, prints the received lines.

    Returns:
    - None
    """
    while True:
        line = conf.readline()
        if line == b'':
            break
        if verbose:
            print(line)

def baudrate_data(conf: Serial) -> None:
    """
    Configures the data UART baudrate for the radar sensor.

    Args:
    - conf: Serial - The serial connection object.

    Returns:
    - None
    """
    # Config for data UART
    conf.write(b'configDataPort 921600 1\n')
    read_until_empty(conf)

def config_radar(conf: Serial, start: bool = False) -> None:
    """
    Configures the radar sensor with the desired parameters.

    Args:
    - conf: Serial - The serial connection object.
    - start: bool - If True, starts the sensor after configuration.

    Returns:
    - None
    """
    # Stop sensor before configuration
    stop_radar(conf, verbose=False)

    # List of commands to configure the radar
    commands = [
        b'dfeDataOutputMode 1',
        b'channelCfg 15 7 0',
        b'adcCfg 2 1',
        b'adcbufCfg -1 0 1 1 1',
        b'profileCfg 0 60 993 7 40 0 0 100 1 144 4500 0 0 158',
        b'chirpCfg 0 0 0 0 0 0 0 1',
        b'frameCfg 0 0 32 0 33.333 1 0',
        b'lowPower 0 0',
        b'guiMonitor -1 1 1 0 0 0 1',
        b'cfarCfg -1 0 2 8 4 3 0 15 1',
        b'cfarCfg -1 1 0 8 4 4 1 15 1',
        b'multiObjBeamForming -1 1 0.5',
        b'clutterRemoval -1 0',
        b'calibDcRangeSig -1 0 -5 8 256',
        b'extendedMaxVelocity -1 0',
        b'lvdsStreamCfg -1 0 0 0',
        b'compRangeBiasAndRxChanPhase 0.0 1 0 -1 0 1 0 -1 0 1 0 -1 0 1 0 -1 0 1 0 -1 0 1 0 -1 0',
        b'measureRangeBiasAndRxChanPhase 0 1.5 0.2',
        b'CQRxSatMonitor 0 3 4 99 0',
        b'CQSigImgMonitor 0 71 4',
        b'analogMonitor 0 0',
        b'aoaFovCfg -1 -90 90 -90 90',
        b'cfarFovCfg -1 0 0 5.40',
        b'cfarFovCfg -1 1 -1.21 1.21',
        b'calibData 0 0 0',
        b'sensorStart'
    ]
    
    # Execute each command in sequence
    for command in commands:
        read_until_empty(conf)
        conf.write(command)

    if start:
        start_radar(conf, full_config=True)

def start_radar(conf: Serial, full_config: bool = False, verbose: bool = True) -> None:
    """
    Starts the radar sensor.

    Args:
    - conf: Serial - The serial connection object.
    - full_config: bool - If True, starts the sensor with full configuration.
    - verbose: bool - If True, prints the received lines.

    Returns:
    - None
    """
    # Start sensor
    if full_config:
        conf.write(b'sensorStart\n')
    else:
        conf.write(b'sensorStart 0\n')
    read_until_empty(conf, verbose=verbose)

def stop_radar(conf: Serial, verbose: bool = True) -> None:
    """
    Stops the radar sensor.

    Args:
    - conf: Serial - The serial connection object.
    - verbose: bool - If True, prints the received lines.

    Returns:
    - None
    """
    # Stop radar
    conf.write(b'sensorStop\n')
    read_until_empty(conf, verbose=verbose)

if __name__ == '__main__':
    # test: configurate radar
    conf = Serial('COM4', baudrate = 115200, timeout=0.1)
    baudrate_data(conf)
    config_radar(conf)
    start_radar(conf)
    stop_radar(conf)
