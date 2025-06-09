pipeline {
    agent any
    
    environment {
        AWS_DEFAULT_REGION = 'us-west-2'
        ECR_REPO = 'YOUR_ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/cricket-game'
        CLUSTER_NAME = 'cricket-game-cluster'
        SERVICE_NAME = 'cricket-game'
        SONAR_PROJECT_KEY = 'cricket-game'
    }
    
    tools {
        nodejs 'NodeJS-18'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'npm ci'
            }
        }
        
        stage('Code Quality - SonarQube') {
            steps {
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.sources=client/src,server \
                            -Dsonar.exclusions=**/node_modules/**,**/dist/**,**/*.test.js \
                            -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info
                        """
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                sh 'npm audit --audit-level=moderate'
            }
        }
        
        stage('Build Application') {
            steps {
                sh 'npm run build'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    def image = docker.build("${ECR_REPO}:${BUILD_NUMBER}")
                    docker.withRegistry("https://${ECR_REPO}", 'ecr:us-west-2:aws-credentials') {
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
        
        stage('Security Scan - Docker Image') {
            steps {
                sh """
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                    aquasec/trivy:latest image ${ECR_REPO}:${BUILD_NUMBER}
                """
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                script {
                    withAWS(credentials: 'aws-credentials', region: 'us-west-2') {
                        sh """
                            aws eks update-kubeconfig --region us-west-2 --name ${CLUSTER_NAME}
                            sed -i 's|YOUR_ECR_REPO|${ECR_REPO}|g' k8s/deployment.yaml
                            sed -i 's|latest|${BUILD_NUMBER}|g' k8s/deployment.yaml
                            kubectl apply -f k8s/
                            kubectl rollout status deployment/cricket-game-deployment -n cricket-game
                        """
                    }
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    sh """
                        sleep 30
                        kubectl get pods -n cricket-game
                        kubectl get svc -n cricket-game
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
            slackSend channel: '#deployments',
                      color: 'good',
                      message: "✅ Cricket Game deployed successfully - Build ${BUILD_NUMBER}"
        }
        failure {
            echo 'Pipeline failed!'
            slackSend channel: '#deployments',
                      color: 'danger',
                      message: "❌ Cricket Game deployment failed - Build ${BUILD_NUMBER}"
        }
    }
}
