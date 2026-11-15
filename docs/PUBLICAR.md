# Publicar no GitHub

1. Entre em https://github.com/new e crie um repositório público chamado `beleza-exemplo`. Não marque a criação automática de README, licença ou .gitignore.
2. Extraia a pasta `beleza-exemplo` do ZIP. O arquivo contém também a pasta oculta `.git`, com histórico local de commits reais do projeto.
3. Instale o Git se necessário. No PowerShell, entre na pasta extraída.
4. Confira o histórico: `git log --oneline`.
5. Configure o endereço remoto (substitua SEU-USUARIO pelo seu usuário do GitHub):

```powershell
git remote add origin https://github.com/SEU-USUARIO/beleza-exemplo.git
git push -u origin main
```

6. Autentique sua conta quando solicitado. Após o envio, abra o repositório e confirme que aparece como Public. A aba Actions mostra a execução dos testes.
7. Cole o endereço real do repositório no campo da faculdade, por exemplo `https://github.com/SEU-USUARIO/beleza-exemplo`.

Caso prefira o envio de arquivos pelo navegador, use Add file → Upload files, mantendo a estrutura de pastas. Essa alternativa não preserva o histórico original de commits; prefira o procedimento acima.

O repositório contém código e documentação, não é um site hospedado. Para apresentar o MVP, execute-o localmente conforme o README.
