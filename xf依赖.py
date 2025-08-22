import subprocess
import importlib
import sys
import argparse

def check_and_install_package(package_name, install_name=None, mirror=None):
    """检查并安装指定的包"""
    if install_name is None:
        install_name = package_name
    
    try:
        # 特殊处理：pycryptodome的模块名是Crypto
        if package_name == "Crypto":
            importlib.import_module("Crypto")
        else:
            importlib.import_module(package_name)
        print(f"✓ {package_name} 已安装")
        return True
    except ImportError:
        print(f"✗ {package_name} 未安装，正在安装...")
        try:
            # 构建安装命令
            install_cmd = [sys.executable, "-m", "pip", "install"]
            
            # 添加镜像源
            if mirror:
                install_cmd.extend(["-i", mirror])
            
            # 添加包名
            install_cmd.append(install_name)
            
            # 使用pip安装包
            subprocess.check_call(install_cmd)
            print(f"✓ {package_name} 安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ {package_name} 安装失败: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="自动安装Python依赖包")
    parser.add_argument("--mirror", "-m", default="https://pypi.mirrors.ustc.edu.cn/simple/",
                       help="指定pip镜像源，默认为中国科技大学源")
    args = parser.parse_args()
    
    print("开始检查并安装必要的Python依赖包...")
    print(f"使用镜像源: {args.mirror}")
    print("-" * 60)
    
    # 要检查的包列表 (模块名, 安装名)
    packages = [
        ("requests", "requests"),
        ("Crypto", "pycryptodome"),
        ("requests", "requests[socks]")  # requests[socks]会安装requests及其socks支持
    ]
    
    all_installed = True
    for module_name, install_name in packages:
        if not check_and_install_package(module_name, install_name, args.mirror):
            all_installed = False
    
    print("-" * 60)
    if all_installed:
        print("所有依赖包已成功安装！")
    else:
        print("部分依赖包安装失败，请手动检查。")
        sys.exit(1)

if __name__ == "__main__":
    main()