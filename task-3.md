# Utilizando o GitLab como sistema de controle de versão

Resumo para simular cenários de conflitos e aprender a resolvê-los com `git merge` e `git rebase`.

## 1. Trabalhando com TAGs

No terminal, navegue até o diretório do repositório local:
```bash
cd /home/$USER/my-golang-app/
```

Crie uma tag inicial chamada `v1.0`.
```bash
git tag v1.0
```

Podemos verificar se está tudo corretamente usando:
```bash
git tag
```

Faça uma alteração em um arquivo existente. Por exemplo, adicione uma nova linha ao arquivo ReadMe.
```bash
echo "Esta é uma nova alteração" >> ReadMe
```

Salve as alterações em um commit:
```bash
git add ReadMe
git commit -m "Adicionando nova alteração"
```

## 2. Alternando entre TAGs

Crie uma nova tag chamada `v1.1`:
```bash
git tag v1.1
```

E verifique se foi criada corretamente:
```bash
git tag
```

Agora, tente voltar para a versão `v1.0` do seu código:
```bash
git checkout v1.0
```

Para voltar a versão atual do código use:
```bash
git checkout v1.1
```

## 3. Resolvendo conflitos com o comando merge

Se você não estiver no repositório local, use:
```bash
cd /home/$USER/my-golang-app/
```

Crie uma nova branch chamada `feature`.
```bash	
git checkout -b feature
```

Adicione uma nova linha ao arquivo ReadMe.
```bash
echo "Esta é uma nova feature" >> ReadMe
```

Faça um commit das alterações:
```bash
git add ReadMe
git commit -m "Adicionando nova feature"
```

Volte para a master usando:
```bash
git checkout master
```

Façamos uma alteração no mesmo arquivo que foi modificado na branch `feature`, criando assim um conflito.
```bash
echo "Esta é uma alteração na master" >> ReadMe
```

Salve em um commit:
```bash
git add ReadMe
git commit -m "Adicionando alteração na master"
```

Agora, experimente fazer o merge da branch `feature` na `master`:
```bash
git merge feature
```

Se tudo foi seguido corretamente, aparecerá uma mensagem de erro indicando que existe um conflito. Abra o arquivo ReadMe:
```bash
cat ReadMe
```

Teremos algo do tipo:
```bash
<<<<<< HEAD
Esta é uma alteração na master
======
Esta é uma nova feature
>>>>>> feature
```

Para resolvermos isso, basta editar o arquivo para ficar apenas com as informações geradas previamente:
```bash
nano ReadMe
```

```bash
Esta é uma nova alteração
Esta é uma alteração na master
Esta é uma nova feature
```

Por fim, faça um commit das alterações:
```bash
git add ReadMe
git commit -m "Resolução de conflito de merge"
```

## 4. Conflito com rebase

Vamos criar uma nova branch chamada `feature2` a partir da `master`:
```bash	
git checkout -b feature2
```

Criamos uma alteração em um arquivo existente:
```bash
echo "Esta é uma nova feature com o nome feature2" >> ReadMe
```

Restando apenas criar um commit das alterações:
```bash
git add ReadMe
git commit -m "Adicionando nova feature através da branch feature2"
```

Volte a `master`:
```bash
git checkout master
```

E adicione a seguinte linha ao arquivo ReadMe:
```bash
echo "Esta é a segunda alteração na master" >> ReadMe
```

Por fim, realizamos um commit das alterações:
```bash
git add ReadMe
git commit -m "Adicionando a segunda alteração da master"
```

Pronto. Agora tente fazer o rebase da branch `master` na `feature2`:
```bash	
git checkout feature2
git rebase master
```

Obtém-se uma mensagem de erro indicando um conflito. No arquivo, resolva editando o arquivo da seguinte maneira:
```bash
Esta é uma segunda alteração na master
Esta é uma nova feature2
```

E adicione o arquivo ao staging area e continue o rebase:
```bash
git add ReadMe
git rebase --continue
```

__TIPS:__
- _para salvar e sair do nano, pressione `Ctrl + X`, digite `Y` e pressione `enter`._
- _se tiver problemas com o rebase,_
    - _use `git rebase --abort` para cancelar o rebase e tente novamente._
    - _use `git rebase -skip` para pular o commit que está causando conflito e continuar o rebase._
    - _use `git rebase --edit-todo` para abrir o arquivo de rebase-todo e editar manualmente o rebase._

Por fim, salve o estado da seguinte forma:
```bash
git add ReadMe
git commit -m "Resolução de conflito via reabase"
```

## 5. Resolução de conflitos com stash

No repositório local usado, crie uma nova branch chamada `feature3`:
```bash
cd /home/$USER/my-golang-app/
git checkout -b feature3
```

Faça uma alteração no arquivo ReadMe:
```bash
echo "Está é uma nova feature3
```

E mude para a `master`:
```bash
git checkout master
```

Com esses passos, receberemos uma mensagem de erro indicando que temos que salvar as alterações não salvas que serão sobrescritas pela mudança de branch.

Use o comando `git stash` para salvar temporariamente as alterações e limpar o diretório de trabalho.

Agora é possível alternar para a branch `master`.

Façamos uma nova alteração no arquivo ReadMe, agora via branch `master`, criando assim um conflito.
```bash
echo "Esta é uma terceira alteração pela master" >> ReadMe
```

Faça o commit das alterações e volte para a branch `feature3`.
```bash
git add ReadMe
git commit -m "Adicionando a terceira alteração na master"
git checkout feature3
```

Agora na branch `feature3`, use o commando `git stash pop`. Encontramos um conflito para resolver. Edite o arquivo conforme desejar, por exemplo:
```bash
Esta é uma terceira alteração na master
Esta é uma nova feature3
```

Faça um commit das alterações da seguinte forma:
```bash
git add ReadMe
git commit -m "Resolvendo conflitos via stash"
git push
```

Através desses passos, você tem uma boa compreensão dos principais recursos de controle de versão que são utilizados tornando mais eficiente gerenciar o código em um ambiente de desenvolvimento.
