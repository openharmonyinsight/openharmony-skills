from xdevice.__main__ import main_process

if __name__ == "__main__":
  # 执行testcases下的Example.py用例
  main_process("run -l Example -ta agent_mode:bin;screenshot:true")


