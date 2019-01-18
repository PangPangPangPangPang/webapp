# Docker搭建笔记

>最近由于自己的vps又又又又过期了，迫不得已又又又又要重新部署一下自己的blog。
其实很早之前就想要使用Docker来部署，然而拖延症一直让我拖延到现在。
这次其实是蹭了朋友的vps用，想了想也不能用自己的糙脚本直接在朋友的vps上用，
一旦给人家的vps环境搞炸了怎么办，
而且用的还是node+python这种库一升级连自己都跑不起来的技术写的blog。所以这次下定决心用上Docker，最终的结果还是不错的。

-------
[date] 2019-1-14 15:09:36
[tag] Docker 技术

## Docker介绍
>首先贴一个介绍Docker的[教程](https://yeasy.gitbooks.io/docker_practice/container/attach_exec.html), 以下的介绍很多是基于这个教程而来的

### 什么是Docker
Docker 使用 Google 公司推出的 Go 语言 进行开发实现，基于 Linux 内核的 cgroup，namespace，以及 AUFS 类的 Union FS 等技术，对进程进行封装隔离，属于 操作系统层面的虚拟化技术。由于隔离的进程独立于宿主和其它的隔离的进程，因此也称其为容器。

### 为啥要用Docker
Docker具体的优势可以翻阅之前的教程来详细了解，对我个人而言，Docker降低了部署成本。顺便也带来了更好的效率，以及降低了持续交付和部署的成本。（目前并没有感受到- -!）

## Docker的基本概念

### Image
这个Image就是大家印象中的那个Image，就是某种定制的镜像文件。（比如Debian啥的）另外Docker构建镜像的时候还有个分层的概念，暂时还没有理解到作用，以后又机会在分析吧。

### Container
Container就是一个Image运行起来真正对应到一个进程后的定义。可以类比成**类**跟**实例**。

## Docker安装
由于我的环境是Manjaro跟MacOS，所以运行**pacman -S docker**或者**brew cask install docker**就成功安装了，也不需要其他特别的操作。（棒棒！）其他操作系统的安装可以借鉴文首的教程。（总之不会有很多坑就是了！）

## Docker常用命令

### 获取镜像

```
  docker pull [选项] [Docker Registry 地址[:端口号]/]仓库名[:标签]
  # 例如：docker pull ubuntu:18.04
```

### 运行镜像

```
  docker run -i -t --rm ubuntu:18.04 /bin/bash
  # -i表示交互式 -t表示终端 --rm表示退出容器即删除容器
  # -d可以让Docker以守护态的形式运行
```

### 镜像列表

```
  docker images
```
或者
```
  docker image ls
  # docker system df 可以总体查询镜像以及容器的真实占用空间。
```

### 镜像删除

```
  docker image rm <镜像>
  # 什么镜像名，镜像ID都可以用来删除（很贴心有木有）
```

### 容器相关基础操作
```
  docker container ls
  # 容器列表

  docker container stop <容器>
  docker container start <容器>
  docker container restart <容器>
  docker container rm <容器>

  docker container prune
  # 清理所有已经stop的容器
```

### 进入容器
如果容器最开始以守护态运行，或者另起了一个shell，这个时候如果我们想要再进入这个容器改怎么操作呢？

```
  docker -it attach <镜像> /bin/bash
  # 其中的参数跟**docker run**的时候的参数意义一致
```

