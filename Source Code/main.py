import cv2
from utils import (
    detect_edges,
    region_of_interest,
    detect_lines,
    draw_lines,
    get_lane_lines,
    get_lane_center,
    get_steering_angle,
    draw_steering_line,
    fill_lane_area
)

video = cv2.VideoCapture("C:/Users/N Yashwanthraj/Downloads/Opencv/test_video2.mp4")

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    frame = cv2.resize(frame, (960, 540))

    edges = detect_edges(frame)
    roi = region_of_interest(edges)
    lines = detect_lines(roi)

    lane_lines = get_lane_lines(frame, lines)

    result = fill_lane_area(frame, lane_lines)

    line_image = draw_lines(frame, lane_lines)
    result = cv2.addWeighted(result, 1, line_image, 1, 1)

    center_data = get_lane_center(frame, lane_lines)
    if center_data is not None:
        lane_center, frame_center = center_data
        angle = get_steering_angle(frame, lane_center, frame_center)

        steering_image = draw_steering_line(frame, angle)
        result = cv2.addWeighted(result, 1, steering_image, 1, 1)

        cv2.putText(
            result,
            f"Steering Angle: {angle}",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

    cv2.imshow("Lane Assist", result)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
