## 运行前准备工作
确保依赖已安装且 **可访问**  
推荐使用虚拟环境(venv)。以下部署步骤默认在虚拟环境下完成。

0. 如果需要，可以创建一个新用户用于同步。
1. 下载源码(git clone或下载压缩包并解压)，并放到你想放的位置(以下以`$WORKDIR`指代该目录，执行命令时注意替换)。
2. 配置虚拟环境: `python3 -m venv venv`
3. 如果需要同步Spigot，需要编译docker镜像与容器: `cd $WORKDIR/docker && sh ./build.sh $WORKDIR`。请确保所有项均为`success`。
4. 编辑`plugin/__init__.py`，`active`存储了所有会进行同步的服务端。如果不需要同步某一服务端，将其移除出`active`即可。
5. 确保`auth/token`文件存在，否则无法上传数据.
6. 编辑`lib/config.py`，将`submit_url`修改为需要上传的地址。
7. 如果需要手动同步，输入`python sync.py`即可。
8. 如果需要定时任务，例如每天0点定时同步，请先输入`crontab -e`编辑`cron`，在文件最后一行添加`0 0 * * * source $WORKDIR/venv/bin/activate && python $WORKDIR/sync.py`

注意事项: 
1. 请确保文件所有者是执行更新的用户。
2. 如果需要使用docker，请确保执行更新的用户能够正常执行`docker build`、`docker run`和`docker start`。
3. 本项目虽然不对`$WORKDIR/auth/token`的权限做强制要求，但是为保证安全，请确保其权限为600
4. 如果对服务器的内存和CPU性能有足够的信心(请确保内存至少有8GiB)，可以将`sync.py`中的`__async_enable__`设置为`True`以启用异步模式。
5. 
## 依赖  

软件包:  
> docker  
> python3 >= 3.5  
> python3-pip  
> *python3-venv

python库:   
> pytz == 2021.1  
> aiohttp == 3.6.2  
> docker == 5.0.3  

<!-- 环境变量:   
> *SUBMIT_URL   -->

注: 带 * 的为可选项。