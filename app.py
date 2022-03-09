# -*- coding: utf-8 -*-
from re import template
import re
import sys
import requests
import uuid
#from flask.scaffold import F
import kubernetes
from kubernetes.client import api
from werkzeug.wrappers import response
import yaml
import json
from Lib.tkinter.tix import IMAGE
# from Modules._decimal.tests.deccheck import log
import secret
from os import name, path
from flask import Flask, jsonify, request
from flask_cors import CORS
from kubernetes.client.rest import ApiException
from kubernetes.client import api_client
from kubernetes.client.api import core_v1_api
from kubernetes.client.api import CustomObjectsApi
from kubernetes.client.api import RbacAuthorizationV1Api
from kubernetes import client, config


class KubernetesTools(object):
    def __init__(self):
        self.k8s_url = 'https://10.61.4.71:6443'

    def get_token(self):
        with open('token.txt', 'r') as file:
            Token = file.read().strip('\n')
            return Token

    def get_api(self):
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

    def get_apir(self):
        configuration = client.Configuration()
        configuration.host = self.k8s_url
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + self.get_token()}
        client1 = api_client.ApiClient(configuration=configuration)
        apir = RbacAuthorizationV1Api(client1)
        return apir


    def get_rbac(self):
        configuration = client.Configuration()
        configuration.host = self.k8s_url
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + self.get_token()}
        client1 = api_client.ApiClient(configuration=configuration)
        apirbac = RbacAuthorizationV1Api(client1)
        return apirbac

    def create_secret(self, secret_name):
        api = self.get_api()
        f = open(secret_name, 'r')
        dep = yaml.safe_load(f)
        ret = api.create_namespaced_secret(namespace='default', body=dep)
        return ret

    def patch_secret(self,name,secret_name):
        api = self.get_api()
        f = open(secret_name, 'r')
        dep = yaml.safe_load(f)
        ret = api.patch_namespaced_secret(name=name, namespace='default', body=dep)
        return ret

    def create_service_account(self, service_account_name):
        api = self.get_api()
        f = open(service_account_name, 'r')
        dep = yaml.safe_load(f)
        ret = api.create_namespaced_service_account(namespace='default', body=dep)
        return ret

    def patch_service_account(self, name, service_account_name):
        api = self.get_api()
        f = open(service_account_name, 'r')
        dep = yaml.safe_load(f)
        ret = api.patch_namespaced_service_account(name=name, namespace='default', body=dep)
        return ret

    def create_clusterrole(self,cr_name):
        apir = self.get_apir()
        f = open(cr_name, 'r')
        dep = yaml.safe_load(f)
        ret = apir.create_cluster_role(body=dep)
        return ret

    def patch_clusterrole(self,name, cr_name):
        apir = self.get_apir()
        f = open(cr_name, 'r')
        dep = yaml.safe_load(f)
        ret = apir.patch_cluster_role(name=name, body=dep)
        return ret


    def create_clusterrolebinding(self,crb_name):
        apir = self.get_apir()
        f = open(crb_name, 'r')
        dep = yaml.safe_load(f)
        ret = apir.create_cluster_role_binding(body=dep)
        return ret


    def patch_clusterrolebinding(self,name, crb_name):
        apir = self.get_apir()
        f = open(crb_name, 'r')
        dep = yaml.safe_load(f)
        ret = apir.patch_cluster_role_binding(name=name, body=dep)
        return ret

    def create_docker_resource(self,doname):
        apiv = self.get_apiv()
        f = open(doname, 'r')
        dep = yaml.safe_load(f)
        ret = apiv.create_namespaced_custom_object(group="tekton.dev", version="v1alpha1", namespace="default", plural="pipelineresources", body=dep)
        return ret


    def patch_docker_resource(self,name, doname):
        apiv = self.get_apiv()
        f = open(doname, 'r')
        dep = yaml.safe_load(f)
        ret = apiv.patch_namespaced_custom_object(group="tekton.dev", version="v1alpha1", namespace="default", plural="pipelineresources", name = name, body=dep)
        return ret

    def create_git_resource(self, giname):
        apiv = self.get_apiv()
        f = open(giname, 'r')
        dep = yaml.safe_load(f)
        ret = apiv.create_namespaced_custom_object(group="tekton.dev", version="v1alpha1", namespace="default", plural="pipelineresources", body=dep)
        return ret

    def patch_git_resource(self, name, giname):
        apiv = self.get_apiv()
        f = open(giname, 'r')
        dep = yaml.safe_load(f)
        ret = apiv.patch_namespaced_custom_object(group="tekton.dev", version="v1alpha1", namespace="default", plural="pipelineresources", name=name, body=dep)
        return ret

    def get_namespace_list(self):
        api = self.get_api()
        namespace_list = []
        for ns in api.list_namespace().items:
            # print(ns.metadata.name)
            namespace_list.append(ns.metadata.name)
        return namespace_list

    def get_services(self):
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

    def create_namespaced_pod(self, ns, pn):
        api = self.get_api()
        with open(path.join(path.dirname(__file__), "/root/Python-3.9.5/" + pn + ".yaml")) as f:
            dep = yaml.safe_load(f)
        ret = api.create_namespaced_pod(namespace=ns, body=dep)
        return ret

    def get_pod_info(self):
        api = self.get_api()
        # 示例参数
        namespaces = "lian"
        pod_name = "test-nginx"
        resp = api.read_namespaced_pod(namespace=namespaces, name=pod_name)
        # 详细信息
        print(resp)
        return resp

    def get_pod_log(self):
        api = self.get_api()
        namespaces = "kube_system"
        pod_name = "kube-proxy-2qwmv"
        resp = api.read_namespaced_pod_log_with_http_info(namespace=namespaces, name=pod_name)
        return resp

    def get_task_info(self):

        apiv = self.get_apiv()
        ret = apiv.get_namespaced_custom_object(group="tekton.dev", version="v1alpha1", namespace="lian",
                                                plural="tasks", name="echo")
        return ret

    def get_task_status(self):
        apiv = self.get_apiv()
        res = apiv.get_namespaced_custom_object_status(group="tekton.dev", version="v1alpha1", namespace="lian",
                                                       plural="tasks", name="echo")
        return res

    def patch_namespaced_task(self,name, taname):
        apiv = self.get_apiv()
        f = open(taname, 'r')
        dep = yaml.safe_load(f)
        ret = apiv.patch_namespaced_custom_object(group="tekton.dev", version="v1beta1", namespace="default", plural="tasks", name=name, body=dep)
        return ret

    def create_namespaced_task(self):
        apiv = self.get_apiv()
        with open(path.join(path.dirname(__file__), "E:/李安/vue/flask+vue/flask-vue-crud/server/task.yaml")) as f:
            dep = yaml.safe_load(f)
            resp_2 = apiv.create_namespaced_custom_object(group="tekton.dev", version="v1beta1", namespace="default",
                                                          plural="tasks", body=dep)
            print("Pod created. status='%s'" % resp_2.metadata.name)

    def create_task_by_name(self, taname):
        apiv = self.get_apiv()
        f = open(taname, 'r')
        dep = yaml.safe_load(f)
        ret = apiv.create_namespaced_custom_object(group="tekton.dev", version="v1beta1", namespace="default", plural="tasks", body=dep)
        return ret



    def create_task_run(self, runame):
        apiv = self.get_apiv()
        f = open(runame, 'r')
        dep = yaml.safe_load(f)
        ret = apiv.create_namespaced_custom_object(group="tekton.dev", version="v1beta1", namespace="default",plural="taskruns", body=dep)
        return ret

    def patch_taskrun(self,name,runame):
        apiv = self.get_apiv()
        f = open(runame, 'r')
        dep = yaml.safe_load(f)
        ret = apiv.patch_namespaced_custom_object(group="tekton.dev", version="v1beta1", namespace="default",plural="taskruns", name=name, body=dep)
        return ret

    def deploy_resource(self, rename):
        apiv = self.get_apiv()
        f = open(rename, 'r')
        dep = yaml.safe_load(f)
        apiv.create_namespaced_custom_object(group="tekton.dev", version="v1alpha1", namespace="lian",
                                             plural="pipelineresources", body=dep)

    def deploy_pvc(self, pvcname):
        api = self.get_api()
        f = open(pvcname, 'r')
        dep = yaml.safe_load(f)
        api.create_namespaced_persistent_volume_claim(namespace='lian', body=dep)

    def deploy_pv(self, pvname):
        api = self.get_api()
        f = open(pvname, 'r')
        dep = yaml.safe_load(f)
        api.create_persistent_volume(body=dep)

    def deploy_cluster_role(self, roname):
        apirbac = self.get_rbac()
        f = open(roname, 'r')
        dep = yaml.safe_load(f)
        apirbac.create_cluster_role(body=dep)

    def deploy_cluster_role_binding(self, roname):
        apirbac = self.get_rbac()
        f = open(roname, 'r')
        dep = yaml.safe_load(f)
        apirbac.create_cluster_role_binding(body=dep)

    def deploy_trigger_binding(self, trname):
        apiv = self.get_apiv()
        f = open(trname, 'r')
        dep = yaml.safe_load(f)
        apiv.create_namespaced_custom_object(group="triggers.tekton.dev", version="v1alpha1", namespace="lian",
                                             plural="triggerbindings", body=dep)

    def deploy_eventlistener(self, evname):
        apiv = self.get_apiv()
        f = open(evname, 'r')
        dep = yaml.safe_load(f)
        apiv.create_namespaced_custom_object(group="triggers.tekton.dev", version="v1alpha1", namespace="lian",
                                             plural="eventlisteners", body=dep)

    def deploy_template_by_name(self, tename):
        apiv = self.get_apiv()
        f = open(tename, 'r')
        dep = yaml.safe_load(f)
        apiv.create_namespaced_custom_object(group="triggers.tekton.dev", version="v1beta1", namespace="lian",
                                             plural="triggertemplates", body=dep)

    def list_namespaced_po(self, naname):
        api = self.get_api()
        pod_list = api.list_namespaced_pod(namespace=naname)
        return pod_list

    def get_pod_log(self, poname, coname, ns):
        api = self.get_api()
        content = api.read_namespaced_pod_log(name=poname, namespace=ns, tail_lines=5, container=coname)
        print(content)
        return content

    def delete_pod(self, poname, ns):
        api = self.get_api()
        result = api.delete_namespaced_pod(name=poname, namespace=ns)
        print(result)
        return result

    def replace_pod(self, poname, ns):
        api = self.get_api()
        with open(path.join(path.dirname(__file__), "/root/Python-3.9.5/" + poname + ".yaml")) as f:
            dep = yaml.safe_load(f)
        ret = api.patch_namespaced_pod(name=poname, namespace=ns, body=dep)
        return ret

    def create_pod(self,poname,ns):
        api = self.get_api()
        f = open(poname+".yaml", 'r')
        dep = yaml.safe_load(f)
        ret = api.create_namespaced_pod(namespace=ns, body=dep)
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

CONTAINERS = []
CONTAINERS_FULL = []
POD_NAME = []
STATES = []
VISUAL = []
IMAGE_LIST = []

textarea = [
    {
        'secret': ''
    }
]

test1 = 'fine'
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


def get_dockerhub_list(docker_url):
    list_2 = []
    url = "https://registry.hub.docker.com/v1/repositories/" + docker_url + "/tags"
    response = requests.get(url)
    if response.status_code < 200 or response.status_code >= 300:
        return ["error:", "url: " + url, "status code:" + str(response.status_code)]
    r = response.json()
    for i in r:
        list_2.append(i['name'])
    print(list_2)
    return list_2


# sanity check route
@app.route('/get_list', methods=['GET', 'POST'])
def get_list():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        li = post_data.get('img_repo')
        IM = get_dockerhub_list(li)
        response_object['img_list'] = IM
        print(IM)
    return jsonify(response_object)


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


@app.route('/save_task_template', methods=['GET', 'POST'])
def get_task():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        file = generate_task_template(post_data.get('task_name'), post_data.get('task_body'))
        KubernetesTools().deploy_task_by_name(file)
        response_object['message'] = 'task template has been generated!'
    return jsonify(response_object)

@app.route('/deploy_pod_by_images',methods=['GET','POST'])
def deploy():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        pod_ns = post_data.get('namespace')
        img_repo = post_data.get('img_repo')
        img_ver = post_data.get('img_version')
        secret.generate_pod(img_repo, img_ver)
        KubernetesTools().create_pod(poname='sample2',ns= pod_ns)
        response_object['message'] = 'task template has been generated!'
    return jsonify(response_object)


@app.route('/generate_git_secret', methods=['GET', 'POST'])
def get_secret():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        secret.auto_generate_task(post_data.get('list'), post_data.get('version'))
        s2 = secret.generate_dockerhub_secret(post_data.get('dhb_username'), post_data.get('dhb_pwd'))
        s3 = secret.generate_git_resource(post_data.get('git_url'))
        s4 = secret.generate_program_secret(post_data.get('type'), post_data.get('git_username'), post_data.get('git_pwd'))
        s5 = secret.generate_docker_resources(post_data.get('dhb_url'))
        s6 = secret.generate_rbac()
        s7 = secret.generate_tasks_run()
        s8 = secret.generate_service_account(post_data.get('type'))
        s9 = secret.generate_role_binding()
        #KubernetesTools().create_secret(secret_name='dockerhub_secret.yaml')
        # rbac_r = secret.generate_role()
        #pv_r = secret.generate_pv(post_data.get('cap'), post_data.get('nfs_path'), post_data.get('nfs_server'))
        #pvc_r = secret.generate_pvc(post_data.get('cap'))
        #print(git_secret_r)
        #print(docker_secret_r)
        #print(pvc_r)
        response_object['message'] = 'pvc_r'
    return jsonify(response_object)

@app.route('/deploy_yaml', methods=['GET', 'POST'])
def deploy_ya():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data.get('status') == 'ready':
            try:
                KubernetesTools().create_secret(secret_name='dockerhub_secret.yaml')
            except Exception as e:
                print("except:",e)
                ret = KubernetesTools().patch_secret(name='docker-auth', secret_name='dockerhub_secret.yaml')
                print(ret)
            try:
                KubernetesTools().create_secret(secret_name='github_secret.yaml')
            except Exception as e:
                print("except:",e)
                ret = KubernetesTools().patch_secret(name='github-auth', secret_name='github_secret.yaml')
                print(ret)
            try:
                KubernetesTools().create_service_account(service_account_name='service-account.yaml')
            except Exception as e:
                print("except:",e)
                ret = KubernetesTools().patch_service_account(name='build-sa', service_account_name='service-account.yaml')
                print(ret)
            try:
                KubernetesTools().create_clusterrole(cr_name='rbac.yaml')
            except Exception as e:
                print("except:",e)
                ret = KubernetesTools().patch_clusterrole(name='cluste-admin',cr_name='rbac.yaml')
                print(ret)
            try:
                KubernetesTools().create_clusterrolebinding(crb_name='tekton-admin.yaml')
            except Exception as e:
                print("except:",e)
                ret = KubernetesTools().patch_clusterrolebinding(name='tekton-cluster-admin',crb_name='tekton-admin.yaml')
                print(ret)
            try:
                KubernetesTools().create_docker_resource(doname='resources.yaml')
            except Exception as e:
                print("except:",e)
                ret = KubernetesTools().patch_docker_resource(name='output-images',doname='resources.yaml')
                print(ret)
            try:
                KubernetesTools().create_git_resource(giname='git_resource.yaml')
            except Exception as e:
                print("except:",e)
                ret = KubernetesTools().patch_git_resource(name='download-git', giname='git_resource.yaml')
                print(ret)
            try:
                KubernetesTools().create_task_by_name(taname='ta-default.yaml')
            except Exception as e:
                print("except:",e)
                ret = KubernetesTools().patch_namespaced_task(name='process', taname='ta-default.yaml')
                print(ret)
            try:
                KubernetesTools().create_task_run(runame='taskrun.yaml')
            except Exception as e:
                print("except:", e)
                ret = KubernetesTools().patch_taskrun(name='mytaskrun', runame='taskrun.yaml')
                return ret
    response_object['message'] = 'pvc_r'
    return jsonify(response_object)

@app.route('/generate_status', methods=['GET', 'POST'])
def return_status():
    response_object = {'status': 'success'}
    count = 0
    CONTAINERS = []
    CONTAINERS_FULL = []
    POD_NAME = []
    STATES = []
    VISUAL = []
    if request.method == 'POST':
        post_data = request.get_json()
        judege = post_data.get('status')
        print(judege)
        if judege == 'ready':
            na = post_data.get('namespace')
            ret = KubernetesTools().list_namespaced_po(na)
            for i in ret.items:
                POD_NAME.append({
                    'value': i.metadata.name

                })
                VISUAL.append({
                    'value': 'invisable'
                })
                co = i.status.container_statuses
                for j in co:
                    count = count + 1
                    if j.state.running is not None:
                        times = j.state.running.started_at
                        pattern = re.compile(r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})')
                        word = str(times)
                        n1 = pattern.match(word)
                        CONTAINERS.append({
                        'name': j.name,
                        'image': j.image,
                        'timestamp': n1.group(0),
                        'count': count
                        })
                    if j.state.running is None:
                        CONTAINERS.append({
                        'name': j.name,
                        'image': j.image,
                        'timestamp': '',
                        'count': count
                     })
                    count = 0
                CONTAINERS_FULL.append(CONTAINERS)
                print(len(CONTAINERS))
                CONTAINERS = []
        response_object['pods_name'] = POD_NAME
        response_object['containers_name'] = CONTAINERS_FULL
        response_object['containers_state'] = STATES
        response_object['visual'] = VISUAL
        print(CONTAINERS_FULL)
    return jsonify(response_object)


@app.route('/get_log', methods=['POST', 'PUT'])
def get_log():
    response_object = {'status': 'success'}
    LOG = []
    if request.method == 'POST':
        count = 0
        post_data = request.get_json()
        poname = post_data.get('pod_name')
        ns = post_data.get('namespace')
        coname = post_data.get('co_name')
        index = post_data.get('post_index')
        TOOL = []
        TOOL_2 = []
        for i in coname:
            print(i['name'])
            ret = KubernetesTools().get_pod_log(poname['value'], i['name'], ns)
            # print(ret)
            TOOL = ret.split("\n")
            # print(TOOL)
            LOG.append({
                'value': TOOL
            })
            TOOL = []
            # print(index)
        print(LOG)
        # print(LOG[0]['value'][0])
        response_object['visual'] = 'true'
        response_object['log'] = LOG
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


@app.route('/image_replace', methods=['POST', 'DELETE'])
def image_auto():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        ns = "kube-system"
        post_data = request.get_json()
        pn = post_data.get('pod_name')
        im = post_data.get('image_name')
        ve = post_data.get('version')
        st = secret.generate_template_by_images(im, pn, ve)
        if st == 'success':
            print("yes")
            KubernetesTools().replace_pod(pn, ns)
            # KubernetesTools().delete_pod(pn,ns)
            # KubernetesTools().create_namespaced_pod(ns,pn)
    return jsonify(response_object)


@app.route('/generate_list', methods=['POST', 'DELETE'])
def get_ns_list():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        judege = post_data.get('status')
        if judege == 'ready':
            nsl = KubernetesTools().get_namespace_list()
            response_object['nss'] = nsl
    return jsonify(response_object)


@app.route('/delete_pod', methods=['POST', 'DELETE'])
def delete_auto():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        ns = post_data.get('namespace')
        pn = post_data.get('pod_name')
        KubernetesTools().delete_pod(pn, ns)
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
    nsp = 'kube-system'
    test1 = 'myspod'
    s = 'calendulagirl/k8s_python_sample_code'
    v = 'v1'
    #ta = KubernetesTools().get_pod_info()
    # na = KubernetesTools().get_pod_log()
    # secret.generate_role()
    ra = 'etcd-kvm01'
    # KubernetesTools().deploy_cluster_role(ra)
    ma = 'ta-default.yaml'
    ru = 'tasktestrun.yaml'
    #secret.generate_template_by_images(s, test1, v)
    # KubernetesTools().create_namespaced_pod(nsp,test1)
    # KubernetesTools().delete_pod(test1,nsp)
    # ret = KubernetesTools().get_pod_log(ra)
    # print(ta.spec.containers)
    # for i in ta.spec.containers:
    #    print(i.name)
    #   CONTAINERS.append({
    #      'name': i.name
    # })

    # for j in ta.status.container_statuses:
    #     print(j.ready)
    # print(CONTAINERS)
    #nss = KubernetesTools().get_namespace_list()
    #print(nss)
    #namespace_list = KubernetesTools().list_namespaced_po(nsp)
    #KubernetesTools().deploy_task_by_name(ma)
    # get_dockerhub_list(s)
    # print(namespace_list)
    # print(namespace_list.items)
    # KubernetesTools().deploy_template_by_name(ma)
    # print(ta.metadata.labels)
    # print (na)

    # ref = KubernetesTools().get_pod_info()
    # fe_2 = KubernetesTools().get_namespaced_services()
    # fe_1 = KubernetesTools().get_task_info()
    # fe_3 = KubernetesTools().get_task_status()
    # print(fe_3)
    # KubernetesTools().deploy_task()
    # fs = KubernetesTools().list_namespace_po()
    # KubernetesTools().deploy_task_by_name(ma)
    # KubernetesTools().deploy_task_run(ru)
    # print(fs.metadata)
    # get_special_task_status(na)
    # generate_task_template(ta, na)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
