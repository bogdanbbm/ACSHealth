variable "chart_name" {
  type = string
  default = "mysql"
  description = "chart name"
}

variable "helm_chart_version" {
  type = string
  description = "version of mysql chart"
}

variable "mysql" {
  type = object({
    username = string
    password = string
  })
  description = "mysql connection details"
}