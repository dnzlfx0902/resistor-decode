# Decodificador de resistencias de 4 y 5 bandas

Traduce bandas de color a ohmios y de ohmios a bandas para resistencias de 4 y 5 bandas, validando cada banda contra su posición y con tabla de casos conocidos en los tests.

`electronica` · 2026-10-27

## Instalación

```bash
python3 --version   # 3.10 o superior
# sin dependencias: sólo biblioteca estándar
```

## Uso

```bash
python3 resistor_decode.py --demo
python3 resistor_decode.py --bandas rojo violeta marron oro
python3 resistor_decode.py --ohmios 4700
```

Salida real de una corrida de ejemplo:

```text
rojo violeta marron oro                ->     270 Ω ±5%
amarillo violeta negro rojo marron     ->     47 kΩ ±1%
codificar(470 Ω) = amarillo violeta marron oro
```

## Cómo probar

```bash
python3 -m unittest discover -s tests -v
```

## Estructura

```text
2026-10-27-resistor-decode/
├── .github/
│   └── workflows/
│       └── ci-python.yml
├── .gitignore
├── LICENSE
├── resistor_decode.py
└── tests/
    └── test_resistor_decode.py
```

## Licencia

Distribuido bajo la licencia MIT.
