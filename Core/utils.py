import platform
import locale

def get_os():
    return platform.system()


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"


def handle_rawdata(response, count):
    if is_linux():
        sys_lan = locale.getdefaultlocale()
        if sys_lan[0] == "en_US":
            res = ""
            for i in range(1, count+1):
                target_str = "seq=" + str(i)
                is_timeout = True
                for j in range(len(response)):
                    if str(response[j]).find(target_str) != -1:
                        is_timeout = False
                        start_idx = str(response[j]).find("time=")
                        end_idx = str(response[j]).find("ms")
                        res += str(i) + " " + response[j][start_idx + 5:end_idx - 1] + "\n"
                if is_timeout:
                    res += str(i) + " " + "timeout\n"
    if is_windows():
        str_list = response.split("\n")
        str_list = str_list[2:count + 2]
        sys_lan = locale.getdefaultlocale()
        res = ""
        if sys_lan[0] == "zh_CN":
            for i in range(len(str_list)):
                if str_list[i] == "请求超时。":
                    res += str(i+1) + " " + "timeout\n"
                else:
                    start_idx = str(str_list[i]).find("时间=")
                    end_idx = str(str_list[i]).find("ms")
                    res += str(i+1) + " " + str_list[i][start_idx+3:end_idx] + "\n"
    res = res[:-1]
    return res
