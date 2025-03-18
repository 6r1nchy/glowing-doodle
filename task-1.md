# Configuração do ambiente de trabalho com GitLab

## 1. Instalação do Docker e GitLab em uma VM Ubuntu

Instalação do GitLab com Docker:
```bash
sudo docker network create gitlab
```

Executando o container:
```bash
sudo docker run --detach \
  --hostname gitlab.example.com \
  --publish 80:80 \
  --publish 443:443 \
  --publish 9022:22 \
  --name gitlab \
  --restart always \
  --network gitlab \
  --volume /srv/gitlab/config:/etc/gitlab \
  --volume /srv/gitlab/logs:/var/log/gitlab \
  --volume /srv/gitlab/data:/var/opt/gitlab \
  gitlab/gitlab-ce:16.9.6-ce.0
```

Pode ser verificado através do comando `docker ps`.

Obtendo senha de user root, préviamente definida:
```bash
sudo docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
```

Para trocar a senha inicial, use:
```bash
sudo docker exec -it gitlab gitlab-rake "gitlab:password:reset"
```

→ Após o comando, será necessário inserir o usuário e senha para reset.

## 2. Criaçãoo e importação de uma aplicação golang no gitlab

Criando uma aplicação golang e acessando o diretório:
```bash
mkdir /home/aluno/my-golang-app
cd my-golang-app
```

Crie um novo arquivo chamado `main.go` e edite com `nano main.go`.

Adicione o seguinte código ao arquivo `main.go`:
```go
package main

import (
  "fmt"
  "net/http"
  "os"
)

func main() {
  greeting := os.Getenv("MESSAGE")
  if greeting == "" {
      greeting = "Hello, World!"
  }

  http.HandleFunc("/", handler(greeting))

  port := os.Getenv("PORT")
  if port == "" {
      port = "8080"
  }

  fmt.Printf("Listening on port %s...\n", port)
  http.ListenAndServe(":"+port, nil)
}

// Handler function to allow testing
func handler(greeting string) http.HandlerFunc {
  return func(w http.ResponseWriter, r *http.Request) {
     fmt.Fprintf(w, "%s\n", greeting)
  }
}
```

Na interface gráfica do GitLab, crie o repositório que irá receber a aplicação.

No diretório da aplicação local, inicialize um novo repositório git:
```bash
git config --global user.name "Seu nome"
git config --global user.email "Seu email"
git init --initial-branch=master
```

Adicione todos os arquivos e faça um commit inicial:
```bash
git add .
git commit -m "Initial commit"
```

Importando a aplicação para o GitLab, na máquina virtual, adicione a url do GitLab como `origin`:
```bash
git remote add origin http://192.168.98.10/root/my-golang-app.git
```

Empure o commit inicial para o GitLab:
```bash
git push -u origin master
```

Por fim, digite o user e a senha anteriormente configurada.

## 3. Criação e gerenciamento de grupos e usuários no GitLab via linha de comando

Para realizar os próximos passos, é preciso um token de acesso pessoal do GitLab com permissões apropriadas. Deve-se gerar um token na interface de usuário do GitLab em "Settigins > Access Tokens".

Para criar um grupo, chamado "DevOps Team", por meio de linha de comando digite:
```bash
curl --request POST --header "PRIVATE-TOKEN: <<your_access_token>>" --data "name=DevOps Team&path=devops-team" "http://192.168.98.10/api/v4/groups"
```

Para criar usuários, por exemplo, faça da seguinte forma:
```bash
curl --request POST --header "PRIVATE-TOKEN: <<your_access_token>>" --data "email=user1@example.com&password=securepassword&username=user1&name=User1" "http://192.168.98.10/api/v4/users"

curl --request POST --header "PRIVATE-TOKEN: <<your_access_token>>" --data "email=user2@example.com&password=securepassword&username=user2&name=User2" "http://192.168.98.10/api/v4/users"

curl --request POST --header "PRIVATE-TOKEN: <<your_access_token>>" --data "email=user3@example.com&password=securepassword&username=user3&name=User3" "http://192.168.98.10/api/v4/users"
```

Para adicionar usuários a um grupo, é preciso obter o ID do usuário desejado:
```bash
curl --request GET --header "PRIVATE-TOKEN: <<your_access_token>>" "http://192.168.98.10/api/v4/users?username=user1"
```

Por fim, execute o seguinte comando para adicionar o usuário ao grupo anteriormente criado:
```bash
curl --request POST --header "PRIVATE-TOKEN: <<your_access_token>>" --data "user_id=<user_id>&access_level=30" "http://192.168.98.10/api/v4/groups/devops-team/members"
```

## Resumo da atividade prática proposta
- Instalação do GitLab
- Criação e importação de uma aplicação golang no GitLab.
- Criação e gerenciamento de grupos e usuários no GitLab via linha de comando.