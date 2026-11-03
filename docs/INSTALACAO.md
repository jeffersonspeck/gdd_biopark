# Como montar um servidor igual

Este guia considera uma hospedagem com painel, como a EnxadaHost. Em outro host, os passos são os mesmos.

> **Teste antes de usar com alunos.** Os schematics e os modelos de configuração deste repositório ainda não foram testados em um servidor. Veja [STATUS.md](STATUS.md).

## 1. Criar o servidor

1. Crie um servidor **Paper** na mesma versão do jogo usada pela turma.
2. Use a versão do Java exigida por essa versão do Paper.
3. Reserve ao menos 4 GB de RAM para uma turma de cerca de 30 alunos e ajuste conforme o uso.
4. Copie `config/server.properties.exemplo` e aplique os valores no `server.properties`.
5. Inicie uma vez, aceite o EULA e pare o servidor.

## 2. Instalar os plugins

Baixe os plugins listados em [PLUGINS.md](PLUGINS.md) nas páginas oficiais, envie para `plugins/` e reinicie.

Confira no console se todos carregaram:

```text
plugins
```

## 3. Preparar o mundo

Crie um mundo plano e, no jogo, defina as regras:

```text
/gamerule doDaylightCycle false
/gamerule doMobSpawning false
/gamerule keepInventory true
/gamerule doFireTick false
/time set day
/weather clear
/defaultgamemode adventure
```

Alguns nomes de gamerule podem mudar entre versões do jogo. Use o preenchimento automático do chat para conferir.

Depois, ligue a lista de permissão:

```text
/whitelist on
/whitelist add NomeDoJogador
```

## 4. Colar as construções

1. Envie os arquivos de `schematics/` para `plugins/WorldEdit/schematics/`.
2. No jogo, fique onde deve ficar o canto noroeste e mais baixo da construção.
3. Rode:

```text
//schem load fachada_colegio_donaduzzi
//paste
```

```text
//schem load painel_circuitos
//paste
```

As zonas das trilhas usam os mesmos comandos, com os nomes da tabela abaixo. A zona `trilha_t4_painel` já inclui o painel, então use uma ou outra.

A fachada olha para o sul (+Z). Para girar antes de colar, use `//rotate 90` depois de carregar o arquivo. Se errar, use `//undo`.

| Arquivo | Tamanho (L × A × C) | Conteúdo |
|---|---|---|
| `fachada_colegio_donaduzzi.schem` | 123 × 19 × 35 | Portal, alas, torre, calçada, árvores, bancos e palmeiras |
| `painel_circuitos.schem` | 46 × 20 × 14 | Painel de 40 × 18 e bancadas AND, OR e NOT |
| `trilha_t1_lab_hardware.schem` | 27 × 10 × 51 | Laboratório com peças gigantes do computador |
| `trilha_t2_rua_redes.schem` | 83 × 19 × 37 | Calçada com computador, roteador e servidor |
| `trilha_t3_sala_hexagonal.schem` | 47 × 10 × 39 | Sala com mesas hexagonais |
| `trilha_t4_painel.schem` | 61 × 26 × 55 | Painel de circuitos dentro do laboratório |

## 5. Colocar o letreiro

1. Hospede `assets/letreiro_donaduzzi_42x5.png` em uma URL acessível pelo servidor.
2. Crie a imagem no ImageFrame com 42 × 5 mapas. Veja a sintaxe em `/imageframe help`, pois ela pode variar conforme a versão.
3. Coloque molduras de item sobre o painel azul da fachada e aplique os mapas.
4. Na Sala Hexagonal, faça o mesmo com `logo_faculdade_12x4.png` e `frase_parede_12x4.png`, na parede bordô. Cada imagem usa 12 × 4 mapas.

## 6. Proteger as regiões

Siga [MAPA_E_REGIOES.md](MAPA_E_REGIOES.md) e use os comandos de `config/worldguard_regioes.txt`.

## 7. Criar os NPCs

1. Vá ao ponto de cada NPC e rode os comandos de `config/citizens_npcs.txt`.
2. Anote o UUID de cada NPC. Com ele selecionado, use `/npc select` e `/npc id` ou consulte `plugins/Citizens/saves.yml`.

## 8. Configurar as missões

1. Abra `config/quests.yml`.
2. Substitua cada `UUID_...` pelo UUID real do NPC.
3. Ajuste as coordenadas em `locations-to-reach`.
4. Copie para `plugins/Quests/quests.yml` e reinicie o servidor ou use `/questadmin reload`.
5. Veja `/quests` no jogo para confirmar que todas carregaram.

## 9. Pacote de texturas (opcional)

Coloque a URL e o hash SHA-1 do pacote em `resource-pack` e `resource-pack-sha1` no `server.properties`. Mantenha `require-resource-pack=false` para não impedir a entrada de quem tem computador mais fraco.

## 10. Checklist antes da primeira sessão

- [ ] Todos os plugins aparecem em verde no comando `plugins`.
- [ ] Uma conta de aluno entra no servidor em modo aventura.
- [ ] A conta de aluno não quebra blocos fora das áreas de atividade.
- [ ] As bancadas AND, OR e NOT respondem como a tabela-verdade.
- [ ] Todas as missões podem ser iniciadas e concluídas.
- [ ] As falas aparecem com acentos corretos.
- [ ] Foi feito um backup do mundo.
- [ ] A lista de permissão contém apenas os participantes.

## 11. Operação

- Faça backup antes de cada sessão.
- Atualize os plugins fora do horário das aulas e em uma cópia do servidor.
- Baixe os logs ao final de cada sessão pelo painel da hospedagem. Eles ficam em `logs/`.
- Guarde os logs fora do repositório, pois eles contêm nomes de jogadores.
