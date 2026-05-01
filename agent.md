# Diretrizes do Agente IA (Antigravity)

Ao trabalhar neste projeto (ConfereAI), você (a IA) DEVE obrigatoriamente referenciar e seguir as diretrizes/metodologias listadas na pasta `superpowers/skills` conforme o contexto da tarefa em mãos.

Sempre que o Humano solicitar uma alteração ou criação, verifique qual skill se aplica e aja rigorosamente de acordo com ela:

## 1. Regra Geral de Inicialização
- NUNCA comece a escrever código ou desenhar componentes para uma nova feature sem antes consultar e executar o processo iterativo definido em `superpowers/skills/brainstorming/SKILL.md`. O Humano deve aprovar a ideia antes do código nascer.

## 2. Para Tarefas de Machine Learning (Motor)
- A precisão matemática é inegociável. Para qualquer script de processamento de dados, manipulação de tensores ou modelo em si, leia e aplique OBRIGATORIAMENTE o fluxo de `superpowers/skills/test-driven-development/SKILL.md`.
- Se o Humano relatar anomalias no treinamento (loss não cai, acurácia baixa) ou na inferência, NÃO altere nada sem antes invocar o `superpowers/skills/systematic-debugging/SKILL.md` para isolar a causa-raiz cientificamente.
- Quando uma etapa crucial do modelo for finalizada, exija as provas estabelecidas em `superpowers/skills/verification-before-completion/SKILL.md`.

## 3. Para Tarefas de Frontend (Dashboard UI/UX)
- Antes de alterar layouts, reescrever CSS ou criar novos componentes globais, execute os passos em `superpowers/skills/writing-plans/SKILL.md`. Mostre o plano (passo a passo de 2 a 5 minutos) ao Humano e espere aprovação.
- Se a refatoração for de alto impacto, siga o `superpowers/skills/using-git-worktrees/SKILL.md` para criar um ambiente isolado de testes que proteja o dashboard atual.
- Para manter a harmonia do Design System, crie o hábito de acionar o `superpowers/skills/requesting-code-review/SKILL.md` ao final de cada etapa visual, passando a bola para o Humano aprovar a usabilidade.

---
**Nota para o Agente:** Este arquivo é a sua espinha dorsal neste repositório. Confie nas metodologias do diretório *superpowers/skills* em detrimento de abordagens mais fáceis e desestruturadas.
