# RADE V1 — Transceptor em português (no browser)

Uma página que faz **RADE V1** (a voz digital do FreeDV) com o seu rádio, **sem instalar nada**: é um único ficheiro, `index.html`, que se abre no **Chrome** ou no **Edge**. Baseado no [rade-tx](https://github.com/Sparks72/rade-tx) de Sparks72 (licença BSD); versão portuguesa com lista de rádios por CU2ED.

O RADE é o código verdadeiro do FreeDV (rade_c, Opus, FARGAN) compilado para WebAssembly: corre todo no seu computador, nada é enviado para a internet.

## O que precisa

- Um computador com **Chrome ou Edge** (Windows, Linux ou macOS). O Firefox e o Safari não servem para o CAT.
- O rádio ligado ao computador por **USB** (placa de som USB + CAT). Rádios na lista:
  - **Yaesu FT-710, FTDX10, FTDX101, FT-991A, FT-891**
  - **Kenwood TS-570D / TS-570S** (áudio pela ACC2 e CAT pela porta série)
  - **QRP Labs QMX / QDX**
  - **Outro rádio**: só o PTT, com os comandos escritos à mão
- Um microfone ou auricular, e altifalantes.

## Preparar o rádio (Yaesu FT-710 / FTDX101)

1. Cabo **USB A-B** do rádio ao computador. Instale o driver **Silicon Labs CP210x** (aparecem duas portas COM: use a **Enhanced COM Port**).
2. Menus do rádio, no grupo do modo **SSB**:
   - **MOD SOURCE = USB**
   - **USB MOD GAIN**: começar baixo (acerta-se no passo 6)
   - **USB OUT LEVEL**: nível do áudio para o computador
   - **CAT-1 RATE**: a mesma velocidade que escolher na página (de fábrica **38400**)
3. Processador de voz (**PROC**) desligado, EQ de emissão plano.

(Kenwood TS-570D: menu 35 = 57600 "576-1"; áudio na ACC2 pino 11 com blindagem no pino 12; menu 33 = nível de entrada; menu 32 = OFF.)

## Usar

1. **Abrir a página**: duplo clique no `index.html` (ou o link que lhe enviarem), no Chrome ou no Edge.
2. **Rádio e CAT**: escolha o **Rádio** na lista (a velocidade e os comandos de emissão/receção ficam preenchidos) e carregue em **Ligar CAT**; escolha a porta do rádio na janela que aparece.
3. **Áudio**: carregue em **Procurar dispositivos de áudio** e autorize o microfone. Escolha:
   - Emissão: **Microfone** (o seu) → **Para o rádio** (a placa de som USB do rádio)
   - Receção: **Do rádio** (a placa de som USB do rádio) → **Altifalantes** (os seus)
4. **Receber**: com **Receber** marcado, a página ouve logo. Quando apanha uma estação aparece **sinal RADE** com o SNR; no fim de cada emissão aparece **fim de emissão**. Os botões de **Banda** levam o rádio às frequências habituais do FreeDV (ex.: 14,236 MHz).
5. **Emitir**: botão **Emitir** ou tecla **Espaço** para começar, e outra vez para acabar. **Esc** corta a emissão de imediato. Há um **limite de segurança** (2 minutos por defeito).
6. **Níveis** (primeira vez, numa carga fictícia ou com pouca potência): emita e suba o **USB MOD GAIN** no rádio (ou o **Nível TX** na página) até o **ALC** do rádio **mal se mexer**. O RADE é quase uma portadora contínua: atenção ao aquecimento do amplificador em emissões longas.

As escolhas (rádio, velocidade, dispositivos) ficam memorizadas no browser.

## Limitações

- Só **RADE V1** (o modo atual do FreeDV).
- O fim de emissão é enviado mas **sem indicativo**, por isso não aparece no **FreeDV Reporter**. Para isso use o programa FreeDV oficial.
- A voz chega ao ar cerca de 0,4 s depois de falar; a receção tem cerca de 0,25 s de atraso.
- Ainda sem relatórios de QSO no ar com os rádios Yaesu: os comandos CAT foram tirados do manual oficial e testados com uma porta série simulada. Diga como correu!

## Para quem mantém a página

- Código da página: `pt/rade-pt.src.html`; módulos WebAssembly: `pt/modules/`.
- Montar o `index.html`: `python pt/assemble.py build` (não precisa do Emscripten).
- Perfis de rádio: a lista `RIGS` no código (velocidade, comandos de PTT, dígitos do `FA`, comando de modo).
