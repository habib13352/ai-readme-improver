# README Improver

![Logo](assets/logo.png)

*Genera README pulidos con un solo comando.*

[Read this in English](README.md)

[![CI](https://github.com/username/ai-readme-improver/actions/workflows/readme-improver.yml/badge.svg?branch=main)](https://github.com/username/ai-readme-improver/actions/workflows/readme-improver.yml)
[![Docs](https://img.shields.io/badge/docs-passing-brightgreen)](https://github.com/username/ai-readme-improver/actions/workflows/auto-docs.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](pyproject.toml)

README Improver es una herramienta de línea de comandos y GitHub Action que usa OpenAI para mejorar archivos `README.md`. Genera un breve resumen, sugerencias y una versión reescrita del documento.

## Características

- 📄 Genera un resumen TL;DR y sugerencias de mejora
- 📝 Produce un README reescrito con estilo moderno
- 🧩 Funciona localmente o como GitHub Action

## Tabla de Contenidos

1. [Instalación](#instalación)
2. [Uso](#uso)
3. [Configuración de GitHub Action](#configuración-de-github-action)
4. [Contribuir](#contribuir)
5. [Licencia](#licencia)
6. [Mantenedores](#mantenedores)
7. [Agradecimientos](#agradecimientos)
8. [Contacto](#contacto)

## Instalación

Instala README Improver en un entorno de Python 3.10:

1. **Crea un entorno virtual**
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configura la clave de API**
   ```bash
   cp .env.example .env
   echo "OPENAI_API_KEY=tu-clave" >> .env
   ```

## Uso

La herramienta analiza y reescribe el README del directorio actual.

```bash
git clone https://github.com/username/ai-readme-improver.git
cd ai-readme-improver
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=tu-clave
python main.py --readme README.md --improved README.improved.md
```

Opciones principales:

- `--model` – modelo de OpenAI (por defecto `gpt-3.5-turbo`).
- `--summary-prompt`, `--suggest-prompt`, `--rewrite-prompt` – sobrescribe los prompts.
- `--verbose` – activa registro detallado.

Tras ejecutar, `suggestions.md` contiene el resumen y la lista de mejoras, mientras que `README.improved.md` guarda el documento reescrito. Los registros se almacenan en `logs/`.

## Configuración de GitHub Action

Configura la acción para mejorar automáticamente el README en las pull requests añadiendo el siguiente workflow a `.github/workflows/readme-improver.yml`:

```yaml
name: "README Improver CI"
on:
  pull_request:
    paths: ["README.md"]
jobs:
  improve-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: pip install "openai>=1.0" python-dotenv markdown2
      - run: echo "OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}" >> $GITHUB_ENV
      - run: python main.py
      - name: Replace README with improved version
        run: |
          mv README.improved.md README.md
          rm suggestions.md
      - name: Commit improved README
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md
          git diff --cached --quiet || git commit -m "chore: apply AI-suggested README improvements"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - uses: actions/upload-artifact@v4
        with:
          name: readme-improver-logs
          path: logs
      - run: python post_comment.py
```

## Contribuir

Las contribuciones como reportes de errores o pull requests son bienvenidas.

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).

## Mantenedores

- Alice Johnson (@alicej)
- Bob Smith (@bobsmith)

## Agradecimientos

Gracias a OpenAI y a la comunidad por sus comentarios.

## Contacto

- Email: you@example.com
