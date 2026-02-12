import cv2
import time
from utils import (
    detect_edges,
    region_of_interest,
    detect_lines,
    get_lane_lines,
    fill_lane_area,
    draw_lines,
    get_lane_center,
    get_steering_angle,
    draw_steering_line,
    get_road_center,
    draw_road_path
)

video = cv2.VideoCapture("C:/Users/N Yashwanthraj/Downloads/Opencv/Vids/noolane2.mp4")

fps_video = video.get(cv2.CAP_PROP_FPS)
if fps_video == 0:
    fps_video = 30
frame_delay = 1.0 / fps_video

prev_time = time.time()

while video.isOpened():
    start_time = time.time()
    ret, frame = video.read()
    if not ret:
        break

    frame = cv2.resize(frame, (960, 540))

    edges = detect_edges(frame)
    roi = region_of_interest(edges)
    lines = detect_lines(roi)
    lane_lines = get_lane_lines(frame, lines)

    result = frame.copy()

    if len(lane_lines) == 2:
        result = fill_lane_area(result, lane_lines)
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
                (255, 255, 255),
                2
            )
    else:
        road_center, mask = get_road_center(frame)
        if road_center is not None:
            frame_center = frame.shape[1] // 2
            angle = get_steering_angle(frame, road_center, frame_center)
            result = draw_road_path(result, road_center, mask)
            steering_image = draw_steering_line(frame, angle)
            result = cv2.addWeighted(result, 1, steering_image, 1, 1)
            cv2.putText(
                result,
                f"Road Mode Angle: {angle}",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    fps_text = f"FPS: {int(fps)}"
    text_size = cv2.getTextSize(fps_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
    text_x = result.shape[1] - text_size[0] - 20

    cv2.putText(
        result,
        fps_text,
        (text_x, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("ADAS Lane Assist", result)

    elapsed = time.time() - start_time
    wait_time = max(1, int((frame_delay - elapsed) * 1000))
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
