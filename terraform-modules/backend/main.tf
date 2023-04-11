resource "kubernetes_namespace" "mysql-namespace" {
  metadata {
    name = "mysql"
  }
}

resource "kubernetes_persistent_volume" "mysql-pv" {
   metadata {
    name = "data-mysql"
  }
  spec {
    capacity = {
      storage = "8Gi"
    }
    access_modes = ["ReadWriteOnce"]
    persistent_volume_source {
      host_path {
        path = "/home/ion/facultate_ip/data_mysql"
        type = "DirectoryOrCreate"
      }
    }
  }
}

resource "helm_release" "mysql-chart" {
  name                = var.chart_name
  namespace           = kubernetes_namespace.mysql-namespace.metadata.0.name
  repository          = "https://charts.bitnami.com/bitnami"
  chart               = "mysql"
  version             = var.helm_chart_version
  timeout             = 600

  depends_on = [
    kubernetes_namespace.mysql-namespace
  ]

  values = [
    yamlencode({
        auth = {
            database = "ip"
            username = var.mysql.username
            password = var.mysql.password
        }
    })
  ]
}