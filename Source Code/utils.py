import cv2
import numpy as np

previous_left = None
previous_right = None
previous_angle = 90
previous_road_center = None


# ---------------- EDGE DETECTION ----------------
def detect_edges(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.Canny(blur, 50, 150)


# ---------------- ROI ----------------
def region_of_interest(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)

    polygon = np.array([[
        (0, height),
        (width, height),
        (width, int(height * 0.6)),
        (0, int(height * 0.6))
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    return cv2.bitwise_and(edges, mask)


# ---------------- HOUGH ----------------
def detect_lines(roi):
    return cv2.HoughLinesP(
        roi,
        1,
        np.pi / 180,
        threshold=50,
        minLineLength=40,
        maxLineGap=100
    )


# ---------------- LINE PROCESSING ----------------
def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line

    y1 = height
    y2 = int(height * 0.6)

    if abs(slope) < 0.1:
        slope = 0.1

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return [[x1, y1, x2, y2]]


def average_slope_intercept(frame, lines):
    global previous_left, previous_right

    left_fit = []
    right_fit = []

    if lines is None:
        return previous_left, previous_right

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        if x1 == x2:
            continue

        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        if slope < -0.3:
            left_fit.append((slope, intercept))
        elif slope > 0.3:
            right_fit.append((slope, intercept))

    if left_fit:
        left_avg = np.average(left_fit, axis=0)
        previous_left = make_points(frame, left_avg)

    if right_fit:
        right_avg = np.average(right_fit, axis=0)
        previous_right = make_points(frame, right_avg)

    return previous_left, previous_right


def get_lane_lines(frame, lines):
    return average_slope_intercept(frame, lines)


# ---------------- DRAWING ----------------
def draw_lines(frame, lines):
    line_image = np.zeros_like(frame)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 6)

    return line_image


def fill_lane_area(frame, lane_lines):
    overlay = frame.copy()

    left = lane_lines[0][0]
    right = lane_lines[1][0]

    points = np.array([[
        (left[0], left[1]),
        (left[2], left[3]),
        (right[2], right[3]),
        (right[0], right[1])
    ]], dtype=np.int32)

    cv2.fillPoly(overlay, points, (0, 255, 0))
    return cv2.addWeighted(frame, 1, overlay, 0.3, 0)


def get_lane_center(frame, lane_lines):
    left = lane_lines[0][0]
    right = lane_lines[1][0]

    lane_center = (left[2] + right[2]) // 2
    frame_center = frame.shape[1] // 2

    return lane_center, frame_center


# ---------------- STEERING ----------------
def get_steering_angle(frame, lane_center, frame_center):
    global previous_angle

    width = frame.shape[1]
    offset = lane_center - frame_center
    offset_norm = offset / width

    angle = int(90 + offset_norm * 45)  # normalized scaling
    angle = int(previous_angle * 0.85 + angle * 0.15)

    angle = max(45, min(135, angle))  # clamp

    previous_angle = angle
    return angle


def draw_steering_line(frame, angle):
    height, width, _ = frame.shape
    steering_image = np.zeros_like(frame)

    angle_rad = np.deg2rad(angle)
    length = height // 2

    x1 = width // 2
    y1 = height

    x2 = int(x1 + length * np.sin(angle_rad))
    y2 = int(y1 - length * np.cos(angle_rad))

    cv2.line(steering_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

    return steering_image


# ---------------- ROAD FALLBACK ----------------
def get_road_center(frame):
    global previous_road_center

    height, width, _ = frame.shape
    roi = frame[int(height * 0.6):height, :]

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 0, 50])
    upper = np.array([180, 80, 200])

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    moments = cv2.moments(mask)

    roi_area = mask.shape[0] * mask.shape[1]

    if moments["m00"] > 0.02 * roi_area:
        cx = int(moments["m10"] / moments["m00"])

        if previous_road_center is not None:
            cx = int(previous_road_center * 0.8 + cx * 0.2)

        previous_road_center = cx
        return cx, mask

    return previous_road_center, mask


def draw_road_path(frame, center_x):
    height, width, _ = frame.shape
    overlay = frame.copy()

    if center_x is not None:
        cv2.line(
            overlay,
            (center_x, height),
            (center_x, int(height * 0.6)),
            (0, 200, 255),
            6
        )

    return cv2.addWeighted(frame, 1, overlay, 0.7, 0)
