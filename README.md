# Biopark Toledo no Minecraft: Informática que Joga

Servidor educacional em Minecraft, inspirado nos espaços do Biopark Toledo, para ensinar informática e pensamento computacional a estudantes da educação básica por meio de missões.

Projeto de extensão da Faculdade Donaduzzi / Biopark Educação, em parceria com o Colégio Donaduzzi (Toledo - PR).

## Por onde começar

| Quero... | Arquivo |
|---|---|
| Entender o jogo | [docs/GDD.md](docs/GDD.md) |
| Montar um servidor igual | [docs/INSTALACAO.md](docs/INSTALACAO.md) |
| Ver os plugins | [docs/PLUGINS.md](docs/PLUGINS.md) |
| Ver zonas e regiões | [docs/MAPA_E_REGIOES.md](docs/MAPA_E_REGIOES.md) |
| Aplicar as aulas | [docs/ATIVIDADES.md](docs/ATIVIDADES.md) |
| Gerar as imagens das atividades | [docs/IMAGENS_ATIVIDADES.md](docs/IMAGENS_ATIVIDADES.md) |
| Registrar resultados | [docs/AVALIACAO_E_EVIDENCIAS.md](docs/AVALIACAO_E_EVIDENCIAS.md) |
| Saber o que está pronto | [docs/STATUS.md](docs/STATUS.md) |
| Ler as falas dos NPCs | [dialogos/](dialogos/) |

## Estrutura

```text
docs/         GDD, instalação, plugins, mapa, atividades, avaliação e status
dialogos/     falas dos NPCs em .txt, uma trilha por arquivo
config/       modelos de quests, NPCs, regiões e server.properties
schematics/   construções prontas para o WorldEdit (.schem)
assets/       letreiro em PNG para o ImageFrame
dados/        schemas JSON e planilhas em branco para presença e avaliação
tools/        scripts Python que geram os schematics e o letreiro
referencias/  fotos reais usadas como referência e capturas do servidor
```

## Resumo rápido

1. Crie um servidor Paper e instale os plugins de [docs/PLUGINS.md](docs/PLUGINS.md).
2. Copie `schematics/` para `plugins/WorldEdit/schematics/`.
3. Cole as construções, crie as regiões e os NPCs, seguindo [docs/INSTALACAO.md](docs/INSTALACAO.md).
4. Ajuste os UUIDs dos NPCs em `config/quests.yml` e copie o arquivo para `plugins/Quests/`.
5. Teste todas as missões com uma conta de aluno antes de abrir o servidor.

## Direitos e privacidade

- Marcas e logos da Biopark e da Donaduzzi pertencem às instituições. Confirme a autorização antes de tornar este repositório público.
- O letreiro em `assets/` é um redesenho aproximado, não o logo oficial.
- Texturas e arquivos do jogo não fazem parte deste repositório.
- Nunca versione dados de alunos, listas de presença preenchidas, logs de sessões com nomes de jogadores ou fotos de menores.
