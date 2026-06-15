import sqlite3

# 数据库文件名
# DB_NAME 是常量，常量名通常用全大写，这是 Python 里的约定俗成
DB_NAME = "waifu_lore.db"


def init_db():
    """
    初始化数据库。

    init 是 initialize 的缩写，意思是“初始化”。
    init_db 这个名字不是必须的，但很常见。

    这个函数负责：
    1. 连接 SQLite 数据库
    2. 如果 memories 表不存在，就创建它
    3. 提交修改
    4. 关闭数据库连接
    """

    # 连接 SQLite 数据库
    # 如果 waifu_lore.db 不存在，sqlite3 会自动创建这个文件
    conn = sqlite3.connect(DB_NAME)

    # 创建 cursor
    # cursor 是“游标”，可以理解成执行 SQL 的工具
    cursor = conn.cursor()

    # 创建 memories 表
    # IF NOT EXISTS 表示：如果表不存在才创建，已经存在就不重复创建
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 提交修改
    # CREATE TABLE / INSERT / UPDATE / DELETE 这类操作通常需要 commit
    conn.commit()

    # 关闭数据库连接
    conn.close()


def save_memory(character_id, content):
    """
    保存一条长期记忆。

    参数:
        character_id:
            角色文件夹名，例如 "411"、"tsuki"。
            这里不用角色显示名，是因为角色显示名以后可能会改。
            文件夹名更适合作为稳定 id。

        content:
            要保存的记忆内容。
            例如："用户正在开发 Waifu Lore 项目。"

    返回:
        不需要返回值。
        因为这个函数的作用是把数据写入数据库。
        写入成功后，结果已经保存在 waifu_lore.db 文件里。
    """

    # 连接数据库
    conn = sqlite3.connect(DB_NAME)

    # 创建 cursor，用来执行 SQL
    cursor = conn.cursor()

    # 插入一条记忆
    # ? 是占位符，不是普通问号
    # 后面的 (character_id, content) 会按顺序填进两个 ?
    # 这样写比 f-string 更安全，是数据库操作的常见写法
    cursor.execute(
        """
        INSERT INTO memories (character_id, content)
        VALUES (?, ?)
        """,
        (character_id, content)
    )

    # INSERT 是修改数据库，所以需要 commit
    conn.commit()

    # 关闭数据库连接
    conn.close()
def load_memories(character_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #
    cursor.execute(
        """
        SELECT content from memories
        WHERE character_id = ?
        ORDER BY created_at ASC
        """,
        (character_id,)
    )
    rows = cursor.fetchall()
    # 关闭数据库连接
    conn.close()

    memories = []

    for row in rows:
        memories.append(row[0])
    return memories
#测试用,查看database内容
if __name__ == "__main__":
    init_db()


    print(load_memories("411"))