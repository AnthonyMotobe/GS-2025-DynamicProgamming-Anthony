"""
Global Solution FIAP 2025 - Dynamic Programming
Otimização de Portfólio de Projetos (0/1 Knapsack Problem)

Alunos: Anthony - RM558488
"""

# ============================================================================
# FASE 1: ESTRATÉGIA GULOSA (GREEDY)
# ============================================================================

def estrategia_gulosa(projetos, capacidade):
    """
    Abordagem Greedy: Seleciona projetos com maior relação Valor/Horas.
    Complexidade: O(n log n) devido à ordenação.
    """
    # Calcular relação valor/horas para cada projeto
    projetos_ordenados = []
    for nome, valor, horas in projetos:
        if horas > 0:
            relacao = valor / horas
            projetos_ordenados.append((nome, valor, horas, relacao))
    
    # Ordenar por relação (decrescente)
    projetos_ordenados.sort(key=lambda x: x[3], reverse=True)
    
    # Selecionar projetos até esgotar capacidade
    capacidade_restante = capacidade
    valor_total = 0
    projetos_selecionados = []
    
    for nome, valor, horas, relacao in projetos_ordenados:
        if horas <= capacidade_restante:
            projetos_selecionados.append(nome)
            valor_total += valor
            capacidade_restante -= horas
    
    return valor_total, projetos_selecionados


# ============================================================================
# FASE 2: SOLUÇÃO RECURSIVA PURA
# ============================================================================

def recursiva_pura(projetos, capacidade, indice=0):
    """
    Solução recursiva explorando todas as combinações.
    Complexidade: O(2^n) - Exponencial.
    
    Recorrência: MaximoValor(i, c) = max(
        MaximoValor(i-1, c),                      # Não incluir
        Valor[i] + MaximoValor(i-1, c-Horas[i])   # Incluir
    )
    """
    # Caso base: sem projetos ou sem capacidade
    if indice >= len(projetos) or capacidade <= 0:
        return 0
    
    nome, valor, horas = projetos[indice]
    
    # Não incluir o projeto atual
    nao_incluir = recursiva_pura(projetos, capacidade, indice + 1)
    
    # Incluir o projeto atual (se couber)
    incluir = 0
    if horas <= capacidade:
        incluir = valor + recursiva_pura(projetos, capacidade - horas, indice + 1)
    
    return max(nao_incluir, incluir)


# ============================================================================
# FASE 3: PROGRAMAÇÃO DINÂMICA TOP-DOWN (MEMOIZAÇÃO)
# ============================================================================

def pd_memoizacao(projetos, capacidade, indice=0, memo=None):
    """
    Programação Dinâmica com Memoização (Top-Down).
    Complexidade: O(n * C) onde n = número de projetos, C = capacidade.
    Armazena resultados de subproblemas para evitar recálculo.
    """
    if memo is None:
        memo = {}
    
    # Caso base
    if indice >= len(projetos) or capacidade <= 0:
        return 0
    
    # Verificar se subproblema já foi calculado
    chave = (indice, capacidade)
    if chave in memo:
        return memo[chave]
    
    nome, valor, horas = projetos[indice]
    
    # Não incluir o projeto atual
    nao_incluir = pd_memoizacao(projetos, capacidade, indice + 1, memo)
    
    # Incluir o projeto atual (se couber)
    incluir = 0
    if horas <= capacidade:
        incluir = valor + pd_memoizacao(projetos, capacidade - horas, indice + 1, memo)
    
    # Armazenar resultado antes de retornar
    resultado = max(nao_incluir, incluir)
    memo[chave] = resultado
    
    return resultado


# ============================================================================
# FASE 4: PROGRAMAÇÃO DINÂMICA BOTTOM-UP (ITERATIVA)
# ============================================================================

def pd_iterativa(projetos, capacidade):
    """
    Programação Dinâmica Bottom-Up (Iterativa).
    Complexidade: O(n * C).
    
    T[i][c] = valor máximo obtido com os primeiros i projetos e capacidade c.
    """
    n = len(projetos)
    
    # Criar tabela inicializada com zeros
    T = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]
    
    # Preencher tabela iterativamente
    for i in range(1, n + 1):
        nome, valor, horas = projetos[i - 1]
        
        for c in range(capacidade + 1):
            # Não incluir projeto i
            T[i][c] = T[i - 1][c]
            
            # Incluir projeto i (se houver capacidade)
            if horas <= c:
                incluir = valor + T[i - 1][c - horas]
                T[i][c] = max(T[i][c], incluir)
    
    # Resultado final na última célula
    return T[n][capacidade]


def pd_iterativa_com_rastreamento(projetos, capacidade):
    """
    Versão estendida que identifica quais projetos foram selecionados.
    """
    n = len(projetos)
    T = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]
    
    # Preencher tabela
    for i in range(1, n + 1):
        nome, valor, horas = projetos[i - 1]
        for c in range(capacidade + 1):
            T[i][c] = T[i - 1][c]
            if horas <= c:
                incluir = valor + T[i - 1][c - horas]
                T[i][c] = max(T[i][c], incluir)
    
    # Rastrear projetos selecionados
    projetos_selecionados = []
    i, c = n, capacidade
    
    while i > 0 and c > 0:
        if T[i][c] != T[i - 1][c]:
            nome, valor, horas = projetos[i - 1]
            projetos_selecionados.append(nome)
            c -= horas
        i -= 1
    
    return T[n][capacidade], projetos_selecionados[::-1]


# ============================================================================
# CASOS DE TESTE
# ============================================================================

def executar_testes():
    print("=" * 80)
    print("OTIMIZAÇÃO DE PORTFÓLIO DE PROJETOS - GLOBAL SOLUTION FIAP 2025")
    print("=" * 80)
    
    # CASO DE TESTE 1: Exemplo do enunciado
    print("\n[TESTE 1] Exemplo do Enunciado")
    print("-" * 80)
    projetos1 = [
        ("Projeto A", 12, 4),
        ("Projeto B", 10, 3),
        ("Projeto C", 7, 2),
        ("Projeto D", 4, 3)
    ]
    capacidade1 = 10
    
    print(f"Capacidade: {capacidade1} Horas-Especialista")
    print("Projetos: A(V=12,E=4), B(V=10,E=3), C(V=7,E=2), D(V=4,E=3)")
    
    valor_guloso, proj_guloso = estrategia_gulosa(projetos1, capacidade1)
    valor_recursivo = recursiva_pura(projetos1, capacidade1)
    valor_memo = pd_memoizacao(projetos1, capacidade1)
    valor_iterativo, proj_iterativo = pd_iterativa_com_rastreamento(projetos1, capacidade1)
    
    print(f"\nGulosa:        Valor={valor_guloso}, Projetos={proj_guloso}")
    print(f"Recursiva:     Valor={valor_recursivo}")
    print(f"Memoização:    Valor={valor_memo}")
    print(f"PD Iterativa:  Valor={valor_iterativo}, Projetos={proj_iterativo}")
    
    # CASO DE TESTE 2: Falha do Greedy
    print("\n\n[TESTE 2] Demonstração de Falha da Estratégia Gulosa")
    print("-" * 80)
    projetos2 = [
        ("Projeto X", 60, 10),
        ("Projeto Y", 50, 8),
        ("Projeto Z", 50, 8)
    ]
    capacidade2 = 16
    
    print(f"Capacidade: {capacidade2} Horas-Especialista")
    print("Projetos: X(V=60,E=10,R=6.0), Y(V=50,E=8,R=6.25), Z(V=50,E=8,R=6.25)")
    
    valor_guloso2, proj_guloso2 = estrategia_gulosa(projetos2, capacidade2)
    valor_iterativo2, proj_iterativo2 = pd_iterativa_com_rastreamento(projetos2, capacidade2)
    
    print(f"\nGulosa:        Valor={valor_guloso2}, Projetos={proj_guloso2}")
    print(f"               ❌ Escolhe Y+Z mas desperdiça capacidade")
    print(f"PD Iterativa:  Valor={valor_iterativo2}, Projetos={proj_iterativo2}")
    print(f"               ✅ Solução ótima: Y+Z = 100 (usa 16h completas)")
    
    # CASO DE TESTE 3: Portfólio complexo
    print("\n\n[TESTE 3] Portfólio Complexo")
    print("-" * 80)
    projetos3 = [
        ("AI Platform", 25, 5),
        ("Mobile App", 15, 3),
        ("Web Dashboard", 20, 4),
        ("API Integration", 10, 2),
        ("Data Analytics", 18, 4)
    ]
    capacidade3 = 12
    
    print(f"Capacidade: {capacidade3} Horas-Especialista")
    valor_iterativo3, proj_iterativo3 = pd_iterativa_com_rastreamento(projetos3, capacidade3)
    print(f"Solução Ótima: Valor={valor_iterativo3}, Projetos={proj_iterativo3}")
    
    # CASO DE TESTE 4: Alta capacidade
    print("\n\n[TESTE 4] Alta Capacidade")
    print("-" * 80)
    projetos4 = [
        ("Blockchain", 40, 8),
        ("IoT System", 35, 7),
        ("Cloud Migration", 30, 6),
        ("Security Audit", 25, 5)
    ]
    capacidade4 = 20
    
    print(f"Capacidade: {capacidade4} Horas-Especialista")
    valor_iterativo4, proj_iterativo4 = pd_iterativa_com_rastreamento(projetos4, capacidade4)
    print(f"Solução Ótima: Valor={valor_iterativo4}, Projetos={proj_iterativo4}")
    
    # ANÁLISE DE COMPLEXIDADE
    print("\n\n" + "=" * 80)
    print("ANÁLISE DE COMPLEXIDADE TEÓRICA")
    print("=" * 80)
    print("""
1. ESTRATÉGIA GULOSA
   Tempo: O(n log n) | Espaço: O(n)
   Rápida mas NÃO garante solução ótima.

2. RECURSIVA PURA
   Tempo: O(2^n) | Espaço: O(n)
   Exponencial - impraticável para n > 20.

3. MEMOIZAÇÃO (Top-Down)
   Tempo: O(n × C) | Espaço: O(n × C)
   Ótima - cada subproblema calculado uma vez.

4. PD ITERATIVA (Bottom-Up)
   Tempo: O(n × C) | Espaço: O(n × C)
   MAIS EFICIENTE - evita overhead de recursão e é cache-friendly.

CONCLUSÃO: A PD Iterativa é a mais eficiente na prática por ter
complexidade polinomial e evitar chamadas recursivas.
    """)


if __name__ == "__main__":
    executar_testes()
