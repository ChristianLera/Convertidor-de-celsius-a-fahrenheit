# 🌡️ Conversor Profesional de Temperatura

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

Aplicación de escritorio profesional con interfaz gráfica moderna para conversión de temperaturas entre Celsius y Fahrenheit.

## ✨ Características

- 🔄 **Conversión instantánea** con botón dedicado
- 📜 **Historial completo** de conversiones con fecha y hora
- 📊 **Estadísticas detalladas** de uso
- 🌓 **Tema claro/oscuro** intercambiable
- ⌨️ **Atajos de teclado** para mayor eficiencia
- 💾 **Persistencia de datos** (el historial se guarda automáticamente)
- 📤 **Exportación a TXT** del historial
- 🎨 **Interfaz profesional** con dos paneles de conversión
- ✅ **Validación de errores** amigable

## 🖼️ Capturas de Pantalla

*[Agrega aquí capturas de tu aplicación ejecutándose]*

## 🚀 Instalación y Ejecución

### Requisitos Previos

- Python 3.7 o superior instalado en tu sistema
- Tkinter (viene incluido con Python por defecto)

### En Windows

**Opción 1 - Script Batch:**
```batch
ejecutar.bat
```

**Opción 2 - Script PowerShell:**
```powershell
.\ejecutar.ps1
```

**Opción 3 - Manual:**
```bash
python ConvertidorGrados.py
```

### En Linux/Mac

```bash
python3 ConvertidorGrados.py
```

## ⌨️ Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| `Enter` | Convertir (según campo activo) |
| `Ctrl + C` | Limpiar todos los campos |
| `Ctrl + H` | Ver historial de conversiones |
| `F1` | Abrir ayuda |
| `Escape` | Salir de la aplicación |

## 📚 Referencias Rápidas

| Celsius | Fahrenheit | Referencia |
|---------|------------|------------|
| 0°C | 32°F | Congelación del agua |
| 100°C | 212°F | Ebullición del agua |
| 37°C | 98.6°F | Temperatura corporal |
| 20°C | 68°F | Temperatura ambiente |
| -40°C | -40°F | Punto de equivalencia |

## 📁 Estructura del Proyecto

```
Conversor-Temperatura/
├── ConvertidorGrados.py      # Archivo principal de la aplicación
├── historial_tkinter.json    # Historial de conversiones (se genera automáticamente)
├── ejecutar.bat              # Script de inicio para Windows
├── ejecutar.ps1              # Script de inicio para PowerShell
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

## 📊 Características Técnicas

- **Interfaz**: Tkinter con estilos personalizados
- **Persistencia**: JSON para almacenar historial
- **Validación**: Manejo robusto de errores de entrada
- **Temas**: Claro/Oscuro con actualización dinámica
- **Estadísticas**: Cálculo de mínimos, máximos y promedios

## 🛠️ Tecnologías Utilizadas

- **Python 3.7+** - Lenguaje de programación
- **Tkinter** - Biblioteca de interfaz gráfica
- **JSON** - Almacenamiento de datos
- **Datetime** - Registro temporal de conversiones

## 📝 Uso

1. Ingresa un valor numérico en el campo Celsius o Fahrenheit
2. Presiona el botón "CONVERTIR"
3. El resultado aparecerá instantáneamente
4. La conversión se guarda automáticamente en el historial
5. Puedes ver estadísticas y exportar tus conversiones

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Haz un Fork del proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## 👨‍💻 Autor

**Christian Lera**

---

## ⭐ Muestra tu apoyo

Si este proyecto te ha sido útil, ¡dale una estrella en GitHub!

---

*Versión: 2.1.0 | Última actualización: 2024*
