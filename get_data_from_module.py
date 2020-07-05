import serial, csv, re
import time
from datetime import datetime
import serial_ports

def try_decode(x:bytes):
    try:
        decoded = x.decode()
        return decoded.replace('\r\n', ' ').replace('\n', ' ')
    except:
        return ''

def constructor(databit:list, temporal_object:list):
    try:
        test_temp = "".join(databit).strip(' ')
        if re.search('mode = 1', test_temp):
            temporal_object.pop(0)
            temporal_object.pop(0)
            new_temp = "".join(temporal_object)

            t_bodys = re.findall(r'T body = ......', new_temp)
            t_body = t_bodys[-1][9:]
            return t_body
        else:
            temporal_object.extend(databit)
    except:
        pass

def send(temperature_list: list):
    with open('out.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        for row in temperature_list:
            writer.writerow(row)

def read_temperature():
    ports_available = serial_ports.serial_ports()
    ser = serial.Serial(
        port=ports_available[0],
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0)

    print("connected to: " + ser.portstr)
    start_time = datetime.now()
    i = 0
    parsed_objects = []
    temporal_object = []
    MAX_TEMP = 10
    while True:
        lecture = ser.readlines()
        if len(lecture) > 0 and not str(lecture[0])[2:-1].startswith('Vbat'):
            # time_delta = datetime.now() - start_time
            # if time_delta.total_seconds() >= 20:
            #     break
            res = list(map(try_decode, lecture))
            response_t_body = constructor(res, temporal_object)

            if response_t_body:
                time_delta = datetime.now() - start_time # If total seconds >= 10
                start_time = datetime.now()
                #print(time_delta.total_seconds())
                parsed_objects.append([start_time.strftime("%d/%m/%Y %H:%M:%S"), response_t_body])
                temporal_object.clear()
                i += 1
                # Verify if there're 10 reg
                if i == MAX_TEMP:
                    send(parsed_objects)
                    parsed_objects.clear()
                    i = 0

    ser.close()

read_temperature()