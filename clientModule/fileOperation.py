#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2020/8/18 16:57

import os
from chardet import detect
from misc.encoding import Encode

class FileOPT:
    def __init__(self, client, cmd, sendBufferSize = 4096, recvBufferSize = 8192):
        self.client = client
        self.cmd = cmd
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize

    # 上传(控制端上传)
    def upload(self):
        rRemoteFile = self.cmd.split()[2]
        if "/" not in rRemoteFile:
            rRemoteFile = "./" + rRemoteFile
        if not os.path.isfile(rRemoteFile):
            self.client.send("1".encode(Encode.encoding))
            self.createFile(rRemoteFile)
            return 0
        # 已存在同名文件，执行可选覆盖操作
        self.client.send("0".encode(Encode.encoding))
        choice = self.client.recv(self.recvBufferSize).decode(Encode.encoding)
        if choice.split()[0] == "cover":
            self.createFile(rRemoteFile)
        # else:
        #     return 0

    # 下载(控制端下载)
    def download(self):
        rRemoteFile = self.cmd.split()[1]
        if "/" not in rRemoteFile:
            rRemoteFile = "./" + rRemoteFile
        if not self.checkLocalFile(rRemoteFile):
            return 0
        with open(rRemoteFile, "rb") as r:
            binData = r.read()
        self.client.send(binData)

    # 创建文件并写入内容
    def createFile(self, FileName):
        targetFile = FileName  # 上传文件
        binData = self.client.recv(self.recvBufferSize)
        fileEncoding = detect(binData)["encoding"]
        try:
            with open(targetFile, "w", encoding=fileEncoding) as w:
                w.writelines(binData.decode(fileEncoding))
                self.client.send(("Success").encode(Encode.encoding))
        except:
            self.client.send(("Fail").encode(Encode.encoding))

    # 判断本地文件是否存在
    def checkLocalFile(self, localFilePath):
        if not os.path.isfile(localFilePath):
            self.client.send("findERROR".encode(Encode.encoding))
        else:
            try:
                # 文件读取权限校验
                with open(localFilePath, "rb") as r:
                    self.client.send("checkOK".encode(Encode.encoding))
                    return True
            except:
                self.client.send("openERROR".encode(Encode.encoding))
        return False

