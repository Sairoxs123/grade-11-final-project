import cv2
import os
from random import choice
from time import sleep
from cs50 import SQL


def compare_images(image1_path, image2_path):
    # Read the images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Convert the images to grayscale
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Calculate the ORB features for each image
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(image1_gray, None)
    kp2, des2 = orb.detectAndCompute(image2_gray, None)

    # Use FLANN matcher to find matches between the two sets of descriptors
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Filter matches using Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # If there are enough good matches, consider the person to be present in both images
    if len(good_matches) > 50:
        return True
    else:
        return False



def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    chars = [chr(x) for x in range(65, 91)]

    ret, frame = cap.read()
    sleep(3)
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(delay) & 0xFF
    cv2.imwrite('{}.{}'.format(base_path, ext), frame)

    cv2.destroyWindow(window_name)



def register():
    db = SQL("mysql://root:@localhost:3306/final")
    name = input("Enter name: ")
    jssid = input("Enter jssid: ")
    grade_sec = input("Enter grade and section: ")

    res = db.execute("SELECT * FROM students WHERE jssid = (?)", jssid)

    if len(res) > 0:
        print("\nStudent is already registered.\n")

    else:
        print("\nPlease look at the camera.\n")
        save_frame_camera_key(0, 'photos/users', jssid)

        filepath1 = str(f"photos/users/{jssid}.jpg")

        results = db.execute("SELECT * FROM students")

        if len(results) > 0:
            for i in results:
                filepath2 = str(f"photos/users/{i['photo']}")

                exists = compare_images(filepath2, filepath1)

                if exists:
                    break

            if exists:
                print("Student with this face already exists.\n\n")
                os.remove(filepath1)

            else:
                db.execute("INSERT INTO students (name, class, jssid, photo) VALUES (?, ?, ?, ?)", name, grade_sec, jssid, f"{jssid}.jpg")
                print("You have registered successfully.")

        else:
            db.execute("INSERT INTO students (name, class, jssid, photo) VALUES (?, ?, ?, ?)", name, grade_sec, jssid, f"{jssid}.jpg")
            print("You have registered successfully.")

