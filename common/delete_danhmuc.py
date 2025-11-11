# Hàm kết nối MySQL (Được cung cấp từ ảnh trước đó)
import mysql
from mysql.connector import Error


def connect_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='qlythuocankhang'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Lỗi kết nối MySQL: {e}")
        return None


# --- Bắt đầu hàm xóa ---

# Hàm xóa danh mục theo ID
def delete_danhmuc(madm):
    connection = None
    try:
        connection = connect_mysql()
        if connection is None:
            return

        cursor = connection.cursor()

        # Câu lệnh SQL DELETE
        # Đây là phần tiếp theo từ hình ảnh của bạn
        sql = "DELETE FROM danhmuc WHERE madm = %s"

        # Thực thi truy vấn với ID danh mục được truyền vào
        cursor.execute(sql, (madm,))  # Lưu ý: (madm,) là một tuple có một phần tử

        # Lưu thay đổi vào database
        connection.commit()

        # Kiểm tra và in thông báo
        if cursor.rowcount > 0:
            print(f"✅ Đã xóa thành công danh mục có ID: {madm}")
        else:
            print(f"⚠️ Không tìm thấy danh mục có ID: {madm} để xóa.")

    except Error as e:
        print(f"❌ Lỗi khi xóa danh mục: {e}")

    finally:
        # Đảm bảo đóng kết nối và cursor
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Ví dụ về cách sử dụng hàm:
# delete_danhmuc(5)  # Xóa danh mục có madm = 5