# Criação e configuração de pipelines no GitLab

## Pré-requisitos

- Conta no GitLab
- Projeto de exemplo no Gitlab
- Conhecimento básico de Git e CI/CD

## 1. Preparação do Ambiente

Crie um driteório chamado `gitlab-runner` no caminho `/home/aluno`:
```bash
mkdir /home/aluno/gitlab-runner
```

Navegue até o diretório criado e crie um arquivo `docker-compose.yml` para implantar o `gitlab-runner`:
```bash
nano docker-compose.yml
```

Adicione o seguinte conteúo:
```bash
version: '3.8'

services:
  gitlab-runner1:
    image: gitlab/gitlab-runner:alpine
    restart: always
    container_name: gitlab-runner1
    hostname: gitlab-runner1
    volumes:
      - ./config/gitlab-runner:/etc/gitlab-runner
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      gitlab-network: 
        aliases:
          - gitlab-runner1

networks:
  gitlab-network:
    external: 
      name: gitlab
```

Salve as alterações no arquivo e saia do editor.
- __TIP:__ `Ctrl + X` e `Enter`.

Execute o comando para subir o container do `gitlab-runner`:
```bash
docker-compose up -d
```

Agora, você precisa´ra do token de registro o `gitlab-runner` no GitLab. Para obter o token de registro, as etapas são:
- Acesse o Gitlab e vá para o projeto `gitlab-runner`.
- No menu à esquerda, clique em "Settings" e depois em "CI/CD".
- Role para baixo até a seção "Runners" e copie o token de registro.
- O token de registro será necessário para registrar o runner no Gitlab.
- Anote o token de registro para uso posterior.

Uma vez implantado o `gitlab-runner`, vamos criar um script para registar o runner no GitLab chamado `gitlab-runner-register.sh`:
```bash
nano gitlab-runner-register.sh
```

E adicione o seguinte conteúdo:
```bash
#!/bin/sh
# Token e Registro
registration_token="<Insira o token criado no Passo 1.2.e>"
url="http://192.168.98.10"

sudo docker exec -it gitlab-runner1 \
gitlab-runner register \
    --non-interactive \
    --registration-token ${registration_token} \
    --locked=false \
    --description docker-stable \
    --url ${url} \
    --executor docker \
    --docker-image docker:stable \
    --docker-volumes "/var/run/docker.sock:/var/run/docker.sock" \
    --docker-network-mode gitlab
```

Após salvar e sair do editor, execute o script:
```bash
bash gitlab-runner-register.sh
```

## 2. Preparação do Build

Vá até o diretório da aplicação e crie o arquivo `Dockerfile`:
```bash
cd /home/$USER/my-golang-app/
nano Dockerfile
```

E insira o seguinte conteúdo:
```bash
FROM golang:1.22
WORKDIR /app
COPY main.go .
RUN go build -o app main.go
EXPOSE 8081
CMD ["./app"]
```

Garanta que no `main.go` tenha o seguinte conteúdo:
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

Crie o arquivo `go.mod` para gerenciar as dependências do projeto:
```bash
nano go.mod
```

E insira o conteúdo:
```go
module my-golang-app

go 1.19
```

salve as alterações e saia do editor.

## 3. Configuração do Pipeline Básico

Abra o arquivo `.gitlab-ci.yml` no diretório `/home/$USER/my-golang-app/` por meio do editor de texto nano e insira todos os blocos de texto seguintes no mesmo arquivo.
```bash
nano .gitlab-ci.yml
```

Adicione o seguinte conteúdo para definir os estágios do pipeline:
```yml
variables:
  DOCKER_TLS_CERTDIR: "/certs"
  DOCKER_CLIENT_TIMEOUT: 600
  COMPOSE_HTTP_TIMEOUT: 600    
  DOCKER_BUILDKIT: 0
  COMPOSE_DOCKER_CLI_BUILD: 0    

stages:
  - build
  - test1
  - test2
  - deploy
  - notify
```

Defina o trabalho de construção (`build_job`) com o seguinte conteúdo:
```yml
build_job:
   stage: build
   image: docker:20.10.16
   services:
       - docker:20.10.16-dind
   script:
       - docker build -t ex-build-dev:latest .
```

Defina o trabalho de teste (`test_job`) com o seguinte conteúdo:
```yml
test_job:
   stage: test1
   image: golang:1.19
   script:
      - echo "Testing the app"
      - mkdir -p coverage 
      - go test -v -coverprofile=coverage.out -covermode=set ./... 
      - pwd 
      - ls -la coverage 
      - cat coverage.out
   artifacts:
      paths:
         - coverage.out
      expire_in: 1 week
```

Salve as alterações no arquivo e atualize o repositório do GitLab:
```bash
git add .
git commit -m "Adicionado pipeline básico"
git push origin master
```

Por fim, verifique se o pipeline foi criado com sucesso no GitLab.

## 4. Configuração do Deploy

Abra o arquivo `.gitlab-ci.yml` no diretório editor de texto do GitLab:
```bash
nano .gitlab-ci.yml
```

Insira o conteúdo abaixo no arquivo `.gitlab-ci.yml`:
```yml
deploy_job:
    stage: deploy
    image: docker:20.10.16
    services:
        - docker:20.10.16-dind
    before_script:        
        - echo "Remove anterior"
        - PORT_CONTAINERS=$(docker ps --filter "publish=8081" -q)
        - echo $PORT_CONTAINERS
        - if [ -n "$PORT_CONTAINERS" ]; then
            docker stop $PORT_CONTAINERS;
            docker rm $PORT_CONTAINERS;
            sleep 5; 
          fi
    script:
        - echo "Deploying the app"
        - docker run -d -p 8081:8080 ex-build-dev:latest
```

Salve as alterações, saia do editor e adicione ao git através do seguinte commit e empurre para o repositório remoto:
```bash
git add .
git commit -m "Added Deploy job"
git push origin master
```

Verifique se o trabalho de análise de código foi adicionado corretamente no pipeline no GitLab.

## 5. Monitoramento do Pipeline

Na interface gráfica do GitLab:

1. No GitLab, vá para o seu projeto e clique em "Build" no menu à esquerda.
2. Clique na opção "Pipelines" para visualizar o status do seu pipeline.
3. Clique em um dos trabalhos do seu pipeline para ver os registros de execução.
4. Analise os registros de execução para identificar quaisquer problemas ou gargalos.
5. Volte para a visão geral do pipeline e explore as várias opções de visualização e monitoramento disponíveis.

## Resumo

Com essas atividades práticas, utilizando o GitLab como ferramenta central de DevOps, realizou-se:

- **Preparação do Ambiente:** o ambiente foi preparado para a configuração do pipeline. O diretório do projeto foi acessado e o arquivo .gitlab-ci.yml foi criado.
- **Configuração do Pipeline Básico:** o arquivo .gitlab-ci.yml foi configurado para definir os estágios básicos do pipeline: construção, teste e implantação. Cada estágio foi associado a um trabalho específico.
- **Execução de Testes no Pipeline:** o trabalho de teste foi configurado para executar testes automatizados no código. Isso inclui a execução de testes de unidade e a geração de relatórios de cobertura de código.
- **Implantação da Aplicação:** o trabalho de implantação foi configurado para implantar a aplicação em um ambiente de teste. Isso inclui a remoção de versões anteriores e a implantação da versão mais recente da aplicação.
- **Monitoramento do Pipeline:** o pipeline foi monitorado através da interface do GitLab. Os registros de execução foram analisados para identificar problemas ou gargalos.

Essas atividades básicas ajudam a criar um pipeline de CI/CD robusto e eficiente, automatizando o processo de construção, teste e implantação, mantendo a equipe informada sobre o status do pipeline.