from ketnoidb.ketnoi_mysql import connect_mysql


def get_all_danhmuc():
    connection = None
    try:
        connection = connect_mysql()
        if connection is None:
            return []  # Trả về danh sách rỗng nếu kết nối thất bại

        cursor = connection.cursor()

        # Câu lệnh SQL SELECT
        sql = "SELECT madm, tendm, mota FROM danhmuc"

        # Thực thi truy vấn
        cursor.execute(sql)

        # Lấy tất cả các dòng kết quả
        danhmuc_records = cursor.fetchall()

        print("✅ Truy vấn danh mục thành công!")

        # Hiển thị kết quả dưới dạng bảng (tùy chọn)
        print("\n--- Dữ liệu Danh mục ---")
        print(f"{'ID':<5} | {'TÊN DANH MỤC':<20} | {'MÔ TẢ'}")
        print("--------------------------------------------------")

        for record in danhmuc_records:
            madm, tendm, mota = record
            print(f"{madm:<5} | {tendm:<20} | {mota}")

        return danhmuc_records

    except Error as e:
        print(f"❌ Lỗi khi truy vấn danh mục: {e}")
        return []

    finally:
        # Đảm bảo đóng kết nối và cursor
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Ví dụ về cách sử dụng hàm:
# tat_ca_danh_muc = get_all_danhmuc()
# print(f"\nTổng số danh mục: {len(tat_ca_danh_muc)}")