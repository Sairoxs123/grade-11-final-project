import cv2
import os
from random import choice
from time import sleep
from cs50 import SQL
from datetime import date


def save_frame_camera_key(
    device_num, dir_path, basename, ext="jpg", delay=1, window_name="frame"
):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    chars = [chr(x) for x in range(65, 91)]

    rand = ""

    for i in range(5):
        rand += choice(chars)

    ret, frame = cap.read()
    sleep(2)
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(delay) & 0xFF
    cv2.imwrite("{}_{}.{}".format(base_path, rand, ext), frame)

    cv2.destroyWindow(window_name)

    return str(f"testing_{rand}.jpg")


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


def markattendance():
    db = SQL("mysql://root:@localhost:3306/final")
    print("\nLook into the camera please.\n")
    file1 = save_frame_camera_key(0, "photos/testing", "testing")
    image1_path = str(f"photos/testing/{file1}")
    results = db.execute("SELECT * FROM students")

    registered = False
    details = {}

    for i in results:
        image2_path = str(f"photos/users/{i['photo']}")
        is_person_present = compare_images(image1_path, image2_path)

        if is_person_present:
            registered = True
            details = {"name": i["name"], "class": i["class"], "jssid": i["jssid"]}
            break

        else:
            registered = False

    if registered:
        res = db.execute(
            "SELECT * FROM attendance WHERE jssid = (?) AND date = (?)",
            details["jssid"],
            date.today(),
        )

        if len(res) > 0:
            print("\n\nYou have already been marked present today.\n\n")

        else:
            db.execute(
                "INSERT INTO attendance (name, class, jssid, date) VALUES (?, ?, ?, ?)",
                details["name"],
                details["class"],
                details["jssid"],
                date.today(),
            )

            print("\n\nYou have been marked present.\n\n")

        os.remove(image1_path)

    else:
        print(
            """\n\nThe program is not able to recognize your face. Possible errors are:
1. You have not registered your details.
2. The lighthing in the surroundings is not sufficient.
3. The angle of the photo taken is not proper.\n\n"""
        )
        os.remove(image1_path)
