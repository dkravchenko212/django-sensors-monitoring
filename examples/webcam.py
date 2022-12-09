"""
Simply display the contents of the webcam with optional mirroring using OpenCV
Press <esc> to quit.
"""

import cv2


def save_video_webcam(mirror=False):
    n = 1
# use the device /dev/video{n} in this case /dev/video0
# On windows use the first connected camera in the device tree
    cap = cv2.VideoCapture(n)
    if cap.isOpened():
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(frame_height, frame_width, fps)
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('web_out.avi', fourcc, fps, (frame_width, frame_height))
        while True:
            ret, image_np = cap.read()
            if ret == True:
                # cv2.imshow('object detection', cv2.resize(image_np, (800, 600)))
                out.write(image_np)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows()


def main():
    save_video_webcam(mirror=True)


if __name__ == '__main__':
    main()

