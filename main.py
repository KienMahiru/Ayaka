import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


def save_image(frame):
    global image, edges, zoom_scale, image_loaded
    try:
        if image_loaded:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[
                ("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                if frame == "original":
                    # Apply the zoom factor to the original image before saving
                    zoomed_image = cv2.resize(
                        image, None, fx=zoom_scale, fy=zoom_scale)
                    cv2.imwrite(file_path, zoomed_image)
                elif frame == "edges":
                    if edges is None:
                        messagebox.showerror(
                            "Lỗi", "Vui lòng thực hiện chức năng tách biên trước khi lưu ảnh tách biên.")
                        return
                    # Apply the zoom factor to the edges before saving
                    zoomed_edges = cv2.resize(
                        edges, None, fx=zoom_scale, fy=zoom_scale)
                    cv2.imwrite(file_path, zoomed_edges)
                messagebox.showinfo("Thông báo", "Ảnh đã được lưu thành công.")
        else:
            messagebox.showinfo(
                "Thông báo", "Vui lòng nhập ảnh")
    except:
        messagebox.showerror("Error", "Vui lòng nhập ảnh")


# Mở ảnh từ file
def open_image():
    global image, zoom_scale, img_label, edges_label, image_loaded
    file_path = filedialog.askopenfilename()

    if file_path:
        try:
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            file_extension = file_path[file_path.rfind('.'):].lower()

            if file_extension not in allowed_extensions:
                messagebox.showerror(
                    "Lỗi", "Chọn sai định dạng ảnh! Vui lòng chọn lại.")
                return

            img_label.destroy()
            edges_label.destroy()
            image = cv2.imread(file_path)
            if image is not None:
                zoom_scale = 1.0
                image_loaded = True
                create_image_labels()
                update_image_display()
            else:
                messagebox.showerror(
                    "Lỗi", "Không thể đọc ảnh từ file. Vui lòng chọn lại.")
                image_loaded = False
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi mở ảnh.")
            image_loaded = False


def capture_from_camera():
    global image, zoom_scale, img_label, edges_label, image_loaded, capture

    # Release any existing camera capture
    if capture is not None and hasattr(capture, 'release'):
        capture.release()

    # Open a new camera capture
    # 0 corresponds to the default camera (change if necessary)
    capture = cv2.VideoCapture(0)

    ret, frame = capture.read()
    if ret:
        img_label.destroy()
        edges_label.destroy()

        # Convert the image to RGB color space
        image = frame

        # Update zoom scale and other parameters
        zoom_scale = 1.0
        image_loaded = True
        create_image_labels()
        update_image_display()
    else:
        messagebox.showerror("Lỗi", "Không thể mở camera. Vui lòng thử lại.")
        image_loaded = False

    # Auto-release the camera after capturing
    if capture is not None and hasattr(capture, 'release'):
        capture.release()


def create_image_labels():
    global img_label, edges_label
    img_label = tk.Label(img_frame)
    img_label.pack(pady=10)
    edges_label = tk.Label(edges_frame)
    edges_label.pack(pady=10)


# Xóa ảnh
def clear_frames():
    global image, edges, image_loaded
    try:
        if image_loaded:
            img_label.destroy()
            edges_label.destroy()
            image = None  # Cập nhật trạng thái khi xóa ảnh
            edges = None
            image_loaded = False
            messagebox.showinfo("Thông báo", "Ảnh đã được xóa thành công.")
        else:
            messagebox.showinfo(
                "Thông báo", "Vui lòng nhập ảnh")
    except AttributeError:
        pass
    except Exception as e:
        print(f"Error: {e}")


def canny_edge_detection(image, T1, T2):
    edges = cv2.Canny(image, T1, T2)
    return edges


# Tách biên ảnh bằng phương pháp Canny
def canny_edge_detection(image, T1, T2):
    edges = cv2.Canny(image, T1, T2)
    return edges


def Tachbien():
    global image, edges
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except:
        messagebox.showerror("Lỗi", "Vui lòng nhập ảnh")
        return
    try:
        T1 = int(T1_entry.get())
        T2 = int(T2_entry.get())
    except:
        messagebox.showerror("Lỗi", "Vui lòng nhập số")
        return
    edges = canny_edge_detection(gray, T1, T2)
    edges_img = Image.fromarray(edges)
    edges_img = edges_img.resize(
        (int(400 * zoom_scale), int(400 * zoom_scale)))
    edges_tk = ImageTk.PhotoImage(edges_img)
    edges_label.configure(image=edges_tk)
    edges_label.image = edges_tk


# Xoay ảnh
def Xoay():
    global image, image_loaded
    try:
        if image_loaded:
            height, width = image.shape[:2]
            center = (width // 2, height // 2)
            matrix = cv2.getRotationMatrix2D(center, 90, 1.0)
            image = cv2.warpAffine(
                image, matrix, (width, height), borderMode=cv2.BORDER_REPLICATE)
            update_image_display()
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập ảnh")
    except NameError:
        messagebox.showerror("Lỗi", "Vui lòng nhập ảnh")
        return


def update_image_display():
    global image, zoom_scale
    if image is not None:
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(rgb_image)
        img = img.resize((int(400 * zoom_scale), int(400 * zoom_scale)))
        img_tk = ImageTk.PhotoImage(img)
        img_label.configure(image=img_tk)
        img_label.image = img_tk
    else:
        # Hiển thị hộp thoại "Vui lòng nhập ảnh" nếu không có ảnh
        messagebox.showinfo(
            "Thông báo", "Vui lòng nhập ảnh")


# Phóng to, thu nhỏ ảnh
def zoom_in():
    try:
        global zoom_scale
        zoom_scale += 0.1
        update_image_display()
    except:
        messagebox.showerror("Error", "Vui lòng nhập ảnh")


def zoom_out():
    try:
        global zoom_scale
        if zoom_scale > 0.1:
            zoom_scale -= 0.1
            update_image_display()
    except:
        messagebox.showerror("Error", "Vui lòng nhập ảnh")


# Điều chỉnh độ tương phản của ảnh
def adjust_contrast():
    global image, image_loaded
    try:
        if image_loaded:
            if image is not None:
                # Convert BGR to RGB
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Get the contrast value from the slider
                contrast_value = float(contrast_slider.get())

                # Apply contrast adjustment
                adjusted_image = cv2.convertScaleAbs(
                    rgb_image, alpha=contrast_value, beta=0)

                # Convert back to BGR for further processing if needed
                image = cv2.cvtColor(adjusted_image, cv2.COLOR_RGB2BGR)

                # Display the adjusted image
                adjusted_img = Image.fromarray(adjusted_image)
                adjusted_img = adjusted_img.resize(
                    (int(400 * zoom_scale), int(400 * zoom_scale)))
                adjusted_img_tk = ImageTk.PhotoImage(adjusted_img)
                img_label.configure(image=adjusted_img_tk)
                img_label.image = adjusted_img_tk
        else:
            messagebox.showerror(
                "Error", "Vui lòng nhập ảnh")
    except:
        messagebox.showerror("Error", "Vui lòng nhập ảnh")


capture = None
image_loaded = False  # Biến kiểm soát trạng thái có ảnh trên giao diện hay không
edges = None
zoom_scale = 1.0

window = tk.Tk()
window.title("Canny Edge Detection")
scale_percent = 1
# Tạo nút "Open Image"
open_button = tk.Button(window, text="Open Image", command=open_image)
open_button.pack(pady=10)

capture_button = tk.Button(
    window, text="Capture from Camera", command=capture_from_camera)
capture_button.pack(pady=10)


# Tạo khung và tiêu đề cho phần cài đặt ngưỡng
threshold_frame = tk.Frame(window, bg="white", padx=20, pady=10)
threshold_frame.pack()

threshold_label = tk.Label(threshold_frame, text="Cài đặt ngưỡng:", font=(
    "Arial", 12, "bold"), bg="white")
threshold_label.pack()

# Tạo cột nhập ngưỡng 1
T1_frame = tk.Frame(threshold_frame, bg="white")
T1_frame.pack(pady=5)

T1_label = tk.Label(T1_frame, text="Ngưỡng thấp:",
                    font=("Arial", 10), bg="white")
T1_label.pack(side=tk.LEFT)

T1_entry = tk.Entry(T1_frame, width=10)
T1_entry.pack(side=tk.LEFT)
# Thêm văn bản khuyến khích bên phải của T1_entry
T1_hint_label = tk.Label(T1_frame, text="Khuyến khích chọn ngưỡng 40-50",
                         font=("Arial", 8), fg="gray", bg="white")
T1_hint_label.pack(side=tk.RIGHT)
# Tạo cột nhập ngưỡng 2
T2_frame = tk.Frame(threshold_frame, bg="white")
T2_frame.pack(pady=5)

T2_label = tk.Label(T2_frame, text=" Ngưỡng cao:",
                    font=("Arial", 10), bg="white")
T2_label.pack(side=tk.LEFT)

T2_entry = tk.Entry(T2_frame, width=10)
T2_entry.pack(side=tk.LEFT)
# Thêm văn bản khuyến khích bên phải của T1_entry
T2_hint_label = tk.Label(T2_frame, text="Khuyến khích chọn ngưỡng 80-100",
                         font=("Arial", 8), fg="gray", bg="white")
T2_hint_label.pack(side=tk.RIGHT)
# Tạo nút "Tách biên"
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

tachbien_button = tk.Button(button_frame, text="Tách biên", command=Tachbien)
tachbien_button.pack(side=tk.LEFT, padx=5)

nut_xoay = tk.Button(button_frame, text="Xoay", command=Xoay)
nut_xoay.pack(side=tk.LEFT, padx=5)

zoom_in_button = tk.Button(button_frame, text="Zoom In", command=zoom_in)
zoom_in_button.pack(side=tk.LEFT, padx=5)

zoom_out_button = tk.Button(button_frame, text="Zoom Out", command=zoom_out)
zoom_out_button.pack(side=tk.LEFT, padx=5)

clear_frames_button = tk.Button(
    button_frame, text="Xóa ảnh", command=clear_frames)
clear_frames_button.pack(side=tk.LEFT, padx=5)

# Tạo nút "Lưu ảnh" cho cả ảnh gốc và biên ảnh
save_original_button = tk.Button(
    button_frame, text="Lưu ảnh (Original)", command=lambda: save_image("original"))
save_original_button.pack(side=tk.LEFT, padx=5)

save_edges_button = tk.Button(
    button_frame, text="Lưu ảnh (Edges)", command=lambda: save_image("edges"))
save_edges_button.pack(side=tk.LEFT, padx=5)


# Thêm thanh trượt độ tương phản vào giao diện người dùng
contrast_frame = tk.Frame(window, bg="white", padx=20, pady=10)
contrast_frame.pack()

contrast_label = tk.Label(contrast_frame, text="Điều chỉnh độ tương phản:", font=(
    "Arial", 12, "bold"), bg="white")
contrast_label.pack()

contrast_slider = tk.Scale(contrast_frame, from_=0.1,
                           to=3.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
contrast_slider.set(1.0)  # Đặt giá trị mặc định
contrast_slider.pack()

# Thêm nút áp dụng điều chỉnh độ tương phản
apply_contrast_button = tk.Button(
    contrast_frame, text="Áp dụng Độ Tương Phản", command=adjust_contrast)
apply_contrast_button.pack()


# Tạo hai khung hình để hiển thị ảnh gốc và biên ảnh Canny
img_frame = tk.Frame(window)
img_frame.pack(side=tk.LEFT, padx=10)
edges_frame = tk.Frame(window)
edges_frame.pack(side=tk.LEFT, padx=10)

img_label = tk.Label(img_frame)
img_label.pack(pady=10)
edges_label = tk.Label(edges_frame)
edges_label.pack(pady=10)

# Tạo labels ban đầu
create_image_labels()

# Chạy ứng dụng
window.mainloop()
