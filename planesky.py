import pygame
import random
import string

pygame.init()

largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Plane Sky - Treino de Digitação")

BRANCO = (255, 255, 255)
CINZA_CLARO = (200, 200, 200)
CINZA_MEDIO = (150, 150, 150)
PRETO = (0, 0, 0)
COR_BOTAO = (170, 170, 170)

imagem_fundo = pygame.image.load("planetsky.png")
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura_tela, 200))

aviao_img = pygame.Surface((50, 30))
aviao_img.fill(CINZA_MEDIO)

class Aviao:
    def __init__(self):
        self.imagem = aviao_img
        self.rect = self.imagem.get_rect()
        self.rect.center = (largura_tela // 2, altura_tela - 50)
        self.velocidade = 5
        self.altura = 0

    def mover(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT] and self.rect.right < largura_tela:
            self.rect.x += self.velocidade
        self.rect.y = altura_tela - 50 - self.altura

    def desenhar(self):
        tela.blit(self.imagem, self.rect)

    def ajustar_altura(self, pontos, erros):
        self.altura = max(0, self.altura + pontos * 2 - erros * 5)

def gerar_letra():
    return random.choice(string.ascii_uppercase)

def desenhar_botao(texto, posicao, largura, altura):
    retangulo = pygame.Rect(posicao[0], posicao[1], largura, altura)
    pygame.draw.rect(tela, COR_BOTAO, retangulo, border_radius=15)
    fonte = pygame.font.Font(None, 36)
    texto_renderizado = fonte.render(texto, True, PRETO)
    texto_rect = texto_renderizado.get_rect(center=retangulo.center)
    tela.blit(texto_renderizado, texto_rect)

def tela_inicial():
    tela.fill(CINZA_CLARO)
    tela.blit(imagem_fundo, (0, 0))
    
    opcoes = ["3 minutos", "5 minutos", "7 minutos"]
    largura_botao = 250
    altura_botao = 60
    espacamento = 20
    for i, opcao in enumerate(opcoes):
        posicao = (largura_tela // 2 - largura_botao // 2, altura_tela // 2 + i * (altura_botao + espacamento) - altura_botao // 2)
        desenhar_botao(opcao, posicao, largura_botao, altura_botao)

def main():
    clock = pygame.time.Clock()
    aviao = Aviao()
    letra_atual = gerar_letra()
    pontos = 0
    teclas_pressionadas = 0
    erros = 0
    tempo_total = 60
    tempo_restante = tempo_total
    jogando = False
    rodando = True
    cor_fundo = CINZA_CLARO
    efeito_acerto = 0
    efeito_erro = 0
    aumentando = False

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN and jogando:
                if event.unicode.upper() == letra_atual:
                    pontos += 1
                    teclas_pressionadas += 1
                    letra_atual = gerar_letra()
                    efeito_acerto = 255
                    aumentando = True
                    aviao.ajustar_altura(pontos, erros)
                else:
                    erros += 1
                    efeito_erro = 255
                    aumentando = True
                    aviao.ajustar_altura(pontos, erros)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not jogando:
                    largura_botao = 250
                    altura_botao = 60
                    espacamento = 20
                    retangulos = []
                    for i in range(3):
                        posicao = (largura_tela // 2 - largura_botao // 2, altura_tela // 2 + i * (altura_botao + espacamento) - altura_botao // 2)
                        retangulos.append(pygame.Rect(posicao[0], posicao[1], largura_botao, altura_botao))
                    for i, retangulo in enumerate(retangulos):
                        if retangulo.collidepoint(event.pos):
                            tempo_escolhido = (i + 1) * 3
                            tempo_restante = tempo_escolhido * 60
                            jogando = True
                            letra_atual = gerar_letra()

        if jogando:
            aviao.mover()
            tempo_restante -= clock.get_time() / 1000
            if tempo_restante <= 0:
                jogando = False

            if aumentando:
                if efeito_acerto > 0:
                    efeito_acerto -= 5
                    cor_fundo = (0, efeito_acerto, 0)
                elif efeito_erro > 0:
                    efeito_erro -= 5
                    cor_fundo = (efeito_erro, 0, 0)
                else:
                    aumentando = False

            tela.fill(cor_fundo)
            aviao.desenhar()
            fonte = pygame.font.Font(None, 72)
            texto = fonte.render(letra_atual, True, PRETO)
            tela.blit(texto, (largura_tela // 2 - 30, altura_tela // 2 - 30))
            texto_pontos = fonte.render(f"Pontos: {pontos}", True, PRETO)
            tela.blit(texto_pontos, (10, 10))
            texto_teclas = fonte.render(f"Teclas: {teclas_pressionadas}", True, PRETO)
            tela.blit(texto_teclas, (10, 50))
            texto_erros = fonte.render(f"Erros: {erros}", True, PRETO)
            tela.blit(texto_erros, (10, 90))
            texto_tempo = fonte.render(f"Tempo: {int(tempo_restante)}s", True, PRETO)
            tela.blit(texto_tempo, (largura_tela // 2 - 50, 10))

        else:
            tela.fill(CINZA_CLARO)
            aviao.desenhar()
            fonte_fim = pygame.font.Font(None, 48)
            mensagem_fim = fonte_fim.render("Fim de Jogo!", True, PRETO)
            tela.blit(mensagem_fim, (largura_tela // 2 - 100, altura_tela // 2 - 30))
            resultado = fonte_fim.render(f"Pontos: {pontos} | Teclas: {teclas_pressionadas} | Erros: {erros}", True, PRETO)
            tela.blit(resultado, (largura_tela // 2 - 300, altura_tela // 2 + 10))
            acertos = pontos
            texto_acertos = fonte_fim.render(f"Acertos: {acertos}", True, PRETO)
            tela.blit(texto_acertos, (largura_tela // 2 - 300, altura_tela // 2 + 50))
            botao_inicio = fonte_fim.render("Clique para Reiniciar", True, PRETO)
            tela.blit(botao_inicio, (largura_tela // 2 - 150, altura_tela // 2 + 90))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pontos = 0
                teclas_pressionadas = 0
                erros = 0
                aviao.altura = 0
                cor_fundo = CINZA_CLARO
                jogando = False

        if not jogando:
            tela_inicial()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
