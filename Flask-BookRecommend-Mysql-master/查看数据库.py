import pymysql

# 配置数据库信息
config = {
    'user': 'root',
    'password': '123456',
    'port': 3306,
    'host': '127.0.0.1',
    'db': 'Book',
    'charset': 'utf8'
}


# 查询所有表内容
def query_all_tables():
    try:
        # 连接数据库
        connection = pymysql.connect(**config)
        cursor = connection.cursor()

        # 查询所有表名
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        # 遍历所有表
        for table in tables:
            table_name = table[0]
            print(f"\n=== Table: {table_name} ===")

            # 查询表内容
            try:
                cursor.execute(f"SELECT * FROM {table_name};")
                results = cursor.fetchall()
                if results:
                    for row in results:
                        print(row)
                else:
                    print("No data found in this table.")
            except Exception as e:
                print(f"Error querying table {table_name}: {e}")

    except Exception as e:
        print(f"Database connection error: {e}")
    finally:
        cursor.close()
        connection.close()


# 调用函数
query_all_tables()
