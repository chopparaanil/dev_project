Jenkins Installation on Rocky Linux 9 (Step-by-Step)
This guide follows the installation process you just completed, including fixing the Java version and port conflict.

Step 1: Update the System
sudo dnf update -y

Step 2: Install Java 21
Check the current Java version:
java -version
If Java 21 is not installed:
sudo dnf install java-21-openjdk java-21-openjdk-devel -y
Verify:
java -version
Expected:
openjdk version "21.x.x"

Step 3: Set Java 21 as Default
List installed Java versions:
sudo alternatives --config java
Example:
1  Java 17
2  Java 11
3  Java 21
Select the Java 21 option.
Configure the compiler:
sudo alternatives --config javac
Verify:
java -version
javac -version

Step 4: Add the Jenkins Repository
Import the Jenkins repository key:
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
Create the repository:
sudo curl -o /etc/yum.repos.d/jenkins.repo \
https://pkg.jenkins.io/redhat-stable/jenkins.repo

Step 5: Install Jenkins
sudo dnf install jenkins -y
Check the version:
jenkins --version

Step 6: Enable Jenkins
sudo systemctl enable jenkins

Step 7: Start Jenkins
sudo systemctl start jenkins
Check status:
sudo systemctl status jenkins
Expected:
Active: active (running)

Step 8: If Jenkins Doesn't Start
View logs:
sudo journalctl -u jenkins -n 100 --no-pager
Common Error 1
Running with Java 17
Supported Java versions are: 21,25
Solution
Install Java 21 and make it the default.

Common Error 2
Address already in use
Check what's using port 8080:
sudo ss -tulpn | grep :8080
Example:
docker-proxy
This means another application (such as Docker/Nginx) is already using port 8080.

Step 9: Change Jenkins Port (Example: 8081)
Create a systemd override:
sudo mkdir -p /etc/systemd/system/jenkins.service.d
Create the override file:
sudo tee /etc/systemd/system/jenkins.service.d/override.conf >/dev/null <<EOF
[Service]
Environment="JENKINS_PORT=8081"
EOF
Reload systemd:
sudo systemctl daemon-reload
Restart Jenkins:
sudo systemctl restart jenkins
Verify:
sudo systemctl status jenkins
Expected:
Active: active (running)

Step 10: Check the Listening Port
sudo ss -tulpn | grep 8081
Expected:
java LISTEN 0.0.0.0:8081

Step 11: Open Jenkins
Open your browser:
http://<server-ip>:8081
or
http://localhost:8081

Step 12: Get the Initial Admin Password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
Copy the password.

Step 13: Unlock Jenkins
Paste the password into the Jenkins web page and click Continue.

Step 14: Install Plugins
Click:
Install suggested plugins
Jenkins downloads and installs the recommended plugins.

Step 15: Create the First Admin User
Fill in:
Username
Password
Confirm Password
Full Name
Email
Click Save and Continue.

Step 16: Configure the Jenkins URL
Example:
http://localhost:8081/
or
http://<server-ip>:8081/
Click Save and Finish.

Step 17: Start Using Jenkins
Click:
Start using Jenkins
You will see the Jenkins Dashboard.

Step 18: Verify the Installation
Dashboard:
Dashboard
├── New Item
├── Build History
├── Manage Jenkins
├── Nodes
└── Credentials

Jenkins Installation Flow
Install Java 21
       │
       ▼
Add Jenkins Repository
       │
       ▼
Install Jenkins
       │
       ▼
Enable Jenkins Service
       │
       ▼
Start Jenkins
       │
       ▼
Fix Java Version (if needed)
       │
       ▼
Fix Port Conflict (if needed)
       │
       ▼
Open Browser
       │
       ▼
Unlock Jenkins
       │
       ▼
Install Suggested Plugins
       │
       ▼
Create Admin User
       │
       ▼
Configure Jenkins URL
       │
       ▼
Jenkins Dashboard Ready















                  GitHub
                     │
              git push main
                     │
                     ▼
                Jenkins Server
                     │
        ┌────────────┼─────────────┐
        │            │                                                     │
        ▼            ▼                                                  ▼
   Checkout      Docker                              Build   Docker Login
        │            │                                                      
        └────────────┼─────────────┘
                     ▼
             Push Docker Image
                     │
                     ▼
               Docker Hub
                     │
                     ▼
             Kubernetes Cluster
                     │
                     ▼
             Student App Updated


