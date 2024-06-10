import mediapipe as mp
import cv2
import time
import pyautogui

class handDetector():
    def __init__(self, mode=False, maxHands=1, complexity=0, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands    
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.handedness = None

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
    
        if self.results.multi_hand_landmarks:
            self.handedness = self.results.multi_handedness
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                    
        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (0, 0, 255), -1)
        return lmList
    
    def fingersUp(self, lmList):
        tips = [4, 8, 12, 16, 20]
        fingers = []

        # Thumb
        if lmList[tips[0]][1] < lmList[tips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if lmList[tips[id]][2] < lmList[tips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    prev_index_finger_pos = None
    movement_threshold = 20  # Adjust this value based on your needs
    finger_up = False
    action_triggered = False

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        
        if len(lmList) != 0 and detector.handedness:
            handedness = detector.handedness[0].classification[0].label
            if handedness == "Left":
                fingers = detector.fingersUp(lmList)
                index_finger_pos = lmList[8] if len(lmList) > 8 else None
                print(fingers)
                index_middle_fingers_state = fingers[1:3]
                
                if fingers[1] == 1:
                    if not finger_up:
                        finger_up = True
                        prev_index_finger_pos = index_finger_pos
                        action_triggered = False
                    elif not action_triggered and prev_index_finger_pos:
                        dx = abs(index_finger_pos[1] - prev_index_finger_pos[1])
                        dy = abs(index_finger_pos[2] - prev_index_finger_pos[2])
                        if dx > movement_threshold or dy > movement_threshold:
                            print("Change")
                            pyautogui.press('right')
                            print('right')
                            time.sleep(1)
                            action_triggered = True          
                else:
                    finger_up = False
                    prev_index_finger_pos = None
                    action_triggered = False

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
