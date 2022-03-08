import json


def generate_dockerhub_secret(username, pwd):
    filename = "dockerhub_secret.yaml"
    f = open(filename, 'w')
    line1 = "apiVersion: v1"
    line2 = "kind: Secret"
    line3 = "metadata:"
    line4 = "  name: docker-auth"
    line5 = "  annotations:"
    line6 = "    tekton.dev/docker-0: https://index.docker.io/v1/"
    line7 = "type: kubernetes.io/basic-auth"
    line8 = "stringData:"
    line9 = "  username: " + username
    line10 = "  password: " + pwd
    f.write(line1)
    f.write("\n")
    f.write(line2)
    f.write("\n")
    f.write(line3)
    f.write("\n")
    f.write(line4)
    f.write("\n")
    f.write(line5)
    f.write("\n")
    f.write(line6)
    f.write("\n")
    f.write(line7)
    f.write("\n")
    f.write(line8)
    f.write("\n")
    f.write(line9)
    f.write("\n")
    f.write(line10)
    f.close()
    status = "success"
    return status


def generate_program_secret(type, username, pwd):
    line1 = "apiVersion: v1"
    line2 = "kind: Secret"
    line3 = "metadata:"
    line5 = "  annotations:"
    line7 = "type: kubernetes.io/basic-auth"
    line8 = "stringData:"
    line9 = "  username: " + username
    line10 = "  password: " + pwd
    status = "success"
    if type == "gitlab":
        filename = "gitlab_secret.yaml"
        line4 = "  name: gitlab-auth"
        line6 = "    tekton.dev/git-0: https://gitlab.com/users/sign_in"
    if type == "github":
        filename = "github_secret.yaml"
        line4 = "  name: github-auth"
        line6 = "    tekton.dev/git-0: https://github.com/login"
    else:
        status = "error"
    f = open(filename, 'w')
    f.write(line1)
    f.write("\n")
    f.write(line2)
    f.write("\n")
    f.write(line3)
    f.write("\n")
    f.write(line4)
    f.write("\n")
    f.write(line5)
    f.write("\n")
    f.write(line6)
    f.write("\n")
    f.write(line7)
    f.write("\n")
    f.write(line8)
    f.write("\n")
    f.write(line9)
    f.write("\n")
    f.write(line10)
    f.close()
    return status


def generate_webhook_secret(type, token):
    status = "success"
    if type == "gitlab":
        filename = "gitlab_webhook.yaml"
        line4 = "  name: gitlab-webhook"
    if type == "github":
        filename = "github_webhook.yaml"
        line4 = "  name: github-webhook"
    else:
        status = "error"
    line1 = "apiVersion: v1"
    line2 = "kind: Secret"
    line3 = "metadata:"
    line5 = "type: Opaque"
    line6 = "stringData:"
    line7 = "  secretToken: " + token + ""
    f = open(filename, 'w')
    f.write(line1)
    f.write("\n")
    f.write(line2)
    f.write("\n")
    f.write(line3)
    f.write("\n")
    f.write(line4)
    f.write("\n")
    f.write(line5)
    f.write("\n")
    f.write(line6)
    f.write("\n")
    f.write(line7)
    f.write("\n")
    return status


def generate_docker_resources(hub):  # dockerhub 上传镜像资源
    line1 = "apiVersion: tekton.dev/v1alpha1"
    line2 = "kind: PipelineResource"
    line3 = "metadata:"
    line4 = "  name: output-images"
    line5 = "spec:"
    line6 = "  type: image"
    line7 = "  params:"
    line8 = "  - name: url"
    line9 = "    value: " + hub
    status = "success"
    filename = "resources.yaml"
    f = open(filename, 'w')
    f.write(line1)
    f.write("\n")
    f.write(line2)
    f.write("\n")
    f.write(line3)
    f.write("\n")
    f.write(line4)
    f.write("\n")
    f.write(line5)
    f.write("\n")
    f.write(line6)
    f.write("\n")
    f.write(line7)
    f.write("\n")
    f.write(line8)
    f.write("\n")
    f.write(line9)
    f.write("\n")
    f.close()
    return status


def generate_git_resource(git_address):  # 下载git资源
    content = []
    content.append("apiVersion: tekton.dev/v1alpha1")
    content.append("kind: PipelineResource")
    content.append("metadata:")
    content.append("  name: download-git")
    content.append("spec:")
    content.append("  type: git")
    content.append("  params:")
    content.append("    - name: url")
    content.append("      value: " + git_address)
    filename = "git_resource.yaml"
    f = open(filename, 'w')
    for j in range(len(content)):
        f.write(content[j])
        f.write("\n")
    content.clear()
    f.close()
    status = "success"
    return status


def generate_service_account(type):  # 绑定密码
    line1 = "apiVersion: v1"
    line2 = "kind: ServiceAccount"
    line3 = "metadata:"
    line4 = "  name: build-sa"
    line5 = "secrets:"
    line8 = "- name: docker-auth"
    status = "success"
    if type == "gitlab":
        line7 = "- name: gitlab-auth"
    if type == "github":
        line7 = "- name: github-auth"
    else:
        status = "error"
    filename = "service-account.yaml"
    f = open(filename, 'w')
    f.write(line1)
    f.write("\n")
    f.write(line2)
    f.write("\n")
    f.write(line3)
    f.write("\n")
    f.write(line4)
    f.write("\n")
    f.write(line5)
    f.write("\n")
    f.write(line7)
    f.write("\n")
    f.write(line8)
    f.write("\n")
    f.close()
    return status





def generate_rbac():
    content = []
    content.append("kind: ClusterRole")
    content.append("apiVersion: rbac.authorization.k8s.io/v1")
    content.append("metadata:")
    content.append("  name: cluste-admin")
    content.append("rules:")
    content.append("- apiGroups: [\"triggers.tekton.dev\"]")
    content.append("  resources: [\"eventlisteners\", \"triggerbindings\", \"triggertemplates\"]")
    content.append("  verbs: [\"get\"]")
    content.append("- apiGroups: [\"\"]")
    content.append("  resources: [\"configmaps\", \"secrets\", \"serviceaccounts\", \"pods\"]")
    content.append("  verbs: [\"get\", \"list\", \"watch\", \"create\"]")
    content.append("- apiGroups: [\"tekton.dev\"]")
    content.append("  resources: [\"pipelineruns\", \"pipelineresources\", \"taskruns\", \"tasks\"]")
    content.append("  verbs: [\"create\"]")
    filename = "rbac.yaml"
    f = open(filename, 'w')
    for j in range(len(content)):
        f.write(content[j])
        f.write("\n")
    content.clear()
    f.close()
    status = "success"
    return status

def generate_pod(imgp, ver):
    content = []
    content.append("apiVersion: v1")
    content.append("kind: Pod")
    content.append("metadata:")
    content.append("  name: mypod")
    content.append("spec:")
    content.append("  containers:")
    content.append("  - name: sample2")
    content.append("    image: "+imgp+":"+ver)
    content.append("    imagePullPolicy: IfNotPresent")
    filename = "sample2.yaml"
    f = open(filename, 'w')
    for j in range(len(content)):
        f.write(content[j])
        f.write("\n")
    content.clear()
    f.close()
    status = "success"
    return status


def generate_role_binding():
    line1 = "apiVersion: rbac.authorization.k8s.io/v1"
    line2 = "kind: ClusterRoleBinding"
    line3 = "metadata:"
    line4 = "  name: tekton-cluster-admin"
    line5 = "subjects:"
    line6 = "  - kind: ServiceAccount"
    line7 = "    name: build-sa"
    line8 = "    namespace: tekton-pipelines"
    line9 = "roleRef:"
    line10 = "  kind: ClusterRole"
    line11 = "  name: cluste-admin"
    line12 = "  apiGroup: rbac.authorization.k8s.io"
    filename = "tekton-admin.yaml"
    f = open(filename, 'w')
    f.write(line1)
    f.write("\n")
    f.write(line2)
    f.write("\n")
    f.write(line3)
    f.write("\n")
    f.write(line4)
    f.write("\n")
    f.write(line5)
    f.write("\n")
    f.write(line6)
    f.write("\n")
    f.write(line7)
    f.write("\n")
    f.write(line8)
    f.write("\n")
    f.write(line9)
    f.write("\n")
    f.write(line10)
    f.write("\n")
    f.write(line11)
    f.write("\n")
    f.write(line12)
    f.close()
    status = "success"
    return status


def generate_triggerBinding(type):
    if type == "gitlab":
        line1 = "apiVersion: triggers.tekton.dev/v1alpha1"
        line2 = "kind: TriggerBinding"
        line3 = "metadata:"
        line4 = "  name: gitlab-push-binding"
        line5 = "spec:"
        line6 = "  params:"
        line7 = "  - name: gitrevision"
        line8 = "    value: $(body.checkout_sha)"
        line9 = "  - name: gitrepositoryurl"
        line10 = "    value: $(body.repository.git_http_url)"
        filename = "gitlab-triggerBinding.yaml"
        f = open(filename, 'w')
        f.write(line1)
        f.write("\n")
        f.write(line2)
        f.write("\n")
        f.write(line3)
        f.write("\n")
        f.write(line4)
        f.write("\n")
        f.write(line5)
        f.write("\n")
        f.write(line6)
        f.write("\n")
        f.write(line7)
        f.write("\n")
        f.write(line8)
        f.write("\n")
        f.write(line9)
        f.write("\n")
        f.write(line10)
        f.close()
    if type == "github":
        line1 = "apiVersion: triggers.tekton.dev/v1alpha1"
        line2 = "kind: TriggerBinding"
        line3 = "metadata:"
        line4 = "  name: github-push-binding"
        line5 = "spec:"
        line6 = "  params:"
        line7 = "  - name: gitrevision"
        line8 = "    value: $(body.before)"
        line9 = "  - name: gitrepositoryurl"
        line10 = "    value: $(body.clone_url)"
        filename = "gitlab-triggerBinding.yaml"
        f = open(filename, 'w')
        f.write(line1)
        f.write("\n")
        f.write(line2)
        f.write("\n")
        f.write(line3)
        f.write("\n")
        f.write(line4)
        f.write("\n")
        f.write(line5)
        f.write("\n")
        f.write(line6)
        f.write("\n")
        f.write(line7)
        f.write("\n")
        f.write(line8)
        f.write("\n")
        f.write(line9)
        f.write("\n")
        f.write(line10)
        f.close()


def generate_listener(type):
    if type == "gitlab":
        line1 = "apiVersion: triggers.tekton.dev/v1alpha1"
        line2 = "kind: EventListener"
        line3 = "metadata:"
        line4 = "  name: gitlab-listener"
        line5 = "spec:"
        line6 = "  serviceAccountName: build-sa"
        line7 = "  triggers:"
        line8 = "    - name: gitlab-push-events-trigger"
        line9 = "      interceptors:"
        line10 = "        - name: \"verify-gitlab-payload\""
        line11 = "          ref:"
        line12 = "            name: \"gitlab\""
        line13 = "            kind: ClusterInterceptor"
        line14 = "          params:"
        line15 = "            - name: secretRef"
        line16 = "              value:"
        line17 = "                secretName: \"gitlab-webhook\""
        line18 = "                secretKey: \"secretToken\""
        line19 = "            - name: eventTypes"
        line20 = "              value:"
        line21 = "                - \"Push Hook\""
        line22 = "      bindings:"
        line23 = "        - ref: gitlab-push-binding"
        line24 = "      template:"
        line25 = "        - ref: gitlab-template"
        filename = "gitlab-eventlistener.yaml"
        f = open(filename, 'w')
        f.write(line1)
        f.write("\n")
        f.write(line2)
        f.write("\n")
        f.write(line3)
        f.write("\n")
        f.write(line4)
        f.write("\n")
        f.write(line5)
        f.write("\n")
        f.write(line6)
        f.write("\n")
        f.write(line7)
        f.write("\n")
        f.write(line8)
        f.write("\n")
        f.write(line9)
        f.write("\n")
        f.write(line10)
        f.write("\n")
        f.write(line11)
        f.write("\n")
        f.write(line12)
        f.write("\n")
        f.write(line13)
        f.write("\n")
        f.write(line14)
        f.write("\n")
        f.write(line15)
        f.write("\n")
        f.write(line16)
        f.write("\n")
        f.write(line17)
        f.write("\n")
        f.write(line18)
        f.write("\n")
        f.write(line19)
        f.write("\n")
        f.write(line20)
        f.write("\n")
        f.write(line21)
        f.write("\n")
        f.write(line22)
        f.write("\n")
        f.write(line23)
        f.write("\n")
        f.write(line24)
        f.write("\n")
        f.write(line25)
        f.close()
        status = "success"
    if type == "github":
        line1 = "apiVersion: triggers.tekton.dev/v1alpha1"
        line2 = "kind: EventListener"
        line3 = "metadata:"
        line4 = "  name: github-listener"
        line5 = "spec:"
        line22 = "  serviceAccountName: build-sa"
        line6 = "  triggers:"
        line7 = "    - name: github-push-events-trigger"
        line8 = "      interceptors:"
        line9 = "        - ref:"
        line10 = "            name: \"github\""
        line11 = "          params:"
        line12 = "            - name: \"secretRef\""
        line13 = "              value:"
        line14 = "                secretName: github-webhook"
        line15 = "                secretKey: secretToken"
        line16 = "            - name: \"eventTypes\""
        line17 = "              value: [\"push\"]"
        line18 = "      bindings:"
        line19 = "        - ref: github-push-binding"
        line20 = "      template:"
        line21 = "        ref: github-template"
        filename = "github-eventlistener.yaml"
        f = open(filename, 'w')
        f.write(line1)
        f.write("\n")
        f.write(line2)
        f.write("\n")
        f.write(line3)
        f.write("\n")
        f.write(line4)
        f.write("\n")
        f.write(line5)
        f.write("\n")
        f.write(line22)
        f.write("\n")
        f.write(line6)
        f.write("\n")
        f.write(line7)
        f.write("\n")
        f.write(line8)
        f.write("\n")
        f.write(line9)
        f.write("\n")
        f.write(line10)
        f.write("\n")
        f.write(line11)
        f.write("\n")
        f.write(line12)
        f.write("\n")
        f.write(line13)
        f.write("\n")
        f.write(line14)
        f.write("\n")
        f.write(line15)
        f.write("\n")
        f.write(line16)
        f.write("\n")
        f.write(line17)
        f.write("\n")
        f.write(line18)
        f.write("\n")
        f.write(line19)
        f.write("\n")
        f.write(line20)
        f.write("\n")
        f.write(line21)
        f.close()
        status = "success"
    else:
        status = "error"
    return status


def auto_generate_task(list_,version):
    content = []
    content.append("apiVersion: tekton.dev/v1beta1")
    content.append("kind: Task")
    content.append("metadata:")
    content.append("  name: process")
    content.append("spec:")
    content.append("  resources:")
    content.append("    inputs:")
    content.append("    - name: git-source")
    content.append("      type: git")
    content.append("    outputs:")
    content.append("    - name: builtImage")
    content.append("      type: image")
    content.append("  workspaces:")
    content.append("    - name: cache")
    content.append("  steps:")
    content.append("    - name: clone-source")
    content.append("      image: ubuntu")
    content.append("      script: |")
    content.append("        cp -avr $(inputs.resources.git-source.path)/ $(workspaces.cache.path)/")
    content.append("        ls $(workspaces.cache.path)/git-source/")
    filename = "ta-default.yaml"
    f = open(filename, 'w')
    for z in range(len(content)):
        f.write(content[z])
        f.write("\n")
        print(content[z])
    content.clear()
    for i in range(len(list_)):
        if list_[i]['value'] == "show":
            content.append("    - name: seeson")
            content.append("      image: ubuntu")
            content.append("      script: |")
            content.append("        #! /bin/bash")
            content.append("        ls -la $(workspaces.cache.path)")
            for j in range(len(content)):
                f.write(content[j])
                f.write("\n")
                print(content[j])
            content.clear()
        if list_[i]['value'] == "install":
            content.append("    - name: npm-install")
            content.append("      image: node")
            content.append("      workingDir: $(workspaces.cache.path)/git-source/")
            content.append("      command:")
            content.append("        - /bin/sh")
            content.append("        - -c")
            content.append("      args:")
            content.append("        - npm install")
            for j in range(len(content)):
                f.write(content[j])
                f.write("\n")
            content.clear()
        if list_[i]['value'] == "update":
            content.append("    - name: npm-update")
            content.append("      image: node")
            content.append("      workingDir: $(workspaces.cache.path)/git-source/")
            content.append("      command:")
            content.append("        - /bin/sh")
            content.append("        - -c")
            content.append("      args:")
            content.append("        - npm audit fix --force")
            for j in range(len(content)):
                f.write(content[j])
                f.write("\n")
            content.clear()
        if list_[i]['value'] == "run":
            content.append("    - name: npm-run")
            content.append("      image: node")
            content.append("      workingDir: $(workspaces.cache.path)/git-source/")
            content.append("      command:")
            content.append("        - /bin/sh")
            content.append("        - -c")
            content.append("      args:")
            content.append("        - npm run build:prod")
            for j in range(len(content)):
                f.write(content[j])
                f.write("\n")
            content.clear()
        if list_[i]['value'] == "image":
            content.append("    - name: build-images")
            content.append("      image: cnych/kaniko-executor:v0.22.0")
            content.append("      env:")
            content.append("        - name: DOCKER_CONFIG")
            content.append("          value: /tekton/home/.docker")
            content.append("      args:")
            content.append("      - --dockerfile=Dockerfile")
            content.append("      - --destination=$(outputs.resources.builtImage.url):"+version)
            content.append("      - --context=$(workspaces.cache.path)/git-source/")
            for j in range(len(content)):
                f.write(content[j])
                f.write("\n")
            content.clear()
    f.close()
    status = "success"
    return status


def auto_generate_template():
    line1 = "apiVersion: triggers.tekton.dev/v1beta1"
    line2 = "kind: TriggerTemplate"
    line3 = "metadata:"
    line4 = "  name: simple-template"
    line5 = "spec:"
    line6 = "  params:"
    line7 = "    - name: gitrevision"
    line8 = "    - name: gitrepositoryurl"
    line9 = "  resourcetemplates:"
    line10 = "    - apiVersion: tekton.dev/v1alpha1"
    line11 = "      kind: TaskRun"
    line12 = "      metadata:"
    line13 = "        generateName: gitlab-run-"
    line14 = "      spec:"
    line15 = "        serviceAccountName: build-sa"
    line16 = "        taskRef:"
    line17 = "          name: process  "
    line18 = "        resources:"
    line19 = "          inputs:"
    line20 = "            - name: source  "
    line21 = "              resourceSpec:"
    line22 = "                type: git"
    line23 = "                params:"
    line24 = "                  - name: revision"
    line25 = "                    value: $(tt.params.gitrevision) "
    line26 = "                  - name: url"
    line27 = "                    value: $(tt.params.gitrepositoryurl)"
    line28 = "          outputs:"
    line29 = "            - name: builtImage "
    line30 = "              resourceRef:"
    line31 = "                name: registry-pipeline-resource"
    line32 = "        workspaces:"
    line33 = "          - name: cache"
    line34 = "            persistentVolumeClaim:"
    line35 = "              claimName: cache-pvc"
    filename = "task-default.yaml"
    f = open(filename, 'w')
    f.write(line1)
    f.write("\n")
    f.write(line2)
    f.write("\n")
    f.write(line3)
    f.write("\n")
    f.write(line4)
    f.write("\n")
    f.write(line5)
    f.write("\n")
    f.write(line6)
    f.write("\n")
    f.write(line7)
    f.write("\n")
    f.write(line8)
    f.write("\n")
    f.write(line9)
    f.write("\n")
    f.write(line10)
    f.write("\n")
    f.write(line11)
    f.write("\n")
    f.write(line12)
    f.write("\n")
    f.write(line13)
    f.write("\n")
    f.write(line14)
    f.write("\n")
    f.write(line15)
    f.write("\n")
    f.write(line16)
    f.write("\n")
    f.write(line17)
    f.write("\n")
    f.write(line18)
    f.write("\n")
    f.write(line19)
    f.write("\n")
    f.write(line20)
    f.write("\n")
    f.write(line21)
    f.write("\n")
    f.write(line22)
    f.write("\n")
    f.write(line23)
    f.write("\n")
    f.write(line24)
    f.write("\n")
    f.write(line25)
    f.write("\n")
    f.write(line26)
    f.write("\n")
    f.write(line27)
    f.write("\n")
    f.write(line28)
    f.write("\n")
    f.write(line29)
    f.write("\n")
    f.write(line30)
    f.write("\n")
    f.write(line31)
    f.write("\n")
    f.write(line32)
    f.write("\n")
    f.write(line33)
    f.write("\n")
    f.write(line34)
    f.write("\n")
    f.write(line35)
    f.write("\n")
    f.close()
    status = "success"
    return status
    # for i in range(len(list)):
    #   if list[i]['image'] == "show":

    print('ok')


# role = "user_01"
# user_name = "lian"
# password = "yylian2016"
# generate_dockerhub_secret(role, user_name, password)
def generate_pv(cap, nfs_path, nfs_server):
    content = []
    content.append("apiVersion: v1")
    content.append("kind: PersistentVolume")
    content.append("metadata:")
    content.append("  name: nfspv1")
    content.append("  labels:")
    content.append("    app: vnc")
    content.append("spec:")
    content.append("  capacity:")
    content.append("    storage: " + cap)
    content.append("  accessModes:")
    content.append("  - ReadWriteMany")
    content.append("  persistentVolumeReclaimPolicy: Retain")
    content.append("  storageClassName: nfsv1")
    content.append("  nfs:")
    content.append("    path: " + nfs_path)
    content.append("    server: " + nfs_server)
    filename = "PV.yaml"
    f = open(filename, 'w')
    for j in range(len(content)):
        f.write(content[j])
        f.write("\n")
    content.clear()
    f.close()
    status = "success"
    return status


def generate_pvc(cap):
    content = []
    content.append("apiVersion: v1")
    content.append("kind: PersistentVolumeClaim")
    content.append("metadata:")
    content.append("  name: cache-pvc")
    content.append("  labels:")
    content.append("    app: vnc")
    content.append("spec:")
    content.append("  accessModes:")
    content.append("  - ReadWriteMany")
    content.append("  resources:")
    content.append("    requests:")
    content.append("      storage: " + cap)
    content.append("  selector:")
    content.append("    matchLabels:")
    content.append("     app: vnc")
    content.append("  storageClassName: nfsv1")
    filename = "PVC.yaml"
    f = open(filename, 'w')
    for j in range(len(content)):
        f.write(content[j])
        f.write("\n")
    content.clear()
    f.close()
    status = "success"
    return status


def generate_template_by_images(im, po, ver):
    content = []
    content.append("apiVersion: v1")
    content.append("kind: Pod")
    content.append("metadata:")
    content.append("  name: " + po)
    content.append("spec:")
    content.append("  containers:")
    content.append("  - name: sample")
    content.append("    image: " + im + ":" + ver)
    content.append("    imagePullPolicy: IfNotPresent")
    filename = po + ".yaml"
    f = open(filename, 'w')
    for j in range(len(content)):
        f.write(content[j])
        f.write("\n")
    content.clear()
    f.close()
    status = "success"
    return status


def generate_tasks_run():
    content = []
    content.append("apiVersion: tekton.dev/v1beta1")
    content.append("kind: TaskRun")
    content.append("metadata:")
    content.append("  name: mytaskrun")
    content.append("spec:")
    content.append("  resources:")
    content.append("    inputs:")
    content.append("      - name: git-source ")
    content.append("        resourceRef:")
    content.append("          name: download-git")
    content.append("    outputs:")
    content.append("      - name: builtImage")
    content.append("        resourceRef:")
    content.append("          name: output-images")
    content.append("  serviceAccountName: build-sa")
    content.append("  taskRef:")
    content.append("    name: process")
    content.append("  workspaces:")
    content.append("   - name: cache")
    content.append("     emptyDir: {}")
    filename = "taskrun.yaml"
    f = open(filename, 'w')
    for j in range(len(content)):
        f.write(content[j])
        f.write("\n")
    content.clear()
    f.close()
    status = "success"
    return status


auto_generate_template()