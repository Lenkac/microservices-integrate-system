# ！/usr/bin/python3
# -*- coding: utf-8 -*-
import uuid
import yaml
import json
import secret
from os import path
from flask import Flask, jsonify, request
from flask_cors import CORS
from kubernetes.client import api_client
from kubernetes.client.api import core_v1_api
from kubernetes.client.api import CustomObjectsApi
from kubernetes import client, config


class KubernetesTools(object):
    def __init__(self):
        self.k8s_url = 'https://133.133.135.39:6443'

    def get_token(self):
        """
        获取token
        :return:
        """
        with open('token.txt', 'r') as file:
            Token = file.read().strip('\n')
            return Token

    def get_api(self):
        """
        获取API的CoreV1Api版本对象
        :return:
        """
        configuration = client.Configuration()
        configuration.host = self.k8s_url
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + self.get_token()}
        client1 = api_client.ApiClient(configuration=configuration)
        api = core_v1_api.CoreV1Api(client1)
        return api

    def get_apiv(self):
        configuration = client.Configuration()
        configuration.host = self.k8s_url
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + self.get_token()}
        client1 = api_client.ApiClient(configuration=configuration)
        apiv = CustomObjectsApi(client1)
        return apiv


    def create_secret(self, secret_name):
        api = self.get_api()
        with open(path.join(path.dirname(__file__), "E:/李安/vue/flask+vue/flask-vue-crud/server/secret.yaml")) as f:
            dep = yaml.safe_load(f)
        ret = api.create_namespaced_secret(namespace=secret_name, body=dep)
        return ret


    def create_service_account(self, service_account_name):
        api = self.get_api()
        with open(path.join(path.dirname(__file__), "E:/李安/vue/flask+vue/flask-vue-crud/server/service_account_name.yaml")) as f:
            dep = yaml.safe_load(f)
        ret = api.create_namespaced_service_account(namespace=service_account_name, body=dep)
        return ret

    def get_namespace_list(self):
        """
        获取命名空间列表
        :return:
        """
        api = self.get_api()
        namespace_list = []
        for ns in api.list_namespace().items:
            # print(ns.metadata.name)
            namespace_list.append(ns.metadata.name)

        return namespace_list

    def get_services(self):
        """
        获取所有services
        :return:
        """
        api = self.get_api()
        ret = api.list_service_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s \t%s \t%s \t%s \t%s \n" % (
                i.kind, i.metadata.namespace, i.metadata.name, i.spec.cluster_ip, i.spec.ports))

    def get_namespaced_services(self):

        api = self.get_api()
        namespaces = "default"
        ret = api.list_namespaced_service(namespace=namespaces)
        for i in ret.items:
            print("%s \t%s \t%s \t%s \t%s \n" % (
                i.kind, i.metadata.namespace, i.metadata.name, i.spec.cluster_ip, i.spec.ports))

    def get_pod_info(self):
        """
        查看pod信息
        :param namespaces: 命令空间，比如：default
        :param pod_name: pod完整名称，比如：flaskapp-1-5d96dbf59b-lhmp8
        :return:
        """
        api = self.get_api()
        # 示例参数
        namespaces = "tekton-pipelines"
        pod_name = "tekton-pipelines-controller-6fd67c849f-nwv55"
        resp = api.read_namespaced_pod(namespace=namespaces, name=pod_name)
        # 详细信息
        print(resp)
        return resp


    def get_task_info(self):

        apiv = self.get_apiv()
        ret = apiv.get_namespaced_custom_object(group="tekton.dev",version="v1alpha1",namespace="lian",plural="tasks",name="echo")
        return ret

    def get_task_status(self):
        apiv = self.get_apiv()
        res = apiv.get_namespaced_custom_object_status(group="tekton.dev",version="v1alpha1",namespace="lian",plural="tasks",name="echo")
        return res

    def deploy_task(self):
        apiv = self.get_apiv()
        with open(path.join(path.dirname(__file__), "E:/李安/vue/flask+vue/flask-vue-crud/server/task.yaml")) as f:
            dep = yaml.safe_load(f)
            resp_2 = apiv.create_namespaced_custom_object(group="tekton.dev",version="v1alpha1",namespace="lian",plural="tasks",body=dep)
            print("Pod created. status='%s'" % resp_2.metadata.name)

    def deploy_task_by_name(self, taname):
        apiv = self.get_apiv()
        f = open(taname, 'r')
        dep = yaml.safe_load(f)
        apiv.create_namespaced_custom_object(group="tekton.dev", version="v1alpha1", namespace="lian", plural="tasks", body=dep)

    def deploy_task_run(self, runame):
        apiv = self.get_apiv()
        f = open(runame, 'r')
        dep = yaml.safe_load(f)
        apiv.create_namespaced_custom_object(group="tekton.dev", version="v1alpha1", namespace="lian", plural="taskruns", body=dep)

    def list_namespace_po(self):
        api = self.get_api()
        ret = api.list_namespaced_pod(namespace="lian")
        return ret


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

TEKTON = [
    {
        'mission': 'I am cute and sweet',
        'name': 'tekton1',
        'process': 'ing',
        'region': 'gitlab'
    }
]

textarea = [
    {
        'secret':''
    }
]

test1 = 'default'
test2 = ''
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


def get_special_task_status(task_name):
    full_list = KubernetesTools().list_namespace_po()
    for i in full_list.items:
        obj = i.to_dict()
        items = obj['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration']
        items = json.loads(items)
        items1 = items["metadata"]["name"]
        if items1 == task_name:
            print(i.metadata.name)


def generate_task_template(task_name, task_body):
    filename = task_name + ".yaml"
    f = open(filename, "w")
    f.write(task_body)
    f.close()
    print("the file is generated!")
    return filename


# sanity check route
@app.route('/tekton', methods=['GET', 'POST'])
def add_tekton():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TEKTON.append({
            id: post_data.get('id')
        })
        response_object['message'] = 'tekton added'
    else:
        response_object['tekton'] = TEKTON
    return jsonify(response_object)

@app.route('/save_task_template', methods=['GET','POST'])
def get_task():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        file = generate_task_template(post_data.get('task_name'), post_data.get('task_body'))
        KubernetesTools().deploy_task_by_name(file)
        response_object['message'] = 'task template has been generated!'
    return jsonify(response_object)



@app.route('/tek_data', methods=['POST', 'DELETE'])
def mission_auto():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TEKTON.append({
                'mission': post_data.get('mission'),
                'name': post_data.get('name'),
                'process': post_data.get('process'),
                'region': post_data.get('region')
            })
        response_object['message'] = 'mission added'
    return jsonify(response_object)


@app.route('/yaml_data', methods=['POST', 'DELETE'])
def yaml_auto():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        textarea.append({
                'mission': post_data.get('mission'),
                'name': post_data.get('name'),
                'process': post_data.get('process'),
                'region': post_data.get('region')
            })
        response_object['message'] = 'mission added'
        print(textarea)
    return jsonify(response_object)


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    namespace_list = KubernetesTools().get_namespace_list()
    ta = 'ft'
    na = 'echo'
    ma = 'task.yaml'
    ru = 'tasktestrun.yaml'
    print(namespace_list)
    # ref = KubernetesTools().get_pod_info()
    # fe_2 = KubernetesTools().get_namespaced_services()
    # fe_1 = KubernetesTools().get_task_info()
    # fe_3 = KubernetesTools().get_task_status()
    # print(fe_3)
    # KubernetesTools().deploy_task()
    fs = KubernetesTools().list_namespace_po()
    #KubernetesTools().deploy_task_by_name(ma)
    #KubernetesTools().deploy_task_run(ru)
    #print(fs.metadata)
    #get_special_task_status(na)
    #generate_task_template(ta, na)

    app.run()

