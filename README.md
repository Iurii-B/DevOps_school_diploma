## Diploma project for EPAM DevOps Internship #20

A light-weight Python/Flask application with MariaDB database.
It requests Covid19 world-wide statistics via API (https://covidtracker.bsg.ox.ac.uk/about-api), stores it in the database and presents to the user.

CI/CD pipeline and IaC approach are implemented. 

Tools/components used:
 * application - Python + Flask + SQLAlchemy
 * compute - AWS/EC2 instances as Kubernetes worker nodes
 * containers - Docker
 * orchestration - AWS/EKS Kubernetes
 * database - AWS/RDS MariaDB
 * IaC - Terraform
 * CI/CD - GitHub Actions
 * container registry / artifact storage - AWS/ECR
 * logging and monitoring - AWS/CloudWatch and AWS/Route53
 * code quality gate - SonarCloud

Terraform manifests are located in a separate repository: https://github.com/Iurii-B/DevOps_school_diploma_infra

The only component created manually prior to all other steps is AWS ECR.

After running ```terraform apply``` the whole infrastructure is created and the initial version of the application (**:init** tag) is deployed.
Please be patient and give some time to provision all components and populate the database.