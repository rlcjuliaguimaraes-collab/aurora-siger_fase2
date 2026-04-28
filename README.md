# 🚀 MGPEB — Módulo de Gerenciamento de Pouso e Estabilização de Base

> Protótipo desenvolvido para a **missão Aurora Siger** — Atividade Integradora da **Fase 2 | FIAP | 2026**.

Simula, em Python, o sistema responsável por organizar pousos de módulos de uma colônia em Marte, gerenciar informações operacionais e aplicar regras de governança em uma base nascente.

---

## 📋 Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Conteúdos aplicados](#conteúdos-aplicados)
- [Arquitetura do sistema](#arquitetura-do-sistema)
- [Como executar](#como-executar)
- [Estruturas de dados](#estruturas-de-dados)
- [Regras de decisão (lógica booleana)](#regras-de-decisão-lógica-booleana)
- [Algoritmos implementados](#algoritmos-implementados)
- [Modelagem matemática](#modelagem-matemática)
- [Saída esperada](#saída-esperada)
- [Entregáveis](#entregáveis)
- [Equipe](#equipe)
- [Licença](#licença)

---

## Sobre o projeto

O **MGPEB** é um sistema embarcado simulado que coordena o pouso de módulos da colônia Aurora Siger em Marte. Ele recebe módulos em órbita, avalia condições críticas (combustível, sensores, atmosfera, área de pouso) e decide — com base em **lógica booleana** — quais podem pousar com segurança, quais devem aguardar e quais entram em estado de alerta.

O projeto também contempla **modelagem matemática** da geração de energia solar marciana e uma reflexão sobre **governança ESG** em ambientes de fronteira.

## Conteúdos aplicados

- ✅ Portas lógicas e funções booleanas
- ✅ Estruturas avançadas de lógica e programação em Python
- ✅ Estruturas lineares: listas, pilhas e filas
- ✅ Algoritmos clássicos de busca (sequencial e binária) e ordenação (selection e insertion sort)
- ✅ Modelagem de funções aplicadas (modelo senoidal de energia solar)
- ✅ Histórico e evolução da computação
- ✅ Princípios de governança ambiental, social e corporativa (ESG)

## Arquitetura do sistema

\`\`\`
┌─────────────────────────────────────────────────────────┐
│              FILA DE POUSO (deque FIFO)                 │
│  [Habitação] → [Energia] → [Lab] → [Logística] → ...    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │  REGRAS BOOLEANAS DE POUSO   │
        │  (combustível ∧ sensores ∧   │
        │   área_livre ∧ atmosfera)    │
        └──────────────┬───────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ POUSADOS │  │ EM ESPERA│  │ ALERTAS  │
   │  (lista) │  │  (lista) │  │  (lista) │
   └──────────┘  └──────────┘  └──────────┘
                       │
                       ▼
           ┌─────────────────────────┐
           │ PILHA DE EVENTOS (LIFO) │
           │   auditoria / rollback  │
           └─────────────────────────┘
\`\`\`

## Como executar

**Pré-requisitos:** Python 3.8 ou superior. Sem dependências externas.

\`\`\`bash
# Clone o repositório
git clone https://github.com/<seu-usuario>/mgpeb-aurora-siger.git
cd mgpeb-aurora-siger

# Execute o protótipo
python mgpeb.py
\`\`\`

## Estruturas de dados

| Estrutura | Tipo | Função no MGPEB |
|---|---|---|
| \`fila_pouso\` | \`deque\` (Fila / FIFO) | Módulos aguardando autorização |
| \`pousados\` | \`list\` | Módulos que pousaram com sucesso |
| \`em_espera\` | \`list\` | Módulos com condições não atendidas |
| \`alertas\` | \`list\` | Módulos críticos em situação de risco |
| \`pilha_eventos\` | \`list\` (Pilha / LIFO) | Histórico de ações para auditoria e rollback |

## Regras de decisão (lógica booleana)

A autorização de pouso segue a expressão:

\`\`\`
AUTORIZADO = (C ≥ 50 ∨ EMERGÊNCIA) ∧ S_OK ∧ A_LIVRE ∧ ATM_OK
\`\`\`

Onde:
- \`C\` = nível de combustível (%)
- \`S_OK\` = integridade dos sensores
- \`A_LIVRE\` = área de pouso disponível
- \`ATM_OK\` = condições atmosféricas aceitáveis
- \`EMERGÊNCIA\` = módulo CRÍTICO com combustível entre 45–50% (override)

### Diagrama de portas lógicas

\`\`\`
  C ≥ 50  ──┐
            ├── OR ──┐
  EMERG.  ──┘        │
                     ├── AND ──┐
  S_OK    ───────────┘         │
                               ├── AND ──┐
  A_LIVRE ─────────────────────┘         │
                                         ├── AND ──► AUTORIZADO
  ATM_OK  ───────────────────────────────┘
\`\`\`

## Algoritmos implementados

### Buscas
- **Busca sequencial** — menor combustível e filtro por criticidade — \`O(n)\`
- **Busca binária** — por prioridade em lista ordenada — \`O(log n)\`

### Ordenações
- **Selection Sort** — ordenação por prioridade — \`O(n²)\`
- **Insertion Sort** — ordenação por combustível — \`O(n²)\` (eficiente em listas quase ordenadas)

> A escolha por algoritmos \`O(n²)\` é deliberada: em sistemas embarcados de missão espacial com \`n\` pequeno, eles oferecem **previsibilidade e baixo overhead de memória**, atributos críticos sob restrições marcianas.

## Modelagem matemática

A geração de energia solar é modelada por uma **função senoidal**:

\`\`\`
E(t) = A · sen(π · (t − t₀) / L),   para t₀ ≤ t ≤ t₀ + L
E(t) = 0,                            caso contrário
\`\`\`

**Parâmetros (Marte):**
- \`A\` = 8,0 kW (potência de pico dos painéis)
- \`t₀\` = 6h (nascer do Sol marciano)
- \`L\` = 12,3h (duração do período de luz)

A energia total acumulada no dia marciano é calculada por **integração numérica (regra dos trapézios)** e usada para limitar quantos pousos podem ocorrer simultaneamente.

## Saída esperada

\`\`\`
============================================================
  MGPEB — AURORA SIGER | FASE 2 | FIAP 2026
============================================================

============================================================
  PROCESSAMENTO DA FILA DE POUSO
============================================================
  Modulos na fila: 7

  ✓ Habitacao                | AUTORIZADO | Comb: 62%
  ✓ Energia                  | AUTORIZADO | Comb: 78%
  x Laboratorio_Cientifico   | AGUARDANDO | Area de pouso indisponivel
  ✓ Logistica                | AUTORIZADO | Comb: 91%
  ! Suporte_Medico           | ALERTA     | Condicoes atmosfericas adversas
  ! Mineracao                | ALERTA     | Falha de sensor detectada
  ✓ Comunicacoes             | AUTORIZADO | Comb: 70%
...
\`\`\`

## Entregáveis

- 📄 **Relatório técnico** (PDF, 5–10 páginas)
- 🐍 **Código fonte Python** (`mgpeb.py`)
- 📊 **Anexo de estruturas de dados**
- 📐 **Diagramas de portas lógicas**
- 🌱 **Reflexão ESG** sobre governança em Marte

## Equipe

- Nome — RM572241
- Nome — RM570393

## Licença

Projeto acadêmico desenvolvido para fins educacionais — FIAP 2026.
