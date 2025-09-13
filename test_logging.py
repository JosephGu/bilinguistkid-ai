import os
import sys
import logging
from logging.config import fileConfig

# 加载日志配置
try:
    log_conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_conf.ini')
    print(f"尝试加载日志配置文件: {log_conf_path}")
    print(f"配置文件是否存在: {os.path.exists(log_conf_path)}")
    
    if os.path.exists(log_conf_path):
        fileConfig(log_conf_path)
        print("日志配置从文件加载成功")
    else:
        # 如果没有配置文件，使用基本配置
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler("log/app.log", encoding='utf-8'),
                                logging.StreamHandler(sys.stdout)
                            ])
        print("使用基本日志配置")
    
    logger = logging.getLogger(__name__)
    print("Logger创建成功")
    
    # 测试日志输出
    logger.info("这是一条测试信息")
    logger.warning("这是一条警告信息")
    logger.error("这是一条错误信息")
    
    print("日志测试完成，请查看log/app.log文件")
    
    # 检查log文件夹是否存在
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')
    print(f"log文件夹是否存在: {os.path.exists(log_dir)}")
    
    # 检查app.log文件是否创建
    log_file = os.path.join(log_dir, 'app.log')
    print(f"app.log文件是否存在: {os.path.exists(log_file)}")
    if os.path.exists(log_file):
        print(f"app.log文件大小: {os.path.getsize(log_file)} 字节")
        # 读取前几行日志内容
        with open(log_file, 'r', encoding='utf-8') as f:
            print("日志文件前几行内容:")
            for i in range(5):
                line = f.readline()
                if not line:
                    break
                print(line.strip())
    

except Exception as e:
    print(f"测试过程中发生错误: {str(e)}")
    import traceback
    traceback.print_exc()