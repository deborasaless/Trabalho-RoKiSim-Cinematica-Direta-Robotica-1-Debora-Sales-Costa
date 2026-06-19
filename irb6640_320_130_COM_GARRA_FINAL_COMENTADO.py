import math
import numpy as np

# ============================================================
# TRABALHO DE ROBÓTICA I - RoKiSim
# Aluna: Debora Sales Costa
# Robô: ABB IRB6640 320 130
# Garra: IRB1600_Pince
#
# OBJETIVO DO PROGRAMA:
#   Calcular a posição final da garra (ponto H) a partir dos ângulos das juntas - Cinemática Direta.
#
# ENTRADA:
#   M1 M2 M3 M4 M5 M6 em graus
#
# SAÍDA:
#   Posição final da ponta da garra H (Hx, Hy, Hz)
#
#   =====CINEMÁTICA DIRETA=====
#
# ============================================================


ROBOT = [
    # alpha,   a,       theta_offset,   d
    (0.0,      0.0,       0.0,        780.0),   # Junta 1
    (-90.0,  320.0,     -90.0,          0.0),   # Junta 2
    (0.0,   1280.0,       0.0,          0.0),   # Junta 3
    (-90.0,  200.0,       0.0,       1592.0),   # Junta 4
    (90.0,     0.0,       0.0,          0.0),   # Junta 5
    (-90.0,    0.0,     180.0,        200.0),   # Junta 6
]


# Primeiro modelamos o robô até o frame 6.
# Depois adicionamos a garra.
#
# No RoKiSim, a garra aparece como:
#
#   Tool frame w.r.t. ref. 6:
#   x = 0.00 mm
#   y = 0.00 mm
#   z = 233.37 mm
#   rx = 0°
#   ry = 0°
#   rz = 0°
#
# Isso quer dizer:
#
#   "A ponta H da garra está 233.37 mm à frente do frame 6,
#    no eixo Z local do próprio frame 6."
#
#   [x, y, z, 1]
#
# O número 1 no final permite que a matriz 4x4 faça rotação e translação
# ao mesmo tempo.

TOOL_6H = np.array([0.0, 0.0, 233.37, 1.0])

#
#   [ R11 R12 R13 X ]
#   [ R21 R22 R23 Y ]
#   [ R31 R32 R33 Z ]
#   [  0   0   0  1 ]
#
# A parte 3x3 da esquerda é rotação.
# A última coluna é a posição X, Y, Z.
#
# Por isso, no final, para pegar a posição, usamos:
#
#   T[0, 3] → X
#   T[1, 3] → Y
#   T[2, 3] → Z


def rx(deg):
    """
    Cria uma matriz de rotação em torno do eixo X.

    deg = ângulo em graus.
    
    Se você gira algo em torno do eixo X,
    o eixo X fica parado,
    mas Y e Z mudam.
    """

    # Python trabalha com seno e cosseno em radianos.
    # Por isso convertemos graus para radianos.
    r = math.radians(deg)

    # Calcula cosseno e seno do ângulo.
    c, s = math.cos(r), math.sin(r)

    # Retorna a matriz 4x4 de rotação em X.
    return np.array([
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1],
    ], dtype=float)


def tx(mm):
    """
    Cria uma matriz de translação ao longo do eixo X.

    mm = deslocamento em milímetros.

    Exemplo:
        tx(320) significa andar 320 mm no eixo X.
    """

    # Começamos com a matriz identidade.
    T = np.eye(4)

    # Colocamos o deslocamento X na última coluna.
    T[0, 3] = mm

    return T


def rz(deg):
    """
    Cria uma matriz de rotação em torno do eixo Z.

    deg = ângulo em graus.

    Essa é a rotação usada pelas juntas do robô,
    porque cada junta rotativa gira em torno do seu eixo Z local.
    """

    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)

    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1],
    ], dtype=float)


def tz(mm):
    """
    Cria uma matriz de translação ao longo do eixo Z.

    mm = deslocamento em milímetros.

    Exemplo:
        tz(780) significa subir/avançar 780 mm no eixo Z local.
    """

    T = np.eye(4)
    T[2, 3] = mm
    return T


# Cada junta do robô é montada nesta ordem:
#
#   1. Rx(alpha)
#      gira em torno de X
#
#   2. Tx(a)
#      anda no eixo X
#
#   3. Rz(theta_total)
#      gira em torno de Z
#      theta_total = theta_offset + ângulo digitado
#
#   4. Tz(d)
#      anda no eixo Z
#
# A matriz final da junta é:
#
#   A = Rx(alpha) @ Tx(a) @ Rz(theta_total) @ Tz(d)
#
#   Em matriz, a ordem importa!!!!!!!!!!!!!!!!!!


def link_transform(alpha, a, theta_total, d):
    """
    Monta a matriz 4x4 de uma junta/elo do robô.
    """

    return rx(alpha) @ tx(a) @ rz(theta_total) @ tz(d)


# A ideia é multiplicar as 6 matrizes:
#
#   T_R6 = A1 @ A2 @ A3 @ A4 @ A5 @ A6
#
# Onde:
#
#   R  = origem/base do robô
#   6  = frame 6/flange do robô
#
# Cada A_i depende do ângulo M_i.
#
# Exemplo:
#   Se o input for:
#
#       0 45 0 0 0 0
#
#   então:
#       M1 = 0
#       M2 = 45
#       M3 = 0
#       M4 = 0
#       M5 = 0
#       M6 = 0


def fk_robot(motores):
    """
    Calcula a matriz T_R6, ou seja,
    a transformação da base do robô até o frame 6.

    motores = lista com 6 ângulos:
        [M1, M2, M3, M4, M5, M6]
    """

    # Garante que a pessoa digitou exatamente 6 ângulos.
    if len(motores) != 6:
        raise ValueError("Digite exatamente 6 ângulos: M1 M2 M3 M4 M5 M6")

    # Começamos na matriz identidade.
    # Isso significa:
    #   "estou na base do robô, sem nenhuma transformação ainda".
    T = np.eye(4)

    # Passamos por cada junta do robô.
    for i, (alpha, a, theta_offset, d) in enumerate(ROBOT):

        # O ângulo real usado na junta é:
        #   offset fixo do robô + ângulo input.
        theta_total = theta_offset + motores[i]

        # Monta a matriz da junta atual.
        A_i = link_transform(alpha, a, theta_total, d)

        # Acumula a transformação.
        #
        # Depois da junta 1:
        #   T = A1
        #
        # Depois da junta 2:
        #   T = A1 @ A2
        #
        # Depois da junta 3:
        #   T = A1 @ A2 @ A3
        #
        # E assim por diante até a junta 6.
        T = T @ A_i

    # No final, T é T_R6.
    return T


# Depois que temos T_R6, adicionamos a garra.
#
# T_R6 transforma coordenadas do frame 6 para o mundo/base.
#
# TOOL_6H é a posição da ponta H vista a partir do frame 6.
#
# Então:
#
#   pH = T_R6 @ TOOL_6H
#
# O resultado pH tem:
#
#   pH[0] = Hx
#   pH[1] = Hy
#   pH[2] = Hz
# ============================================================

def calcular(motores):
    """
    Calcula duas posições:

    1. p6:
       posição do frame 6 sem a garra.

    2. pH:
       posição final H com a garra IRB1600_Pince.
    """

    # Calcula a matriz da base até o frame 6.
    T_R6 = fk_robot(motores)

    # A posição do frame 6 está na última coluna da matriz.
    p6 = T_R6[:3, 3]

    # Agora aplicamos a garra.
    # TOOL_6H está escrito em relação ao frame 6.
    # Multiplicando por T_R6, obtemos H em relação ao mundo/base.
    pH = T_R6 @ TOOL_6H

    # Retornamos:
    #   p6[:3] = X6, Y6, Z6
    #   pH[:3] = Hx, Hy, Hz
    return p6, pH[:3]


# ============================================================
# TESTE AUTOMÁTICO DO HOME
# ============================================================
#
# HOME significa:
#
#   M1 = 0
#   M2 = 0
#   M3 = 0
#   M4 = 0
#   M5 = 0
#   M6 = 0
#
# Esse teste é importante porque confirma se o programa está
# batendo com o RoKiSim.
#
# Sem garra, o RoKiSim mostrou:
#
#   Frame 6 = 2112.000, 0.000, 2260.000
#
# Com garra IRB1600_Pince, o RoKiSim mostrou:
#
#   H = 2345.370, 0.000, 2260.000
#
# Se o programa calcular esses mesmos valores,
# é um forte sinal de que a modelagem está certa e foram escolhidos o robô e a garra corretamente.
# ============================================================

def teste_home():
    """
    Imprime uma validação rápida para a posição HOME.
    """

    p6, pH = calcular([0, 0, 0, 0, 0, 0])

    print("Validação HOME")
    print("-" * 50)

    print("Frame 6 esperado no RoKiSim sem garra:")
    print("X6 = 2112.000 mm, Y6 = 0.000 mm, Z6 = 2260.000 mm")

    print("Frame 6 calculado pelo programa:")
    print(f"X6 = {p6[0]:.3f} mm, Y6 = {p6[1]:.3f} mm, Z6 = {p6[2]:.3f} mm")

    print()

    print("Ponto H esperado no RoKiSim com IRB1600_Pince:")
    print("Hx = 2345.370 mm, Hy = 0.000 mm, Hz = 2260.000 mm")

    print("Ponto H calculado pelo programa:")
    print(f"Hx = {pH[0]:.3f} mm, Hy = {pH[1]:.3f} mm, Hz = {pH[2]:.3f} mm")

    print("-" * 50)
    print()


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================
#
# INPUT: 6 ângulos.
# O programa calcula e mostra:
#
#   - posição do frame 6 sem garra
#   - posição final H com garra
#
# ============================================================

def main():
    print("ABB IRB6640 320 130 + IRB1600_Pince")
    print("Cinemática direta para o RoKiSim")
    print()

    # Primeiro faz o teste HOME automaticamente.
    teste_home()

    print("Digite os seis ângulos em graus, separados por espaço.")
    print("Exemplo: 0 0 0 0 0 0")
    print("Digite sair para encerrar.")
    print()

    while True:
        # Lê uma linha digitada pelo usuário.
        entrada = input("M1 M2 M3 M4 M5 M6 = ").strip()

        # Permite encerrar o programa.
        if entrada.lower() in {"sair", "exit", "q"}:
            break

        try:
            # Transforma a linha digitada em números.
            #
            # Exemplo:
            #   "0 45 0 0 0 0"
            #
            # vira:
            #   [0.0, 45.0, 0.0, 0.0, 0.0, 0.0]
            #
            # O replace(",", ".") permite digitar número com vírgula,
            # como 10,5, caso seja necessário.
            motores = [float(x.replace(",", ".")) for x in entrada.split()]

            # Calcula frame 6 e ponto H.
            p6, pH = calcular(motores)

            print()
            print("Resultado sem garra - frame 6:")
            print(f"X6 = {p6[0]:.3f} mm")
            print(f"Y6 = {p6[1]:.3f} mm")
            print(f"Z6 = {p6[2]:.3f} mm")

            print()
            print("Resultado final com garra - ponto H:")
            print(f"Hx = {pH[0]:.3f} mm")
            print(f"Hy = {pH[1]:.3f} mm")
            print(f"Hz = {pH[2]:.3f} mm")
            print()

        except Exception as e:
            # Se a pessoa digitar errado, o programa não quebra.
            # Ele mostra a mensagem de erro e pede para tentar de novo.
            print(f"Erro: {e}")
            print("Tente no formato: 0 0 0 0 0 0")
            print()


# ============================================================
# INÍCIO DO PROGRAMA
# ============================================================
#
# Essa linha faz o Python executar main()
# somente quando este arquivo é rodado diretamente.
#
# ============================================================

if __name__ == "__main__":
    main()
