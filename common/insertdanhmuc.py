
from ketnoidb.ketnoi_mysql import connect_mysql
from mysql.connector import Error

def insert_danhmuc(tendm, mota):
    connection = None  # Khởi tạo connection để sử dụng trong khối finally
    try:
        connection = connect_mysql()
        if connection is None:
            return

        # 1. Tạo đối tượng cursor
        cursor = connection.cursor()

        # 2. Câu lệnh SQL và dữ liệu
        sql = "INSERT INTO danhmuc (tendm, mota) VALUES (%s, %s)"
        data = (tendm, mota)

        # 3. Thực thi truy vấn
        cursor.execute(sql, data)

        # 4. Lưu thay đổi vào database
        connection.commit()

        print(f"✅ Đã thêm danh mục: {tendm}")

    except Error as e:
        print(f"❌ Lỗi khi thêm danh mục: {e}")

    finally:
        # 5. Đảm bảo đóng kết nối và cursor
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Ví dụ về cách sử dụng hàm:
# insert_danhmuc("Thời trang Nam", "Các sản phẩm quần áo, phụ kiện cho nam giới")
# insert_danhmuc("Điện thoại", "Các mẫu smartphone mới nhất")