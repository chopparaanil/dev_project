pipeline {

    agent any

    environment {
        DOCKER_USERNAME = "anilchoppara"
        IMAGE_NAME = "student-app"
        IMAGE = "${DOCKER_USERNAME}/${IMAGE_NAME}"
        IMAGE_TAG = "${BUILD_NUMBER}"
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

        stage('Python Checks') {
            steps {
                sh '''
                docker run --rm \
                    -v $WORKSPACE:/app \
                    -w /app \
                    python:3.12-slim \
                    sh -c "
                        pip install --no-cache-dir -r requirements.txt &&
                        pip install flake8 pytest &&
                        flake8 . &&
                        pytest
                    "
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                  -t $IMAGE:$IMAGE_TAG \
                  -t $IMAGE:latest .
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
                docker push $IMAGE:$IMAGE_TAG
                docker push $IMAGE:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                    kubectl set image deployment/student-app \
                    student-app=$IMAGE:$IMAGE_TAG

                    kubectl rollout status deployment/student-app
                    '''
                }
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