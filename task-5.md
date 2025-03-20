# Criação e Execução de Testes Unitários e Automatizados

O objetivo desta atividade proposta é criar e executar testes unutários em uma aplicação GO, integrando-os em uma pipeline de CI/CD no GitLab.

## Pré-requisitos

- Uma instância local do GitLab rodano em uma VM (Ubuntu) com containers.
- Um projeto GitLab configurado com um arquivo `gitlab-cli.yml` válido.
- Conhecimento básico de linguagem de programação.

## 1. Configurando o SonarQube

**OBS:** utilizando uma instância disponibilizada previamente.

Abra o navegador e acesse a interface web do SonarQube em `http://192.168.98.10:9000`. Você verá a página de login do SonarQube.

Utilize as seguintes credenciais para fazer login.

Após fazer login, navegue até a aba "Administration" no canto superior direito da página. Em seguida, clique em "Projects" e depois em "Management". Clique no botão "Create Project". Após clicar em "Create Project", você verá uma página para adicionar um novo projeto.

![Configuração do projeto.](/image-t5-1.avif)

**OBS:** preencha os campos conforme consta na imagem disponibilizada e clique em "Next".

Após criar o projeto, você verá uma tela para selecionar o baseline. Selecione a opção "Use the global setting" e clique em "Create Project".

Após criar o projeto, você verá uma tela para selecionar a forma de análise do código. Selecione a opção "Locally" e clique em "Continue".

Em seguida você verá uma página com um botão para gerar um token de acesso "Generate".

Clique nele e copie o token e guarde-o em um local seguro. Você precisará dele para configurar a análise de código no GitLab, em seguida clique em "Continue".

Na próxima tela, você verá as instruções para configurar a análise de código.

## 2. Integrando o SonarQube com o GitLab

Crie um novo arquivo chamado `sonar-project.properties` no diretório `my-golang-app`:
```bash
nano sonar-project.properties
```

e adicione o seguinte código:
```properties
sonar.projectKey=my-golang-app
sonar.projectName=my-golang-app
sonar.projectVersion=1.0
sonar.sources=.
sonar.exclusions=**/*_test.go
sonar.tests=.
sonar.test.inclusions=**/*_test.go
sonar.go.coverage.reportPaths=coverage.out
sonar.host.url=http://192.168.98.10:9000
sonar.token=<Insira o token gerado no SonarQube>
```

Salve o arquivo, saia do editor e faça um commit da alteração:
```bash
git add .
git commit -m "Added SonarQube configuration file"
```

Abra o arquivo `.gitlab-ci.yml` no diretório editor de texto do GitLab.
```bash
nano .gitlab-ci.yml
```

Adicione um novo estágio de teste para a análise estática do código. Este estágio deve estar logo após o estágio "test_job". Nomeie o trabalho como `code_analysis`.
```yml
code_analysis:
    stage: test2
    image: sonarsource/sonar-scanner-cli:latest
    dependencies:
        - test_job
    script:
        - echo "Verificando artefatos do test_job"
        - pwd 
        - ls -la 
        - cat coverage.out
        - if [ -f coverage.out ]; then cat coverage.out; else echo "coverage.out não encontrado"; fi
        - sonar-scanner -D sonar.go.coverage.reportPaths=coverage.out
```

Salve as anterações no arquivo, saia do editor, faça um commit da alteração e empure para o repositório remoto.
```bash
git add .
git commit -m "Added code analysis job"
git push origin master
```

Verifique se o trabalho de análise de código foi adicionado com sucesso ao pipeline no GitLab.

## 3. Criando o arquivo de testes

Crie um novo arquivo chamado `main_test.go` com o nano e adicione o seguinte código:
```go
package main

import (
    "net/http"
    "net/http/httptest"
    "os"
    "testing"
    "time"  // Adicionado para usar funções do pacote time
)

func TestMainHandler(t *testing.T) {
    greeting := "Test Message"
    req := httptest.NewRequest("GET", "/", nil)
    w := httptest.NewRecorder()
    handler(greeting).ServeHTTP(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("Expected status OK but got %v", w.Code)
    }

    if w.Body.String() != greeting+"\n" {
        t.Errorf("Expected body %s but got %s", greeting+"\n", w.Body.String())
    }
}

func TestHandlerWithEnvVars(t *testing.T) {
    // Teste com variável de ambiente MESSAGE definida
    os.Setenv("MESSAGE", "Olá, Mundo!")
    defer os.Unsetenv("MESSAGE") // Limpa a variável de ambiente após o teste

    req := httptest.NewRequest("GET", "/", nil)
    w := httptest.NewRecorder()
    handler(os.Getenv("MESSAGE")).ServeHTTP(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("Expected status OK but got %v", w.Code)
    }

    if w.Body.String() != "Olá, Mundo!\n" {
        t.Errorf("Expected body 'Olá, Mundo!' but got %s", w.Body.String())
    }
}

func TestHandlerWithDefaultMessage(t *testing.T) {
    // Teste sem variável de ambiente MESSAGE definida
    os.Unsetenv("MESSAGE")

    req := httptest.NewRequest("GET", "/", nil)
    w := httptest.NewRecorder()
    handler("Mensagem Padrão!!").ServeHTTP(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("Expected status OK but got %v", w.Code)
    }

    if w.Body.String() != "Mensagem Padrão!!\n" {
        t.Errorf("Expected body 'Mensagem Padrão!!' but got %s", w.Body.String())
    }
}

func TestServerInitialization(t *testing.T) {
    os.Setenv("PORT", "9090")
    defer os.Unsetenv("PORT") // Limpa a variável de ambiente após o teste

    // Inicia o servidor em uma goroutine
    go func() {
        main()
    }()

    // Dá um tempo para o servidor inicializar
    tchan := make(chan bool)
    go func() {
        http.Get("http://localhost:9090/")
        tchan <- true
    }()
    select {
    case <-tchan:
        // Servidor iniciou corretamente
    case <-time.After(3 * time.Second):  // Corrigido para usar time.After e time.Second
        t.Fatal("Expected server to start but timed out")
    }
}
```

Salve as anterações no arquivo, saia do editor, faça um commit da alteração e empure para o repositório remoto.
```bash
git add .
git commit -m "Added test file"
git push origin master
```

## 4. Explorando o Pipeline do Gitlab

1. Por meio do navegador acesse a sua instância local do GitLab e navegue até o seu projeto.
2. No menu à esquerda, clique em "Build" e depois em "Pipelines". Aqui, você pode ver o status de todas as suas pipelines.
3. Clique na pipeline referente ao teste para ver mais detalhes. Você pode ver o status de cada job na pipeline, bem como informações sobre quando a pipeline foi criada e quanto tempo levou para ser executada.
4. Ainda na página de detalhes da pipeline, clique em um job para ver os seus detalhes.
5. Aqui, você pode ver os logs do job. Isso pode ser útil para depurar problemas se um job falhar.

## 5. Explorando o SonarQube

1. Abra o navegador e acesse a interface web do SonarQube
2. Navegue até o seu projeto.
3. Aqui, você pode ver informações sobre a qualidade do código, incluindo métricas como cobertura de código, complexidade, duplicação de código e muito mais.
![SonarQube Overview](/image-t5-2.avif)

4. Navegue até a aba Security Hotspots para ver informações sobre possíveis vulnerabilidades de segurança no código.
![SonarQube Security Hotspots](/image-t5-3.avif)

5. Navegue até a aba Measures para ver informações sobre métricas de qualidade do código.
![SonarQube Measures](/image-t5-4.avif)

## Resumo

O contexto de testes no conceito DevOps, resume-se aos seguintes passos:

- **Configuração do SonarQube:** configurar o SonarQube para análise de código estática.
- **Integração GitLab Local com SonarQube:** integrar o GitLab local com o SonarQube para análise de código.
- **Criação de Arquivo de Teste e Integração com o GitLab:** criar um arquivo de teste para um aplicativo em Go e o integraram com o GitLab.
- **Exploração do Pipeline do GitLab:** explorar o pipeline do GitLab para ver o status de suas pipelines e jobs.
- **Exploração do SonarQube:** explorar o SonarQube para ver informações sobre a qualidade do código e possíveis vulnerabilidades de segurança.