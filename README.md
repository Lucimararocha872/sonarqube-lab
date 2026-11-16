# SonarQube Lab 🔍

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![SonarQube](https://img.shields.io/badge/SonarQube-Community%20Build-4E9BCD?logo=sonarqube&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-local-2496ED?logo=docker&logoColor=white)
![pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)

> 🇺🇸 Hands-on lab to understand static code analysis with **SonarQube Community Build**: Quality Gates, issues, coverage and the *Clean as You Code* approach.
>
> 🇧🇷 Laboratório prático para entender análise estática de código com o **SonarQube Community Build**: Quality Gates, issues, coverage e a abordagem *Clean as You Code*.

---

## 📌 About / Sobre

**🇺🇸** This repository contains a small Python application with **intentional problems** (security, reliability and maintainability) used to run real SonarQube analyses locally. The goal was to learn, in practice, how SonarQube evaluates code, how the Quality Gate reacts to new code and what the limitations of the free Community Build are.

**🇧🇷** Este repositório contém uma pequena aplicação Python com **problemas colocados de propósito** (segurança, confiabilidade e manutenção), usada para rodar análises reais do SonarQube localmente. O objetivo foi aprender, na prática, como o SonarQube avalia o código, como o Quality Gate reage ao código novo e quais são as limitações do Community Build, a versão gratuita.

---

## 🧰 Stack

| Tool / Ferramenta | Role / Função |
| --- | --- |
| SonarQube Community Build (Docker) | Analysis server / Servidor de análise |
| SonarScanner CLI (Docker) | Sends the analysis to the server / Envia a análise ao servidor |
| Python 3.12 + pytest + pytest-cov | App, tests and coverage report / Aplicação, testes e relatório de coverage |
| Ubuntu on WSL2 | Development environment / Ambiente de desenvolvimento |

---

## 🗂️ Structure / Estrutura

```
sonarqube-lab/
├── app/
│   ├── calculos.py        # clean code, fully tested / código limpo e testado
│   └── usuarios.py        # intentional issues, no tests / problemas propositais, sem testes
├── tests/
│   └── test_calculos.py
├── .coveragerc            # relative paths for the containerized scanner / caminhos relativos
├── requirements-dev.txt
└── sonar-project.properties
```

---

## 🚀 How to run / Como executar

### 1. Start SonarQube / Subir o SonarQube

**🇺🇸** The JVM memory limits keep SonarQube usable on machines with ~8 GB of RAM. On Linux/WSL, Elasticsearch requires `vm.max_map_count >= 524288`.

**🇧🇷** Os limites de memória da JVM deixam o SonarQube utilizável em máquinas com ~8 GB de RAM. No Linux/WSL, o Elasticsearch exige `vm.max_map_count >= 524288`.

```bash
sudo sysctl -w vm.max_map_count=524288

docker run -d --name sonarqube -p 9000:9000 \
  -e SONAR_WEB_JAVAOPTS="-Xmx512m -Xms128m" \
  -e SONAR_CE_JAVAOPTS="-Xmx512m -Xms128m" \
  -e SONAR_SEARCH_JAVAOPTS="-Xmx512m -Xms512m" \
  -v sonarqube_data:/opt/sonarqube/data \
  -v sonarqube_extensions:/opt/sonarqube/extensions \
  -v sonarqube_logs:/opt/sonarqube/logs \
  sonarqube:community

docker logs -f sonarqube   # wait for / aguarde "SonarQube is operational"
```

Open / Acesse: `http://localhost:9000` (first login / primeiro acesso: `admin` / `admin`).

### 2. Create the project and token / Criar o projeto e o token

**🇺🇸** *Create a local project* → project key `sonarqube-lab` (must match `sonar-project.properties`) → new code following the instance default → *Locally* → generate a **project token**.

**🇧🇷** *Create a local project* → project key `sonarqube-lab` (precisa ser igual à do `sonar-project.properties`) → new code seguindo o padrão da instância → *Locally* → gerar um **project token**.

### 3. Run tests with coverage / Rodar os testes com coverage

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest --cov --cov-report=xml
```

### 4. Run the scanner / Rodar o scanner

**🇺🇸** Both containers share a Docker network, so the scanner reaches the server by its container name.

**🇧🇷** Os dois containers ficam na mesma rede Docker, então o scanner encontra o servidor pelo nome do container.

```bash
docker network create sonar-net
docker network connect sonar-net sonarqube
export SONAR_TOKEN="<your-token>"

docker run --rm --network sonar-net \
  -e SONAR_HOST_URL="http://sonarqube:9000" \
  -e SONAR_TOKEN="$SONAR_TOKEN" \
  -v "$PWD:/usr/src" \
  sonarsource/sonar-scanner-cli
```

---

## 🧪 The experiment / O experimento

**🇺🇸** Three analyses were run on `main`, each after merging a Pull Request:

**🇧🇷** Foram feitas três análises na `main`, cada uma depois do merge de um Pull Request:

| # | Change / Mudança | Quality Gate | Issues (overall) |
| --- | --- | --- | --- |
| 1 | Initial code with 2 security issues (`random` for tokens, `md5`) / Código inicial com 2 problemas de segurança | ✅ Passed | 2 |
| 2 | Fixed both, but added a new one (`random` in a new function) / Corrigiu os dois, mas introduziu um novo | ❌ Failed | 1 |
| 3 | Fixed the new issue with `secrets` / Corrigiu o novo problema com `secrets` | ✅ Passed | 0 |

**🇺🇸** Analysis #2 is the key one: the codebase **improved overall** (2 → 1 issue), yet the Quality Gate **failed** because a *new* issue was introduced. That is *Clean as You Code*: the gate judges what enters the code, not the legacy.

**🇧🇷** A análise nº 2 é a principal: o código **melhorou no geral** (de 2 para 1 issue), mas o Quality Gate **falhou** porque entrou uma issue *nova*. Isso é o *Clean as You Code*: o gate avalia o que entra no código, não o legado.

---

## 💡 Key learnings / Principais aprendizados

- **🇺🇸** **Community Build analyzes only the main branch.** No branch/PR analysis and no PR decoration. Analyzing another branch overwrites the project result.
  **🇧🇷** **O Community Build analisa só a branch principal.** Não tem análise de branch/PR nem comentários no PR. Analisar outra branch sobrescreve o resultado do projeto.

- **🇺🇸** **SonarQube does not watch the repository.** A merge alone triggers nothing: the scanner must run, usually in a CI pipeline on every push to `main`.
  **🇧🇷** **O SonarQube não monitora o repositório.** O merge sozinho não dispara nada: o scanner precisa rodar, normalmente numa pipeline de CI a cada push na `main`.

- **🇺🇸** **The first analysis always passes.** There is no "new code" yet, so the Quality Gate has nothing to evaluate.
  **🇧🇷** **A primeira análise sempre passa.** Ainda não existe "código novo", então o Quality Gate não tem o que avaliar.

- **🇺🇸** **Coverage and duplication conditions are skipped for small changes** (fewer than 20 new lines), to avoid failing tiny changes on percentages.
  **🇧🇷** **As condições de coverage e duplicação são ignoradas em mudanças pequenas** (menos de 20 linhas novas), para não reprovar mudanças mínimas por percentual.

- **🇺🇸** **Findings depend on the Quality Profile.** The default *Sonar way* does not enable every rule (e.g. unused imports were not flagged). Custom rules require a custom profile.
  **🇧🇷** **O que é apontado depende do Quality Profile.** O *Sonar way* padrão não ativa todas as regras (ex.: import não usado não foi apontado). Regras extras exigem um perfil próprio.

- **🇺🇸** **Security Hotspots are deprecated in recent versions.** In Community Build 26.x they show up as security issues instead.
  **🇧🇷** **Os Security Hotspots foram descontinuados nas versões recentes.** No Community Build 26.x eles aparecem como issues de segurança.

- **🇺🇸** **Instance mode: MQR vs Standard Experience.** This instance runs in MQR mode (Security / Reliability / Maintainability with High / Medium / Low severities).
  **🇧🇷** **Modo da instância: MQR vs Standard Experience.** Esta instância roda em modo MQR (Security / Reliability / Maintainability com severidades High / Medium / Low).

---

## 🛠️ Troubleshooting

| Problem / Problema | Fix / Solução |
| --- | --- |
| PC freezes while SonarQube starts / PC trava na inicialização | Limit JVM memory with `SONAR_*_JAVAOPTS`; stop it when idle with `docker stop sonarqube` / Limitar a memória com `SONAR_*_JAVAOPTS`; parar quando não usar |
| Coverage shows 0% / Coverage aparece 0% | Generate `coverage.xml` before the scanner and use `relative_files = True` / Gerar o `coverage.xml` antes do scanner e usar `relative_files = True` |
| Scanner can't reach `localhost:9000` / Scanner não alcança o servidor | Put both containers on the same Docker network / Colocar os dois containers na mesma rede Docker |
| Result didn't change after merge / Resultado não mudou após o merge | Run the scanner again on `main` / Rodar o scanner de novo na `main` |

---

## 🔭 Next steps / Próximos passos

- **🇺🇸** Automate the analysis with GitHub Actions on every push to `main`.
  **🇧🇷** Automatizar a análise com GitHub Actions a cada push na `main`.
- **🇺🇸** Create a custom Quality Profile enabling extra rules.
  **🇧🇷** Criar um Quality Profile próprio com regras extras.
- **🇺🇸** Run SonarQube on a cloud VM with PostgreSQL instead of the embedded database.
  **🇧🇷** Rodar o SonarQube numa VM na nuvem com PostgreSQL, no lugar do banco embutido.

---

## 👩‍💻 Author / Autora

**Lucimara Silva**: Cloud / DevOps Engineer · GCP Associate Cloud Engineer