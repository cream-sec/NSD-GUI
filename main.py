import re
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
from tkinter import scrolledtext
from operation.getDomainCount import domainCount
from operation.getIpCount import ipCount
from operation.getIpGroupCount import ipGroupCount
from operation.getNameandAddress import ruleNameAddress
from operation.getNatServer import NatServerClient
from operation.groupAddIp import addIP
from operation.groupAddDomain import addDomain
from operation.huaweiNGFW import NgfwLogin


class IP_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("USG6300-FIREWALL-02")
        self.master.geometry("1070x620")
        self.master.resizable(False, False)

        # 上方认证区
        self.fr1 = tk.LabelFrame(self.master, text="华为防火墙", width=200, height=200)
        self.fr1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.lab1 = tk.Label(self.fr1, text="服务器:")
        self.lab1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.en1 = tk.Entry(self.fr1, width=20)
        self.en1.insert(0, "192.168.0.1")
        self.en1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.lab2 = tk.Label(self.fr1, text="用户名:")
        self.lab2.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.en2 = tk.Entry(self.fr1, width=20)
        self.en2.insert(0, "adminapi")
        self.en2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.lab4 = tk.Label(self.fr1, text="API密钥:")
        self.lab4.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.en3 = tk.Entry(self.fr1, width=20, show="*")
        self.en3.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.bt1 = tk.Button(self.fr1, text="登录认证", command=self.login_check, cursor="hand2")
        self.bt1.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # 下方日志区
        self.fr2 = tk.LabelFrame(self.master, text="日志回显", width=200, height=300)
        self.fr2.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.log_area = scrolledtext.ScrolledText(self.fr2, wrap=tk.WORD, width=20, height=20)
        self.log_area.pack(padx=5, pady=5, fill="both", expand=True)

        # 右侧上菜单区:数据查询区域
        self.fr3 = tk.LabelFrame(self.master, text="数据查询", width=800, height=200)
        self.fr3.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # 防火墙策略
        self.bt2 = tk.Button(self.fr3, text="防火墙策略", command=self.display_rules, width=25, cursor="hand2",state='disabled')
        self.bt2.grid(row=0, column=0, padx=5, pady=5, sticky="nwse")

        self.frame1 = tk.Frame(self.fr3, width=25)
        self.frame1.grid(row=1, column=0, padx=5, pady=5, sticky="nwse")
        self.cb1 = ttk.Combobox(self.frame1, width=25,state='disabled')
        self.cb1.grid(row=0, column=0, padx=0, pady=0, sticky="nwse")
        self.cb1.bind("<<ComboboxSelected>>", self.btchecksate)

        self.btcheck = tk.Button(self.frame1, text="数量查询", command=self.updateButtonText, width=10, cursor="hand2",state='disabled')
        self.btcheck.grid(row=0, column=1, padx=0, pady=0, sticky="nwse")

        self.en5 = tk.Entry(self.fr3, width=25,state='disabled')
        self.en5.grid(row=2, column=0, padx=5, pady=5, sticky="nwse")

        # 内外网IP映射查询
        self.fm1 = tk.Frame(self.fr3, width=25)
        self.fm1.grid(row=3, column=0, padx=0, pady=0, sticky="nwse")

        self.lab5 = tk.Label(self.fm1, text="查询IP：")
        self.lab5.grid(row=0, column=0, padx=5, pady=5, sticky="nwse")

        self.en6 = tk.Entry(self.fm1, width=13,state='disabled')
        self.en6.insert(0, "192.168.0.1")
        self.en6.grid(row=0, column=1, padx=5, pady=5, sticky="nwse")

        self.bt3 = tk.Button(self.fm1, text="映射查询", command=self.dispay_NatServer, width=10, cursor="hand2",state='disabled')
        self.bt3.grid(row=0, column=2, padx=5, pady=5, sticky="nwse")

        self.NatServer_log_area = scrolledtext.ScrolledText(self.fr3, wrap=tk.WORD, width=50, height=10)
        self.NatServer_log_area.grid(row=0, column=1, rowspan=4, padx=5, pady=5, sticky="w")

        # 右侧下IP管理区
        self.fr4 = tk.LabelFrame(self.master, text="IP/URL管理", width=720, height=300)
        self.fr4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.cb2 = ttk.Combobox(self.fr4, width=33,state='disabled')
        self.cb2.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.tips = tk.Label(self.fr4, text="注意：每次封禁IP前需要先查询指定组的内容数量！", fg="red",
                             font=("Arial", 12, "bold"))
        self.tips.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.ip_area = scrolledtext.ScrolledText(self.fr4, wrap=tk.WORD, width=105, height=25,state='disabled')
        self.ip_area.grid(row=1, column=0, columnspan=2, padx=5, pady=0, sticky="nsew")

        self.bt4 = tk.Button(self.fr4, text="IP拉黑", command=self.display_addIp, width=33, cursor="hand2",state='disabled')
        self.bt4.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.bt5 = tk.Button(self.fr4, text="URL拉黑", command=self.display_addDomain, width=33, cursor="hand2",state='disabled')
        self.bt5.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    ##登录检查
    def login_check(self):
        server_ip = self.en1.get().strip()
        api_username = self.en2.get().strip()
        api_key = self.en3.get().strip()

        if not server_ip or not api_username or not api_key:
            messagebox.showwarning("输入错误", "所有字段都是必填的，请输入完整信息。")
            return

        try:
            self.bt1.config(state=tk.DISABLED)
            self.log_area.insert(tk.END, "正在尝试登录...\n")
            self.log_area.yview(tk.END)

            result = NgfwLogin(server_ip, api_username, api_key)
            if result:  # 假设认证成功返回True
                self.bt1.config(fg='green', activeforeground='red', text='登录成功')
                self.log_area.insert(tk.END, "登录成功。\n")
                self.enable_controls()
            else:
                self.bt1.config(fg='red', text='登录失败')
                self.log_area.insert(tk.END, "登录失败。\n")
        except Exception as e:
            self.bt1.config(fg='red', text='登录失败')
            messagebox.showerror("登录失败", f"登录过程中发生错误: {e}")
            self.log_area.insert(tk.END, f"登录过程中发生错误: {e}\n")
        finally:
            self.bt1.config(state=tk.NORMAL)
            self.log_area.yview(tk.END)

    def enable_controls(self):
        self.bt2.config(state='normal')
        self.cb1.config(state='normal')
        self.btcheck.config(state='normal')
        self.en5.config(state='normal')
        self.en6.config(state='normal')
        self.bt3.config(state='normal')
        self.NatServer_log_area.config(state='normal')
        self.cb2.config(state='normal')
        self.ip_area.config(state='normal')
        self.bt4.config(state='normal')
        self.bt5.config(state='normal')
    ##下拉框变动后调整按钮文字和清空下方输入框内容
    def btchecksate(self, event=None):
        self.btcheck.config(text="点击查询")
        self.en5.delete(0, tk.END)

    # 查询数据并调整按钮文字
    def updateButtonText(self):
        self.btcheck.config(text="查询中...")
        self.master.update_idletasks()
        self.master.after(100, self.displayCount)

    ##显示查询到的防火墙规则信息
    def display_rules(self):
        server_ip = self.en1.get().strip()
        api_username = self.en2.get().strip()
        api_key = self.en3.get().strip()
        rules = ruleNameAddress(server_ip, api_username, api_key)
        self.NatServer_log_area.delete(1.0, tk.END)
        data = []
        if rules:
            self.log_area.insert(tk.END, "防火墙规则信息查询成功！\n")
            self.cb1['values'] = ()
            self.NatServer_log_area.insert(tk.END, "查询到的防火墙规则信息:\n")
            for rule in rules:
                self.NatServer_log_area.insert(tk.END, f"规则名称: {rule['name']}\n")
                self.NatServer_log_area.insert(tk.END, f"  规则行动: {rule['action']}\n")
                self.NatServer_log_area.insert(tk.END, f"  规则状态: {rule['enable']}\n")
                self.NatServer_log_area.insert(tk.END, f"  来源地址: {rule['source_addresses']}\n")
                if rule['source_addresses'] != 'any':
                    if ',' in rule['source_addresses']:
                        source_addresses = [addr.strip() for addr in rule['source_addresses'].split(',')]
                        data.extend(source_addresses)
                    else:
                        data.append(rule['source_addresses'].strip())
                self.NatServer_log_area.insert(tk.END, f"  目的地址: {rule['destination_addresses']}\n")
                if rule['destination_addresses'] != 'any':
                    if ',' in rule['destination_addresses']:
                        source_addresses = [addr.strip() for addr in rule['destination_addresses'].split(',')]
                        data.extend(source_addresses)
                    else:
                        data.append(rule['destination_addresses'].strip())
                self.NatServer_log_area.insert(tk.END, "\n")
                data.append(rule['domain_sets'].strip())
                self.cb1['values'] = data
            self.cb1['values'] = list(set(data))
            self.cb2['values'] = list(set(data))
        else:
            self.log_area.insert(tk.END, "未查询到任何防火墙规则信息。\n")
            self.cb1['values'] = ()

    ##显示查询到的内外网IP映射信息
    def dispay_NatServer(self):
        server_ip = self.en1.get().strip()
        api_username = self.en2.get().strip()
        api_key = self.en3.get().strip()
        query_ip = self.en6.get().strip()
        client = NatServerClient(server_ip, api_username, api_key)
        client.fetch_data()
        results = client.search(query_ip)
        self.NatServer_log_area.delete(1.0, tk.END)

        if results:
            for result in results:
                self.log_area.insert(tk.END, f"{query_ip}:内外网映射查询成功!\n")

                self.NatServer_log_area.insert(tk.END, f"\n")
                self.NatServer_log_area.insert(tk.END, f"查询IP:{query_ip}\n")
                self.NatServer_log_area.insert(tk.END, f"映射名称:{result['name']}\n")
                self.NatServer_log_area.insert(tk.END, f"外网IP:{result['global_start_ip']}\n")
                self.NatServer_log_area.insert(tk.END, f"外网端口:{result['global_start_port']}\n")
                if result['global_end_port']:
                    self.NatServer_log_area.insert(tk.END, f"外网端口:{result['global_end_port']}\n")
                self.NatServer_log_area.insert(tk.END, f"内网端口:{result['inside_start_ip']}\n")
                self.NatServer_log_area.insert(tk.END, f"内网端口:{result['inside_start_port']}\n")
                if result['inside_end_port']:
                    self.NatServer_log_area.insert(tk.END, f"内网端口:{result['inside_end_port']}\n")
                self.NatServer_log_area.insert(tk.END, f"\n")
                print()
        else:
            self.log_area.insert(tk.END, f"{query_ip}:未查询到任何映射信息!\n")
        pass

    ##显示IP组里的IP数量，方便后续添加IP
    def displayCount(self, event=None):
        check_ip = self.cb1.get().strip()
        server_ip = self.en1.get().strip()
        api_username = self.en2.get().strip()
        api_key = self.en3.get().strip()
        ipgroupcountResult = self.check_result(server_ip, api_username, api_key, check_ip)
        if ipgroupcountResult:
            self.en5.delete(0, tk.END)
            self.en5.insert(0, ipgroupcountResult[1])
            self.log_area.insert(tk.END, f"{ipgroupcountResult[0]}{check_ip}查询数量成功!\n")
            self.btcheck.config(text="查询完毕")
        else:
            self.en5.delete(0, tk.END)
            self.log_area.insert(tk.END, f"{check_ip}查询失败!\n")
            self.btcheck.config(text="查询完毕")

    ##查询指定对象的数量
    def check_result(self, server_ip, api_username, api_key, check_object):
        query_result = ["", ""]
        result = ipCount(server_ip, api_username, api_key, check_object)  # 判断在地址内存在，如果存在计算其内容数量
        if result is not None:
            query_result[0] = "地址(Object)"
            query_result[1] = str(result)
            return query_result
        result = ipGroupCount(server_ip, api_username, api_key, check_object)  # 判断地址组内存在，如果存在计算其内容数量
        if result is not None:
            query_result[0] = "地址组(Group)"
            query_result[1] = str(result)
            return query_result
        result = domainCount(server_ip, api_username, api_key, check_object)  # 判断域名内存在，如果存在计算其内容数量
        if result is not None:
            query_result[0] = "域名组(Domain)"
            query_result[1] = str(result)
            return query_result
        return None

    def iptexttoarray(self, text):
        pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)(?:/(\d+))?')
        # 将每行的IP转换为数组
        addresses = []
        for line in text.strip().split('\n'):
            match = pattern.match(line.strip())
            if match:
                ip = match.group(1)
                subnet = match.group(2) if match.group(2) else None
                addresses.append((ip, subnet))

        return addresses

    ##添加IP到指定地址组
    def display_addIp(self, event=None):
        server_ip = self.en1.get().strip()
        api_username = self.en2.get().strip()
        api_key = self.en3.get().strip()
        group = self.cb2.get().strip()
        ip_address = self.ip_area.get("1.0", "end").strip()
        count = self.en5.get().strip()

        if count == "":
            messagebox.showwarning("警告", "请先查询所选IP组的IP数量，再添加IP。")
            return
        else:
            iparray = self.iptexttoarray(ip_address)
            result = addIP(server_ip, api_username, api_key, group, iparray, int(count))
            if result:
                self.log_area.insert(tk.END, f"{group}!IP拉黑成功！\n")
                self.ip_area.delete(1.0, tk.END)
                self.en5.delete(0, tk.END)
            else:
                self.log_area.insert(tk.END, f"{group}!IP拉黑失败！\n")

    def is_valid_domain(self, domain):
        domain_pattern = re.compile(
            r'^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}\.?|localhost)$')
        return re.match(domain_pattern, domain) is not None

    def read_domains_from_text(self, text):
        domains = text.split()
        valid_domains = [domain for domain in domains if self.is_valid_domain(domain)]
        return valid_domains

    ##添加域名到指定域名组
    def display_addDomain(self, event=None):
        server_ip = self.en1.get().strip()
        api_username = self.en2.get().strip()
        api_key = self.en3.get().strip()
        group = self.cb2.get().strip()
        domains = self.read_domains_from_text(self.ip_area.get("1.0", "end").strip())
        result = addDomain(server_ip, api_username, api_key, group, domains)
        if result:
            self.log_area.insert(tk.END, f"域名拉黑成功！\n")
            self.ip_area.delete(1.0, tk.END)
        else:
            self.log_area.insert(tk.END, f"域名拉黑失败！\n)")


if __name__ == '__main__':
    root = tk.Tk()
    app = IP_GUI(root)
    root.mainloop()
