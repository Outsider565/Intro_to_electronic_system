# 这里是用来配置树莓派的脚本，不需要懂得它做了什么
NAME="pi"
sudo echo "deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib rpi
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib rpi">/etc/apt/sources.list
sudo echo "deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui">/etc/apt/sources.list.d/raspi.list
sudo apt install vim,zsh,git,tldr
sh -c "$(curl -fsSL https://raw.staticdn.net/ohmyzsh/ohmyzsh/master/tools/install.sh)"
cd /home/$NAME/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDRTvPNa+Ib6Pcnb3CGYtdHwh8abrHUmHbIRomJhPg/qweoBPTC5EbjEQL1Dj2aSTnMiqlXou6MPYumleg+dnkaKkcz5B+uHe8io7hgnQE8l1uiRd2ofDb/obcmxF8Jneb0DvG/3a6FNKQ4cw3bbrX8XAwaQ8yLdEjF3LlUSYxCerBZGX6SQMjA7jm4tDDu5JewawPEbfFz3YO4I9d+VCQwO0gUi+LXTeUwPwttVP33b+X5JN7F5jhBnPyoL6bc0/0VJcGkHOOf4U6briW0+T9+AI3s/sr2s3xVf3dO1IhRC5UnEgXF/YPnoihzU79dHN4PZL1NM+BFaC0ySNStKbd3OhJAJPpcW7Eh3lg7y8pSrsYPWp/dSGY3rPbT+x/Q2dHIgDgNika61GToBGkLkvP6JQ3vVeN+O5tDwNT+/+eAUtpOLpAtycz00N6DgLvDy6AbsOtXgOlDaDuY5erY/OR60en6rTF5eE0a5sMIqsl2eqXHAc8QyOvHThZj9Sn3h5EFDP8xsdhfegMxXUjeVmGu9d3ghUSrctgtPiPluPMgsTeu4Br6DnbY6ldoVgdvoP2cxV69dvEOsxpjQrh/SH3+ZY4wMm0AwPMfsN98baYrguvhCTL7WxDIcPSztkn43JKdEzULpy3ASqIMHZRtSlsnBplZeSzCnGMmhw34poMbqQ== shaowenwang@iCloud.com" >> authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDkC6NSwrmp8U3Cc2oZHF7Le0Vu0e2t5jbnmUXWp9Nb0A3POnPfaW1S6bpng55IRuO1nUMZPsMP9B3nkxb/ZZt33+f4kFdBIbu9aQH3MtA7Sszvms1uZlKU8C6uzMXQ5sRzNslTOqkL/zg1K7lv/GaABXhzLWY20mIeulhxxrhLRUlC4BV2GTzrIEIrxibLAy+9FV9cxDJ7biegxTiwFHdWro/pEyjBxM3/ayDUwhMM4+Cb6V9S8TT8ozF1Zsav6she+PQIi7f6/EIZ/Ga+ilFYLBrS+4Xnm4PzZ6En5Ko6jwDyGETl/JCdm0XvyCqzeYBJy9IsGFPYU8P5MM8scJxT admin@wswlp" >>authorized_keys
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
ssh-keygen -t rsa -C "shaowenwang@iCloud.com"
cd /home/$NAME/.ssh
cat id_rsa.pub
echo "打开github.com，设置git即可"
read -p "设置好后按enter继续"
pip3 install wiringpi