"""
This script is a Skeleton of a program to controll the Nextsar 8SE Telescope 
Just run it and watch the telescope move, then come back and implement your CV algorithms
For further info about the Telecontrol API visit the Telecontorl.py file
Written by Arkadi, Modified by Dor,Oren and Eldar
"""
import Telecontrol
import cv2
#import required modules for your code

class Telescope():
    
    def __init__(self,telescopeEnabled = True,camera_id = 1,port = 'com8'):
        #constructor for the telescope objects
        self.old_points = np.array([[0, 0]],dtype=np.float32)
        self.point_selected = False
        self.point = (0, 0)
        self.telescopeEnabled = telescopeEnabled()
        if telescopeEnabled:
            #TODO: Error handling
            self.telescope = Telecontrol.Telcontrol(port)
            time.sleep(2)
        self.camera_id = camera_id 
        self.output_folder = 'telescope_output/'
        self.output_file = "track" + str(time.ctime()).replace(" ", "_") + ".avi"

        print("Telescope is Ready for Remote Control")

    def init_camera(self):
        #init the camera, should be used to perform CV algorithms on frames captured 
        #from the mounted camera on the telescope
        self.cap = cv2.VideoCapture(self.camera_id)

    def test(self):
        if self.telescopeEnabled:
            self.telescope.goToZero()

if __name__ == "__main__":
    """ 
    -If you are using windows machine, check for the correct port on the device manager / or run the port_chacker_windows.py. 
    -If you are using linux machine, check for the correct port on the dev/ttyUSB folder
    """

    telescope = Telescope(camera_id = 1,port = 'com8') # 1-USB camera | 0-Built in Camera #
    telescope.init_camera() # For initializing VideoCapture # 
    telescope.test() # Now telescope will move a little #

    #if you have used cv2, uncomment these lines:
    #telescope.cap.release()
    #cv2.destroyAllWindows()

