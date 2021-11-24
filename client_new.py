import serial #pip install pyserial
import struct
import os


#port name
portx="/dev/ttyUSB0"
#baud rate
bps=115200
timex=5
# open serial
ser=serial.Serial(portx,bps,timeout=timex)
package_sum=0
No=1
lead_code=b'\xaa'
sync_word=b'\x55'
filetime_client = str(time.time())
filepath = "to_uav_end.pt"

#judge filepath or not
if os.path.isfile(filepath):
    #file info  s(1 byte)  s(1 byte)  12s(12 bytes)  h(2bytes)   16s(16bytes)  h(2bytes)
    #           lead_code  sync_word  filename       filesize     filetime     package_sum
    fileinfo_size = struct.calcsize('ss12sh16sh')

    #bytes
    filesize=os.stat(filepath).st_size>>3
    package_sum=filesize/128

    # head_info include:lead_code,sync_word,fliename,filesize,filetime,package_sum
    fhead = struct.pack('ss12sh16sh',lead_code,sync_word,
    filename.encode('utf-8'),filesize,
    filetime_client.encode('utf-8'),package_sum)
    # send fhead including lead_code,sync_word,fliename,filesize,filetime,package_sum
    ser.write(fhead)

    #binary object
    fp = open(filepath, 'rb')
    while 1:
      data = fp.read(128)
      package_size=128
      package_No=No
      package = struct.pack('ss128sss',lead_code,sync_word,data,package_No,package_size)
      if not data:
          print('{0} file send over...'.format(os.path.basename(filepath)))
          break
      ser.write(package)
      No=No+1
    # close object
    ser.close()
    fp.close()

