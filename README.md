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

In this demo, the user can see how the CLI tool enhances a README file by automatically adding badges, a table of contents, and formatting the content for better readability.
```

```markdown
## Installation

```bash
pip install ai-readme-improver
```

```

## Usage

```bash
ai-readme-improver --config config.yaml --archive-dir oldreadme --logo company_logo.png --email hello@example.com
```

Briefly explain: This command runs the improver with your custom config, archives old files under oldreadme/, uses the specified company logo, and sets the contact email to hello@example.com.

## Features
- 📁 Archives previous README and suggestions
- 📝 Generates TL;DR summaries, suggestions, and full rewrites
- ⚙️ Configurable via config.yaml
- ⚡ GitHub Action integration
- 🔒 Commits only on real changes

## Configuration

| Key           | Description                                 | Default                  |
| ------------- | ------------------------------------------- | ------------------------ |
| project_name  | The name of the project                     | None                     |
| logo_path     | The file path to the project's logo image   | None                     |
| email         | The contact email address for the project   | None                     |
| badges        | Whether to display badges on the project    | True                     |
| extra_sections| Additional sections to include in the project documentation | None  |

```markdown
## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Submitting pull requests
- Writing tests
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Maintainers
- John Smith (@johnsmith)
- Sarah Johnson (@sarahjohnson)
- Michael Lee (@michaellee)

## Acknowledgements

- The OpenAI team for their support and collaboration throughout this project.
- Our community contributors for their valuable feedback and contributions.
- Our mentors for their guidance and expertise.
- Our friends and family for their endless support and encouragement.

```markdown
## Contact

- Email: hamzahabib10@gmail.com
```