import OpenOPC
opc = OpenOPC.client()
opc.connect('OPCServer.WinCC.1')
rd1 = opc.read('INPUT1')
print rd1
opc.close()
 