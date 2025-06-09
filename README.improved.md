# AI README Improver

![Logo](assets/logo.png)

[![Build Status](https://img.shields.io/github/actions/workflow/status/habib13352/ai-readme-improver/readme-improver.yml?branch=main)](https://github.com/habib13352/ai-readme-improver/actions) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Contents

- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Maintainers](#maintainers)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

```markdown
## Demo

![Demo](assets/demo.gif)

In this demo, the CLI tool is shown improving a README by adding badges, table of contents, and formatting the content for better readability.
```

## Installation

```bash
pip install ai-readme-improver
```

```

## Usage

```bash
ai-readme-improver --config config.yaml --archive-dir oldreadme --logo company_logo.png --email user@example.com
```

Briefly explain: This command runs the improver with your custom config, archives old files under oldreadme/, adds the company logo to the readme, and includes the user's email for contact information.

## Features  
- 📚 Archives previous README and suggestions  
- 📝 Generates TL;DR summaries, suggestions, and full rewrites  
- ⚙️ Configurable via config.yaml  
- 🤖 GitHub Action integration  
- 💡 Commits only on real changes

## Configuration

| Key           | Description                                   | Default           |
|---------------|-----------------------------------------------|-------------------|
| project_name  | The name of the project                      | None              |
| logo_path     | The path to the project's logo image          | None              |
| email         | The email address for project communication   | None              |
| badges        | List of badges to display in the README       | None              |
| extra_sections| List of additional sections to include in README | None            |

```markdown
## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Submitting pull requests
- Writing tests
```

```markdown
## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
```

## Maintainers
- Hamza Ali Habib (@habib13352)

## Acknowledgements
- The OpenAI team for their valuable insights and support.
- Our community contributors for their dedication and feedback.

## Contact
- Email: hamzahabib10@gmail.com