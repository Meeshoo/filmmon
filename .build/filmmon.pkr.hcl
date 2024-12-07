source "docker" "debian" {
  image = "debian"
  commit = true
  changes = [
    "WORKDIR /filmmon",
    "CMD [\"main.py\"]",
    "ENTRYPOINT [\"python3\"]"
  ]
}

build {
  sources = ["source.docker.debian"]

  provisioner "shell" {
    inline = ["apt update; apt-get install -y python3 chromium-browser"]
  }

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
