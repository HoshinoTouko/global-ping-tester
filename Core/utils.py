import platform
import locale

def get_os():
    return platform.system()


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"


def handle_rawdata(res, count):
    if is_windows():
        str_list = res.split("\n")
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
