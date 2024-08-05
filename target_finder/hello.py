import argparse
import cv2

def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-c", "--camera", type=int, default=0, help="camera index (default: 0)")
    args = vars(ap.parse_args())

    # determine whether to open a video file or use the camera
    if args["video"]:
        camVideo = cv2.VideoCapture(args["video"])
        if not camVideo.isOpened():
            print(f"Error: Could not open video file {args['video']}")
            return
    else:
        camVideo = cv2.VideoCapture(args["camera"])
        if not camVideo.isOpened():
            print(f"Error: Could not open camera with index {args['camera']}")
            return

    # keep looping
    while True:
        # grab the current frame and initialize the status text
        (grabbed, frame) = camVideo.read()
        status = "No Target in sight"

        # check to see if we have reached the end of the video
        if not grabbed:
            break

        # convert the frame to grayscale, blur it, and detect edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # grayscale
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)  # blur
        edged = cv2.Canny(blurred, 50, 150)  # canny edge detection

        # find contours in the edge map
        cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for cnt in cnts:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

            if len(approx) == 5:
                cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                status = "Target(s) in sight!"

        # draw the status text on the frame
        cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # show the frame and record if a key is pressed
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 's' key is pressed, stop the loop
        if key == ord("s"):
            break

    # cleanup the input recorded video and close any open windows
    camVideo.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()  