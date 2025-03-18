# Operação do ambiente de trabalho com GitLab

Como pré-requisito, o GitLab deve estar instaladolocalmente.

## 1. Acessando o repositório e verificando o status

Os seguintes comandos são mais utilizados:
```bash
git status  # Verifica o status do repositório.
git log     # Verifica o histórico de commits.
git log --oneline # Verifica o histórico de forma simplificada.
git log --graph   # Mostra de maneira gráfica o histórico de commits.
git log --oneline --graph --all # verifica o histórico de forma simplificada e gráfica.
```

## 2. Definindo permissões de acesso

Objetivo é usar a API através da linha de comando usando o `curl`. É necessário ter ou gerar um token de acesso.

- __WARNING:__ _Quaisquer alterações em comandos, digitados de forma equivocada, pode causar um erro do tipo '403 Forbidden'._

Use o seguinte comando para listar os usuários existentes:
```bash
curl --header "PRIVATE-TOKEN: <your_access_token>" "http://192.168.98.10/api/v4/users"
```

Definindo como admnistrador um usuário associado a um ID.
```bash
curl --request PUT --header "PRIVATE-TOKEN: <your_access_token>" "http://192.168.98.10/api/v4/users/user_id" --data "admin=true"
```

## 3. Fluxo básico de trabalho

1. Crie um novo arquivo com o nome "ReadMe".
2. Adicione o arquivo ao repositório
3. Faça um commit com a mensagem "InicioProjeto".
4. Verifique o status do repositório.
5. Verifique o histórico de commits.
6. Faça algumas alterações no arquivo "ReadMe".
7. Verifique as alterações feitas no arquivo "ReadMe".
8. Adicione as alterações ao repositório.
9. Faça um commit com a mensagem "Alterado ReadMe".
10. Verifique o status do repositório.
11. Verifique o histórico de commits.
12. Faça o push das alterações para o repositório remoto.
13. Verifique o status do repositório.
14. Ajuste a URL do repositório remoto para a URL do seu repositório GitLab.

## 4. Operações com branches

1. Crie uma nova branch.
2. Mude para a nova branch.
3. Faça algumas alterações no repositório.
4. Adicione as alterações ao repositório.
5. Faça um commit.
6. Mude de volta para a branch principal.
7. Faça um merge da branch secundária na branch principal.
8. Faça o push das alterações para o repositório remoto.
9. Verifique o status do repositório.
10. Verifique o histórico de commits de forma simplificada e com gráfico.

## 5. Trabalhando com issues

A gestão de issues é feita via GUI do GitLab na página do projeto.