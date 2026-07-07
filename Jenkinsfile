pipeline {

    agent any

    environment {
    IMAGE_NAME = "anilchoppara/student-app"
    IMAGE_TAG = "${BUILD_NUMBER}"
    KUBECONFIG = "/var/jenkins_home/.kube/config"
}

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                    -t $IMAGE_NAME:$IMAGE_TAG \
                    -t $IMAGE_NAME:latest .
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'PASSWORD'
                    )
                ]) {
                    sh '''
                    echo "$PASSWORD" | docker login -u "$USERNAME" --password-stdin
                    '''
                }
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                docker push $IMAGE_NAME:$IMAGE_TAG
                docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl get nodes

                kubectl set image deployment/student-app \
                student-app=$IMAGE_NAME:$IMAGE_TAG

                kubectl rollout status deployment/student-app
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                kubectl get pods
                kubectl get svc
                '''
            }
        }

    }

    post {

        success {
            echo "Deployment Successful"
        }

        failure {
            echo "Deployment Failed"
        }

        always {
            sh '''
            docker image prune -f || true
            docker logout || true
            '''
        }

    }

}