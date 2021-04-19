# microservices-integrate-system
一个用于部署微服务架构软件应用，并实时显示部署过程以进行故障诊断的微服务集成系统平台</br>
![](https://img.shields.io/badge/version-1.2-yellowgreen)
## 技术架构
本系统由基于Vue进行开发的前端应用与基于flask开发的轻量级布局构成</br>
![](https://github.com/Lenkac/microservices-integrate-system/blob/main/process.jpg)

## 技术特色
本系统充分简化了传统CICD流程进行部署的复杂性，界面相对目前主流的jenkins要更加简单，并且便于开发人员对接。与此同时，由于该系统基于tekton进行开发，所以其完全符合云原生环境规范，既轻量又适用于多个场景。
## 代码结构
注：模块层级关系及说明

## 部署方式
## Vue前端
1.拉取该项目至本地</br>
2.打开前端对应文件夹</br>
```
cd front
```
3.安装依赖</br>
```
npm install
```
4.运行前端</br>
```
npm run server
```

## Flask后端
1.在kubernetes集群中输入命令： 
```
APISERVER=$(kubectl config view --minify | grep server | cut -f 2- -d ":" | tr -d " ") echo $APISERVER
```
2.利用admin.yaml创建权限：
```
 kubectl apply -f admin.yaml
```
3.获取token: 
```
Token=$(kubectl describe secret $(kubectl get secret -n kube-system | grep ^admin-user | awk '{print $1}') -n kube-system | grep -E '^token'| awk '{print $2}') echo $Token
```
4.复制token至server文件夹中的token.txt
5.运行软件：
```
python app.py
```


## 使用说明
1.本系统前端并未封装，可根据需求随意增删模块
如需在特定服务器使用，则将代码中的： path = `http://127.0.0.1:5000/tek_data` 修改为后端中对应地址与对应功能
