## 🌿 Estrutura de branches

```plaintext
main                → branch principal, estável, pronta para entrega/apresentação
│
├── dev             → branch de desenvolvimento integrando o que cada um faz
│   ├── gui/xxx     → branches temporárias para features específicas da interface
│   ├── core/xxx    → branches temporárias para lógica de Tomasulo
│   ├── tests/xxx   → testes e métricas
│   └── refactor/xx → refatorações de código
```

---

## 📌 Descrição das branches

| Branch       | Função                                                                          |
| ------------ | --------------------------------------------------------------------------------|
| `main`       | Apenas código **testado e estável**. A ser entregue. Nada quebra aqui.          |
| `dev`        | Integração dos membors. Cada um trabalha em features separadas e dá merge aqui. |
| `core/*`     | Lógica do Tomasulo (ex: `core/rob`, `core/reservation-station`)                 |
| `gui/*`      | Interface gráfica (ex: `gui/layout`, `gui/table-rob`, `gui/step-mode`)          |
| `tests/*`    | Testes ou métricas                                                              |
| `refactor/*` | Mudanças na estrutura sem novas funcionalidades                                 |

---

## 👥 Fluxo de trabalho

1. **Cada membro cria branches específicas** a partir de `dev`:

   ```bash
   git checkout dev
   git checkout -b core/rob
   ```

2. **Trabalha e commita normalmente** na branch.

3. Quando terminar a funcionalidade (ex: `core/rob`), abre um **pull request (PR) para `dev`**:

   * Um revisa o código do outro.
   * Se tudo estiver ok: merge.
   * Pode usar labels no PR: `feat`, `bug`, `refactor`, `ready`, `in review`.

4. Periodicamente (ou quando for apresentar), **merge do `dev` para `main`**:

   ```bash
   git checkout main
   git merge dev
   git tag v1.0
   ```

---

## ✅ Exemplo prático

```plaintext
Colega 1:
├── core/instruction-decoder
├── core/reservation-station
└── gui/layout-mock

Colega 2:
├── core/rob
├── core/branch-prediction
└── gui/step-controller

→ Ambos fazem merge para `dev`, testam juntos → Merge final para `main`
```

---

## 🧠 Dicas extras

* **Commits pequenos e frequentes** são melhores que commits gigantes.
* **Padrão de commit** (ex: Conventional Commits):

  * `feat:` nova funcionalidade
  * `fix:` correção de bug
  * `refactor:` melhoria sem mudar funcionalidade
  * `docs:` mudanças no README
* Use o nosso Quadro Kanban no Notion para organizar as tarefas.
