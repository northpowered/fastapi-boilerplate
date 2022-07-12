ui = true

log_level = "trace"

api_addr = "http://127.0.0.1:8200"

disable_mlock = true

storage "file" {
    path = "/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}