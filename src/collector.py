import datetime
import serial

class Collector:
    def __init__(self, config):
        self.config = config
        self.serial = serial.Serial('/dev/ttyAMA4', 115200, timeout=None)
        self.start_time = datetime.datetime.now()

    def collect(self):
        try:
            line = self.serial.readline().decode().strip()
        except UnicodeDecodeError:
            return
        
        if line == '':
            return None
        
        data = line.split(':')
        if len(data) != 6:
            return None
        
        try:
            for i in range(2):
                data[i] = int(data[i])
        except ValueError:
            return None

        try:
            for i in range(2, 5):
                data[i] = float(data[i])
        except ValueError:
            return None
    
        return {
            'lat': int(data[0]),
            'long': int(data[1]),
            'roll': float(data[2]),
            'pitch': float(data[3]),
            'yaw': float(data[4]),
            'gs': float(data[5])
        }
    
    def commit_to_fs(self, data):
        # get current date
        now = datetime.datetime.now()
        date = now.date().isoformat()
        filename = '/var/data/' + date + '.csv'
        line = now.isoformat() + ',' + data['lat'] + ',' + data['long'] + ',' + data['roll'] + ',' + data['pitch'] + ',' + data['yaw'] + ',' + data['gs'];
        needs_header = file.exists(filename) == False
        with open(filename, 'a') as file:
            if needs_header:
                file.write('time,lat,long,roll,pitch,yaw,gs\n')
            file.write(line + '\n')

    def run(self):
        while True:
            data = self.collect()
            if data is not None:
                print(data)
                self.commit_to_fs(data)

if __name__ == '__main__':
    print('[collector] "You look fun! Wanna play?"')
    collector = Collector("/etc/blackbox/config.yaml")
    collector.run()
