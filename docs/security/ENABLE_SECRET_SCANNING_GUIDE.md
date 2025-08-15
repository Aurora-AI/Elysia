# Guia: Como ativar Secret Scanning no GitHub

Este guia mostra os passos para ativar o Secret Scanning no repositório `Aurora-AI/Aurora-Plataform`.

1. Abra o repositório no GitHub: https://github.com/Aurora-AI/Aurora-Plataform
2. Clique em **Settings** (repositório) na barra superior.
3. No menu lateral, abra **Code security and analysis**.
4. Na secção **GitHub Advanced Security**, localize **Secret scanning**.
5. Clique em **Enable** para ativar a verificação automática de segredos.
6. (Opcional) Configure **push protection** para bloquear pushes que contenham segredos.
7. Verifique as entradas em **Security → Secret scanning** e revoke quaisquer tokens expostos.

Observações operacionais:
- Confirme com a equipa que todas as credenciais detectadas foram rotacionadas antes de forçar reescrita de histórico.
- Para remover segredos do histórico, use `git-filter-repo` em conjunto com uma política de coordenação de equipe.

