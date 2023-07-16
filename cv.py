import cv2
import os
import numpy as np


def blur_stream():
    cap = cv2.VideoCapture(0)
    model = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
    while True:
        status , photo = cap.read()
        gray = cv2.cvtColor(photo,cv2.COLOR_BGR2GRAY)
        face = model.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in face:
            #to store the clear image face 
            face_clear = photo[y:y+h,x:x+w]
            dst = cv2.GaussianBlur(photo,(19,19),30)
            #to replace the blurred image with clear face image
            dst[y:y+h,x:x+w] = face_clear
            cv2.imshow("My blureed image",dst)
        if cv2.waitKey(1) == 13:
            break
    cv2.destroyAllWindows()
    cap.release()

def background_blur():
    # Load the Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read the frame from the webcam
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Apply a blur effect to the background
        blurred = cv2.GaussianBlur(frame, (99, 99), 0)

        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract the region of interest (face) from the frame
            face = frame[y:y+h, x:x+w]

            # Replace the face region with the original, unblurred face
            blurred[y:y+h, x:x+w] = face

            # Display the result
            cv2.imshow('Background Blur with Visible Face', blurred)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) == 13:
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

def goggle_filter():
    cap = cv2.VideoCapture(0)

    # Load the face cascade XML file for face detection
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    # Load the goggles image with transparency
    goggles_img = cv2.imread('heart.png', cv2.IMREAD_UNCHANGED)

    while True:
        # Read the current frame from the video stream
        status, photo = cap.read()

        if not status:
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Process each detected face
        for (x, y, w, h) in faces:
            # Calculate the position and size of the face region
            face_roi = photo[y:y + h, x:x + w]

            # Resize the goggles image to match the dimensions of the face region
            goggles_resized = cv2.resize(goggles_img, (w, h))

            # Extract the alpha channel of the goggles image
            alpha = goggles_resized[:, :, 3] / 255.0

            # Create a mask for the goggles region
            mask = alpha.astype(np.uint8)

            # Apply the mask to remove the goggles region from the face
            bg_removed = cv2.bitwise_and(face_roi, face_roi, mask=(1 - mask))

            # Overlay the resized goggles image onto the face region
            output = bg_removed + cv2.bitwise_and(goggles_resized[:, :, :3], goggles_resized[:, :, :3], mask=mask)

            # Replace the face region with the modified output
            photo[y:y + h, x:x + w] = output

            # Draw a rectangle around the face
            #cv2.rectangle(photo, (x, y), (x + w, y + h), [0, 255, 0], 5)

        # Display the modified frame
        cv2.imshow("Video", photo)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(10) == 13:
            break

    # Release the video capture and close the windows
    cap.release()
    cv2.destroyAllWindows()

def separate_crop():
    #cropped face
    # Load the Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read the frame from the webcam
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Process each detected face
        for (x, y, w, h) in faces:
            # Crop the detected face from the frame
            face = frame[y:y+h, x:x+w]

            # Display the cropped face in a separate window
            cv2.imshow('Detected Face', face)

            # Draw a rectangle around the detected face in the original frame
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the frame with detected faces
        cv2.imshow('Face Detection', frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

def wink():
    # Load the pre-trained face and eye cascade classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Initialize the video capture
    cap = cv2.VideoCapture(0)

    # Variables for blink detection
    left_blink_counter = 0
    right_blink_counter = 0
    blink_threshold = 3  # Adjust this value according to your need

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Convert the frame to grayscale for face and eye detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Iterate over the detected faces
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Extract the region of interest (ROI) within the face
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            # Detect eyes within the ROI
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # Check for eye blinks
            for (ex, ey, ew, eh) in eyes:
                if ex < w/2:  # Check if left eye
                    if len(eyes) == 1:  # Only one eye detected
                        left_blink_counter += 1
                    else:
                        left_blink_counter = 0

                    if left_blink_counter >= blink_threshold:
                        # Open Chrome when the blink threshold is reached for the left eye
                        left_blink_counter = 0
                        right_blink_counter = 0  # Reset the blink counters

                else:  # Right eye
                    if len(eyes) == 1:  # Only one eye detected
                        right_blink_counter += 1
                    else:
                        right_blink_counter = 0

                    if right_blink_counter >= blink_threshold:
                        # Open Chrome when the blink threshold is reached for the right eye
                        pyautogui.press('win')
                        pyautogui.typewrite('https:https://youtu.be/_KhQT-LGb-4')
                        pyautogui.press('enter')
                        left_blink_counter = 0
                        right_blink_counter = 0  # Reset the blink counters

                # Draw rectangles around the eyes
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

        # Display the frame
        cv2.imshow('Eye Detection', frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1)==13:
            break

    # Release the video capture and close the windows
    cap.release()
    cv2.destroyAllWindows()

def cv():
    ch = 0
    while ch != 4:
        os.system('tput setaf 10')
        print("""
            -----------------------------------------------------
                Computer Vision:
            -----------------------------------------------------   
                1. Blur Face
                2. Background Blur
                3. Try Goggles
                4. Crop Yourself
                5. Main Menu
                6. Main Menu
            -----------------------------------------------------
            """)
        os.system("tput setaf 2")
        ch  = ""
        while ch == "":
            ch = input("Enter choice : ")
        ch = int(ch)

        if ch == 6:
            os.system("clear")
            break
        elif ch == 1:
            blur_stream()
        elif ch == 2:
            background_blur()
        elif ch  == 3:
            goggle_filter()
        elif ch == 4:
            separate_crop()
            

