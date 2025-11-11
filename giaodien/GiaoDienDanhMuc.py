import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

from common.delete_danhmuc import connect_mysql


# =======================================================
# LƯU Ý QUAN TRỌNG:
# Đảm bảo các hàm CSDL mà bạn đã tạo (connect_mysql,
# insert_danhmuc, update_danhmuc, delete_danhmuc,
# get_all_danhmuc) đã được định nghĩa hoặc import TRƯỚC
# khi class DanhmucApp được chạy.
# =======================================================

# -------------------------------------------------------
# KHỞI TẠO LẠI CÁC HÀM CSDL ĐỂ CHẠY THỬ (NẾU BẠN CHƯA CÓ)
# NẾU CÓ RỒI, HÃY XÓA PHẦN NÀY ĐI
# -------------------------------------------------------



def get_all_danhmuc():
    connection = None
    try:
        connection = connect_mysql()
        if connection is None: return []

        cursor = connection.cursor()
        sql = "SELECT madm, tendm, mota FROM danhmuc"
        cursor.execute(sql)
        records = cursor.fetchall()
        return records

    except Error as e:
        print(f"❌ Lỗi khi truy vấn danh mục: {e}")
        return []


def insert_danhmuc(tendm, mota):
    connection = None
    try:
        connection = connect_mysql()
        if connection is None: return
        cursor = connection.cursor()
        sql = "INSERT INTO danhmuc (tendm, mota) VALUES (%s, %s)"
        data = (tendm, mota)
        cursor.execute(sql, data)
        connection.commit()
    except Error as e:
        raise Exception(f"Lỗi khi thêm danh mục: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def update_danhmuc(madm, tendm_moi, mota_moi):
    connection = None
    try:
        connection = connect_mysql()
        if connection is None: return
        cursor = connection.cursor()
        sql = "UPDATE danhmuc SET tendm = %s, mota = %s WHERE madm = %s"
        data = (tendm_moi, mota_moi, madm)
        cursor.execute(sql, data)
        connection.commit()
    except Error as e:
        raise Exception(f"Lỗi khi cập nhật danh mục: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def delete_danhmuc(madm):
    connection = None
    try:
        connection = connect_mysql()
        if connection is None: return
        cursor = connection.cursor()
        sql = "DELETE FROM danhmuc WHERE madm = %s"
        cursor.execute(sql, (madm,))
        connection.commit()
        return cursor.rowcount  # Trả về số dòng bị ảnh hưởng
    except Error as e:
        raise Exception(f"Lỗi khi xóa danh mục: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# -------------------------------------------------------


class DanhmucApp:
    def __init__(self, master):
        self.master = master
        master.title("Quản Lý Danh Mục Sản Phẩm")
        master.geometry("800x550")

        # --- Biến lưu trữ dữ liệu ---
        self.madm = tk.StringVar()
        self.tendm = tk.StringVar()
        self.mota = tk.StringVar()

        # --- Khung chứa các trường nhập liệu ---
        self.frame_input = tk.Frame(master)
        self.frame_input.pack(pady=10, padx=10, fill="x")

        tk.Label(self.frame_input, text="ID (Chỉ xem):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self.frame_input, textvariable=self.madm, state='readonly', width=50).grid(row=0, column=1, padx=5,
                                                                                            pady=5, sticky="ew")

        tk.Label(self.frame_input, text="Tên Danh Mục:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self.frame_input, textvariable=self.tendm, width=50).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(self.frame_input, text="Mô Tả:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self.frame_input, textvariable=self.mota, width=50).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Cấu hình grid column để trường nhập liệu tự mở rộng
        self.frame_input.grid_columnconfigure(1, weight=1)

        # --- Khung chứa các nút chức năng ---
        self.frame_buttons = tk.Frame(master)
        self.frame_buttons.pack(pady=10)

        ttk.Button(self.frame_buttons, text="➕ Thêm", command=self.add_danhmuc).pack(side="left", padx=10)
        ttk.Button(self.frame_buttons, text="✍️ Sửa", command=self.update_danhmuc).pack(side="left", padx=10)
        ttk.Button(self.frame_buttons, text="❌ Xóa", command=self.delete_danhmuc).pack(side="left", padx=10)
        ttk.Button(self.frame_buttons, text="🔄 Làm Mới", command=self.load_data).pack(side="left", padx=10)

        # --- Bảng hiển thị dữ liệu (Treeview) ---
        self.tree = ttk.Treeview(master, columns=("ID", "TenDM", "MoTa"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Định nghĩa các cột
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("TenDM", text="Tên Danh Mục", anchor="w")
        self.tree.heading("MoTa", text="Mô Tả", anchor="w")

        # Thiết lập chiều rộng cột
        self.tree.column("ID", width=50, stretch=tk.NO, anchor="center")
        self.tree.column("TenDM", width=200, anchor="w")
        self.tree.column("MoTa", width=400, anchor="w")

        # Gắn sự kiện khi chọn một dòng
        self.tree.bind("<<TreeviewSelect>>", self.select_record)

        # Tải dữ liệu ban đầu
        self.load_data()

    # --- CÁC HÀM XỬ LÝ DỮ LIỆU ---

    def load_data(self):
        """Tải dữ liệu từ CSDL và hiển thị lên Treeview."""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy dữ liệu mới
        try:
            # GỌI TRỰC TIẾP HÀM CSDL CỦA BẠN
            records = get_all_danhmuc()
            for record in records:
                self.tree.insert("", tk.END, values=record)
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu: {e}")

        self.clear_fields()

    def select_record(self, event):
        """Điền dữ liệu từ dòng được chọn vào các trường nhập liệu."""
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, 'values')

        self.madm.set(values[0])
        self.tendm.set(values[1])
        self.mota.set(values[2])

    def clear_fields(self):
        """Xóa nội dung trong các trường nhập liệu."""
        self.madm.set("")
        self.tendm.set("")
        self.mota.set("")

    def add_danhmuc(self):
        """Thêm danh mục mới vào CSDL."""
        tendm_val = self.tendm.get()
        mota_val = self.mota.get()

        if not tendm_val:
            messagebox.showwarning("Thiếu dữ liệu", "Tên Danh Mục không được để trống!")
            return

        try:
            # GỌI TRỰC TIẾP HÀM CSDL CỦA BẠN
            insert_danhmuc(tendm_val, mota_val)
            messagebox.showinfo("Thành công", f"Đã thêm danh mục: {tendm_val}")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", e)  # Lỗi đã được raise trong hàm CSDL

    def update_danhmuc(self):
        """Cập nhật thông tin danh mục."""
        madm_val = self.madm.get()
        tendm_val = self.tendm.get()
        mota_val = self.mota.get()

        if not madm_val:
            messagebox.showwarning("Thiếu ID", "Vui lòng chọn một dòng để Sửa.")
            return

        try:
            # GỌI TRỰC TIẾP HÀM CSDL CỦA BẠN
            update_danhmuc(int(madm_val), tendm_val, mota_val)
            messagebox.showinfo("Thành công", f"Đã cập nhật ID: {madm_val}")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", e)  # Lỗi đã được raise trong hàm CSDL

    def delete_danhmuc(self):
        """Xóa danh mục khỏi CSDL."""
        madm_val = self.madm.get()

        if not madm_val:
            messagebox.showwarning("Thiếu ID", "Vui lòng chọn một dòng để Xóa.")
            return

        if messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc muốn xóa danh mục ID: {madm_val}?"):
            try:
                # GỌI TRỰC TIẾP HÀM CSDL CỦA BẠN
                row_count = delete_danhmuc(int(madm_val))
                if row_count > 0:
                    messagebox.showinfo("Thành công", f"Đã xóa ID: {madm_val}")
                else:
                    messagebox.showwarning("Không tìm thấy", f"Không tìm thấy danh mục ID: {madm_val} để xóa.")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Lỗi CSDL", e)  # Lỗi đã được raise trong hàm CSDL


if __name__ == "__main__":
    # Khởi tạo cửa sổ gốc
    root = tk.Tk()
    app = DanhmucApp(root)
    # Bắt đầu vòng lặp sự kiện
    root.mainloop()