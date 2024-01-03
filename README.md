# Violation Traffic Detector
![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/HoDoTenHuy/app-violation-traffic)


The repository is a Detector project that allows you to easily detect and track vehicle violations in traffic using Simple Web services. Currently, a total of 2 classes of vehicles can be detected with a bounding box: car and motor.

- [x] Image file available
- [x] Video file available
- [ ] New yolo models can be added
- [ ] Other format models can be added

## Table of Contents

- [Structure](#Structure)
- [Usage](#Usage)
- [Examples](#Examples)
- [Team](#Team)
- [License](#License)

## Structure
- Dataset: coming soon
- Model
  - Detection
  - Yolov8 Github : https://github.com/ultralytics/ultralytics
- Tool
  - Frontend : Streamlit - https://docs.streamlit.io/en/stable/#
  - Backend : FastAPI - https://fastapi.tiangolo.com/
  - Annotation Tool : CVAT - https://github.com/openvinotoolkit/cvat

## Usage

1. Clone This Repository

   ```sh
   $ git clone https://github.com/HoDoTenHuy/app-violation-traffic.git
   ```

2. docker-compose commands

   ```sh
   $ docker-compose build
   $ docker-compose up
   ```

3. Visit Streamlit UI

- visit [http://localhost:8501](http://localhost:8501)

4. Run model

- Select model : yolov8
- Test Image or video upload
- Click 'Detect Vehicle Button'

## Example
    update later
1. Image Detect

2. Video Detect

License
----

MIT
