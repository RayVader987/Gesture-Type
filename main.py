import cv2
import mediapipe as mp
import time
import webbrowser
import difflib
import pyautogui
import os
import pygetwindow as gw

# Mediapipe hand tracking setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

# Keyboard layout 
keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", "BACKSPACE"],
    ["+", "-", "*", "/", "%", "=", "SPACE", "CLEAR", "ENTER"],
    ["CAPS", "CLOSE", ".", ",", "!", "?", "#", "$", "@"]
]

key_width = 60
key_height = 60
typed_word = ""
hover_start_time = None
hovered_key = None
hover_duration_required = 1  # seconds
caps_on = True  # CAPS LOCK initially on

# App launch mapping
app_actions = {
    "google": lambda: webbrowser.open("https://www.google.com"),
    "youtube": lambda: webbrowser.open("https://www.youtube.com"),
    "yt": lambda: webbrowser.open("https://www.youtube.com"),
    "gmail": lambda: webbrowser.open("https://mail.google.com"),
    "whatsapp": lambda: webbrowser.open("https://web.whatsapp.com"),
    "spotify": lambda: webbrowser.open("https://open.spotify.com"),
    "linkedin": lambda: webbrowser.open("https://www.linkedin.com"),
    "facebook": lambda: webbrowser.open("https://www.facebook.com"),
    "x": lambda: webbrowser.open("https://x.com/"),
    "instagram": lambda: webbrowser.open("https://www.instagram.com"),
    "insta": lambda: webbrowser.open("https://www.instagram.com"),
    "github": lambda: webbrowser.open("https://github.com"),
    "stackoverflow": lambda: webbrowser.open("https://stackoverflow.com"),
    "notepad": lambda: os.system("notepad.exe"),
    "calculator": lambda: os.system("calc.exe"),
    "vs code": lambda: os.system("code"),
    "vscode": lambda: os.system("code")
}

# Launch apps and focus desktop ones
def launch_app(command):
    cmd = command.strip().lower()
    closest_match = difflib.get_close_matches(cmd, app_actions.keys(), n=1, cutoff=0.5)
    if closest_match:
        matched_app = closest_match[0]
        print(f"✅ Opening: {matched_app}")
        app_actions[matched_app]()
        time.sleep(2)

        desktop_apps = {
            "notepad": "Untitled - Notepad",
            "calculator": "Calculator",
            "vs code": "Visual Studio Code",
            "vscode": "Visual Studio Code"
        }
        if matched_app in desktop_apps:
            try:
                windows = gw.getWindowsWithTitle(desktop_apps[matched_app])
                if windows:
                    win = windows[0]
                    win.activate()
            except:
                pass
    else:
        print("❓ Unknown app:", command)

# Draw keyboard
def draw_keyboard(frame):
    key_positions = {}
    y = 50
    for row in keys:
        row_width = len(row) * (key_width + 10) - 10
        x = (frame.shape[1] - row_width) // 2
        for key in row:
            x1, y1 = x, y
            x2, y2 = x + key_width, y + key_height
            key_positions[key] = (x1, y1, x2, y2)

            color = (0, 255, 0) if key == hovered_key else (255, 0, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            font_scale = 0.6 if len(key) == 1 else 0.5
            text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
            text_x = x1 + (key_width - text_size[0]) // 2
            text_y = y1 + (key_height + text_size[1]) // 2
            cv2.putText(frame, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2)

            x += key_width + 10
        y += key_height + 15
    return key_positions

def get_key_under_finger(x, y, key_positions):
    for key, (x1, y1, x2, y2) in key_positions.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            return key
    return None

# Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=20)

    key_positions = draw_keyboard(frame)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    current_hovered_key = None
    hand_detected = False

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            hand_detected = True
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            index_tip = (int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h))
            cv2.circle(frame, index_tip, 10, (0, 255, 0), -1)

            current_hovered_key = get_key_under_finger(index_tip[0], index_tip[1], key_positions)

            if current_hovered_key != hovered_key:
                hovered_key = current_hovered_key
                hover_start_time = time.time() if hovered_key else None
            else:
                if hovered_key and hover_start_time:
                    elapsed = time.time() - hover_start_time
                    cv2.putText(frame, f"Hovering: {hovered_key} ({elapsed:.1f}s)", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

                    if elapsed >= hover_duration_required:
                        if hovered_key == "SPACE":
                            typed_word += " "
                            pyautogui.press('space')
                        elif hovered_key == "CLEAR":
                            typed_word = ""
                        elif hovered_key == "BACKSPACE":
                            typed_word = typed_word[:-1]
                            pyautogui.press('backspace')
                        elif hovered_key == "ENTER":
                            print(f"Launching: {typed_word}")
                            launch_app(typed_word)
                            pyautogui.press('enter')
                            typed_word = ""
                        elif hovered_key == "CAPS":
                            caps_on = not caps_on
                        elif hovered_key == "CLOSE":
                            try:
                                win = gw.getActiveWindow()
                                if win:
                                    win.close()
                                    print("✅ Closed current window")
                            except Exception as e:
                                print("⚠️ Could not close window:", e)
                        else:
                            char = hovered_key.upper() if caps_on else hovered_key.lower()
                            typed_word += hovered_key
                            pyautogui.press(char)

                        hover_start_time = None
                        hovered_key = None
    else:
        cv2.putText(frame, "❌ Hand NOT detected", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        hovered_key = None
        hover_start_time = None

    if hand_detected:
        cv2.putText(frame, "✅ Hand Detected", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # ✅ New Section: Display Typed Text Below Keyboard with Wrapping
    bottom_y = 50 + len(keys) * (key_height + 15) + 30
    max_width = frame.shape[1] - 60
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    thickness = 2
    wrap_text = []
    line = ""

    for char in typed_word:
        size = cv2.getTextSize(line + char, font, font_scale, thickness)[0]
        if size[0] < max_width:
            line += char
        else:
            wrap_text.append(line)
            line = char
    wrap_text.append(line)

    box_height = (len(wrap_text) + 1) * 35
    box_top_left = (20, bottom_y)
    box_bottom_right = (frame.shape[1] - 20, bottom_y + box_height)

    cv2.rectangle(frame, box_top_left, box_bottom_right, (0, 0, 0), -1)
    cv2.rectangle(frame, box_top_left, box_bottom_right, (0, 255, 255), 2)

    cv2.putText(frame, "Typed:", (30, bottom_y + 30), font, font_scale, (0, 255, 255), thickness)
    for i, line in enumerate(wrap_text):
        y = bottom_y + 30 + (i + 1) * 30
        cv2.putText(frame, line, (30, y), font, font_scale, (0, 255, 255), thickness)

    cv2.imshow("Virtual Gesture Keyboard", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
