import mysql.connector
from mysql.connector import Error

def connect_mysql():
    try:
        # Thông tin kết nối CSDL
        connection = mysql.connector.connect(
            host='localhost',          # địa chỉ server (thường là localhost)
            user='root',             # tên đăng nhập MySQL
            password='',       # mật khẩu
            database='qlythuocankhang'    # tên database muốn kết nối
        )

        if connection.is_connected():
            print('✅ Kết nối MySQL thành công!')
            return connection

    except Error as e:
        print(f'❌ Lỗi kết nối MySQL: {e}')
        return None

# Ví dụ về cách sử dụng hàm:
# conn = connect_mysql()
# if conn:
#     # Thực hiện các truy vấn SQL tại đây
#     conn.close()