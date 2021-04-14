def generate_dockerhub_secret(role_name, username, pwd):
    filename = role_name + ".yaml"
    f = open(filename, 'w')
    line1 = "apiVersion: v1"
    line2 = "kind: Secret"
    line3 = "metadata:"
    line4 = "  name: docker-auth"
    line5 = "  annotations:"
    line6 = "    tekton.dev/docker-0: https://index.docker.io/v1/"
    line7 = "type: kubernetes.io/basic-auth"
    line8 = "stringData:"
    line9 = "username: " + username
    line10 = "password: " + pwd
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
        filename = "gitlab_secret_1.yaml"
        line4 = "  name: gitlab-auth"
        line6 = "    tekton.dev/git-0: https://gitlab.com/users/sign_in"
    if type == "github":
        filename = "github_secret_1.yaml"
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


def generate_webhook_secret(type,token):
    status = "success"
    if type == "gitlab":
        line4 = "  name: gitlab-webhook"
    if type == "github":
        line4 = "  name: github-webhook"
    else:
        status = "error"
    line1 = "apiVersion: v1"
    line2 = "kind: Secret"
    line3 = "metadata:"
    line5 = "type: Opaque"
    line6 = "stringData:"
    line7 = "  secretToken: \"" + token + "\""
    return status

def generate_service_account(type):
    line1 = "apiVersion: v1"
    line2 = "ServiceAccount"
    line3 = "metadata:"
    line4 = "  name: build-sa"
    line5 = "secrets:"
    line8 = "- name: docker-auth"
    status = "success"
    if type == "gitlab":
        line6 = "- name: gitlab-webhook"
        line7 = "- name: gitlab-auth"
    if type == "github":
        line6 = "- name: github-webhook"
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
    f.write(line6)
    f.write("\n")
    f.write(line7)
    f.write("\n")
    f.write(line8)
    f.close()
    return status

def generate_role_binding(type):
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
    line11 = "  name: cluster-admin"
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
    f.close()
    status = "success"
    return status

def generate_listener(type):
    if type == "gitlab":
        line4 = "gitlab-listener"
        line8 = "  - name: gitlab-push-events-trigger"
        line10 = "- name: gitlab-auth"
    if type == "github":
        line6 = "- name: github-webhook"
        line7 = "- name: github-auth"
    else:
        status = "error"
    line1 = "apiVersion: triggers.tekton.dev/v1alpha1"
    line2 = "kind: EventListener"
    line3 = "metadata:"
    line5 = "spec:"
    line6 = "  serviceAccountName: build-sa"
    line7 = "  triggers:"
    line8 = "    namespace: tekton-pipelines"
    line9 = "roleRef:"
    line10 = "  kind: ClusterRole"
    line11 = "  name: cluster-admin"
    line12 = "  apiGroup: rbac.authorization.k8s.io"
    filename = "tekton-admin.yaml"
# role = "user_01"
# user_name = "lian"
# password = "yylian2016"
# generate_dockerhub_secret(role, user_name, password)
