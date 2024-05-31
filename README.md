# CRYPTO DASHBOARD

[![Versiones de Python](https://img.shields.io/pypi/pyversions/dash)](https://www.python.org/downloads/)

Un dashboard versátil construido con Dash (Python) para monitorear los gráficos de precios de las criptomonedas ETHUSDT y XRPUSDT en el exchange BYBIT. Aprovecha la API de BYBIT y se conecta a su cuenta para supervisar las posiciones abiertas. Además, cuenta con un tablero de inteligencia de negocios que presenta la última P&L, ganancias / pérdidas acumuladas, y su saldo actual.

## Índice

- [Introducción](#introducción)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Roadmap](#roadmap)
- [Autores](#autores)

## Introducción

Este proyecto es un panel de control de criptomonedas diseñado para proporcionar monitorización y análisis en tiempo real de los movimientos de precios de ETHUSDT y XRPUSDT en la bolsa BYBIT. Utiliza el poderoso framework Dash para construir aplicaciones web interactivas con Python.

## Características

- Gráficos de precios**: Gráficos de velas interactivos para ETHUSDT y XRPUSDT, impulsados por la API de BYBIT.
- Posiciones abiertas**: Recupere y muestre sus posiciones abiertas en BYBIT.
- Seguimiento de pérdidas y ganancias**: Supervise sus pérdidas y ganancias actuales y acumuladas.
- Saldo de cuenta**: Realice un seguimiento del saldo actual de su cuenta.
- Diseño responsivo**: El panel de control está optimizado para distintos tipos de dispositivo.

## Instalación

Para instalar las dependencias necesarias para este proyecto, necesitas Python 3.9 o 3.10. Usa el siguiente comando con `pip` para instalar los paquetes necesarios:

```bash
pip install -r requisitos.txt
```
## Uso

1. Actualice el archivo de credenciales ubicado en `config/.env` con sus credenciales de entorno de la API de BYBIT.
2. Ejecuta el archivo `app.py` para iniciar la aplicación Dash.
3. Acceda al panel de control navegando a la URL proporcionada en su navegador web
   * --> Prueba en vivo: https://dashboard-prototype.onrender.com/

## Roadmap

### Próximas características

1. **Operación basada en web**: Habilitar la capacidad de ejecutar operaciones directamente desde el tablero web, permitiendo a los usuarios colocar órdenes de compra y venta sin problemas.
2. **Optimización del rendimiento**: Optimizar el cuadro de mandos para un mejor rendimiento, incluyendo una recuperación de datos más rápida, una renderización eficiente y una latencia reducida.
3. **Gráficos avanzados**: Introducir capacidades avanzadas de gráficos, como indicadores técnicos personalizables, herramientas de dibujo y múltiples diseños de gráficos.
4. **Sistema de notificaciones**: Implemente un sistema de notificaciones para alertar a los usuarios sobre movimientos significativos del mercado, objetivos de precios u otros eventos importantes.
5. **Gestión de carteras**: Integrar funciones de gestión de carteras, permitiendo a los usuarios realizar un seguimiento de sus tenencias generales de criptodivisas, la asignación de activos y el rendimiento a través de múltiples intercambios.
6. **Preferencias del usuario**: Permitir a los usuarios personalizar el panel de control de acuerdo a sus preferencias, tales como temas de color, diseño y configuración predeterminada.

## Autores
<table>
  <tr>
<td align="center"><a href="https://github.com/Aviles17"><img src="https://avatars.githubusercontent.com/u/110882455?v=4" width="100px;" alt=""/><br /><sub><b>Santiago Avilés</b></sub></a><br /></td>
<td align="center"><a href="https://github.com/SBoteroP"><img src="https://avatars.githubusercontent.com/u/68749776?s=400&u=985d505e9c62f2f7fa7d08a46e406a451995b5a4&v=4" width="100px;" alt=""/><br /><sub><b>Santiago Botero</b></sub></a><br /></td>
  </tr>
</table>

## Disclaimer

Trading cryptocurrencies involves financial risks. We do not guarantee any profits, and users are advised to understand the risks and adjust the settings according to their preferences and risk tolerance. This project is provided under the MIT License. Please review the [LICENSE](LICENSE) file for more details.

**Note:** Ensure you thoroughly review and understand the code before implementing it in a live trading environment. We are not responsible for any financial losses incurred from using this dashboard.
