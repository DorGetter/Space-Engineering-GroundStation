

import cv2
import math
import time
import Telecontrol


# ---------------------------
# get telescope controll
class telescopeTracker:

    def __init__(self, telescopeEnabled=True):
        self.telescopeEnabled = telescopeEnabled
        if (telescopeEnabled):
            self.telescope = Telecontrol.Telcontrol()
            time.sleep(2)
            print("telescope connected")
        self.camera_id = 0
        self.output_folder = 'telescope_output/'
        self.output_file = "track" + str(time.ctime()).replace(" ", "_") + ".avi"

        print("init start")

    def init_camera(self):

        # init input stream
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        # init output stream
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        self.target_center_x = int(frame_width / 2)
        self.target_center_y = int(frame_height / 2)
        print("image size: " + str(frame_width) + "," + str(frame_height))
        self.fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        print("init end")
        print("select tracking object start")
        # self.out = cv2.VideoWriter(self.output_folder + self.output_file, self.fourcc, 10, (frame_width, frame_height))
        self.out = cv2.VideoWriter(self.output_folder + self.output_file, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                   10, (frame_width, frame_height))

    # get image, and select an object to track on it
    def test(self):
        if (self.telescopeEnabled):
            # telescope.moveX(dx,speedX)
            # telescope.moveY(dy,speedY)

            self.telescope.goToZero()

    def track(self):
        frameCounter = 0
        # skip a few frames
        for i in range(20):
            self.cap.read()

        ok, image = self.cap.read()
        if not ok:
            print('Failed to read video')
            exit()

        bbox = cv2.selectROI("tracking", image)
        # tracker = cv2.TrackerMIL_create()
        # tracker = cv2.TrackerBoosting_create()
        tracker = cv2.TrackerCSRT_create()
        ok = tracker.init(image, bbox)

        def click(event, x, y, flags, param):
            global target_center_x, target_center_y
            if event == cv2.EVENT_LBUTTONDOWN:
                print(" center selected ", x, y)
                target_center_x = x
                target_center_y = y

        cv2.namedWindow("frame")
        cv2.setMouseCallback("frame", click)

        while self.cap.isOpened():
            # show the image
            ok, frame = self.cap.read()
            self.out.write(image)

            # update traker
            tracker_ok, newbox = tracker.update(frame)
            if (tracker_ok):
                image = frame
                # obj bounding box
                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                cv2.rectangle(frame, p1, p2, (200, 0, 0))
                # obj center
                obj_center_x = int((p1[0] + p2[0]) / 2)
                obj_center_y = int((p1[1] + p2[1]) / 2)
                cv2.circle(frame, (obj_center_x, obj_center_y), 10, (200, 0, 0), 3)

                # calc the dist from center frame point to your object
                # the goal is to match between them

                # TODO: maybe the order should be diferent, once you know the axis of the telescope, fix this
                dx = obj_center_x - self.target_center_x
                dy = obj_center_y - self.target_center_y

                # print ("dist to obj "+str(dx)+","+str(dy))
                # listX = [8, 7, 6]
                # listX = [7, 6, 4]
                # listX = [6, 5, 4]
                listX = [4, 3, 2]

                speedX = listX[0]
                if (abs(dx) < 100):
                    speedX = listX[0]

                if (abs(dx) < 75):
                    speedX = listX[1]

                if (abs(dx) < 50):
                    speedX = listX[2]

                # if (abs(dx) < 25):
                #     speedX = 5

                speedY = listX[0];
                if (abs(dy) < 100):
                    speedY = listX[0]

                if (abs(dy) < 75):
                    speedY = listX[1]

                if (abs(dy) < 50):
                    speedY = listX[2]

                # if (abs(dy) < 25):
                #     speedY = 5

                if (self.telescopeEnabled):
                    # telescope.moveX(dx,speedX)
                    # telescope.moveY(dy,speedY)

                    self.telescope.moveY(dx, speedX)
                    self.telescope.moveX(-dy, speedY)

            cv2.circle(frame, (self.target_center_x, self.target_center_y), 10, (0, 200, 0), 8)
            cv2.imshow('frame', frame)

            # keep frame count
            frameCounter = frameCounter + 1
            # print("frame counter"+str(frameCounter))

            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):
                cv2.destroyAllWindows()
                # select the bounding box of the object we want to track (make
                # sure you press ENTER or SPACE after selecting the ROI)
                bbox = cv2.selectROI("tracking", image)
                # tracker = cv2.TrackerMIL_create()
                # tracker = cv2.TrackerBoosting_create()
                tracker = cv2.TrackerCSRT_create()
                ok = tracker.init(image, bbox)

            if key == ord('w'):  # Esc key to stop
                self.telescope.manualUp()
                print('up')
            if key == ord('s'):  # Esc key to stop
                print('down')
                self.telescope.manualDown()
            if key == ord('a'):  # Esc key to stop
                print('left')
                self.telescope.manualLeft()
            if key == ord('d'):  # Esc key to stop
                print('right')
                self.telescope.manualRight()

            # let the drawing thread to work,by waiting for a key
            if key == ord("q"):
                cv2.destroyAllWindows()
                self.cap.release()
                self.out.release()
                if (self.telescopeEnabled):
                    self.telescope.stop()
                    self.telescope.disconnect()
                exit()



if __name__ == '__main__':
    t = telescopeTracker()
    t.init_camera()
    t.track()

