# FM Assessment

| 1 | Vehicle Counting | `car_counter/` | Count vehicles crossing a line in a video using YOLOv8 object tracking. |
| 2 | Deposit Amount OCR | `ocr_deposit_extraction/` | Extract the deposit amount from bank receipt / transfer slip images. |
| 3 | Sales Demand Forecasting | `sale_forecasting/` | Forecast daily sales with an ARIMA time-series model. |
| 4 | Store Location Web Scraping | `webscraping_project/` | Collect convenience-store locations across Malaysia via APIs. |
| 5 | AI Agent Safety Scenario | `Question 5 - The scenario.pdf` | Written answer on Prompt, Context & Harness Engineering. |

---
1. My Approach to Solving the Task

Each task was approached by first understanding the goal, choosing a proven
library rather than reinventing the wheel, and keeping the code simple and
readable.

Task 1 — Store Location Web Scraping (`webscraping_project/`)
- Goal: collect store locations (name, lat/long, address) for several
  convenience-store brands across Malaysia.
- Approach: two independent collectors are provided:
  - `google_places_scraper.py` — queries the **Google Places API (v1
    Text Search)** for each brand, biased to 8 major Malaysian regions, and
    saves the results (with full addresses) to `store_locations.csv`.
  - `store_scraper.py` — a free, key-less alternative using the **OpenStreetMap
    Overpass API**, matching store names within Malaysia's bounding box.
- The collected data is stored as a flat CSV for easy downstream analysis /
  mapping.

Task 2 — Vehicle Counting (`car_counter/`)
- Goal:count how many vehicles pass through a scene, broken down by type.
- Approach: use a pre-trained YOLOv8n model to detect objects in every
  frame, and use YOLO's built-in tracker (`model.track(..., persist=True)`) so
  each vehicle keeps a stable ID across frames.
- Counting logic: a vertical counting line is drawn at `line_x = 960`. For
  every tracked vehicle I store its previous centre-x. When the centre crosses
  the line (`prev_cx < line_x <= cx` or the reverse) and that track ID has not
  been counted before, it is counted once. This prevents double-counting.
- Only relevant classes are counted: `car`, `bus`, `truck`, `motorcycle`.
- The annotated video (boxes, IDs, live counts) is written to `output.mp4` and a
  final tally is printed to the console.

Task 3 — Deposit Amount OCR (`ocr_deposit_extraction/`)
- Goal: read the deposit / transfer amount from a receipt image.
- Approach (two-stage, label-anchored):
  1. EasyOCR: reads all text and bounding boxes from the grayscale image.
  2. I look for an amount label (`jumlah`, `amount`, `amaun`, etc., including
     common OCR misspellings like `ahount`) and find the text box directly
     below / beside it — that cell holds the value.
  3. That cell is cropped, up-scaled, and re-read with Tesseract using a
     digit/currency whitelist and a money regex (`\d[\d,]*\.\d{2}`) for a clean
     numeric result.
  4. Fallback: if the label-anchoring fails, run Tesseract on the whole
     image and search for an `RM <amount>` pattern.
- Using two OCR engines together makes the extraction more robust to noisy,
  low-quality scans.

Task 4 — Sales Demand Forecasting (`sale_forecasting/`)
- Goal: forecast future daily sales demand.
- Approach: aggregate the Kaggle demand-forecasting `train.csv` to total
  sales per day, sort chronologically, and forward-fill any gaps. The last 90
  days are held out as a test set; an ARIMA(5,1,0) model is fitted on the
  remaining history and used to forecast 90 steps ahead.
- Evaluation: MAE, RMSE and MAPE are reported, and actual vs. forecast is
  plotted for a visual sanity check.


---

2. Technologies and Tools Used

Language: Python 3

| Task | Key libraries / tools |
| Vehicle Counting | `ultralytics` (YOLOv8), `opencv-python` |
| Deposit OCR | `easyocr`, `pytesseract` (+ Tesseract OCR engine), `opencv-python`, `re` |
| Sales Forecasting | `pandas`, `numpy`, `statsmodels` (ARIMA), `scikit-learn`, `matplotlib` |
| Web Scraping | `requests`, `pandas`, Google Places API, OpenStreetMap Overpass API |

---

3. Steps to Reproduce the Results

Prerequisites
- Python 3.9+
- (Task 2 only) the Tesseract OCR engine installed on your system:
  ```bash
  # macOS
  brew install tesseract
  ```

- macOS:   `brew install tesseract`
- Ubuntu/Debian:   `sudo apt install tesseract-ocr`
- Windows   Download from https://github.com/UB-Mannheim/tesseract/wiki
  and add it to your PATH (or set `pytesseract.pytesseract.tesseract_cmd`
  to the tesseract.exe path in the script).

Verify with: `tesseract --version`

Install the Python dependencies:
```bash
pip install ultralytics opencv-python easyocr pytesseract \
            pandas numpy statsmodels scikit-learn matplotlib requests
```
run source venv/bin/activate (for each) after every "cd"

Task 1 — Web Scraping
```bash
cd webscraping_project

# Free, no key required (OpenStreetMap):
python store_scraper.py

# Google Places (requires a valid API key set in the script):
python google_places_scraper.py
```
- Output is written to `store_locations.csv`.
- **Note:** replace the API key in `google_places_scraper.py` with your own
  Google Places API key before running it.
- Install : python3 -m pip install pandas requests


Task 2 — Vehicle Counting
```bash
cd car_counter
python main.py
```
- Reads `video.mp4`, writes the annotated `output.mp4`, and prints the final
  count per vehicle type. Press **q** to stop early.
- Install : python3 -m pip install ultralytics opencv-python

Task 3 — Deposit Amount OCR
```bash
cd "ocr_deposit_extraction"
python ocr_deposit_extraction.py      # extract from images.jpeg
python test_run.py                    # run against all test images
python vnv_accuracy.py                # compare results to expected values
```
- Install : python3 -m pip install easyocr pytesseract opencv-python
  
Task 4 — Sales Forecasting
```bash
cd "sale_forecasting/demand-forecasting-kernels-only"
python forecast.py
```
- Prints MAE / RMSE / MAPE and shows the actual-vs-forecast plot.
- Install : python3 -m pip install pandas numpy statsmodels scikit-learn matplotlib

---

Repository Structure
```
FM_Assesment/
├── README.md
├── Question 5 - The scenario.pdf     # Task 5 — LLM safety scenario
├── webscraping_project/              # Task 1 — Store location scraping
│   ├── google_places_scraper.py
│   ├── store_scraper.py
│   └── store_locations.csv
├── car_counter/                      # Task 2 — Vehicle counting
│   ├── main.py                       # YOLOv8 vehicle counter
│   ├── yolov8n.pt                    # pre-trained model weights
│   ├── video.mp4                     # input video
│   └── output.mp4                    # annotated output
├── ocr_deposit_extraction/           # Task 3 — Deposit OCR
│   ├── ocr_deposit_extraction.py
│   ├── test_run.py
│   ├── vnv_accuracy.py
│   └── images.jpeg, rtaImage.jpg
└── sale_forecasting/                 # Task 4 — Sales forecasting
    └── demand-forecasting-kernels-only/
        ├── forecast.py
        └── train.csv, test.csv, sample_submission.csv
