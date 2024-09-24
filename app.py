import os
from flask import Flask, render_template
import psycopg2

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# 環境変数からSupabaseの接続情報を取得
host = os.getenv("SUPABASE_HOST")
dbname = os.getenv("SUPABASE_DB_NAME")
user = os.getenv("SUPABASE_DB_USER")
password = os.getenv("SUPABASE_DB_PASSWORD")
port = os.getenv("SUPABASE_PORT", "5432")  # デフォルトのポートは5432

# データベース接続関数
def get_data_from_db():
    try:
        # PostgreSQLに接続
        connection = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        cursor = connection.cursor()

        # データを取得（ここではusersテーブルを仮定）
        cursor.execute("SELECT id, name, email FROM users;")
        rows = cursor.fetchall()
        return rows

    except Exception as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()

# ルートページ
@app.route('/')
def index():
    # データベースからデータを取得
    data = get_data_from_db()
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
