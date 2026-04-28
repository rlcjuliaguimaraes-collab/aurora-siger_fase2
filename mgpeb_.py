# ============================================================
#  MGPEB — Módulo de Gerenciamento de Pouso e
#           Estabilização de Base — Aurora Siger
#  Fase 2 | FIAP | 2026
# ============================================================
#
#  Conteúdos aplicados:
#   - Estruturas lineares: listas, filas (deque) e pilhas
#   - Algoritmos de busca sequencial e binária
#   - Algoritmos de ordenação por seleção e por prioridade
#   - Lógica booleana com IF / ELIF / ELSE
#   - Modelagem matemática: geração solar senoidal
# ============================================================

import math
from collections import deque

# ─────────────────────────────────────────────
# 1. DEFINIÇÃO DOS MÓDULOS DE POUSO
# ─────────────────────────────────────────────
# Cada módulo é um dicionário com os atributos:
#   nome         : identificação do módulo
#   prioridade   : 1 (máxima) a 5 (mínima)
#   combustivel  : % restante no tanque
#   massa        : toneladas
#   criticidade  : 'CRITICA', 'ALTA', 'MEDIA', 'BAIXA'
#   horario_orbita: hora estimada de chegada à órbita (0-24h)
#   sensores_ok  : True/False — integridade dos sensores
#   area_livre   : True/False — área de pouso disponível
#   atmosfera_ok : True/False — condições atmosféricas aceitáveis

modulos = [
    {
        "nome": "Habitacao",
        "prioridade": 1,
        "combustivel": 62,
        "massa": 18.5,
        "criticidade": "CRITICA",
        "horario_orbita": 6,
        "sensores_ok": True,
        "area_livre": True,
        "atmosfera_ok": True,
    },
    {
        "nome": "Energia",
        "prioridade": 2,
        "combustivel": 78,
        "massa": 12.0,
        "criticidade": "CRITICA",
        "horario_orbita": 7,
        "sensores_ok": True,
        "area_livre": True,
        "atmosfera_ok": True,
    },
    {
        "nome": "Laboratorio_Cientifico",
        "prioridade": 3,
        "combustivel": 55,
        "massa": 9.2,
        "criticidade": "ALTA",
        "horario_orbita": 9,
        "sensores_ok": True,
        "area_livre": False,   # área temporariamente indisponível
        "atmosfera_ok": True,
    },
    {
        "nome": "Logistica",
        "prioridade": 4,
        "combustivel": 91,
        "massa": 22.0,
        "criticidade": "ALTA",
        "horario_orbita": 11,
        "sensores_ok": True,
        "area_livre": True,
        "atmosfera_ok": True,
    },
    {
        "nome": "Suporte_Medico",
        "prioridade": 1,
        "combustivel": 48,   # abaixo do mínimo seguro (50%)
        "massa": 7.8,
        "criticidade": "CRITICA",
        "horario_orbita": 8,
        "sensores_ok": True,
        "area_livre": True,
        "atmosfera_ok": False,  # tempestade de poeira simulada
    },
    {
        "nome": "Mineracao",
        "prioridade": 5,
        "combustivel": 83,
        "massa": 31.0,
        "criticidade": "MEDIA",
        "horario_orbita": 14,
        "sensores_ok": False,  # falha de sensor detectada
        "area_livre": True,
        "atmosfera_ok": True,
    },
    {
        "nome": "Comunicacoes",
        "prioridade": 2,
        "combustivel": 70,
        "massa": 5.5,
        "criticidade": "CRITICA",
        "horario_orbita": 10,
        "sensores_ok": True,
        "area_livre": True,
        "atmosfera_ok": True,
    },
]


# ─────────────────────────────────────────────
# 2. ESTRUTURAS DE DADOS LINEARES
# ─────────────────────────────────────────────

# FILA principal — módulos aguardando autorização de pouso
fila_pouso = deque(modulos)

# LISTA auxiliar — módulos já pousados com sucesso
pousados = []

# LISTA auxiliar — módulos em espera (condições não atendidas)
em_espera = []

# LISTA auxiliar — módulos em situação de alerta
alertas = []

# PILHA de eventos — registra ações realizadas (para auditoria/rollback)
pilha_eventos = []   # operações: append() para empilhar, pop() para desempilhar


def registrar_evento(acao, modulo_nome):
    """Empilha um evento de auditoria na pilha de histórico."""
    pilha_eventos.append({"acao": acao, "modulo": modulo_nome})


def desfazer_ultimo_evento():
    """Desempilha e exibe o último evento registrado (rollback)."""
    if pilha_eventos:
        evento = pilha_eventos.pop()
        print(f"  [ROLLBACK] Acao desfeita: {evento['acao']} -> {evento['modulo']}")
    else:
        print("  [ROLLBACK] Nenhum evento para desfazer.")


# ─────────────────────────────────────────────
# 3. REGRAS DE DECISÃO BOOLEANAS
# ─────────────────────────────────────────────
# Expressão lógica completa:
#   AUTORIZADO = (combustivel >= 50)
#            AND sensores_ok
#            AND area_livre
#            AND atmosfera_ok

def autorizar_pouso(modulo):
    """
    Aplica as regras booleanas de autorização de pouso.
    Retorna True se TODAS as condições forem satisfeitas.

    Regra lógica (notação booleana):
      AUTORIZADO = (C >= 50) AND S_OK AND A_LIVRE AND ATM_OK

    Onde:
      C       = combustivel (%)
      S_OK    = sensores_ok
      A_LIVRE = area_livre
      ATM_OK  = atmosfera_ok
    """
    comb_ok   = modulo["combustivel"] >= 50
    sensor_ok = modulo["sensores_ok"]
    area_ok   = modulo["area_livre"]
    atm_ok    = modulo["atmosfera_ok"]

    # Retrofoguete adicional: módulos CRÍTICOS com combustível entre 45-50%
    # recebem override de emergência (OR lógico condicionado)
    emergencia = (modulo["criticidade"] == "CRITICA") and (modulo["combustivel"] >= 45)

    autorizado = (comb_ok or emergencia) and sensor_ok and area_ok and atm_ok

    # Detalhamento das falhas
    falhas = []
    if not comb_ok and not emergencia:
        falhas.append(f"Combustivel insuficiente ({modulo['combustivel']}% < 50%)")
    if not sensor_ok:
        falhas.append("Falha de sensor detectada")
    if not area_ok:
        falhas.append("Area de pouso indisponivel")
    if not atm_ok:
        falhas.append("Condicoes atmosfericas adversas")

    return autorizado, falhas


# ─────────────────────────────────────────────
# 4. ALGORITMOS DE BUSCA
# ─────────────────────────────────────────────

def busca_menor_combustivel(lista):
    """
    Busca sequencial: encontra o módulo com menor nível de combustível.
    Complexidade: O(n)
    """
    if not lista:
        return None
    menor = lista[0]
    for m in lista[1:]:
        if m["combustivel"] < menor["combustivel"]:
            menor = m
    return menor


def busca_por_criticidade(lista, nivel):
    """
    Busca sequencial: retorna todos os módulos com determinada criticidade.
    Complexidade: O(n)
    """
    return [m for m in lista if m["criticidade"] == nivel]


def busca_binaria_prioridade(lista_ordenada, prioridade_alvo):
    """
    Busca binária em lista já ordenada por prioridade.
    Complexidade: O(log n)
    Retorna o índice do primeiro módulo com a prioridade-alvo, ou -1.
    """
    esq, dir = 0, len(lista_ordenada) - 1
    while esq <= dir:
        meio = (esq + dir) // 2
        p = lista_ordenada[meio]["prioridade"]
        if p == prioridade_alvo:
            return meio
        elif p < prioridade_alvo:
            esq = meio + 1
        else:
            dir = meio - 1
    return -1


# ─────────────────────────────────────────────
# 5. ALGORITMOS DE ORDENAÇÃO
# ─────────────────────────────────────────────

def ordenar_por_prioridade(lista):
    """
    Ordenação por seleção (Selection Sort) pelo campo 'prioridade'.
    Menor valor = maior prioridade.
    Complexidade: O(n²) — adequado para n pequeno em sistemas embarcados.
    """
    lst = list(lista)  # cópia para não alterar o original
    n = len(lst)
    for i in range(n):
        idx_min = i
        for j in range(i + 1, n):
            if lst[j]["prioridade"] < lst[idx_min]["prioridade"]:
                idx_min = j
        lst[i], lst[idx_min] = lst[idx_min], lst[i]
    return lst


def ordenar_por_combustivel(lista):
    """
    Ordenação por inserção (Insertion Sort) pelo campo 'combustivel'.
    Menor combustível = pouso mais urgente.
    Complexidade: O(n²) no pior caso; eficiente para listas quase ordenadas.
    """
    lst = list(lista)
    for i in range(1, len(lst)):
        chave = lst[i]
        j = i - 1
        while j >= 0 and lst[j]["combustivel"] > chave["combustivel"]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = chave
    return lst


# ─────────────────────────────────────────────
# 6. MODELAGEM MATEMÁTICA — ENERGIA SOLAR
# ─────────────────────────────────────────────
# Fenômeno: geração de energia solar ao longo do dia marciano
#
# Modelo senoidal:
#   E(t) = A * sen(pi * (t - t0) / L)  para t0 <= t <= t0 + L
#   E(t) = 0                            caso contrário
#
# Parâmetros (Marte):
#   A  = amplitude = potência de pico dos painéis (kW)  → 8.0 kW
#   t0 = nascer do sol marciano                         → 6h
#   L  = duração do dia solar marciano                  → ~12.3h
#   t  = hora local marciana (0 a 24.6h)
#
# Marte tem dia solar (sol) de ~24h37min = 24.62h.
# A irradiância é ~590 W/m². Com 20 m² de painel a 68% de eficiência ≈ 8 kW pico.

A_SOLAR   = 8.0    # kW — potência de pico
T0_SOL    = 6.0    # h  — nascer do sol
L_DIA     = 12.3   # h  — duração do período de luz solar


def energia_solar(t):
    """
    Calcula a potência gerada pelos painéis solares no instante t (horas).
    Retorna valor em kW. Retorna 0 fora do período de luz.
    """
    if T0_SOL <= t <= T0_SOL + L_DIA:
        return A_SOLAR * math.sin(math.pi * (t - T0_SOL) / L_DIA)
    return 0.0


def energia_acumulada(t_inicio, t_fim, passos=100):
    """
    Integração numérica (método dos trapézios) da energia gerada
    entre t_inicio e t_fim. Retorna energia total em kWh.
    """
    dt = (t_fim - t_inicio) / passos
    total = 0.0
    for i in range(passos):
        t_a = t_inicio + i * dt
        t_b = t_inicio + (i + 1) * dt
        total += (energia_solar(t_a) + energia_solar(t_b)) / 2 * dt
    return total


# ─────────────────────────────────────────────
# 7. SIMULAÇÃO PRINCIPAL DO MGPEB
# ─────────────────────────────────────────────

def exibir_separador(titulo=""):
    print("\n" + "=" * 60)
    if titulo:
        print(f"  {titulo}")
        print("=" * 60)


def processar_fila():
    """
    Processa a fila de pouso aplicando as regras booleanas.
    Módulos autorizados vão para 'pousados'.
    Módulos bloqueados vão para 'em_espera' ou 'alertas'.
    """
    exibir_separador("PROCESSAMENTO DA FILA DE POUSO")
    print(f"  Modulos na fila: {len(fila_pouso)}\n")

    while fila_pouso:
        modulo = fila_pouso.popleft()   # FIFO — primeiro a entrar, primeiro a sair
        autorizado, falhas = autorizar_pouso(modulo)

        if autorizado:
            pousados.append(modulo)
            registrar_evento("POUSO_AUTORIZADO", modulo["nome"])
            print(f"  ✓ {modulo['nome']:25s} | AUTORIZADO | Comb: {modulo['combustivel']}%")
        else:
            # Criticidade CRITICA vai para alertas; demais para em_espera
            if modulo["criticidade"] == "CRITICA":
                alertas.append(modulo)
                registrar_evento("ALERTA_CRITICO", modulo["nome"])
                print(f"  ! {modulo['nome']:25s} | ALERTA     | {' | '.join(falhas)}")
            else:
                em_espera.append(modulo)
                registrar_evento("POUSO_AGUARDANDO", modulo["nome"])
                print(f"  x {modulo['nome']:25s} | AGUARDANDO | {' | '.join(falhas)}")


def exibir_resumo():
    exibir_separador("RESUMO DA OPERACAO")
    print(f"  Pousados com sucesso : {len(pousados)}")
    print(f"  Em alerta critico    : {len(alertas)}")
    print(f"  Aguardando condicoes : {len(em_espera)}")

    if alertas:
        print("\n  --- MODULOS EM ALERTA ---")
        for m in alertas:
            print(f"  >> {m['nome']} (Comb: {m['combustivel']}%, Sensores: {m['sensores_ok']}, Atm: {m['atmosfera_ok']})")


def demo_buscas():
    exibir_separador("DEMONSTRACAO: ALGORITMOS DE BUSCA")
    todos = modulos  # lista original completa

    menor_comb = busca_menor_combustivel(todos)
    print(f"  Busca sequencial — menor combustivel:")
    print(f"    Modulo: {menor_comb['nome']} | {menor_comb['combustivel']}%\n")

    criticos = busca_por_criticidade(todos, "CRITICA")
    print(f"  Busca por criticidade CRITICA ({len(criticos)} encontrados):")
    for m in criticos:
        print(f"    - {m['nome']}")

    ordenados = ordenar_por_prioridade(todos)
    idx = busca_binaria_prioridade(ordenados, 2)
    print(f"\n  Busca binaria — prioridade 2:")
    if idx >= 0:
        print(f"    Encontrado: {ordenados[idx]['nome']}")
    else:
        print("    Nao encontrado.")


def demo_ordenacao():
    exibir_separador("DEMONSTRACAO: ALGORITMOS DE ORDENACAO")

    print("  Ordenacao por PRIORIDADE (Selection Sort):")
    por_prior = ordenar_por_prioridade(modulos)
    for m in por_prior:
        print(f"    Prioridade {m['prioridade']} | {m['nome']}")

    print("\n  Ordenacao por COMBUSTIVEL (Insertion Sort — mais urgentes primeiro):")
    por_comb = ordenar_por_combustivel(modulos)
    for m in por_comb:
        print(f"    {m['combustivel']:3d}% | {m['nome']}")


def demo_energia_solar():
    exibir_separador("MODELAGEM MATEMATICA — ENERGIA SOLAR")
    print("  Funcao: E(t) = 8.0 * sen(pi * (t - 6) / 12.3)  [kW]")
    print("  Periodo de luz: 06h00 ate 18h18 (hora marciana)\n")
    print(f"  {'Hora':>6}  {'Potencia (kW)':>15}  {'Barra visual'}")
    print("  " + "-" * 50)

    for hora in range(0, 25, 2):
        pot = energia_solar(hora)
        barra = "#" * int(pot * 3)
        print(f"  {hora:>5}h  {pot:>13.2f}  {barra}")

    energia_dia = energia_acumulada(T0_SOL, T0_SOL + L_DIA)
    print(f"\n  Energia total gerada no dia marciano: {energia_dia:.2f} kWh")
    print(f"  Decisao de engenharia: com {energia_dia:.1f} kWh disponiveis,")
    print(f"  o MGPEB pode autorizar ate 2 pousos simultaneos (consumo ~{energia_dia/2:.0f} kWh cada).")


def demo_pilha():
    exibir_separador("DEMONSTRACAO: PILHA DE EVENTOS (AUDITORIA)")
    print(f"  Ultimos 5 eventos registrados na pilha:")
    eventos_viz = pilha_eventos[-5:] if len(pilha_eventos) >= 5 else pilha_eventos
    for i, ev in enumerate(reversed(eventos_viz), 1):
        print(f"  {i}. [{ev['acao']}] -> {ev['modulo']}")

    print("\n  Simulando rollback do ultimo evento...")
    desfazer_ultimo_evento()


# ─────────────────────────────────────────────
# 8. EXECUÇÃO
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  MGPEB — AURORA SIGER | FASE 2 | FIAP 2026")
    print("=" * 60)

    processar_fila()
    exibir_resumo()
    demo_buscas()
    demo_ordenacao()
    demo_energia_solar()
    demo_pilha()

    print("\n" + "=" * 60)
    print("  FIM DA SIMULACAO MGPEB")
    print("=" * 60 + "\n")
