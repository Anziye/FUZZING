from sulley import *

def get_greeting_msg(sock):
    greet_message = sock.recv(10000)

#sessions.session.log("Greeting Message -->%s" % get_greeting_msg, 2)
def callback(sessions, node, edge, sock):
    #sessions.session.log("Data sent -->%s" % node.render(), 2)
    pass
#通过分析协议交互报文，编写报文格式
s_initialize("helo")
if s_block_start("helo"):
    s_static("helo")
    s_delim(" ")
    s_static("test.com")
    s_static("\r\n")
    s_block_end()

s_initialize("ehlo")
if s_block_start("ehlo"):
    s_static("ehlo")
    s_delim(" ")
    s_random("xxx.com", 5, 10)
    s_static("\r\n")
    s_block_end()

s_initialize("mail from")
if s_block_start("mail from"):
    s_static("mail from: ")
    s_delim("")
    s_delim("<")
    s_static("haha@ims.com")
    s_delim(">")
    s_static("\r\n")
    s_block_end()

s_initialize("rcpt to")
if s_block_start("rcpt to"):
    s_static("RCPT TO")
    s_delim(":")
    s_static("alice@test.com")
    s_static("\r\n")
    s_block_end()
    
s_initialize("pre_data")
if s_block_start("pre_data"):
    s_static("DATA\r\n")
    s_block_end()
    
s_initialize("data_content")
if s_block_start("data_content"):
    s_static("Receive:")
    s_string("Whatever")
    s_static("\r\n")
    s_static("Subject:")
    s_string("GOGOGOA"*2)
    s_static("\r\n")
    s_static("\r\n")
    s_string("haha")
    s_static("\r\n.\r\n")
    s_block_end()

#构建session，指定目标IP与端口，发送报文开始fuzzing
sess = sessions.session(log_level=100)
target = sessions.target("192.168.1.115",25)
sess.add_target(target)
sess.connect(sess.root, s_get("helo"), callback)
sess.connect(sess.root, s_get("ehlo"), callback)
sess.connect(s_get("helo"), s_get("mail from"), callback)
sess.connect(s_get("ehlo"), s_get("mail from"), callback)
sess.connect(s_get("mail from"), s_get("rcpt to"), callback)
sess.connect(s_get("rcpt to"), s_get("pre_data"), callback)
sess.connect(s_get("pre_data"), s_get("data_content"), callback)
sess.fuzz()
