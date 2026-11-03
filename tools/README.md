# Ferramentas

Os scripts geram os arquivos na pasta atual.

```bash
python gerar_fachada.py
python gerar_painel.py
python gerar_letreiro.py
python gerar_cenarios.py
```

- `gerar_fachada.py` e `gerar_painel.py` usam apenas a biblioteca padrão do Python e criam um `.schem` (Sponge Schematic v2).
- `gerar_letreiro.py` precisa do Pillow (`pip install pillow`) e da fonte Arial Rounded Bold.
- `gerar_cenarios.py` cria as zonas das trilhas e também usa só a biblioteca padrão.
- `gerar_imagens_atividades.py` e `render_voxel.py` criam as ilustrações das missões. Veja [IMAGENS_ATIVIDADES.md](../docs/IMAGENS_ATIVIDADES.md).
- Para mudar a construção, edite as chamadas de `box(...)`. Cada uma preenche um bloco em um intervalo de x, y e z.
- Eixos: x para a direita, y para cima, z para a frente da fachada.
