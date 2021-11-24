import serial
import struct
import os

#port name
portx="/dev/ttyUSB2"
#baud rate
bps=115200
timex=5
# 打开串口
ser=serial.Serial(portx,bps,timeout=timex)


while 1:
    # request same space to storage 
    fileinfo_size = struct.calcsize('ss12sh16sh')
    package_size=struct.calcsize('ss128sss')
    # receive file_head info
    fhead = ser.read(fileinfo_size)
    if fhead:
        #read lead_code  sync_word  filename    filesize    filetime_server     package_sum
        #       s         s            12s          h        16s                h 
        lead_code,sync_word,filename,filesize,filetime_server,package_sum= struct.unpack('ss12sh16sh', fhead)
        #check lead_code and sync_word
        assert(lead_code is b'\xaa')
        assert(sync_word is b'\x55')
        #decode filename and filetime_server
        fn = filename.strip(b'\00')
        fn = fn.decode()
        ft = filetime_server.strip(b'\00')
        ft = ft.decode()
        print('file new name is {0}, filesize is {1},package_sum is {2}'.format(str(fn), filesize,package_sum))

        package_No=1  
        #received file size
        recvd_size = 0  
        # storage path
        fp = open('./' + "new_uav.pt", 'wb')
        print('start receiving...')
        # written binary data stream sequencially
        #unit of filesize is bit but reced_size is byte  
        while not recvd_size == filesize<<3:
            if  package_sum - package_No > 0:
                package = ser.read(package_size)
                lead_code,sync_word,data,package_No,package_size=struct.unpack('ss128sss',package)
                recvd_size += len(data)
                #double check
                assert(recvd_size is (package_No*128)<<3)
                assert(lead_code is b'\xaa')
                assert(sync_word is b'\x55')
                package_No+=1
            else:
                data = ser.read(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)
        fp.close()
        if not (package_sum == package_No):
            print('receive failure,please try again')
        else:
            print('end receive...')
        ser.close()
        break
