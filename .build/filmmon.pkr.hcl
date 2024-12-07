source "docker" "selenium" {
  image = "selenium/standalone-chrome:129.0"
  commit = true
  privileged = true
  changes = [
    "WORKDIR /filmmon",
    "CMD [\"main.py\"]",
    "ENTRYPOINT [\"python3\"]"
  ]
}

build {
  sources = ["source.docker.selenium"]

  provisioner "shell" {
    inline = ["mkdir /filmmon"]
  }

  provisioner "file" {
    source = "../"
    destination = "/filmmon"
  }

  provisioner "shell" {
    inline = ["pip install -r /filmmon/requirements.txt"]
  }

  post-processors {
    post-processor "docker-tag" {
      repository = "550661752655.dkr.ecr.eu-west-1.amazonaws.com/filmmon"
      tags       = ["latest"]
    }

    post-processor "docker-push" {
      ecr_login = true
      login_server = "https://550661752655.dkr.ecr.eu-west-1.amazonaws.com/mitlan"
    }
  }
}
