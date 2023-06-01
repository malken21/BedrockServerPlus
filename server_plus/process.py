import sys
import asyncio


# コンソールに出力
def print_output(process):
    while True:
        output = process.stdout.readline()

        # poll() は 終了していなかったら None を返し、
        # 終了したらステータスを返す
        if (process.poll() is None):
            # コンソール出力
            print(output.strip().decode())
        else:
            # 終了したら return
            return


# コンソールから読み取り
async def read_input(process):
    while True:
        text = await asyncio.create_task(asyncio.to_thread(sys.stdin.readline))
        write_text(process, text)


# 文字 (引数 text) を書き込み
def write_text(process, text: str):
    process.stdin.write(text.encode())
    process.stdin.flush()
