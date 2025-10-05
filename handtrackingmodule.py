import cv2
import mediapipe as mp
import time


class handDetector:
    """Simple wrapper around MediaPipe Hands for detecting and drawing hand landmarks."""
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        # Use named args to match MediaPipe's Hands constructor
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]
        self.results=None
        

    def findhands(self, img, draw=True):
        """Detect hands in a BGR image and optionally draw landmarks.

        Args:
            img: BGR image (as returned by cv2.VideoCapture.read())
            draw: whether to draw landmarks on the image

        Returns:
            img with optional drawings (returns original img if input is None)
        """
        if img is None:
            return img

        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image_rgb)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        self.lmlist=[]

        # This is the corrected line that prevents the error
        if self.results and self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            
            # Optimization: Get image shape once outside the loop
            h, w, c = img.shape
            
            for id, lm in enumerate(myhand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 10, (255,0,0), cv2.FILLED)

        return self.lmlist
    def fingerup(self):
        fingers=[]

        if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0]- 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #4 Fingers
        for id in range (1,5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id]-2][2]:
                fingers.append(1)
            
            else:
                fingers.append(0)
        return fingers
        
def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: cannot open camera. Try different index or check permissions.")
        return

    pTime = time.time()
    detector = handDetector()

    try:
        while True:
            success, img = cap.read()
            if not success or img is None:
                print("Failed to read from capture; exiting loop.")
                break

            img = detector.findhands(img)
            lmlist=detector.findPosition(img)
            if len(lmlist)!=0:
                print(lmlist[4])

            cTime = time.time()
            # protect against division by zero; if delta is 0 just set fps to 0
            delta = cTime - pTime
            fps = 1 / delta if delta > 0 else 0
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)

            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()