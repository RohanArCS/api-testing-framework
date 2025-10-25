pipeline {
  agent any

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }

  environment {
    PROJECT_DIR = '.'
    REPORT_FILE = 'report.html'
  }

  stages {
    stage('Detect project directory') {
      steps {
        script {
          if (fileExists('api_testing_framework/requirements.txt')) {
            env.PROJECT_DIR = 'api_testing_framework'
          } else if (fileExists('requirements.txt')) {
            env.PROJECT_DIR = '.'
          } else {
            error("Could not find requirements.txt at repo root or in api_testing_framework/")
          }
          echo "Using PROJECT_DIR=${env.PROJECT_DIR}"
        }
      }
    }

    stage('Ensure Python is installed') {
      steps {
        bat '''
          @echo off
          python --version >nul 2>&1
          if %errorlevel% neq 0 (
            echo Python not found, downloading installer...
            powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe -OutFile python-installer.exe"
            echo Installing Python silently...
            python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
            echo Adding Python to PATH for this session...
            set "PATH=C:\\Program Files\\Python311;C:\\Program Files\\Python311\\Scripts;%PATH%"
          ) else (
            echo Python already installed.
          )
          set "PATH=C:\\Program Files\\Python311;C:\\Program Files\\Python311\\Scripts;%PATH%"
          python --version
        '''
      }
    }

    stage('Setup Python venv') {
      steps {
        dir(env.PROJECT_DIR) {
          bat '''
            @echo off
            call "C:\\Program Files\\Python311\\python.exe" -m venv venv
            call venv\\Scripts\\activate
            python -m pip install --upgrade pip
            pip install -r requirements.txt
          '''
        }
      }
    }

    stage('Run tests') {
      steps {
        dir(env.PROJECT_DIR) {
          bat '''
            @echo off
            call venv\\Scripts\\activate
            pytest -q --maxfail=1 --html=report.html --self-contained-html
          '''
        }
      }
    }
  }

  post {
    always {
      // Safe publish: skip if plugin missing
      script {
        try {
          publishHTML(target: [
            reportDir: "${env.PROJECT_DIR}",
            reportFiles: "${env.REPORT_FILE}",
            reportName: "API Regression Test Report",
            keepAll: true,
            alwaysLinkToLastBuild: true,
            allowMissing: true
          ])
        } catch (e) {
          echo "HTML Publisher plugin not found or disabled — skipping publishHTML step."
        }
      }

      archiveArtifacts artifacts: "${env.PROJECT_DIR}/${env.REPORT_FILE}, ${env.PROJECT_DIR}/logs/**", fingerprint: true
    }
  }
}
