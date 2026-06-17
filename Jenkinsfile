pipeline {
    agent any

    environment {
        IMAGE_NAME = 'secuesdev-app'
        CONTAINER_NAME = 'secuesdev-app-prod'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Construyendo la imagen Docker de la app...'
                sh 'docker build -t ${IMAGE_NAME} ./app'
            }
        }

        stage('Test') {
            steps {
                echo 'Ejecutando pruebas basicas...'
                sh '''
                    docker rm -f test-container || true
                    docker run -d -p 5050:5000 --name test-container ${IMAGE_NAME}
                    sleep 5
                    docker run --rm --link test-container:app curlimages/curl -f http://app:5000
                    docker rm -f test-container
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Desplegando la aplicacion a produccion...'
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}
                '''
            }
        }
    }

        stage('Security Scan - OWASP ZAP') {
            steps {
                echo 'Ejecutando escaneo de seguridad con OWASP ZAP...'
                sh '''
                    mkdir -p zap-reports
                    chmod 777 zap-reports
                    docker run --rm --network secuesdev-net \
                        -v $(pwd)/zap-reports:/zap/wrk/:rw \
                        ghcr.io/zaproxy/zaproxy:stable \
                        zap-baseline.py -t http://${CONTAINER_NAME}:5000 \
                        -r zap-report.html || true
                '''
            }
        }

    post {
        always {
            archiveArtifacts artifacts: 'zap-reports/*.html', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline completado exitosamente.'
        }
        failure {
            echo 'El pipeline fallo. Revisar logs.'
        }
    }
}
