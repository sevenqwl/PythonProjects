import re

string = "192.168.2.2"
m = re.match("([0-9]{1,3}\.){3}\d{1,3}", string)
print(m.group())

string2 = "Alex li"
m = re.search("[a-z]", string2, flags=re.I)  # flags=re.I不区分大小写
string2 = "alexi \nseven\bli"
m = re.search("^a.*$", string2, flags=re.M)
print(m.group())

# 匹配手机号
phone_str = "hey my name is alex, and my phone number is 13651054607, please call me if you are pretty!"
phone_str2 = "hey my name is alex, and my phone number is 18651054604, please call me if you are pretty!"

m = re.search("(1)([358]\d{9})", phone_str2)
if m:
    print(m.group())