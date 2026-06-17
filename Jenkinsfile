pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Construyendo la aplicacion...'
                sh 'echo "Aqui se construira la imagen Docker de la app vulnerable"'
            }
        }

        stage('Test') {
            steps {
                echo 'Ejecutando pruebas...'
                sh 'echo "Aqui se correran tests unitarios y luego OWASP ZAP"'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Desplegando la aplicacion...'
                sh 'echo "Aqui se desplegara el contenedor a produccion"'
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
