# coding:UTF-8
import datetime
import os

def output(msg, op=True, color="white"):

    try:
        log_date_time = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        output = "{} {}".format(log_date_time, msg)
        if op:
            if color == "white":
                print(output)
            elif color == "green":
                print("\033[32m{}\033[0m".format(output))
            elif color == "red":
                print("\033[31m{}\033[0m".format(output))
                
            
        log_file_path = os.path.join(os.getcwd(), "trace.log")
        with open(log_file_path, "a") as f:
            f.write(output + "\n")
    except:
        pass

def init():
    os.remove("trace.log")
