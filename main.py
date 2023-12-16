import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


# Mở ảnh từ file
def open_image():
    global image, zoom_scale, img_label, edges_label
    file_path = filedialog.askopenfilename()
    if file_path:
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        file_extension = file_path[file_path.rfind('.'):]
        if file_extension.lower() not in allowed_extensions:
            messagebox.showerror("Lỗi", "Chọn sai tệp ảnh! Vui lòng chọn lại")
            return
        try:
            img_label.destroy()
            edges_label.destroy()
        except AttributeError:
            pass
        except Exception as e:
            print(f"Error: {e}")
        image = cv2.imread(file_path)
        zoom_scale = 1.0
        create_image_labels()
        update_image_display()


def create_image_labels():
    global img_label, edges_label
    img_label = tk.Label(img_frame)
    img_label.pack(pady=10)
    edges_label = tk.Label(edges_frame)
    edges_label.pack(pady=10)


# Xóa ảnh
def clear_frames():
    try:
        img_label.destroy()
        edges_label.destroy()
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
    try:
        global image
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        matrix = cv2.getRotationMatrix2D(center, 90, 1.0)
        image = cv2.warpAffine(
            image, matrix, (width, height), borderMode=cv2.BORDER_REPLICATE)
        update_image_display()
    except NameError:
        messagebox.showerror("Lỗi", "Vui lòng nhập ảnh")
        return


def update_image_display():
    img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    img = img.resize((int(400 * zoom_scale), int(400 * zoom_scale)))
    img_tk = ImageTk.PhotoImage(img)
    img_label.configure(image=img_tk)
    img_label.image = img_tk


# Phóng to, thu nhỏ ảnh
def zoom_in():
    global zoom_scale
    zoom_scale += 0.1
    update_image_display()


def zoom_out():
    global zoom_scale
    if zoom_scale > 0.1:
        zoom_scale -= 0.1
        update_image_display()


# Điều chỉnh độ tương phản của ảnh
def adjust_contrast():
    global image
    if image is not None:
        # Lấy giá trị từ thanh trượt để điều chỉnh độ tương phản
        contrast_value = float(contrast_slider.get())

        # Áp dụng điều chỉnh độ tương phản
        adjusted_image = cv2.convertScaleAbs(
            image, alpha=contrast_value, beta=0)

        # Hiển thị ảnh đầu ra trong frame chứa cả ảnh và kết quả của ảnh khi chỉnh độ tương phản
        adjusted_img = Image.fromarray(
            cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB))
        adjusted_img = adjusted_img.resize(
            (int(400 * zoom_scale), int(400 * zoom_scale)))
        adjusted_img_tk = ImageTk.PhotoImage(adjusted_img)
        img_label.configure(image=adjusted_img_tk)
        img_label.image = adjusted_img_tk


window = tk.Tk()
window.title("Canny Edge Detection")
scale_percent = 1
# Tạo nút "Open Image"
open_button = tk.Button(window, text="Open Image", command=open_image)
open_button.pack(pady=10)


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
