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
                    curl -f http://localhost:5050 || exit 1
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

    post {
        success {
            echo 'Pipeline completado exitosamente.'
        }
        failure {
            echo 'El pipeline fallo. Revisar logs.'
        }
    }
}
