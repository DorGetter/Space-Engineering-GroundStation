import serial
#from threading import *
import threading as tr
import time
import math

two_inTwentyFour=16777216




class Telcontrol(tr.Thread):
#everythin in degrees

    telescopeX_Direction = 0; #right,stop,left
    telescopeX_Speed = 0;

    telescopeY_Direction = 0;
    telescopeY_Speed = 0;

    #def __init__(self,port="/dev/ttyUSB0", baudrate="9600", mindx=10, mindy=10,maxdx=1000, maxdy=1000):
    def __init__(self,port = 'com8' ,baudrate="9600", mindx=10, mindy=10, maxdx=1000, maxdy=1000):
        tr.Thread.__init__(self);
        #self.ser = serial.Serial(port, baudrate)  # need to check the com

        self.ser = serial.Serial()
        self.ser.port = 'com8'  # may be called something different
        self.ser.baudrate = 9600  # may be different
        isopenend = self.ser.open()

        print("Connected to Telescope Controll");

        # x = ser.is_open
        self.initProtocol()
        self.mindx=mindx
        self.mindy=mindy
        self.maxdy=maxdy
        self.maxdx=maxdx
        self.isReady=True
        self.whileLock = tr.Semaphore(value=0)
        self.readyLock = tr.Lock()
        #self.lock.acquire()
        self.diffaz = 0
        self.diffelv = 0
        self.start()

        # self.resetAzmTelescope()
        # self.resetAltTelescope()
        self.oldx=0
        self.oldy=0


    def angle_to_24bit(self,ang):
        num = int((ang / 360) * two_inTwentyFour)
        #print(num)
        high = int(num / 65536)
        res = num % 65536
       # print(res)
        medium = int(res / 256)
        res = res % 256
        low = res
        return [high, medium, low]

    def resetAltTelescope(self):
        to_send = chr(80) + chr(4) + chr(17) + chr(4) + chr(0) + chr(0) + chr(0) + chr(0)
        self.ser.write(to_send.encode())

    def resetAzmTelescope(self, resetang=[0, 0, 0]):
        to_send = chr(80) + chr(4) + chr(16) + chr(4) + chr(0) + chr(0) + chr(0) + chr(0)
        self.ser.write(to_send.encode())

    def setAzimut(self, ang):
        if(ang<0):
            ang=360+ang
        if (ang > 360):
            ang = ang-360
        angtosend = self.angle_to_24bit(ang)
        to_send = chr(80) + chr(4) + chr(16) + chr(23) + chr(angtosend[0]) + chr(angtosend[1]) + chr(angtosend[2]) + chr(0)
        self.ser.write(to_send.encode())

    def setAltitude(self,ang):
        if(ang<0):
            ang=0
        if(ang>180):
            ang=0
        angtosend = self.angle_to_24bit(ang)
        to_send = chr(80) + chr(4) + chr(17) + chr(23) + chr(angtosend[0]) + chr(angtosend[1]) + chr(angtosend[2]) + chr(0)
        self.ser.write(to_send.encode())


    def connect(self):
        if not self.ser.is_open:
            self.ser.open()

    def disconnect(self):
        if not self.ser.closed:
            self.ser.close()

    def initProtocol(self):
        self.midLeft = chr(80) + chr(2) + chr(16) + chr(37) + chr(6) + chr(142) + chr(56) + chr(0)  # go left slow speed
        self.midRight = chr(80) + chr(2) + chr(16) + chr(36) + chr(6) + chr(142) + chr(56) + chr(0)  # going right at speed of 4
        self.stop_r = chr(80) + chr(2) + chr(16) + chr(36) + chr(0) + chr(0) + chr(0) + chr(0)  # Stop
        self.stop_l = chr(80) + chr(2) + chr(16) + chr(37) + chr(0) + chr(0) + chr(0) + chr(0)

        #command3 = chr(80) + chr(2) + chr(16) + chr(37) + chr(7) + chr(142) + chr(56) + chr(0)  # left (reset)
        self.midUp = chr(80) + chr(2) + chr(17) + chr(36) + chr(6) + chr(142) + chr(56) + chr(0)  # up
        self.midDown = chr(80) + chr(2) + chr(17) + chr(37) + chr(6) + chr(142) + chr(56) + chr(0)  # down
        self.Stop_d = chr(80) + chr(2) + chr(17) + chr(37) + chr(0) + chr(0) + chr(0) + chr(0)  # stop
        self.Stop_u = chr(80) + chr(2) + chr(17) + chr(36) + chr(0) + chr(0) + chr(0) + chr(0)

        self.StopX = (b':K1\r=\r')
        self.StopY = (b':K2\r=\r')
        self.ImmidiateStop= (b'4c0a\r')

    def getIsReady(self):
        self.readyLock.acquire()
        ans = self.isReady
        self.readyLock.release()
        return ans

    def setReady(self ,isReady):
        self.readyLock.acquire()
        self.isReady=isReady
        self.readyLock.release()

    def setCorrection(self,az=0,elv=0):
        if self.getIsReady():
            self.oldx=self.myAz
            self.oldy = self.myElv
            self.diffelv=elv
            self.diffaz=az
            self.myAz=self.myAz+az
            if (self.myElv < 0):
                self.myElv=self.myElv+elv
            if (self.myAz<0):
                self.myAz=360-self.myAz
            if(self.myAz>360):
                self.myAz=self.myAz-360


            # self.myAz = self.myAz +0.1
            # self.myElv = self.myElv + 0.1
            self.setReady(False)
            self.whileLock.release()
        print("my elv",self.myElv ,"my az",  self.myAz)

    def correct_x(self, rl=0, isStop=0):#  right + left - up+ down -
        print("correct_x")
        #print(math.fabs(self.diffaz), "fabs")
        if( rl>self.mindx):

            self.ser.write(self.midRight.encode())
            #time.sleep(5)
            #self.ser.write(self.stop_rl.encode())
            #self.ser.write(self.stop_rl.encode())
            print(" move right ", rl)
        if (rl <-self.mindx):

            self.ser.write(self.midLeft.encode())
            #time.sleep(5)
            #self.ser.write(self.stop_rl.encode())
            #self.ser.write(self.stop_rl.encode())
            print(" move left ",rl)


        if (math.fabs(rl)> self.maxdx or math.fabs(rl)< self.mindx or isStop==1):
            self.ser.write(self.stop_r.encode())
            self.ser.write(self.stop_l.encode())
            print("stop x")

            #time.sleep(0.1)
        #time.sleep(math.abs(self.dy / self.maxdy))
        #print("up down")
    def correct_y(self, ud=0, isStop=0):#  right + left - up+ down -
        print("correct_y")
        #print(math.fabs(self.diffaz), "fabs")

        if (ud > self.mindy):

            self.ser.write(self.midUp.encode())
            #time.sleep(5)
            #self.ser.write(self.Stop_ud.encode())
            print(" move up ", ud)
        if (ud <- self.mindy):

            self.ser.write(self.midDown.encode())
            #time.sleep(5)

            #self.ser.write(self.Stop_ud.encode())
            print(" move down  ", ud)
        if(math.fabs(ud)> self.maxdy or math.fabs(ud)< self.mindy or isStop==1):
            self.ser.write(self.Stop_d.encode())
            self.ser.write(self.Stop_u.encode())
            print("stop y")
    def stop_x(self):
        self.ser.write(self.stop_r.encode())
        self.ser.write(self.stop_l.encode())

    def stop_y(self):
        self.ser.write(self.Stop_d.encode())
        self.ser.write(self.Stop_u.encode())

            #time.sleep(0.1)
        #time.sleep(math.abs(self.dy / self.maxdy))
        #print("up down")



    # def correct(self):
    #     print("correct")
    #     print(math.fabs(self.diffaz), "fabs")
    #     if ( math.fabs(self.diffaz)> self.maxdx):
    #         self.setAzimut(self.myAz)
    #         self.diffaz=0
    #         print("myaz- move",self.myAz)
    #         #time.sleep(0.1)
    #     if (math.fabs(self.diffelv)> self.maxdy):
    #         self.setAltitude(self.myElv)
    #         self.diffelv=0
    #         print("myelv-move",self.myElv)
    #         #time.sleep(0.1)
    #     #time.sleep(math.abs(self.dy / self.maxdy))
    #     #print("up down")

    # move up
    def run(self):
        while True:
            self.whileLock.acquire()
            self.correct()
            self.setReady(True)

    def stopTelescope(self):
        self.ser.write(self.StopX)
        self.ser.write(self.StopY)
        self.disconnect()
        print("Telescope stopped")

    #    b12AB0500,40000500

    def goToZero(self):
        moveToZero = "b00000000,00000000"
        self.ser.write(moveToZero.encode())
        time.sleep(0.1)

    def getPosition(self):
        # moveRight = chr(69)
        moveRight = chr(122)
        self.ser.write(moveRight.encode())
        time.sleep(0.1)

        dataIn = self.ser.read_all()
        dataStr = str(dataIn)
        print("got from telescope str: " + dataStr)

        dataStr = dataStr.split(",")

        angle_horizontal = dataStr[0].replace('#','').split("'")[1]
        angle_horizontal = int(angle_horizontal,16)
        angle_horizontal = angle_horizontal/4294967296*360
        print ("horizontal: "+str(angle_horizontal))

        angle_vertical = dataStr[1].split("#")[0]
        angle_vertical = int(angle_vertical, 16)
        angle_vertical = angle_vertical / 4294967296 * 360
        print("vertical: " + str(angle_vertical))


    def manualRight(self,speed=3):
        moveRight = chr(80) + chr(2) + chr(16) + chr(36) + chr(speed) + chr(0) + chr(0) + chr(0)
        self.ser.write(moveRight.encode())

    def manualLeft(self,speed=3):
        moveLeft = chr(80) + chr(2) + chr(16) + chr(37) + chr(speed) + chr(0) + chr(0) + chr(0)
        self.ser.write(moveLeft.encode())

    def manualUp(self,speed=3):
        moveUp = chr(80) + chr(2) + chr(17) + chr(36) + chr(speed) + chr(0) + chr(0) + chr(0)
        self.ser.write(moveUp.encode())

    def manualDown(self,speed=3):
        moveDown = chr(80) + chr(2) + chr(17) + chr(37) + chr(speed) + chr(0) + chr(0) + chr(0)
        self.ser.write(moveDown.encode())


    def stopX(self):
        print("stop x")
        stopMoveX = chr(80) + chr(2) + chr(16) + chr(36) + chr(0) + chr(0) + chr(0) + chr(0)
        self.ser.write(stopMoveX.encode())
        time.sleep(0.1)

    def stopY(self):
        print("stop y")
        stopMoveY = chr(80) + chr(2) + chr(17) + chr(36) + chr(0) + chr(0) + chr(0) + chr(0)
        self.ser.write(stopMoveY.encode())
        time.sleep(0.1)


    def stop(self):
        print("calling stop...")
        self.stopX()
        self.stopY()

    def moveX(self,direction,speed):

        if abs(direction)<2:
            if (self.telescopeX_Speed != 0):
                self.stopX()
                self.telescopeX_Speed = 0
        else:
            if (self.telescopeX_Direction != direction | self.telescopeX_Speed != speed):

                self.telescopeX_Direction = direction
                self.telescopeX_Speed = speed

                if (direction > 0):
                    self.manualRight(speed)
                else:
                    self.manualLeft(speed)

    def moveY(self,direction,speed):

        if abs(direction)<2:
            if (self.telescopeY_Speed != 0):
                self.stopY()
                self.telescopeY_Speed = 0
        else:
            if (self.telescopeY_Direction != direction | self.telescopeY_Speed != speed):

                self.telescopeY_Direction = direction
                self.telescopeY_Speed = speed

                if (direction > 0):
                    self.manualDown(speed)
                else:
                    self.manualUp(speed)
    # def manualRight(self):
    #     self.ser.write(self.goRight_9)
    #     time.sleep(0.2)
    #     self.ser.write(self.StopX)
    # def manualLeft(self):
    #     self.ser.write(self.goLeft_9)
    #     time.sleep(0.2)
    #     self.ser.write(self.StopX)
    # def manualUp(self):
    #     self.ser.write(self.goUp)
    #     time.sleep(0.2)
    #     self.ser.write(self.StopX)
    # def manualDown(self):
    #     self.ser.write(self.goDown)
    #     time.sleep(0.2)
    #     self.ser.write(self.StopX)
    def imidiateStop(self):
        self.ser.write(chr(76).encode())

