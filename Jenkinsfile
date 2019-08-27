pipeline {

  environment {
    APP_NAME = "logicapp"
  }

agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
metadata:
labels:
  component: ci
spec:
  # Use service account that can deploy to all namespaces
  serviceAccountName: jenkins-sa
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
  - name: jenkins-gcr-sa-creds
    secret:
      secretName: jenkins-gcr-json
  containers:
  - name: git
    image: gcr.io/cloud-builders/git
    command:
    - cat
    tty: true
  - name: python
    image: gcr.io/cloud-marketplace/google/python
    command:
    - cat
    tty: true
  - name: docker
    image: gcr.io/cloud-builders/docker
    command:
    - cat
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
    - name: jenkins-gcr-sa-creds
      mountPath: /tmp/gcr/
      readOnly: true
    env:
    - name: PROJECT
      valueFrom:
        configMapKeyRef:
          name: jenkins-vars
          key: gcloud-project
  - name: kubectl
    image: gcr.io/cloud-builders/kubectl
    command:
    - cat
    tty: true
    volumeMounts:
    - name: jenkins-gcr-sa-creds
      mountPath: /tmp/gcr/
      readOnly: true
    env:
    - name: PROJECT
      valueFrom:
        configMapKeyRef:
          name: jenkins-vars
          key: gcloud-project
"""
}
  }
  stages {
    stage('Checkout') {
        steps {
            git branch: 'master', url: "${GIT_URL}";
        }
    }
    stage('Code test') {
        steps {
        container('python'){
            sh "pip3 install -r requirements.txt";
            sh "python3 unit_test.py";
          }
        }
    }
    stage('Build and push container') {
      steps {
        container('docker') {
         sh "env"
         sh '''docker build -t eu.gcr.io/${PROJECT}/${APP_NAME}:${GIT_COMMIT} .''';
         sh "docker images";
        }
      }
    }
    stage('Push container') {
      steps {
        container('docker') {
          sh "cat /tmp/gcr/jenkins-gcr.json | docker login -u _json_key --password-stdin https://eu.gcr.io";
          sh '''docker push eu.gcr.io/${PROJECT}/${APP_NAME}:${GIT_COMMIT}''';
          }
      }
    }
    stage('Deploy') {
      steps {
        container('kubectl') {
            sh '''sed -i -e "s/CONTAINERTAG/${GIT_COMMIT}/g" -e "s/PROJECTID/${PROJECT}/g" deployment_dev ''';
            sh "kubectl apply -f deployment_dev";
        }
      }
    }
  }
}
