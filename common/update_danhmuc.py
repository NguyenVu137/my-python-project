from ketnoidb.ketnoi_mysql import connect_mysql
# Hàm cập nhật danh mục
def update_danhmuc(madm, tendm_moi, mota_moi):
    connection = None
    try:
        connection = connect_mysql()
        if connection is None:
            return

        cursor = connection.cursor()

        # Câu lệnh SQL UPDATE hoàn chỉnh
        sql = """
        UPDATE danhmuc 
        SET tendm = %s, mota = %s 
        WHERE madm = %s
        """

        # Dữ liệu cập nhật
        data = (tendm_moi, mota_moi, madm)

        # Thực thi truy vấn
        cursor.execute(sql, data)

        # Lưu thay đổi vào database
        connection.commit()

        # Kiểm tra và in thông báo
        if cursor.rowcount > 0:
            print(f"✅ Đã cập nhật thành công danh mục có ID: {madm} sang tên mới: {tendm_moi}")
        else:
            print(f"⚠️ Không tìm thấy danh mục có ID: {madm} hoặc dữ liệu không thay đổi.")

    except Error as e:
        print(f"❌ Lỗi khi cập nhật danh mục: {e}")

    finally:
        # Đảm bảo đóng kết nối và cursor
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Ví dụ về cách sử dụng hàm:
# Giả sử bạn muốn cập nhật danh mục có ID 5 từ 'Quần áo' thành 'Trang phục'
# update_danhmuc(5, 'Trang phục', 'Quần áo và phụ kiện may sẵn cao cấp')