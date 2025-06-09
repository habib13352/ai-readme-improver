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

In this demo, you can see the CLI tool in action as it automatically generates a table of contents (TOC) for a README file. The tool also adds badges for build status and code coverage, enhancing the overall readability and professionalism of the document.
```

```markdown
## Installation

```bash
pip install ai-readme-improver
```

```

## Usage

```bash
ai-readme-improver --config config.yaml --archive-dir oldreadme --logo company_logo.png --email contact@company.com
```

Briefly explain: This command runs the improver with your custom config, archives old files under oldreadme/, uses company_logo.png as the logo, and sets the contact email to contact@company.com.

## Features
- 📚 Archives previous README and suggestions
- 📝 Generates TL;DR summaries, suggestions, and full rewrites
- ⚙️ Configurable via config.yaml
- 🚀 GitHub Action integration
- 🔒 Commits only on real changes

## Configuration

| Key            | Description                                  | Default                      |
| ---------------|----------------------------------------------|----------------------------- |
| project_name   | The name of the project                      | None                         |
| logo_path      | The path to the project's logo image         | None                         |
| email          | The email address associated with the project| None                         |
| badges         | Whether to display badges on the project page| True                         |
| extra_sections | Additional sections to include on the page   | None                         |

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

- We would like to thank the OpenAI team for their invaluable support and guidance throughout this project.
- Special thanks to our community contributors for their dedication and hard work in helping us achieve our goals.
- We are grateful for the assistance of our mentors and advisors who provided valuable insights and feedback along the way.

## Contact
- Email: hamzahabib10@gmail.com