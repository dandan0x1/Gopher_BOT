#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime
from base64 import b64encode
from colorama import *
import asyncio, random, time, json, re, os, requests, urllib3, warnings, schedule, json,socket, time
import uuid
import platform
import subprocess
import hashlib

# 获取硬件码的函数
def get_hardware_id():
    """获取硬件码"""
    try:
        # 获取系统信息
        system_info = platform.system() + platform.release() + platform.machine()
        
        # 获取MAC地址
        mac = uuid.getnode()
        
        # 获取CPU信息
        cpu_info = platform.processor()
        
        # 组合信息并生成哈希
        hardware_string = f"{system_info}_{mac}_{cpu_info}"
        hardware_hash = hashlib.md5(hardware_string.encode()).hexdigest()
        
        return hardware_hash
    except Exception as e:
        print(f"获取硬件码时出错: {str(e)}")
        return "unknown_hardware_id"

# 获取公网IP地址的函数
def get_public_ip():
    """获取公网IP地址"""
    try:
        # 使用多个IP查询服务来获取公网IP
        ip_services = [
            "https://api.ipify.org",
            "https://ipinfo.io/ip",
            "https://icanhazip.com",
            "https://ident.me",
            "https://checkip.amazonaws.com"
        ]
        
        for service in ip_services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    public_ip = response.text.strip()
                    # 验证IP格式
                    if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', public_ip):
                        return public_ip
            except:
                continue
        
        # 如果所有服务都失败，尝试备用方法
        try:
            response = requests.get("https://httpbin.org/ip", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('origin', '').split(',')[0].strip()
        except:
            pass
            
        return "unknown_public_ip"
    except Exception as e:
        print(f"获取公网IP时出错: {str(e)}")
        return "unknown_public_ip"

# 版权
def show_copyright():
    """展示版权信息"""
    copyright_info = f"""{Fore.CYAN}
    *****************************************************
    *           X:https://x.com/ariel_sands_dan         *
    *           Tg:https://t.me/sands0x1                *
    *           Gopher BOT Version 1.1                  *
    *           Copyright (c) 2025                      *
    *           All Rights Reserved                     *
    *****************************************************
    """
    {Style.RESET_ALL}
    print(copyright_info)
    print('=' * 50)
    print(f"{Fore.GREEN}申请key: https://661100.xyz/ {Style.RESET_ALL}")
    print(f"{Fore.RED}联系Dandan: \n QQ:712987787 QQ群:1036105927 \n 电报:sands0x1 电报群:https://t.me/+fjDjBiKrzOw2NmJl \n 微信: dandan0x1{Style.RESET_ALL}")
    print('=' * 50)

class URLKeyManager:
    def __init__(self, project_id="68ef7ce7dd857608ecba46bc", base_url="https://661100.xyz/get_key.php"):
        """初始化类，设置默认的project_id和基础URL"""
        self.project_id = project_id
        self.base_url = base_url

    def generate_url(self, user_id, key):
        """根据user_id和key生成完整的URL"""
        return f"{self.base_url}?project_id={self.project_id}&user_id={user_id}&key={key}"

    def save_to_file(self, user_id, key, filename="config/credentials.txt"):
        """将user_id和key保存到txt文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"user_id: {user_id}\n")
                file.write(f"key: {key}")
            return f"数据已成功保存到 {filename}"
        except Exception as e:
            return f"保存文件时出错: {str(e)}"

    def read_from_file(self, filename="config/credentials.txt"):
        """从txt文件读取user_id和key"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                user_id = lines[0].strip().replace("user_id: ", "")
                key = lines[1].strip().replace("key: ", "")
            return user_id, key
        except FileNotFoundError:
            return None, None
        except IndexError:
            return "错误: 文件格式不正确", None
        except Exception as e:
            return f"读取文件时出错: {str(e)}", None

    def get_user_input_and_save(self, filename="config/credentials.txt"):
        """获取用户输入并保存user_id和key到文件"""
        user_id = input("请输入用户id: ")
        key = input("请输入项目key: ")
        return self.save_to_file(user_id, key, filename)

    def verify_url(self, user_id, key):
        """验证URL的返回结果"""
        url = self.generate_url(user_id, key)
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查HTTP状态码
            data = response.json()  # 解析JSON响应
            if data.get("status") == "error":
                print(f"验证失败: {data.get('message')}")
                return False
            elif data.get("status") == "success":
                print(f"验证成功: 获取到key - {data.get('key')}")
                return True
            else:
                print("未知的响应状态")
                return False
        except requests.RequestException as e:
            print(f"请求URL时出错: {str(e)}")
            return False
        except ValueError:
            print("响应不是有效的JSON格式")
            return False

    def post_user_info_to_server(self, user_id, key):
        """将用户信息POST到服务器"""
        try:
            # 硬编码服务器URL和配置
            server_url = "https://661100.xyz/user_info.php"
            timeout = 10
            
            # 获取公网IP和硬件码
            public_ip = get_public_ip()
            hardware_id = get_hardware_id()
            
            # 准备POST数据 - 同时支持新旧字段名
            post_data = {
                "user_id": user_id,
                "key": key,
                "public_ip": public_ip,
                "local_ip": public_ip,  # 兼容旧版本
                "hardware_id": hardware_id,
                "timestamp": datetime.now().isoformat(),
                "project_id": self.project_id
            }
            
            # 发送POST请求
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "KeyBot/1.0"
            }
            
            response = requests.post(server_url, json=post_data, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            if result.get("status") == "success":
                print(f"{Fore.GREEN}用户信息已成功发送到服务器{Style.RESET_ALL}")
                print(f"公网IP: {public_ip}")
                print(f"硬件码: {hardware_id}")
                return True, result.get("hardware_check", {})
            else:
                print(f"{Fore.RED}服务器返回错误: {result.get('message', '未知错误')}{Style.RESET_ALL}")
                return False, None
                
        except requests.RequestException as e:
            print(f"{Fore.RED}发送POST请求时出错: {str(e)}{Style.RESET_ALL}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"{Fore.RED}服务器错误详情: {error_detail}{Style.RESET_ALL}")
                except:
                    print(f"{Fore.RED}服务器响应: {e.response.text}{Style.RESET_ALL}")
            return False, None
        except ValueError as e:
            print(f"{Fore.RED}解析服务器响应时出错: {str(e)}{Style.RESET_ALL}")
            return False, None
        except Exception as e:
            print(f"{Fore.RED}发送用户信息时出现未知错误: {str(e)}{Style.RESET_ALL}")
            return False, None

    def replace_hardware_id(self, user_id, hardware_id):
        """请求服务器替换硬件码"""
        try:
            server_url = "https://661100.xyz/replace_hardware.php"
            timeout = 10
            
            post_data = {
                "user_id": user_id,
                "hardware_id": hardware_id
            }
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "KeyBot/1.0"
            }
            
            response = requests.post(server_url, json=post_data, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            result = response.json()
            if result.get("status") == "success":
                print(f"{Fore.GREEN}✅ {result.get('message')}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}替换次数: {result.get('replace_count')}/{result.get('max_replacements')}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}❌ {result.get('message')}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}替换硬件码时出错: {str(e)}{Style.RESET_ALL}")
            return False

    def handle_hardware_id_change(self, user_id, hardware_check):
        """处理硬件码变化"""
        if not hardware_check:
            return True
        
        can_replace = hardware_check.get('can_replace', True)
        message = hardware_check.get('message', '')
        previous_hardware_id = hardware_check.get('previous_hardware_id')
        current_hardware_id = hardware_check.get('current_hardware_id')
        replace_count = hardware_check.get('replace_count', 0)
        max_replacements = hardware_check.get('max_replacements', 3)
        
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
        
        if not can_replace:
            if previous_hardware_id and current_hardware_id:
                print(f"{Fore.YELLOW}⚠️  检测到硬件码变化！{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}上次: {previous_hardware_id}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}当前: {current_hardware_id}{Style.RESET_ALL}")
                print(f"{Fore.RED}❌ 已达到最大替换次数({max_replacements}次)，无法继续替换{Style.RESET_ALL}")
            return False
        
        if previous_hardware_id and current_hardware_id and previous_hardware_id != current_hardware_id:
            print(f"{Fore.YELLOW}⚠️  检测到硬件码变化！{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}上次: {previous_hardware_id}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}当前: {current_hardware_id}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}当前替换次数: {replace_count}/{max_replacements}{Style.RESET_ALL}")
            
            # 询问用户是否要替换
            while True:
                choice = input(f"{Fore.CYAN}是否要替换硬件码？(y/n): {Style.RESET_ALL}").strip().lower()
                if choice in ['y', 'yes', '是']:
                    # 请求服务器替换硬件码
                    if self.replace_hardware_id(user_id, current_hardware_id):
                        return True
                    else:
                        return False
                elif choice in ['n', 'no', '否']:
                    print(f"{Fore.YELLOW}❌ 用户取消替换{Style.RESET_ALL}")
                    return False
                else:
                    print(f"{Fore.RED}请输入 y 或 n{Style.RESET_ALL}")
        
        return True

#ip池检测
class ProxyChecker:
    def __init__(self):
        """初始化，用户输入代理 IP 和端口范围"""
        self.proxy_ip = input("请输入代理 IP (例如 192.168.2.7): ").strip()
        self.start_port, self.end_port = self.get_port_range()
        self.proxy_list = []
        self.valid_proxies = []

    def get_port_range(self):
        """获取用户输入的端口范围"""
        while True:
            try:
                start_port = int(input("请输入起始端口 (如 7000): ").strip())
                end_port = int(input("请输入结束端口 (如 70100): ").strip())
                if start_port > end_port or start_port <= 0 or end_port <= 0:
                    raise ValueError("起始端口必须小于等于结束端口，且必须为正整数。")
                return start_port, end_port
            except ValueError as e:
                print(f"输入错误: {e}，请重新输入！")

    def get_random_proxies(self, count=5):
        """从端口范围内随机抽取一定数量的代理"""
        available_ports = list(range(self.start_port, self.end_port + 1))
        selected_ports = random.sample(available_ports, min(count, len(available_ports)))
        self.proxy_list = [f"{self.proxy_ip}:{port}" for port in selected_ports]

    def check_proxy(self, proxy):
        """检查 HTTP 代理是否可用"""
        print(f"正在检测代理 {proxy} 是否可用...")
        test_url = "https://www.google.com"
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        try:
            response = requests.get(test_url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                print(f"代理 {proxy} 可用！")
                return True
        except requests.exceptions.RequestException:
            pass
        return False

    def filter_valid_proxies(self):
        """筛选可用的代理"""
        print("正在检测可用代理，并保存到 proxy.txt 文件...")
        self.valid_proxies = [proxy for proxy in self.proxy_list if self.check_proxy(proxy)]

    def save_proxies_to_file(self, filename="config/proxy.txt"):
        """将可用代理保存到 txt 文件"""
        if not self.valid_proxies:
            print("未找到可用代理，未生成文件。")
            return

        file_path = os.path.abspath(filename)
        print(f"保存路径: {file_path}")
        with open(filename, "w") as file:
            for proxy in self.valid_proxies:
                line = f"http://{proxy}\n"
                print(f"写入代理: {line.strip()}")
                file.write(line)

    def run(self):
        """主逻辑执行"""
        while True:
            try:
                proxy_count = int(input("请输入要随机抽取的代理数量: ").strip())
                if proxy_count <= 0:
                    raise ValueError("代理数量必须大于 0！")
                break
            except ValueError as e:
                print(f"输入错误: {e}，请重新输入！")

        self.get_random_proxies(count=proxy_count)
        self.filter_valid_proxies()
        self.save_proxies_to_file()

        if self.valid_proxies:
            print(f"已保存 {len(self.valid_proxies)} 个可用代理到 proxy.txt")
        else:
            print("没有可用代理，未生成文件。")

# 终端颜色
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'

    @staticmethod
    def c(text, color):
        return f"{color}{text}{Colors.RESET}"


def log_info(msg: str):
    print(f"{Colors.c('[✓] ' + msg, Colors.GREEN)}")


def log_warn(msg: str):
    print(f"{Colors.c('[⚠] ' + msg, Colors.YELLOW)}")


def log_error(msg: str):
    print(f"{Colors.c('[✗] ' + msg, Colors.RED)}")


def log_success(msg: str):
    print(f"{Colors.c('[✅] ' + msg, Colors.GREEN)}")


def log_loading(msg: str):
    print(f"{Colors.c('[⟳] ' + msg, Colors.CYAN)}")


def log_step(msg: str):
    print(f"{Colors.c(Colors.BOLD + '[➤] ' + msg, Colors.WHITE)}")


RPC_ENDPOINT = "https://rpc-gopher-testnet-validator.dev.masalabs.ai"
API_ENDPOINT = "https://hub.gopher-ai.com/api"
REST_ENDPOINT = "https://gopher-testnet-validator.dev.masalabs.ai"
CHAIN_ID = "gopher-testnet"
DENOM = "ugoai"
PREFIX = "gopher"
WALLET_FILE = "wallets.json"
PRIVATE_KEY_TXT = "config/private_key.txt"
PROXY_TXT = "config/proxy.txt"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
]


def get_random_ua() -> str:
    return random.choice(USER_AGENTS)


# 代理管理
_proxy_list: List[str] = []
_proxy_index: int = 0


def _normalize_proxy(proxy_string: str) -> Optional[str]:
    s = proxy_string.strip()
    if not s:
        return None

    # 与 index.js 等价的多格式解析（尽量兼容）
    import re

    m = re.match(r"^(https?):\/\/([^:]+):(\d+)@([^:]+):(.+)$", s)
    if m:
        return f"{m.group(1)}://{m.group(4)}:{m.group(5)}@{m.group(2)}:{m.group(3)}"

    m = re.match(r"^(https?):\/\/([^:]+):(\d+):([^:]+):(.+)$", s)
    if m:
        return f"{m.group(1)}://{m.group(4)}:{m.group(5)}@{m.group(2)}:{m.group(3)}"

    m = re.match(r"^(https?):\/\/([^:]+):([^@]+)@([^:]+):(\d+)$", s)
    if m:
        return f"{m.group(1)}://{m.group(2)}:{m.group(3)}@{m.group(4)}:{m.group(5)}"

    m = re.match(r"^(https?):\/\/([^:]+):(\d+)$", s)
    if m:
        return s

    m = re.match(r"^([^:]+):(\d+)@([^:]+):(.+)$", s)
    if m:
        return f"http://{m.group(3)}:{m.group(4)}@{m.group(1)}:{m.group(2)}"

    m = re.match(r"^([^:]+):(\d+):([^:]+):(.+)$", s)
    if m:
        return f"http://{m.group(3)}:{m.group(4)}@{m.group(1)}:{m.group(2)}"

    m = re.match(r"^([^:]+):([^@]+)@([^:]+):(\d+)$", s)
    if m:
        return f"http://{m.group(1)}:{m.group(2)}@{m.group(3)}:{m.group(4)}"

    m = re.match(r"^([^:]+):(\d+)$", s)
    if m:
        return f"http://{m.group(1)}:{m.group(2)}"

    log_warn(f"Invalid proxy format: {s}")
    return None


def load_proxies() -> None:
    global _proxy_list, _proxy_index
    _proxy_list = []
    _proxy_index = 0
    try:
        if os.path.exists(PROXY_TXT):
            with open(PROXY_TXT, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            _proxy_list = [p for p in (_normalize_proxy(x) for x in lines) if p]
            if _proxy_list:
                log_info(f"已从 {PROXY_TXT} 加载 {len(_proxy_list)} 条代理")
            else:
                log_warn(f"{PROXY_TXT} 中未找到有效代理，将以直连模式运行")
        else:
            log_warn(f"未找到 {PROXY_TXT}，将以直连模式运行")
    except Exception as e:
        log_error(f"读取 {PROXY_TXT} 出错: {e}")


def _next_proxy() -> Optional[str]:
    global _proxy_index
    if not _proxy_list:
        return None
    p = _proxy_list[_proxy_index]
    _proxy_index = (_proxy_index + 1) % len(_proxy_list)
    return p


def _requests_proxies() -> Optional[Dict[str, str]]:
    p = _next_proxy()
    if not p:
        return None
    # requests 代理字典
    return {"http": p, "https": p}


async def sleep(ms: int) -> None:
    await asyncio.sleep(ms / 1000)


# faucet、staking等
def _axios_like_headers(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'user-agent': get_random_ua(),
    }
    if extra:
        headers.update(extra)
    return headers


def _with_retry(fn, retries: int = 10, delay_ms: int = 5000):
    for i in range(1, retries + 1):
        try:
            return fn()
        except Exception as e:
            is_503 = '503' in str(e)
            is_429 = '429' in str(e)
            if i == retries:
                log_error("所有重试均已失败。")
                raise
            retry_delay = delay_ms
            if is_503:
                retry_delay = delay_ms * 2
                log_warn(f"服务不可用(503)。第 {i}/{retries} 次尝试，等待 {retry_delay/1000:.0f} 秒...")
            elif is_429:
                retry_delay = delay_ms * 3
                log_warn(f"触发限频(429)。第 {i}/{retries} 次尝试，等待 {retry_delay/1000:.0f} 秒...")
                log_warn(f"429错误是ip质量问题或者ip已经被用了!")
                #log_warn(f"详细错误信息: {e}")
            else:
                log_warn(f"第 {i}/{retries} 次尝试失败: {e}。{retry_delay/1000:.0f} 秒后重试...")
            time.sleep(retry_delay / 1000)


def claim_faucet(address: str) -> bool:
    def task():
        headers = _axios_like_headers({
            'Referer': 'https://hub.gopher-ai.com/gopher-faucet',
        })
        proxies = _requests_proxies()
        log_loading(f"正在为 {address} 领取测试币...")
        r = requests.post(f"{API_ENDPOINT}/faucet", json={"address": address}, headers=headers, timeout=30, proxies=proxies)
        if r.status_code != 200:
            error_msg = f"HTTP {r.status_code}: {r.text[:200]}"
            if r.status_code == 429:
                error_msg += f" (响应头: {dict(r.headers)})"
            raise RuntimeError(error_msg)
        data = r.json()
        if not data.get('success'):
            raise RuntimeError(data.get('message') or 'Faucet claim API returned success:false')
        log_success(f"领取成功！信息: {data.get('message')} 交易: {data.get('txHash')}")
        return True

    try:
        return _with_retry(task, retries=3, delay_ms=8000)
    except Exception as e:
        log_error(f"多次重试后领取失败: {e}")
        return False


def get_validator_address(address: str) -> Optional[str]:
    try:
        proxies = _requests_proxies()
        r = requests.get(f"{API_ENDPOINT}/staking/info?address={address}", headers=_axios_like_headers(), timeout=30, proxies=proxies)
        if r.status_code == 200:
            data = r.json()
            if data.get('success') and data.get('data', {}).get('allValidators'):
                return data['data']['allValidators'][0]['address']
        log_warn("未能找到任何验证者。")
        return None
    except Exception as e:
        log_error(f"获取验证者失败: {e}")
        return None


# 使用 cosmpy 进行签名与广播
COSMPY_AVAILABLE = True
try:
    from cosmpy.aerial.wallet import LocalWallet
    from cosmpy.crypto.keypairs import PrivateKey as CosmpyPrivateKey
    from cosmpy.protos.cosmos.gov.v1beta1.tx_pb2 import MsgVote as MsgVoteProto
    from cosmpy.protos.cosmos.tx.signing.v1beta1.signing_pb2 import SignMode
    from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
    from cosmpy.protos.cosmos.tx.v1beta1.tx_pb2 import TxBody, AuthInfo, SignerInfo, ModeInfo, Fee, Tx, SignDoc
    from cosmpy.protos.cosmos.crypto.secp256k1.keys_pb2 import PubKey
    from google.protobuf import any_pb2
except Exception:
    COSMPY_AVAILABLE = False
    log_warn("cosmpy 未安装，委托/投票将使用占位或跳过。请 pip install -r requirements.txt")


@dataclass
class WalletInfo:
    wallet: Any
    address: str


def load_private_keys() -> List[str]:
    keys: List[str] = []
    if os.path.exists(PRIVATE_KEY_TXT):
        with open(PRIVATE_KEY_TXT, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if s:
                    keys.append(s)
    return keys


def create_wallet(private_key_hex: str) -> WalletInfo:
    if not COSMPY_AVAILABLE:
        raise RuntimeError("cosmpy 未安装，无法创建钱包")
    pk_bytes = bytes.fromhex(private_key_hex)
    from cosmpy.crypto.keypairs import PrivateKey as PK
    wallet = LocalWallet(PK(pk_bytes), prefix=PREFIX)
    return WalletInfo(wallet=wallet, address=str(wallet.address()))


def _build_and_broadcast(wallet: WalletInfo, messages: List[Any], fee_amount: str, gas_limit: int, memo: str = "") -> str:
    if not COSMPY_AVAILABLE:
        raise RuntimeError("cosmpy 不可用")

    # 获取账户号/序列号
    proxies = _requests_proxies()
    acc_res = requests.get(f"{REST_ENDPOINT}/cosmos/auth/v1beta1/accounts/{wallet.address}", timeout=15, proxies=proxies)
    if acc_res.status_code != 200:
        raise RuntimeError(f"Failed to fetch account: {acc_res.status_code}")
    acc = acc_res.json().get("account", {})
    account_number = int(acc.get("account_number", 0))
    sequence = int(acc.get("sequence", 0))

    # 公钥
    pub_key_proto = PubKey(key=wallet.wallet.public_key().public_key_bytes)
    pub_key_any = any_pb2.Any()
    pub_key_any.Pack(pub_key_proto, type_url_prefix='')

    signer_info = SignerInfo(
        public_key=pub_key_any,
        mode_info=ModeInfo(single=ModeInfo.Single(mode=SignMode.SIGN_MODE_DIRECT)),
        sequence=sequence,
    )

    fee = Fee(amount=[Coin(denom=DENOM, amount=fee_amount)], gas_limit=gas_limit)

    auth_info = AuthInfo(signer_infos=[signer_info], fee=fee)

    # 打包消息 Any
    any_msgs: List[Any] = []
    for m in messages:
        any_msg = any_pb2.Any()
        any_msg.Pack(m, type_url_prefix='')
        any_msgs.append(any_msg)

    tx_body = TxBody(messages=any_msgs, memo=memo, timeout_height=0)

    sign_doc = SignDoc(
        body_bytes=tx_body.SerializeToString(),
        auth_info_bytes=auth_info.SerializeToString(),
        chain_id=CHAIN_ID,
        account_number=account_number,
    )

    sig = wallet.wallet.signer().sign(sign_doc.SerializeToString())
    tx = Tx(body=tx_body, auth_info=auth_info, signatures=[sig])

    tx_bytes_b64 = base64.b64encode(tx.SerializeToString()).decode()
    r = requests.post(
        f"{REST_ENDPOINT}/cosmos/tx/v1beta1/txs",
        json={"tx_bytes": tx_bytes_b64, "mode": "BROADCAST_MODE_SYNC"},
        timeout=30,
        proxies=proxies,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Broadcast failed: HTTP {r.status_code}")
    res = r.json()
    code = res.get("tx_response", {}).get("code", 0)
    if code != 0:
        raise RuntimeError(res.get("tx_response", {}).get("raw_log", "unknown error"))
    return res.get("tx_response", {}).get("txhash", "")


def delegate_tokens(wallet: WalletInfo, amount_goai: float) -> None:
    def task():
        validator = get_validator_address(wallet.address)
        if not validator:
            raise RuntimeError("Could not get validator address")

        # 通过 API 预制交易，拿到 fee、gas、memo、messages（index.js 行为）
        headers = _axios_like_headers({'Referer': 'https://hub.gopher-ai.com/staking'})
        proxies = _requests_proxies()
        r = requests.post(
            f"{API_ENDPOINT}/staking/prepare-tx",
            json={
                "type": "delegate",
                "delegatorAddress": wallet.address,
                "validatorAddress": validator,
                "amount": str(int(amount_goai * 1_000_000)),
            },
            headers=headers,
            timeout=30,
            proxies=proxies,
        )
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:120]}")
        data = r.json()
        if not data.get('success'):
            raise RuntimeError(data.get('message') or 'Failed to prepare delegation transaction')
        d = data['data']

        # 将 API messages 转 protobuf 需要映射，这里直接构造真实 MsgDelegate
        from cosmpy.protos.cosmos.staking.v1beta1.tx_pb2 import MsgDelegate as MsgDelegateProto
        from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
        msg = MsgDelegateProto(
            delegator_address=wallet.address,
            validator_address=validator,
            amount=Coin(denom=DENOM, amount=str(int(amount_goai * 1_000_000))),
        )
        txhash = _build_and_broadcast(wallet, [msg], fee_amount=d.get('fee', {}).get('amount', '3000'), gas_limit=int(d.get('gasEstimate', 200000)), memo=d.get('memo', 'delegate via Gopher Bot'))
        log_success(f"Delegation successful! Tx Hash: {txhash}")

    try:
        log_loading(f"Delegating {amount_goai} GOAI for {wallet.address}...")
        _with_retry(task, retries=12, delay_ms=7000)
    except Exception as e:
        log_error(f"Delegation failed after all retries: {e}")


def undelegate_tokens(wallet: WalletInfo, amount_goai: float) -> None:
    def task():
        validator = get_validator_address(wallet.address)
        if not validator:
            raise RuntimeError("Could not get validator address")
        headers = _axios_like_headers({'Referer': 'https://hub.gopher-ai.com/staking'})
        proxies = _requests_proxies()
        r = requests.post(
            f"{API_ENDPOINT}/staking/prepare-tx",
            json={
                "type": "undelegate",
                "delegatorAddress": wallet.address,
                "validatorAddress": validator,
                "amount": str(int(amount_goai * 1_000_000)),
            },
            headers=headers,
            timeout=30,
            proxies=proxies,
        )
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:120]}")
        data = r.json()
        if not data.get('success'):
            raise RuntimeError(data.get('message') or 'Failed to prepare undelegation transaction')
        d = data['data']

        from cosmpy.protos.cosmos.staking.v1beta1.tx_pb2 import MsgUndelegate as MsgUndelegateProto
        from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
        msg = MsgUndelegateProto(
            delegator_address=wallet.address,
            validator_address=validator,
            amount=Coin(denom=DENOM, amount=str(int(amount_goai * 1_000_000))),
        )
        txhash = _build_and_broadcast(wallet, [msg], fee_amount=d.get('fee', {}).get('amount', '3000'), gas_limit=int(d.get('gasEstimate', 200000)), memo=d.get('memo', 'undelegate via Gopher Bot'))
        log_success(f"Undelegation successful! Tx Hash: {txhash}")

    try:
        log_loading(f"Undelegating {amount_goai} GOAI for {wallet.address}...")
        _with_retry(task, retries=12, delay_ms=7000)
    except Exception as e:
        log_error(f"Undelegation failed after all retries: {e}")


def get_active_proposal() -> Optional[Dict[str, Any]]:
    try:
        proxies = _requests_proxies()
        r = requests.get(f"{REST_ENDPOINT}/cosmos/gov/v1/proposals?proposal_status=PROPOSAL_STATUS_VOTING_PERIOD", headers=_axios_like_headers({'User-Agent': get_random_ua()}), timeout=30, proxies=proxies)
        if r.status_code == 200:
            data = r.json()
            proposals = data.get('proposals', [])
            if proposals:
                proposals.sort(key=lambda x: int(x.get('id', '0')), reverse=True)
                p = proposals[0]
                log_info(f"发现活跃提案 #{p.get('id')}")
                return p
        log_warn("未找到活跃提案。")
        return None
    except Exception as e:
        log_error(f"获取提案失败: {e}")
        return None


def vote_on_proposal(wallet: WalletInfo, proposal_id: str, vote_option: int) -> None:
    def task():
        if not COSMPY_AVAILABLE:
            raise RuntimeError("cosmpy 不可用，无法进行投票")
        msg = MsgVoteProto(
            proposal_id=int(proposal_id),
            voter=wallet.address,
            option=vote_option,
        )
        txhash = _build_and_broadcast(wallet, [msg], fee_amount="3000", gas_limit=200000, memo="Voted with Gopher Bot")
        log_success(f"投票成功！交易哈希: {txhash}")

    try:
        log_loading(f"正在为 {wallet.address} 对提案 #{proposal_id} 投票...")
        _with_retry(task)
    except Exception as e:
        log_error(f"多次重试后投票失败: {e}")


# 新钱包流程（仅私钥）
from secrets import token_bytes

def generate_new_wallet() -> Dict[str, Any]:
    if not COSMPY_AVAILABLE:
        raise RuntimeError("cosmpy 不可用，无法生成钱包")
    # 直接生成 32 字节私钥
    from cosmpy.crypto.keypairs import PrivateKey as PK
    pk = PK(token_bytes(32))
    wallet = LocalWallet(pk, prefix=PREFIX)
    private_key_hex = pk.private_key_bytes.hex()
    return {"privateKey": private_key_hex, "address": str(wallet.address())}


def save_wallet_to_file(wallet_data: Dict[str, Any]) -> None:
    wallets: List[Dict[str, Any]] = []
    try:
        if os.path.exists(WALLET_FILE):
            with open(WALLET_FILE, 'r', encoding='utf-8') as f:
                wallets = json.load(f)
    except Exception as e:
        log_warn(f"Read {WALLET_FILE} error: {e}")
    wallets.append(wallet_data)
    try:
        with open(WALLET_FILE, 'w', encoding='utf-8') as f:
            json.dump(wallets, f, indent=2, ensure_ascii=False)
        log_success(f"Wallet details successfully saved to {WALLET_FILE}")
    except Exception as e:
        log_error(f"Error saving wallet to {WALLET_FILE}: {e}")


async def run_new_wallet_flow():
    log_step("正在生成新钱包...")
    try:
        data = generate_new_wallet()
        address = data['address']
        private_key_hex = data['privateKey']
        print(Colors.c("--------------------------------------------------", Colors.YELLOW))
        log_success("新钱包已创建！请务必保存私钥！")
        print(f"地址:       {address}")
        print(f"私钥:       {private_key_hex}")
        print(Colors.c("--------------------------------------------------", Colors.YELLOW))
        save_wallet_to_file({"address": address, "privateKey": private_key_hex})

        wallet_info = create_wallet(private_key_hex)

        log_step('1/4: 领取测试币...')
        faucet_success = claim_faucet(address)
        if not faucet_success:
            log_warn(f"由于领水失败，跳过该钱包 {address} 的后续步骤。")
            return
        log_info("等待 20 秒以确认到账...")
        await asyncio.sleep(20)

        log_step('2/4: 质押 1 GOAI...')
        delegate_tokens(wallet_info, 1.0)
        log_info("等待 20 秒...")
        await asyncio.sleep(20)

        log_step('3/4: 解押 0.1 GOAI...')
        undelegate_tokens(wallet_info, 0.1)
        log_info("等待 20 秒...")
        await asyncio.sleep(20)

        log_step('4/4: 在最新提案上投 YES...')
        proposal = get_active_proposal()
        if proposal:
            vote_on_proposal(wallet_info, str(proposal.get('id')), 1)
        else:
            log_warn("跳过投票；未找到活跃提案。")

        log_success("新钱包自动流程已完成！")

    except Exception as e:
        log_error(f"该钱包的自动流程失败: {e}")
        log_warn("继续处理下一个钱包（如有）...")


async def show_existing_wallet_menu():
    print("\n" + Colors.BOLD + "请选择对已有钱包执行的操作:" + Colors.RESET)
    print("1. 领取测试币\n2. 质押 (Delegate)\n3. 解押 (Undelegate)\n4. 提案投票\n5. 返回主菜单\n0. 退出")
    choice = input("请输入序号 > ").strip()
    if choice == '0':
        sys.exit(0)
    if choice == '5':
        return None

    private_keys = load_private_keys()
    if not private_keys:
        log_error("未在 config/private_key.txt 中找到任何私钥。")
        return None

    amount = None
    tx_count = None
    if choice in ['2', '3']:
        try:
            amount = float(input("请输入 GOAI 数量 (例如 0.5): ").strip())
            if amount <= 0:
                raise ValueError()
        except Exception:
            log_error("无效的数量。")
            return None
    if choice in ['1', '2', '3']:
        try:
            tx_count = int(input("每个钱包执行多少次交易? ").strip())
            if tx_count <= 0:
                raise ValueError()
        except Exception:
            log_error("无效的次数。")
            return None

    for key in private_keys:
        try:
            wi = create_wallet(key)
            print(Colors.c(f"[➤] 处理钱包: {wi.address}", Colors.WHITE))
            if choice == '1':
                for i in range(tx_count):
                    claim_faucet(wi.address)
                    if i < tx_count - 1:
                        await asyncio.sleep(5)
            elif choice == '2':
                for i in range(tx_count):
                    delegate_tokens(wi, amount)
                    if i < tx_count - 1:
                        await asyncio.sleep(10)
            elif choice == '3':
                for i in range(tx_count):
                    undelegate_tokens(wi, amount)
                    if i < tx_count - 1:
                        await asyncio.sleep(10)
            elif choice == '4':
                proposal = get_active_proposal()
                if proposal:
                    print("请选择投票选项: 1.Yes  2.Abstain  3.No  4.No with Veto")
                    try:
                        vote_choice = int(input("请输入序号 > ").strip())
                    except Exception:
                        vote_choice = 0
                    if vote_choice in [1, 2, 3, 4]:
                        vote_on_proposal(wi, str(proposal.get('id')), vote_choice)
                    else:
                        log_error("无效的投票选项。")
            else:
                log_warn("无效的选择。")
        except Exception as err:
            log_error(f"处理该钱包时出错: {err}")
        log_info("短暂等待后继续处理下一个钱包...")
        await asyncio.sleep(5)
    return None


async def run_complete_flow():
    """运行完整流程：领水+质押+解押+投票"""
    private_keys = load_private_keys()
    if not private_keys:
        log_error("未在 config/private_key.txt 中找到任何私钥。")
        return
    
    try:
        amount = float(input("请输入质押/解押的 GOAI 数量 (例如 1.0): ").strip())
        if amount <= 0:
            raise ValueError()
    except Exception:
        log_error("无效的数量。")
        return
    
    try:
        tx_count = int(input("每个钱包执行多少次交易? ").strip())
        if tx_count <= 0:
            raise ValueError()
    except Exception:
        log_error("无效的次数。")
        return
    
    # 询问是否定时运行
    print("\n" + Colors.c("是否设置定时运行？", Colors.CYAN))
    print("1. 立即运行一次")
    print("2. 设置定时运行（每天固定时间）")
    choice = input("请选择 (1-2): ").strip()
    
    if choice == "2":
        try:
            hours = int(input("请输入每天运行的小时 (0-23): ").strip())
            minutes = int(input("请输入每天运行的分钟 (0-59): ").strip())
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                raise ValueError()
        except Exception:
            log_error("无效的时间设置。")
            return
        
        log_info(f"已设置每天 {hours:02d}:{minutes:02d} 自动运行完整流程")
        
        # 先立即运行一次
        log_info("🚀 立即执行第一次运行...")
        await execute_wallet_flow(private_keys, amount, tx_count)
        
        # 然后开始定时运行
        log_info("⏰ 第一次运行完成，开始定时运行模式...")
        await run_scheduled_flow(private_keys, amount, tx_count, hours, minutes)
    else:
        log_info(f"开始为 {len(private_keys)} 个钱包运行完整流程...")
        await execute_wallet_flow(private_keys, amount, tx_count)


async def execute_wallet_flow(private_keys, amount, tx_count):
    """执行钱包流程"""
    for i, key in enumerate(private_keys, 1):
        try:
            wallet_info = create_wallet(key)
            log_step(f"处理钱包 {i}/{len(private_keys)}: {wallet_info.address}")
            
            # 1. 领取测试币
            log_step(f"钱包 {i}: 领取测试币...")
            for j in range(tx_count):
                claim_faucet(wallet_info.address)
                if j < tx_count - 1:
                    await asyncio.sleep(5)
            
            await asyncio.sleep(10)  # 等待确认
            
            # 2. 质押
            log_step(f"钱包 {i}: 质押 {amount} GOAI...")
            for j in range(tx_count):
                delegate_tokens(wallet_info, amount)
                if j < tx_count - 1:
                    await asyncio.sleep(10)
            
            await asyncio.sleep(10)  # 等待确认
            
            # 3. 解押
            log_step(f"钱包 {i}: 解押 {amount} GOAI...")
            for j in range(tx_count):
                undelegate_tokens(wallet_info, amount)
                if j < tx_count - 1:
                    await asyncio.sleep(10)
            
            await asyncio.sleep(10)  # 等待确认
            
            # 4. 投票
            log_step(f"钱包 {i}: 提案投票...")
            proposal = get_active_proposal()
            if proposal:
                vote_on_proposal(wallet_info, str(proposal.get('id')), 1)  # 默认投 YES
            else:
                log_warn(f"钱包 {i}: 未找到活跃提案，跳过投票")
            
            log_success(f"钱包 {i} 完整流程已完成！")
            
        except Exception as err:
            log_error(f"钱包 {i} 处理失败: {err}")
        
        # 钱包间等待
        if i < len(private_keys):
            log_info("等待 10 秒后处理下一个钱包...")
            await asyncio.sleep(10)
    
    log_success("所有钱包的完整流程已执行完毕！")


async def run_scheduled_flow(private_keys, amount, tx_count, target_hour, target_minute):
    """定时运行流程"""
    import datetime
    
    while True:
        now = datetime.datetime.now()
        target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        
        # 如果今天的目标时间已过，设置为明天
        if target_time <= now:
            target_time += datetime.timedelta(days=1)
        
        # 计算等待时间
        wait_seconds = (target_time - now).total_seconds()
        
        log_info(f"下次运行时间: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
        log_info("开始倒计时...")
        
        # 倒计时显示
        while wait_seconds > 0:
            hours = int(wait_seconds // 3600)
            minutes = int((wait_seconds % 3600) // 60)
            seconds = int(wait_seconds % 60)
            
            # 每30秒更新一次显示
            if int(wait_seconds) % 30 == 0 or wait_seconds < 60:
                print(f"\r{Colors.c('⏰ 距离下次运行还有: ', Colors.CYAN)}{hours:02d}:{minutes:02d}:{seconds:02d}", end="", flush=True)
            
            await asyncio.sleep(1)
            wait_seconds -= 1
        
        print()  # 换行
        log_info("⏰ 定时运行开始！")
        
        # 执行钱包流程
        await execute_wallet_flow(private_keys, amount, tx_count)
        
        log_info("⏰ 本次定时运行完成，等待下次运行...")


def show_main_menu():
    print("\n" + Colors.BOLD + "--- 主菜单 ---" + Colors.RESET)
    print("1. 创建新钱包并运行自动流程\n2. 使用 private_key.txt 中的钱包\n3. 运行完整流程（领水+质押+解押+投票）\n0. 退出")
    return input("请输入序号 > ").strip()


async def run_main():
    load_proxies()
    while True:
        choice = show_main_menu()
        if choice == '1':
            try:
                wallet_count = int(input("要创建多少个钱包? ").strip())
                if wallet_count <= 0:
                    raise ValueError()
            except Exception:
                log_error("无效的数量，请输入正整数。")
                continue
            for i in range(1, wallet_count + 1):
                log_step(f"--- 正在创建第 {i}/{wallet_count} 个钱包 ---")
                await run_new_wallet_flow()
                if i < wallet_count:
                    log_info("--- 当前钱包流程完成。等待 5 秒后继续下一个... ---\n")
                    await asyncio.sleep(5)
            log_success(f"已成功处理 {wallet_count} 个钱包！")
        elif choice == '2':
            res = await show_existing_wallet_menu()
            if res is None:
                continue
        elif choice == '3':
            await run_complete_flow()
        elif choice == '0':
            log_info("程序结束，正在退出...")
            sys.exit(0)
        else:
            log_warn("无效的选择。")


def get_choice():
    print("\n" + "="*50)
    print(("请选择:"))
    print((f"{Fore.YELLOW}1. 生成代理池可用ip{Style.RESET_ALL}"))
    print((f"{Fore.GREEN}2. 自动完成任务{Style.RESET_ALL}"))
    print((f"{Fore.RED}3. 退出{Style.RESET_ALL}"))
    print("="*50 + "\n")

async def main():
    show_copyright()
    # 创建实例
    url_manager = URLKeyManager()
    filename = "config/credentials.txt"

    # 检查文件是否存在
    if os.path.exists(filename):
        print(f"检测到已有 {filename} 文件，尝试读取并验证...")
        user_id, key = url_manager.read_from_file()
        if user_id is None and key is None:
            print("文件不存在或为空，将要求输入新数据")
        elif isinstance(user_id, str) and "错误" in user_id:
            print(user_id)
            print("文件内容有误，将要求输入新数据")
        else:
            # 使用文件中的user_id和key进行验证
            if url_manager.verify_url(user_id, key):
                print("验证通过，继续执行后续逻辑...")
                
                # 发送用户信息到服务器
                print(f"{Fore.YELLOW}正在发送用户信息到服务器...{Style.RESET_ALL}")
                success, hardware_check = url_manager.post_user_info_to_server(user_id, key)
                
                if success and hardware_check:
                    # 检查硬件码变化
                    if not url_manager.handle_hardware_id_change(user_id, hardware_check):
                        print(f"{Fore.RED}硬件码验证失败，程序退出{Style.RESET_ALL}")
                        exit()

                get_choice()
                choice = input("输入您的选择: ").strip()
                if choice == '3':
                    print("退出...", 'info')
                elif choice == '1':
                    proxy_checker = ProxyChecker()
                    proxy_checker.run()
                elif choice == '2':
                    await run_main()
                else:
                    print("看提示，不要瞎输入", 'info')

            else:
                print("验证失败，程序退出")
            exit()  # 验证完成后退出，避免重复执行

    # 如果文件不存在或读取失败，要求用户输入并保存
    result1 = url_manager.get_user_input_and_save()
    print(result1)
    
    # 读取刚保存的数据并验证
    user_id, key = url_manager.read_from_file()
    if isinstance(user_id, str) and "错误" in user_id:
        print(user_id)
    else:
        if url_manager.verify_url(user_id, key):
            print("验证通过，继续执行后续逻辑...")
            
            # 发送用户信息到服务器
            print(f"{Fore.YELLOW}正在发送用户信息到服务器...{Style.RESET_ALL}")
            success, hardware_check = url_manager.post_user_info_to_server(user_id, key)
            
            if success and hardware_check:
                # 检查硬件码变化
                if not url_manager.handle_hardware_id_change(user_id, hardware_check):
                    print(f"{Fore.RED}硬件码验证失败，程序退出{Style.RESET_ALL}")
                    exit()

            get_choice()
            choice = input("输入您的选择: ").strip()
            if choice == '3':
                print("退出...", 'info')
            elif choice == '1':
                proxy_checker = ProxyChecker()
                proxy_checker.run()
            elif choice == '2':
                await run_main()
            else:
                print("看提示，不要瞎输入", 'info')
        else:
            print("验证失败，程序退出")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Gopher BOT [退出]{Style.RESET_ALL}                                       "                              
        )

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         log_info("程序结束，正在退出...")
#         sys.exit(0)
