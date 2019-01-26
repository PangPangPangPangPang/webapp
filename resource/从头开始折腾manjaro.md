# 从头开始折腾Manjaro
[date] 2019-11-26 11:43:36
[tag] 折腾 Manajo

前几天入了块超便宜的固态硬盘，装上操作系统后让我这个14年的老笔记本彻底复活！

但是不尽如人意的是装上之后发现`/`分区分的磁盘空间太小惹。看了看改逻辑分区的工具`lvm`操作实在有些~~麻烦~~让人懒得看，还是重新装一下系统吧。

## 安装操作系统

* [官网](https://manjaro.org/download/i3/)下载官方镜像，这里选择的i3wm的版本，没别的原因，好用就对了！
* 插上U盘开始flash镜像，这里推荐个[工具](https://etcher.io/)。
* 重启狂按某个**神秘按键**进入到电脑的**bios**并选择你的U盘来启动。
* **Manajo**官方提供的镜像安装操作系统很方便，基本一路点点点就可以了。这里备注一下如何分区

```
/boot      256M
/          100G
/swap      10G
/home/user 剩下的
```

## 配置

配置的时候遇到了很多坑，想想之前其实都遇到过了，只是没有记录下来，导致又重新趟了一遍。

### 初始配置中的一些坑
**Manjaro-i3**默认用的是**Alsa**管理音频，这在我的本子上根本不好使，敲一下**mod+ctrl+h 或者 mod+shift+h**打开帮助文档。可以看到在终端运行**install_pulse**就可以安装熟悉的**Pulseaudio**来管理音频了。(这个帮助文档里也有一些基本的i3操作)

但是不知道是不是我电脑的硬件不兼容的问题，导致启动之后是没有声音的，必须kill掉**Pulseaudio**并重启才能开启声音，所以需要在i3的配置文件中配置开机先杀掉再启动。文件在[这里](https://github.com/PangPangPangPangPang/dotfiles/blob/master/default_config)

~~其实还有一个坑，就是偶尔wireless无效！最开始以为是无线网卡驱动的问题，查了半天，最后发现是没有插好！！！~~

### 正经的初始配置
先换中国源**sudo pacman-mirrors -i -c China -m rank** 。
然后不管三七二十一，先跑一遍**sudo pacman -Syyu**滚一下软件包，结束后重启。

#### AUR支持
[Arch User Repository](https://wiki.archlinux.org/index.php/Arch_User_Repository) （常被称作 AUR），是一个为 Arch 用户而生的社区驱动软件仓库。Debian/Ubuntu 用户的对应类比是 PPA。
官方的**pacman**只支持安装官方背书包，所以需要一个工具支持安装**AUR**中的包。
其实我一开始都是用的**yaourt**，但是在官方文档中已经被标注为不推荐使用了。那就换[yay](https://github.com/Jguer/yay)好了，名字还更好记一点。下面是安装命令：

```sh
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
```

#### 终端
习惯用**terminator**跟**zsh**就还是用它们就好了
```sh
sudo pacman -S terminator zsh

#顺便装上oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

#### 输入法
习惯用**fcitx**了，其实也没什么别的选择。（= =）
```sh
sudo pacman -S fcitx-googlepinyin
sudo pacman -S fcitx-im             
sudo pacman -S fcitx-configtool    
```
然后在`~/.xprofile`文件里面加上
```sh
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS="@im=fcitx"
```
最后重启下

#### 屏幕分辨率
```sh
# ~./.Xresource
# Refresh: xrdb -merge .Xresources

Xft.dpi: 108
```
#### 默认程序修改

在`.config/mimeapps.list`文件中编辑默认程序。

#### 常用应用

* 文件管理器：**pcmanfm**(Manjaro-i3 自带)
* 快捷启动器：**rofi**
  ```sh
  # Add in ~/.i3/config
  bindsym $mod+p exec rofi -show combi
  ```
* 桌面图片管理：**nitrogen**(Manjaro-i3 自带)
  ```sh
  # Add in ~/.i3/config
  exec_always --no-startup-id nitrogen --set-zoom ~/img/background.jpg
  ```
* 浏览器：**google-chrome**
* 音乐播放器：**mocp**(Manjaro-i3 自带)、**netease-cloud-music**
* 开始菜单：**morc_menu**(Manjaro-i3 自带, `mod+z`)
* 通用菜单：**bmenu**(Manjaro-i3 自带, `mod+ctrl+b`)

## 写在最后
Manjaro天下第一！
