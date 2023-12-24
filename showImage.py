import cv2

def show_gray_image(gray):
    # Đặt chiều cao mới (show_height)
    new_height = 800

    # Tính toán tỉ lệ giữa chiều cao mới và chiều cao ban đầu
    ratio = new_height / gray.shape[0]

    # Tính toán chiều rộng mới dựa trên tỉ lệ
    new_width = int(gray.shape[1] * ratio)

    # Resize ảnh với kích thước mới
    resized_gray = cv2.resize(gray, (new_width, new_height))

     # Hiển thị ảnh xám đã resize
    cv2.imshow('show Image', resized_gray)

    cv2.waitKey(0)
    cv2.destroyAllWindows()