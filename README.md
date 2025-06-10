# Tomasulo Visual Simulator 🎯

Simulador interativo e visual do algoritmo de Tomasulo, com foco didático. Suporta instruções MIPS, especulação de desvios e cálculo de métricas como IPC e ciclos de bolha.

## ✨ Funcionalidades

- Execução passo a passo
- Estações de reserva e buffers de reordenação
- Suporte a especulação de desvios condicional
- Visualização em tempo real dos registradores, ROB e instruções
- Cálculo de métricas: IPC, ciclos totais, ciclos de bolha

## 📸 Interface (em desenvolvimento)

> Capturas de tela ou GIFs virão aqui

## 🚀 Como rodar

### 1. Clonar o repositório

```bash
git clone https://github.com/usuario/tomasulo-educational-simulator.git
cd tomasulo-educational-simulator
```

### 2. Instalar dependências (ex: Python + PyQt5)
```
pip install -r requirements.txt
```

### 3. Executar o simulador
```
python main.py
```

## 🗂️ Estrutura do projeto
```
tomasulo-educational-simulator/
├── gui/                    # Interface gráfica (Qt, ImGui, etc)
│   └── ...
├── core/                   # Lógica do simulador (Tomasulo, ROB, etc)
│   ├── instruction.py
│   ├── simulator.py
│   ├── reservation_station.py
│   ├── rob.py
│   ├── register_file.py
│   └── ...
├── utils/                  # Funções auxiliares e métricas
│   └── metrics.py
├── examples/               # Exemplos de instruções MIPS para testes
│   └── selection-sort.mips
├── tests/                  # Testes unitários e de integração
│   └── ...
├── main.py                 # Ponto de entrada do simulador
├── requirements.txt        # Dependências Python (ou pom.xml, CMakeLists.txt, etc.)
└── README.md               # Este arquivo
```

## 🤝 Contribuições
Contribuições são bem-vindas! Veja as issues ou abra um PR.

### 📁 Detalhamento das pastas

| Pasta       | Conteúdo                                                                                                                                 |
|-------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `core/`     | Toda a lógica do simulador de Tomasulo (componentes do algoritmo). **Independente da GUI.**                                             |
| `gui/`      | Código da interface gráfica. Conecta-se com `core/`.                                                                                     |
| `examples/` | Arquivos `.mips` ou `.txt` com exemplos de instruções. Úteis para demonstrar o simulador.                                               |
| `utils/`    | Código de apoio: cálculo de métricas, parser de instruções, etc.                                                                         |
| `tests/`    | Testes automatizados. Pode usar `pytest`, `unittest`, ou seu framework preferido.                                                        |
| `main.py`   | Executável principal que inicializa a GUI e conecta a simulação.                                                                         |

## 📚 Licença
Este projeto está licenciado sob a [MIT License](https://opensource.org/license/mit)
