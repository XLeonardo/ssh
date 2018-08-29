#!/usr/bin/python
# encoding=utf-8

"""
@Filename: ssh_con_pex.py
@Modified By: Erick
@Description: ssh connection
    This runs a command on a remote host using SSH. At the prompts enter hostname, user, password.
"""

from __future__ import print_function

from __future__ import absolute_import

import pexpect
import getpass
import time

try:
    raw_input
except NameError:
    raw_input = input

# SMTP:25 IMAP4:143 POP3:110
tunnel_command = 'ssh -C -N -f -L 25:127.0.0.1:25 -L 143:127.0.0.1:143 -L 110:127.0.0.1:110 %(user)@%(host)'


def get_process_info():
    # This seems to work on both Linux and BSD, but should otherwise be considered highly UNportable.

    ps = pexpect.run('ps ax -O ppid')
    pass


def start_tunnel():
    try:
        ssh_tunnel = pexpect.spawn(tunnel_command % globals())
        ssh_tunnel.expect('password:')
        time.sleep(0.1)
        # ssh_tunnel.sendline (X)
        time.sleep(60)  # Cygwin is slow to update process status.
        ssh_tunnel.expect(pexpect.EOF)

    except Exception as e:
        print(str(e))


def ssh_command(host, user='root'):
    """
    This runs a command on the remote host. This could also be done with the
    pxssh class, but this demonstrates what that class does at a simpler level.
    :param host:
    :param user:
    :return:
    """
    ssh_newkey = 'Are you sure you want to continue connecting'

    # 为 ssh 命令生成一个 spawn 类的子程序对象.
    ssh_tunnel = pexpect.spawn('ssh -T %s@%s' % (user, host))
    time.sleep(0.2)
    i = ssh_tunnel.expect([pexpect.TIMEOUT, ssh_newkey, 'password: ', pexpect.EOF])

    # Time out. 如果登录超时，打印出错信息，并退出.
    if i == 0:
        print('SSH timeout. Here is what SSH said:')
        return

    # SSH does not have the public key. Just accept it. 如果 ssh 没有 public key，接受它.
    elif i == 1:
        ssh_tunnel.sendline('yes')
        time.sleep(0.2)
        i = ssh_tunnel.expect([pexpect.TIMEOUT, 'password: '])

        # Time out. 如果登录超时，打印出错信息，并退出.
        if i == 0:
            print('SSH timeout. Here is what SSH said:')
            return

    elif i == 2:
        pass

    elif i == 3:
        # Match pexpect.EOF
        return ssh_tunnel.before.strip()

    # ssh_tunnel.sendline(X)
    ssh_tunnel.sendline('')
    ssh_echo = ssh_tunnel.before.split('\n')[-1] + 'password: '

    return ssh_echo


def main():
    host = raw_input('Hostname: ')
    user = raw_input('Username: ')
    # X = getpass.getpass('Password: ')

    print(time.asctime(), end=' ')
    print('Starting tunnel:')

    # start_tunnel ()

    if user:
        result_string = ssh_command(host, user)
    else:
        result_string = ssh_command(host)

    if result_string:
        print(result_string)


if __name__ == '__main__':
    main()
