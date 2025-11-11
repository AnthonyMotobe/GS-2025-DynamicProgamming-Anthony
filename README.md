# Otimização de Portfólio de Projetos

**Global Solution FIAP 2025 - Dynamic Programming**

## Integrantes

- [Anthony K. Motobe] - RM: [558488]

## Sobre o Projeto

Implementação do Problema da Mochila 0/1 aplicado à otimização de portfólio de projetos. O objetivo é selecionar projetos que maximizem o valor total sem exceder a capacidade de Horas-Especialista disponíveis.

## Como Executar

```bash
python portfolio_optimization.py
```

**Requisitos:** Python 3.8+

## Implementações

O projeto contém 4 estratégias de solução:

1. **Estratégia Gulosa** - O(n log n) - Rápida mas não garante solução ótima
2. **Recursiva Pura** - O(2^n) - Explora todas combinações (lenta)
3. **Memoização (Top-Down)** - O(n × C) - Recursão com cache
4. **PD Iterativa (Bottom-Up)** - O(n × C) - **Mais eficiente**

## Casos de Teste

O programa executa automaticamente 4 casos de teste, incluindo:
- Exemplo do enunciado
- Caso onde a estratégia gulosa falha
- Portfólio complexo com múltiplos projetos
- Teste de alta capacidade

## Resultados

A **PD Iterativa** é a solução mais eficiente pois:
- Garante solução ótima
- Complexidade polinomial O(n × C)
- Evita overhead de recursão

No Teste 2, demonstramos que a estratégia gulosa pode falhar:
- Gulosa: seleciona apenas projeto X (valor = 60)
- PD Ótima: seleciona projetos Y + Z (valor = 100)

