############################################################
################## Main Tracking Module ####################
############################################################

import cv2
import numpy as np
import Telecontrol
import time
import TrackFunc
class Tracker :
    
    # Init the telesecope control api
    def __init__(self,telescopeEnabled = True):

        self.old_points = np.array([[0, 0]],dtype=np.float32)
        self.point_selected = False
        self.point = (0, 0)
        self.telescopeEnabled = telescopeEnabled
        if (telescopeEnabled):
            self.telescope = Telecontrol.Telcontrol()
            time.sleep(2)
        self.camera_id = 1
        self.output_folder = 'telescope_output/'
        self.output_file = "track" + str(time.ctime()).replace(" ", "_") + ".avi"


        print("Telescope is Ready for Remote Controll")
    #init the camera
    def init_camera(self):
        # init input stream
        self.cap = cv2.VideoCapture(1)

        # init output stream

        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        self.target_center_x = int(frame_width / 2)
        self.target_center_y = int(frame_height / 2)
        """
        print("image size: " + str(frame_width) + "," + str(frame_height))
        self.fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        print("init end")
        print("select tracking object start")
        # self.out = cv2.VideoWriter(self.output_folder + self.output_file, self.fourcc, 10, (frame_width, frame_height))
        self.out = cv2.VideoWriter(self.output_folder + self.output_file, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                   10, (frame_width, frame_height))
        
        """
    #init tracking parameters    
    def tracker(self):

        close_flag = False
        far_flag = True

        is_tracking = False
        ApplyCrop = True
        lk_params = dict(winSize=(10, 10),
                         maxLevel=2,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        def rescale_frame(frame, scale=0.75):
            width = int(frame.shape[1] * scale)
            height = int(frame.shape[0] * scale)
            dimensions = (width, height)

            return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


        # points of the objects we wish to track
        def selected_point(event, x, y, flags, params):
            #global point, point_selected, old_points
            if event == cv2.EVENT_LBUTTONDOWN:
                self.point = (x, y)
                self.point_selected = True
                #print(self.point[0], self.point[1])
                self.old_points = np.array([[x, y]], dtype=np.float32)

        ret, frame1 = self.cap.read()
        ret, frame2 = self.cap.read()
        old_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        cv2.namedWindow("Frame")

        cv2.setMouseCallback("Frame", selected_point)
        point_selected = False

        #self.point = ()
        #self.old_points = np.array([[]])
        
        while self.cap.isOpened():
            #cv2.circle(frame1, (frame1.shape[1]//2, frame1.shape[0]//2), 10, (200, 200, 100), 3)
            diff = cv2.absdiff(frame1, frame2)

            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=5)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            gray_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

            for contour in contours:
                i = 1
                (x, y, w, h) = cv2.boundingRect(contour)
                if cv2.contourArea(contour) > 4000 or cv2.contourArea(contour) < 5:
                    continue

                if self.point_selected is True:
                    new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, self.old_points, None,
                                                                         **lk_params)
                    old_gray = gray_frame.copy()
                    self.old_points = new_points
                    # print(new_points)
                    x_, y_ = new_points.ravel()
                    if (abs(x - x_) <= 25) & (abs(y - y_ <= 25)):
                        is_tracking = True
                        ApplyCrop = False
                        cv2.circle(frame1, ((int)(x_), (int)(y_)), 5, (0, 255, 0), -1)
                        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame1, "tracking", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (40, 235, 249), 2)

                        x_y_coor = "track X: " + str(x_) + ", strack Y: " + '_' + str(y_)
                        cv2.putText(frame1, x_y_coor, (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (40, 235, 249), 2)

                        center = "image center: " + str(frame1.shape[1] // 2) + " , " + str(frame1.shape[0] // 2)
                        cv2.putText(frame1, center, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (40, 235, 249), 2)

                        center2_ = "move X: " + str(round(x_)) + ", move Y: " + str(
                            round(y_))

                        if self.telescopeEnabled:

                            if far_flag:
                                #print(x_,y_)
                                dx = x_-(frame1.shape[1]//2)
                                dy = y_-(frame1.shape[0]//2)
                                sx = 4
                                sy = 4
                                if abs(dx) < 100:
                                    sx = 3
                                if abs(dx) < 75:
                                    sx = 2
                                if abs(dx) < 50:
                                    sx = 1
                                if abs(dx) < 10:
                                    sx = 0

                                if abs(dy) < 100:
                                    sx = 3
                                if abs(dy) < 75:
                                    sx = 2
                                if abs(dy) < 50:
                                    sx = 1
                                if abs(dy) < 10:
                                    sx = 0

                            elif close_flag:
                                # print(x_,y_)
                                dx = x_ - (frame1.shape[1] // 2)
                                dy = y_ - (frame1.shape[0] // 2)
                                sx = 8
                                sy = 8
                                if abs(dx) < 100:
                                    sx = 6
                                if abs(dx) < 75:
                                    sx = 4
                                if abs(dx) < 50:
                                    sx = 2
                                if abs(dx) < 10:
                                    sx = 0

                                if abs(dy) < 100:
                                    sx = 6
                                if abs(dy) < 75:
                                    sx = 4
                                if abs(dy) < 50:
                                    sx = 2
                                if abs(dy) < 10:
                                    sx = 0

                            else:
                                print("no distance flag")

                            put_telescop_data = "dx: " + str(round(dx)) + ", dy: " + str(round(-dy)) + ", tele speed x axis: " + str(sy) + ", tele speed y axis: " + str(sx)
                            cv2.putText(frame1, put_telescop_data, (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (120, 120, 20), 2)

                            self.telescope.moveY(direction=round(dx), speed=sx)
                            self.telescope.moveX(direction=round(-dy), speed=sy)




                    else:
                        old_gray = gray_frame.copy()
                        self.old_points = new_points
                        # print(new_points)
                        x_, y_ = new_points.ravel()
                        p1 = x_
                        p2 = y_
                        cv2.circle(frame1, (int(x_), int(y_)), 5, (50, 50, 100), -1)
                else:
                    cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame1, 'Movement Found!', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

            # frame_resized = self.rescale_frame(frame1, scale=0.5)
            cv2.imshow("Frame", frame1)

            frame1 = frame2
            ret, frame2 = self.cap.read()
            # point_selected = False
            if cv2.waitKey(40) == 27:
                break


    def test(self):
        if (self.telescopeEnabled):
            #self.telescope.moveX(500,8)
            self.telescope.moveX(2,9)
            #self.telescope.goToZero()

if __name__ == "__main__":
    t = Tracker()
    t.init_camera()
    t.tracker()
    #t.test()

    #t.cap.release()
    #cv2.destroyAllWindows()
