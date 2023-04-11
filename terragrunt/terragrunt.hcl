generate "provider" {
    path      = "master_provider.tf"
    if_exists = "overwrite_terragrunt"
    contents  = <<EOF
    provider "helm" {
    kubernetes {
        config_path = "~/.kube/config"
    }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}
EOF
}


terraform {
    source = "/home/ion/facultate_ip/terraform-modules//backend"
}

inputs = {
    chart_name = "mysql-ip"
    helm_chart_version = "9.7.1"
    mysql = {
        username = "test"
        password = "testulescu"
    }
}