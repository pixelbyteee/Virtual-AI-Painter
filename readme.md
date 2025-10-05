# 🎨 AI Virtual Painter

Turn your webcam into a live, gesture‑controlled drawing canvas. This Python app uses real‑time hand tracking (MediaPipe + OpenCV) so you can draw, erase, change colors, and adjust brush size using nothing but intuitive finger gestures.

---
## 📑 Table of Contents
1. Overview
2. Features
3. Requirements
4. Installation
5. Project Structure
6. Running the App
7. Output Preview
8. Gestures & Controls
9. How It Works
10. Configuration & Customization
11. Troubleshooting
12. Roadmap / Ideas
13. License & Acknowledgements

---
## 1. 🧾 Overview
The Virtual Painter overlays your drawing actions onto a blank canvas while showing the live camera feed. A header bar at the top acts as a toolbar for color selection, erasing, and clearing the canvas. Pinch gestures dynamically change brush or eraser thickness.

---
## 2. ✨ Features
- Real‑time hand landmark tracking (MediaPipe Hands)
- Two interaction modes: Selection vs Drawing
- Extendable color palette (toolbar icons)
- Eraser tool & Clear‑All capability (if implemented later)
- Dynamic brush / eraser size via pinch distance
- Smoothed cursor positions (deque averaging)
- Visual feedback (cursor circle, selection rectangle, active header image)
- Separate persistent paint layer blended over live feed
- Simple modular hand tracking wrapper (`handtrackingmodule.py`)

---
## 3. 🛠 Requirements
Python 3.8+ (tested with 3.10). Install dependencies via `requirements.txt` or manually.

Core libraries:
- opencv-python
- mediapipe
- numpy

Optional (ideas / future):
- pillow (save/export images in different formats)
- pyinstaller (create standalone executable)

## 4. 🚀 Installation
Clone or copy the project folder (shown here as `Virtual_Painter`). If you cloned a larger parent repository, `Virtual_Painter` is already present.

### (Recommended) Create a virtual environment (Windows PowerShell)
```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

### Install dependencies
Using the provided file:
```powershell
pip install -r requirements.txt
```

Or minimal manual install:
```powershell
pip install opencv-python mediapipe numpy
```

---
## 5. 🗂 Project Structure
```
Virtual_Painter/
    main.py                # Application entry point (UI loop)
    handtrackingmodule.py  # Wrapper around MediaPipe Hands
    Header/                # Toolbar icon images (order matters)
        1.png
        2.png
        3.png
        4.png
requirements.txt         # Dependency list (root of workspace)
```

Icons in `Header/` are read in sorted order to build the toolbar. Replace them to customize tools/colors.

---
## 6. ▶ Running the App
From inside the project (after activating your venv):
```powershell
python main.py
```
Then point your webcam at your hand. Press `q` to quit.

---
## 7. 🖼 Output Preview
Example (Drawing Mode with toolbar and blended strokes):

![Sample Output](assets/Screenshot%202025-10-06%20022506.png)

<!-- > If the image does not display on GitHub, rename the file to a simpler name without spaces, e.g. `sample_output.png`, then update the link:
> `![Sample Output](assets/sample_output.png)` -->



---
## 8. ✋ Gestures & Controls
| Mode | Gesture | Action | Visual Cue |
|------|---------|--------|------------|
| Selection | Index & Middle fingers up | Hover over header icons to pick tool/color | Rectangle between raised fingers |
| Drawing | Only index finger up | Draw with current color | Colored circle at fingertip |
| Eraser | Same as drawing while eraser selected | Removes strokes (draws in background color) | White (or background) circle |
| Clear Canvas | Select clear icon | Wipes all strokes | Canvas resets |
| Resize Brush/Eraser | Pinch (Thumb–Index distance) | Adjust thickness dynamically | Cursor circle grows/shrinks |

Pinch distance is mapped to a thickness range (e.g. 5–50). Adjust scaling constants in `main.py` to suit preference.

---
## 9. 🧠 How It Works (Architecture)
1. Capture frames via OpenCV.
2. Run MediaPipe Hands to obtain 21 landmark coordinates.
3. Determine which fingers are raised (simple heuristic using y/x comparisons of landmarks).
4. If in Selection Mode: map index fingertip (x,y) to toolbar region and update active tool.
5. If in Drawing Mode: draw line segments from previous to current index fingertip on a persistent canvas layer.
6. If Eraser selected: draw with a thick stroke in background color.
7. Blend canvas layer with live frame (bitwise operations / masking) for a clean overlay.
8. Show combined output plus (optionally) a second window with raw canvas.

`handtrackingmodule.py` encapsulates: initialization, landmark extraction, finger state logic (if implemented there), and convenience helpers for position extraction.

---
## 10. 🔧 Configuration & Customization
| What | Where | How |
|------|-------|-----|
| Colors | List/array near top of `main.py` | Add RGB tuples & toolbar icon |
| Brush thickness | Variable/scaling factor | Adjust min/max clamp values |
| Eraser size | Separate scaling or constant | Tune independently |
| Toolbar icons | `Header/*.png` | Replace images (same dimensions recommended) |
| Camera index | `cv2.VideoCapture(0)` | Change `0` to another index |
| Output size | Frame resize logic | Use `cv2.resize` or set capture properties |

Export idea: capture final canvas with `cv2.imwrite("drawing.png", imgCanvas)`.

---
## 11. 🛠 Troubleshooting
| Issue | Possible Cause | Fix |
|-------|----------------|-----|
| No webcam feed | Wrong camera index | Try `1`, `2`, etc. |
| High CPU usage | Large frame size | Downscale frames (e.g. 960x540) |
| Laggy brush | Drawing every pixel jump | Add smoothing / interpolate points |
| Gesture misclassification | Ambient lighting / finger overlap | Improve lighting; tweak landmark thresholds |
| Icons not loading | Wrong folder path | Ensure `Header/` is alongside `main.py` |

If MediaPipe import fails: `pip install --upgrade mediapipe`.

---
## 12. 🧭 Roadmap / Ideas
- Save & load layers
- Undo / Redo stack
- Multi-hand multi-color simultaneous drawing
- Shape recognition (automatic circles, rectangles)
- Voice command integration
- GUI overlay for settings (Qt or Tkinter)
- Export time-lapse of drawing

---
## 13. 📄 License & Acknowledgements
Choose a license (e.g. MIT) and add it here. If using MediaPipe & OpenCV, retain their respective licenses.

Thanks to the open-source computer vision community for amazing tooling.

---
## 🙋 FAQ
**Q: Why are lines jagged?**  Increase smoothing by averaging last few points.

**Q: Can I use this without a mouse on a touchscreen?**  Yes—this is fully gesture-based; the mouse is not required.

**Q: How do I add more colors?**  Add icon + RGB value and extend the selection logic.

---
## 💡 Quick Reference (PowerShell)
```powershell
# Create & activate virtual environment
python -m venv .venv
./.venv/Scripts/Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run
python Virtual_Painter/main.py
```

Happy creating! 🎨 If you extend this, consider sharing improvements.