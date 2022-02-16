## 添加、修改客户端
### windows
双击运行`script/develop.bat`，然后在`src`文件夹下对源码进行操作。
### linux
在项目根目录运行`sh ./script/develop.sh`，然后在`src`文件夹下对源码进行操作。

## 部署
在项目根目录运行`sh ./script/deploy.sh`。  
要求:  
软件包:  
> docker  
> python3  
> pip3  

python库:   
> requests  
> pytz  

环境变量:   
> SUBMIT_URL  