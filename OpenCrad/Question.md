# 使用过程问题汇总


<h3 style="color:#F00" >【问题1】：出现下图所示报错  </h3>   

<img width="287" alt="image" src="https://user-images.githubusercontent.com/78124261/118395814-f22b7180-b67e-11eb-8bc6-dbf665a41a1c.png">   

<h3 style="color:green" >【解决1】：切换下网络、如关闭节点尝试。   

<h3 style="color:#F00" >【问题2】：出现下图报错：   </h3> 

![image](https://user-images.githubusercontent.com/78124261/118395829-0e2f1300-b67f-11eb-97e7-e4674bbd0a64.png)   

<h3 style="color:green" >【解决2】：</h3>   
  配置文件ck修改时候，格式不对，参考如图，把你的cookie复制只需要替换红框的就行（图为原始配置文件）   
  
![image](https://user-images.githubusercontent.com/78124261/118395838-171fe480-b67f-11eb-9605-62128c3b109f.png)    

<h3 style="color:#F00" >【问题3：脚本运行时-【只有进度打印没有内容】     </h3>  

<h3 style="color:green" >【解决3】：</h3> 
  只有进度，一般是店铺没豆领，脚本是在筛选有豆的店铺进行入会（正常运行），有豆才会打印日志。（你可以配置文件修改printlog = no 这样就可以看所有日志，如图）    
  
![image](https://user-images.githubusercontent.com/78124261/118395843-1edf8900-b67f-11eb-853a-8863dede1aa4.png)    
日志会这样打印  

![image](https://user-images.githubusercontent.com/78124261/118395857-30c12c00-b67f-11eb-84cd-e03c7ba9916d.png)    

<h3 style="color:#F00" >【问题4】：shopid 本地和远程    </h3> 

<h3 style="color:green" >【解决4】：  </h3>   

 * 远程的shopid目前由我这边只爬有豆的shopid更新，每天07点30分更新到云端，可以在8：00后运行一次脚本即可。
    
 * 本地shopid，需要把配置文件里面的 isRemoteSid = no ,并且复制你的shopid保存在与脚本同一目录下文件名一定要是【shopid.txt】 才会生效。  
 
![image](https://user-images.githubusercontent.com/78124261/118395869-3b7bc100-b67f-11eb-8b15-24b76f5d64a7.png)    
  
#### 如果不会配置，建议使用默认远程shopid即可。   

