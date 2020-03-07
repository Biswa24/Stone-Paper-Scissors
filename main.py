import numpy as np
import cv2
import random
from tensorflow.keras.models import load_model


def compare(playerchoice, cpuchoice):
    results = {('Paper', 'Stone'): 'w',
               ('Paper', 'Paper'): 'd',
               ('Paper', 'Scissors'): 'l',
               ('Stone', 'Paper'): 'l',
               ('Stone', 'Scissors'): 'w',
               ('Stone', 'Stone'): 'd',
               ('Scissors', 'Paper'): 'w',
               ('Scissors', 'Scissors'): 'd',
               ('Scissors', 'Stone'): 'l'}
    return results[(playerchoice, cpuchoice)]


cap = cv2.VideoCapture(0)
cv2.namedWindow("Game")
size = 30
usr = 0
comp = 0
arr = ['Stone', 'Paper', 'Scissors']

user = ''
computer = ''


model = load_model('./rps1.model')
while True:

    ret, frame = cap.read()

    cv2.rectangle(frame, (220,200), (500,500),color=(255, 255, 255), thickness=3)
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, "Press 'Space' to play and 'ESC' to exit", (300, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (225, 0, 255),3,cv2.LINE_AA)
    score = "Computer:- "+str(comp)+" Player:- "+str(usr)
    cv2.putText(frame, score, (780, 190), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (0, 120, 255), 2, cv2.LINE_AA)
    usr_choice = "Player: "+str(user)
    comp_choice = "Computer: "+str(computer)
    cv2.putText(frame, comp_choice, (780, 530), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (225, 0, 100), 2, cv2.LINE_AA)
    cv2.putText(frame, usr_choice, (780, 560), cv2.FONT_HERSHEY_COMPLEX_SMALL, .9, (225, 0, 100), 2, cv2.LINE_AA)
    cv2.imshow("Game", frame)

    k = cv2.waitKey(1)
    # ESC
    if k % 256 == 27:
        print("Terminating\n\n")

        if usr > comp:
            print("You defeated Machine by {} points".format(usr-comp))
        elif comp>usr:
            print("Machine defeated you by {} points".format(comp-usr))
        else:
            print("Game is draw")

        print("Closing the Game......\n\n")

        break

    # SPACE
    elif k % 256 == 32:
        im_arr = frame[203:500, 780:1057]
        im_arr = cv2.cvtColor(im_arr, cv2.COLOR_BGR2GRAY)
        im_arr = cv2.resize(im_arr, (size, size))
        user = arr[np.argmax(model.predict(im_arr.reshape(-1, size, size, 1)))]
        # cv2.imshow("Pic",im_arr)
        # print(user)
        # im_arr = []
        # print(im_arr,user)
        computer = random.choice(arr)

        val = compare(user, computer)

        if val == 'w':
            usr = usr+1
            print("Player Won")
            print("Player: {} || Computer: {}\n".format(usr, comp))
        elif val == 'l':
            comp = comp + 1
            print("Computer Won")
            print("Player: {} || Computer: {}\n".format(usr, comp))
        else:
            print("Game Draw")
            print("Player: {} || Computer: {}\n".format(usr, comp))


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
