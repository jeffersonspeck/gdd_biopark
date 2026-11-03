# Imagens das atividades

As 13 missões têm uma ilustração em `referencias/atividades/`, usada em [ATIVIDADES.md](ATIVIDADES.md). As imagens mostram o que cada atividade propõe e não comprovam que ela aconteceu. Para isso, use capturas e registros das sessões.

| Missão | Arquivo | O que mostra |
|---|---|---|
| M0 Primeiros passos | `m0.jpg` | Chegada ao Hub, em frente à fachada |
| T1.1 Peças do computador | `t1_1.jpg` | Peças gigantes no Laboratório de Hardware |
| T1.2 Caminho da informação | `t1_2.jpg` | Quadros de entrada, processamento, armazenamento e saída |
| T1.3 O gerente da máquina | `t1_3.jpg` | Pergunta com portas de resposta |
| T2.1 Viagem do pacote | `t2_1.jpg` | Percurso da Rua das Redes |
| T2.2 Senha forte | `t2_2.jpg` | Portas com senhas de exemplo |
| T2.3 Golpe ou verdade? | `t2_3.jpg` | Placas com mensagens classificadas |
| T3.1 Texto bem feito | `t3_1.jpg` | Documento com título, parágrafo e lista |
| T3.2 Planilha de recursos | `t3_2.jpg` | Planilha com soma e gráfico |
| T3.3 Apresentação do mapa | `t3_3.jpg` | Slide de apresentação |
| T4.1 Liga e desliga | `t4_1.jpg` | Bancada com alavanca e lâmpada |
| T4.2 As três portas | `t4_2.jpg` | Bancadas AND, OR e NOT, com tabela-verdade |
| T4.3 Construa seu circuito | `t4_3.jpg` | Dupla com dois botões e uma porta |

## Como gerar

1. Instale as dependências:

```bash
pip install numpy pillow
```

2. Extraia as texturas do `.jar` do seu cliente para uma pasta fora do repositório. A pasta precisa conter os `.png` de `assets/minecraft/textures/block/`. As texturas não são versionadas nem redistribuídas.

3. Rode, indicando a pasta das texturas e a de saída:

```bash
python tools/gerar_imagens_atividades.py PASTA_DAS_TEXTURAS referencias/atividades
```

Para refazer só algumas imagens, acrescente os nomes ao final, como `t4_1 t4_2`.

## Como o script funciona

- `tools/gerar_imagens_atividades.py` monta cada cena sobre as zonas de `gerar_cenarios.py` e `gerar_fachada.py`, acrescentando quadros, botões e NPCs.
- `tools/render_voxel.py` desenha os blocos com a câmera e a luz definidas para cada imagem.
- Para mudar uma cena, edite a chamada `add(...)` correspondente: bloco, posição da câmera, alvo, quadros e NPCs.

## Limitações

- Quadros, botões e NPCs existem só nas imagens e não fazem parte dos `.schem`. No servidor, crie-os com ImageFrame, blocos e Citizens.
- A fonte dos textos é a Arial Rounded Bold, do Windows. Em outro sistema, o script usa a fonte padrão do Pillow.
