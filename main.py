import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def canny_edge_detection(image, T1, T2):
    edges = cv2.Canny(image, T1, T2)
    return edges

def open_image():
    # Mở hộp thoại chọn tệp
    file_path = filedialog.askopenfilename()
    if file_path:
        # Kiểm tra kiểu tệp
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        file_extension = file_path[file_path.rfind('.'):]
        if file_extension.lower() not in allowed_extensions:
            messagebox.showerror("Lỗi", "Chọn sai tệp ảnh! Vui lòng chọn lại")
            return
        # Xóa ảnh cũ nếu có
        global image
        try:
            del edges_label.image
            del image
        except:
            pass
        # Đọc ảnh
        image = cv2.imread(file_path)
        # Hiển thị ảnh gốc
        img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img = img.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        img_label.configure(image=img_tk)
        img_label.image = img_tk

def Tachbien():
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Thiết lập ngưỡng
    try:
        T1 = int(T1_entry.get())
        T2 = int(T2_entry.get())
    except:
        messagebox.showerror("Lỗi", "Vui lòng nhập số")
        return
    # Phát hiện biên ảnh bằng phương pháp Canny
    edges = canny_edge_detection(gray, T1, T2)
    # Hiển thị biên ảnh Canny
    edges_img = Image.fromarray(edges)
    edges_img = edges_img.resize((400, 400))
    edges_tk = ImageTk.PhotoImage(edges_img)
    edges_label.configure(image=edges_tk)
    edges_label.image = edges_tk

# Tạo cửa sổ giao diện
window = tk.Tk()
window.title("Canny Edge Detection")
window.geometry("850x450")

# Tạo nút "Open Image"
open_button = tk.Button(window, text="Open Image", command=open_image)
open_button.pack(pady=10)


# Tạo khung và tiêu đề cho phần cài đặt ngưỡng
threshold_frame = tk.Frame(window, bg="white", padx=20, pady=10)
threshold_frame.pack()

threshold_label = tk.Label(threshold_frame, text="Cài đặt ngưỡng:", font=("Arial", 12, "bold"), bg="white")
threshold_label.pack()

# Tạo cột nhập ngưỡng 1
T1_frame = tk.Frame(threshold_frame, bg="white")
T1_frame.pack(pady=5)

T1_label = tk.Label(T1_frame, text="Ngưỡng thấp:", font=("Arial", 10), bg="white")
T1_label.pack(side=tk.LEFT)

T1_entry = tk.Entry(T1_frame, width=10)
T1_entry.pack(side=tk.LEFT)
# Thêm văn bản khuyến khích bên phải của T1_entry
T1_hint_label = tk.Label(T1_frame, text="Khuyến khích chọn ngưỡng 40-50", font=("Arial", 8), fg="gray", bg="white")
T1_hint_label.pack(side=tk.RIGHT)
# Tạo cột nhập ngưỡng 2
T2_frame = tk.Frame(threshold_frame, bg="white")
T2_frame.pack(pady=5)

T2_label = tk.Label(T2_frame, text=" Ngưỡng cao:", font=("Arial", 10), bg="white")
T2_label.pack(side=tk.LEFT)

T2_entry = tk.Entry(T2_frame, width=10)
T2_entry.pack(side=tk.LEFT)
# Thêm văn bản khuyến khích bên phải của T1_entry
T2_hint_label = tk.Label(T2_frame, text="Khuyến khích chọn ngưỡng 80-100", font=("Arial", 8), fg="gray", bg="white")
T2_hint_label.pack(side=tk.RIGHT)
# Tạo nút "Tách biên"
tachbien_button = tk.Button(window, text="Tách biên", command=Tachbien)
tachbien_button.pack(pady=10)
# Tạo hai khung hình để hiển thị ảnh gốc và biên ảnh Canny
img_frame = tk.Frame(window)
img_frame.pack(side=tk.LEFT, padx=10)
edges_frame = tk.Frame(window)
edges_frame.pack(side=tk.LEFT, padx=10)

img_label = tk.Label(img_frame, bg="white")
img_label.pack(pady=10)
edges_label = tk.Label(edges_frame, bg="white")
edges_label.pack(pady=10)

# Chạy ứng dụng
window.mainloop()