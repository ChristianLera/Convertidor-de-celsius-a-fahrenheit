"""
CONVERSOR DE TEMPERATURA PROFESIONAL CON TKINTER
------------------------------------------------
Aplicación de escritorio con interfaz gráfica moderna que incluye:
- Conversión en tiempo real
- Validación instantánea
- Historial visual
- Gráficos de tendencias
- Tema claro/oscuro
- Atajos de teclado

Autor: Christian Lera
Versión: 2.1.0
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
from typing import List, Dict


class ConversorTemperaturaPro:
    """
    Clase principal de la aplicación con interfaz gráfica profesional.
    """
    
    def __init__(self):
        """Inicializa la ventana principal y todos los componentes."""
        self.ventana = tk.Tk()
        self.ventana.title("🌡️ Conversor Profesional de Temperatura")
        self.ventana.geometry("700x800")
        self.ventana.resizable(True, True)
        
        # Definir variables de instancia
        self.historial: List[Dict] = []
        self.tema_actual = "claro"
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Inicializar variables tkinter
        self.valor_celsius = tk.StringVar()
        self.valor_fahrenheit = tk.StringVar()
        self.resultado_celsius = tk.StringVar()
        self.resultado_fahrenheit = tk.StringVar()
        
        # Cargar datos
        self.cargar_historial()
        
        # Configurar atajos
        self.configurar_atajos()
        
        # Construir interfaz
        self.crear_widgets()
        
        # Centrar ventana
        self.centrar_ventana()
        
    def configurar_estilos(self):
        """Configura los estilos y colores de la aplicación."""
        self.colores = {
            "claro": {
                "bg": "#f5f5f5",
                "fg": "#333333",
                "button": "#4CAF50",
                "button_hover": "#45a049",
                "entry": "white",
                "historial": "#ffffff"
            },
            "oscuro": {
                "bg": "#2d2d2d",
                "fg": "#ffffff",
                "button": "#2196F3",
                "button_hover": "#0b7dda",
                "entry": "#3d3d3d",
                "historial": "#3d3d3d"
            }
        }
        
        # Configurar ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.aplicar_tema()
    
    def aplicar_tema(self):
        """Aplica el tema actual a toda la aplicación."""
        if not hasattr(self, 'tema_actual'):
            self.tema_actual = "claro"
            
        colores = self.colores.get(self.tema_actual, self.colores["claro"])
        self.ventana.configure(bg=colores["bg"])
        
        self.style.configure('TFrame', background=colores["bg"])
        self.style.configure('TLabel', background=colores["bg"], foreground=colores["fg"])
        self.style.configure('TButton', background=colores["button"])
        self.style.map('TButton', background=[('active', colores["button_hover"])])
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def configurar_atajos(self):
        """Configura atajos de teclado para mejorar la experiencia."""
        self.ventana.bind('<Control-c>', lambda e: self.limpiar_campos())
        self.ventana.bind('<Control-h>', lambda e: self.mostrar_historial())
        self.ventana.bind('<Escape>', lambda e: self.confirmar_salida())
        self.ventana.bind('<F1>', lambda e: self.mostrar_ayuda())
        self.ventana.bind('<Return>', lambda e: self.convertir_activo())  # Enter para convertir
    
    def convertir_activo(self):
        """Detecta qué conversión está activa y la ejecuta."""
        # Verificar qué campo tiene el foco
        focus_widget = self.ventana.focus_get()
        if focus_widget and str(focus_widget).find('celsius_entry') != -1:
            self.convertir_cf()
        elif focus_widget and str(focus_widget).find('fahrenheit_entry') != -1:
            self.convertir_fc()
    
    def crear_widgets(self):
        """Crea todos los elementos de la interfaz."""
        
        # Frame principal con padding
        main_frame = ttk.Frame(self.ventana, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        titulo = ttk.Label(main_frame, text="🌡️ CONVERSOR PROFESIONAL DE TEMPERATURA",
                          font=('Arial', 18, 'bold'))
        titulo.pack(pady=10)
        
        subtitulo = ttk.Label(main_frame, text="Celsius ↔ Fahrenheit",
                             font=('Arial', 11))
        subtitulo.pack(pady=(0, 20))
        
        # Frame para los conversores (2 columnas)
        conversores_frame = ttk.Frame(main_frame)
        conversores_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Panel izquierdo: Celsius a Fahrenheit
        self.crear_panel_conversion(conversores_frame, "🌡️ Celsius → Fahrenheit", 
                                    self.valor_celsius, self.resultado_fahrenheit,
                                    self.convertir_cf, "left", "celsius_entry")
        
        # Panel derecho: Fahrenheit a Celsius
        self.crear_panel_conversion(conversores_frame, "🌡️ Fahrenheit → Celsius",
                                    self.valor_fahrenheit, self.resultado_celsius,
                                    self.convertir_fc, "right", "fahrenheit_entry")
        
        # Frame para botones de acción
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill=tk.X, pady=20)
        
        # Botones principales
        self.crear_boton(botones_frame, "📜 Ver Historial", self.mostrar_historial, 0)
        self.crear_boton(botones_frame, "📊 Estadísticas", self.mostrar_estadisticas, 1)
        self.crear_boton(botones_frame, "🧹 Limpiar", self.limpiar_campos, 2)
        self.crear_boton(botones_frame, "🌓 Cambiar Tema", self.cambiar_tema, 3)
        self.crear_boton(botones_frame, "❌ Salir", self.confirmar_salida, 4)
        
        # Barra de estado
        self.barra_estado = ttk.Label(main_frame, text="✅ Listo | Presiona F1 para ayuda | Enter para convertir",
                                      relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
    
    def crear_panel_conversion(self, parent, titulo, variable_entrada, variable_salida, 
                               comando, lado, entry_name):
        """
        Crea un panel de conversión completo.
        
        Args:
            parent: Frame padre
            titulo: Título del panel
            variable_entrada: Variable tkinter para entrada
            variable_salida: Variable tkinter para salida
            comando: Función de conversión
            lado: 'left' o 'right' para posicionamiento
            entry_name: Nombre identificador del entry
        """
        frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=2)
        frame.pack(side=lado, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título del panel
        ttk.Label(frame, text=titulo, font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Entry con validación - SIN binding automático
        ttk.Label(frame, text="Ingresa el valor:").pack(pady=(20, 5))
        entry = ttk.Entry(frame, textvariable=variable_entrada, font=('Arial', 12),
                          width=20)
        entry.pack(pady=5)
        entry._name = entry_name  # Asignar nombre para identificación
        
        # Botón de conversión (principal)
        colores_actual = self.colores[self.tema_actual]
        btn = tk.Button(frame, text="🔄 CONVERTIR", command=comando,
                       bg=colores_actual["button"],
                       fg="white", font=('Arial', 11, 'bold'),
                       padx=30, pady=8, cursor="hand2")
        btn.pack(pady=15)
        
        # Resultado
        ttk.Label(frame, text="RESULTADO:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        resultado_label = ttk.Label(frame, textvariable=variable_salida,
                                    font=('Arial', 18, 'bold'),
                                    foreground="#FF6B35")
        resultado_label.pack(pady=5)
        
        # Marco para el resultado con fondo
        resultado_frame = ttk.Frame(frame, relief=tk.SUNKEN, borderwidth=1)
        resultado_frame.pack(pady=5, padx=20, fill=tk.X)
        
        # Información adicional
        info_frame = ttk.Frame(frame)
        info_frame.pack(pady=20)
        
        if "Celsius →" in titulo:
            ttk.Label(info_frame, text="📚 REFERENCIAS RÁPIDAS", font=('Arial', 9, 'bold')).pack()
            ttk.Label(info_frame, text="• 0°C = 32°F (Congelación)", font=('Arial', 8)).pack()
            ttk.Label(info_frame, text="• 100°C = 212°F (Ebullición)", font=('Arial', 8)).pack()
            ttk.Label(info_frame, text="• 37°C = 98.6°F (Cuerpo humano)", font=('Arial', 8)).pack()
            ttk.Label(info_frame, text="• -40°C = -40°F (Equivalencia)", font=('Arial', 8)).pack()
        else:
            ttk.Label(info_frame, text="📚 REFERENCIAS RÁPIDAS", font=('Arial', 9, 'bold')).pack()
            ttk.Label(info_frame, text="• 32°F = 0°C (Congelación)", font=('Arial', 8)).pack()
            ttk.Label(info_frame, text="• 212°F = 100°C (Ebullición)", font=('Arial', 8)).pack()
            ttk.Label(info_frame, text="• 98.6°F = 37°C (Cuerpo humano)", font=('Arial', 8)).pack()
            ttk.Label(info_frame, text="• -40°F = -40°C (Equivalencia)", font=('Arial', 8)).pack()
    
    def crear_boton(self, parent, texto, comando, columna):
        """Crea un botón estilizado."""
        colores_actual = self.colores[self.tema_actual]
        btn = tk.Button(parent, text=texto, command=comando,
                       bg=colores_actual["button"],
                       fg="white", font=('Arial', 10, 'bold'),
                       padx=15, pady=8, cursor="hand2")
        btn.grid(row=0, column=columna, padx=5, pady=5)
    
    def convertir_cf(self):
        """Convierte Celsius a Fahrenheit - SOLO CON BOTÓN."""
        try:
            valor = self.valor_celsius.get().strip()
            if not valor:
                messagebox.showwarning("Campo vacío", "Por favor, ingresa un valor en Celsius")
                self.resultado_fahrenheit.set("")
                return
                
            celsius = float(valor)
            fahrenheit = round((celsius * 9/5) + 32, 2)
            self.resultado_fahrenheit.set(f"{fahrenheit} °F")
            self.registrar_conversion("C→F", celsius, fahrenheit)
            self.actualizar_barra(f"✅ {celsius}°C = {fahrenheit}°F")
            
            # Feedback visual - resaltar resultado
            self.ventana.after(100, lambda: self.actualizar_barra(f"✨ Conversión completada con éxito"))
            
        except ValueError:
            self.resultado_fahrenheit.set("❌ ERROR")
            messagebox.showerror("Error de entrada", 
                                f"'{valor}' no es un número válido.\n\nEjemplos válidos:\n• 25\n• -10.5\n• 37.2")
            self.actualizar_barra("⚠️ Error: Ingresa un número válido")
    
    def convertir_fc(self):
        """Convierte Fahrenheit a Celsius - SOLO CON BOTÓN."""
        try:
            valor = self.valor_fahrenheit.get().strip()
            if not valor:
                messagebox.showwarning("Campo vacío", "Por favor, ingresa un valor en Fahrenheit")
                self.resultado_celsius.set("")
                return
                
            fahrenheit = float(valor)
            celsius = round((fahrenheit - 32) * 5/9, 2)
            self.resultado_celsius.set(f"{celsius} °C")
            self.registrar_conversion("F→C", fahrenheit, celsius)
            self.actualizar_barra(f"✅ {fahrenheit}°F = {celsius}°C")
            
            # Feedback visual
            self.ventana.after(100, lambda: self.actualizar_barra(f"✨ Conversión completada con éxito"))
            
        except ValueError:
            self.resultado_celsius.set("❌ ERROR")
            messagebox.showerror("Error de entrada", 
                                f"'{valor}' no es un número válido.\n\nEjemplos válidos:\n• 77\n• 32.5\n• -40")
            self.actualizar_barra("⚠️ Error: Ingresa un número válido")
    
    def registrar_conversion(self, tipo, entrada, salida):
        """Registra la conversión en el historial."""
        registro = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo,
            "entrada": entrada,
            "salida": salida
        }
        self.historial.append(registro)
        self.guardar_historial()
    
    def guardar_historial(self):
        """Guarda el historial en archivo JSON."""
        try:
            with open("historial_tkinter.json", "w", encoding="utf-8") as f:
                json.dump(self.historial, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def cargar_historial(self):
        """Carga el historial desde archivo JSON."""
        try:
            with open("historial_tkinter.json", "r", encoding="utf-8") as f:
                self.historial = json.load(f)
        except:
            self.historial = []
    
    def mostrar_historial(self):
        """Muestra el historial en una ventana emergente."""
        if not self.historial:
            messagebox.showinfo("Historial", "No hay conversiones registradas aún.\n\nRealiza algunas conversiones primero.")
            return
        
        # Crear ventana de historial
        ventana_historial = tk.Toplevel(self.ventana)
        ventana_historial.title("📜 Historial de Conversiones")
        ventana_historial.geometry("650x450")
        ventana_historial.configure(bg=self.colores[self.tema_actual]["bg"])
        
        # Frame con scrollbar
        frame = ttk.Frame(ventana_historial)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview para mostrar datos
        tree = ttk.Treeview(frame, columns=("Fecha", "Tipo", "Entrada", "Salida"), 
                           show="headings", height=15)
        tree.heading("Fecha", text="📅 Fecha y Hora")
        tree.heading("Tipo", text="🔄 Tipo")
        tree.heading("Entrada", text="📥 Valor Original")
        tree.heading("Salida", text="📤 Resultado")
        
        tree.column("Fecha", width=160)
        tree.column("Tipo", width=100)
        tree.column("Entrada", width=120)
        tree.column("Salida", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Agregar datos (mostrar todos, no solo últimos 20)
        for reg in reversed(self.historial):
            tree.insert("", tk.END, values=(reg["fecha"], reg["tipo"], 
                                           f"{reg['entrada']}", f"{reg['salida']}"))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botones
        botones_frame = ttk.Frame(ventana_historial)
        botones_frame.pack(pady=10)
        
        # Botón de exportar
        btn_exportar = tk.Button(botones_frame, text="💾 Exportar a TXT",
                                 command=self.exportar_historial,
                                 bg="#4CAF50", fg="white", padx=20, pady=5,
                                 font=('Arial', 10, 'bold'), cursor="hand2")
        btn_exportar.pack(side=tk.LEFT, padx=5)
        
        # Botón de limpiar historial
        btn_limpiar = tk.Button(botones_frame, text="🗑️ Limpiar Historial",
                                command=lambda: self.limpiar_historial(ventana_historial),
                                bg="#f44336", fg="white", padx=20, pady=5,
                                font=('Arial', 10, 'bold'), cursor="hand2")
        btn_limpiar.pack(side=tk.LEFT, padx=5)
    
    def limpiar_historial(self, ventana):
        """Limpia todo el historial."""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres borrar TODO el historial?\n\nEsta acción no se puede deshacer."):
            self.historial = []
            self.guardar_historial()
            ventana.destroy()
            messagebox.showinfo("Historial limpiado", "El historial ha sido eliminado correctamente.")
            self.actualizar_barra("🗑️ Historial completamente limpiado")
    
    def exportar_historial(self):
        """Exporta el historial a un archivo de texto."""
        try:
            nombre_archivo = f"historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write("="*60 + "\n")
                f.write("HISTORIAL DE CONVERSIONES DE TEMPERATURA\n")
                f.write("="*60 + "\n")
                f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total de conversiones: {len(self.historial)}\n")
                f.write("="*60 + "\n\n")
                
                for i, reg in enumerate(self.historial, 1):
                    f.write(f"{i:3}. {reg['fecha']} | {reg['tipo']}: {reg['entrada']} → {reg['salida']}\n")
                
                f.write("\n" + "="*60 + "\n")
                f.write("✨ Fin del reporte\n")
                
            messagebox.showinfo("Éxito", f"Historial exportado a:\n{nombre_archivo}")
            self.actualizar_barra(f"💾 Historial exportado a {nombre_archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de uso con formato profesional."""
        if not self.historial:
            messagebox.showinfo("Estadísticas", "Aún no hay datos para mostrar.\n\nRealiza algunas conversiones primero.")
            return
        
        total = len(self.historial)
        cf_count = sum(1 for reg in self.historial if reg['tipo'] == 'C→F')
        fc_count = total - cf_count
        
        # Calcular valores mínimos, máximos y promedio
        if cf_count > 0:
            cf_entradas = [reg['entrada'] for reg in self.historial if reg['tipo'] == 'C→F']
            cf_salidas = [reg['salida'] for reg in self.historial if reg['tipo'] == 'C→F']
            cf_min = min(cf_entradas)
            cf_max = max(cf_entradas)
            cf_promedio_entrada = sum(cf_entradas) / cf_count
            cf_promedio_salida = sum(cf_salidas) / cf_count
        else:
            cf_min = cf_max = cf_promedio_entrada = cf_promedio_salida = 0
        
        if fc_count > 0:
            fc_entradas = [reg['entrada'] for reg in self.historial if reg['tipo'] == 'F→C']
            fc_salidas = [reg['salida'] for reg in self.historial if reg['tipo'] == 'F→C']
            fc_min = min(fc_entradas)
            fc_max = max(fc_entradas)
            fc_promedio_entrada = sum(fc_entradas) / fc_count
            fc_promedio_salida = sum(fc_salidas) / fc_count
        else:
            fc_min = fc_max = fc_promedio_entrada = fc_promedio_salida = 0
        
        # Crear ventana personalizada para estadísticas
        stats_ventana = tk.Toplevel(self.ventana)
        stats_ventana.title("📊 Estadísticas de Uso")
        stats_ventana.geometry("550x500")
        stats_ventana.configure(bg=self.colores[self.tema_actual]["bg"])
        
        # Centrar ventana
        stats_ventana.update_idletasks()
        x = (stats_ventana.winfo_screenwidth() // 2) - (550 // 2)
        y = (stats_ventana.winfo_screenheight() // 2) - (500 // 2)
        stats_ventana.geometry(f'550x500+{x}+{y}')
        
        # Frame principal con scrollbar
        canvas = tk.Canvas(stats_ventana, bg=self.colores[self.tema_actual]["bg"],
                           highlightthickness=0)
        scrollbar = ttk.Scrollbar(stats_ventana, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        titulo = tk.Label(scrollable_frame, 
                         text="📊 ESTADÍSTICAS DETALLADAS DE USO",
                         font=('Arial', 14, 'bold'),
                         bg=self.colores[self.tema_actual]["bg"],
                         fg=self.colores[self.tema_actual]["fg"])
        titulo.pack(pady=15)
        
        # Resumen general
        resumen_frame = tk.Frame(scrollable_frame, 
                                bg=self.colores[self.tema_actual]["bg"],
                                relief=tk.RIDGE, bd=2)
        resumen_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(resumen_frame, text="📈 RESUMEN GENERAL",
                font=('Arial', 11, 'bold'),
                bg=self.colores[self.tema_actual]["bg"],
                fg=self.colores[self.tema_actual]["fg"]).pack(pady=5)
        
        tk.Label(resumen_frame, text=f"Total de conversiones: {total}",
                font=('Arial', 10),
                bg=self.colores[self.tema_actual]["bg"],
                fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
        
        tk.Label(resumen_frame, text=f"Primera conversión: {self.historial[0]['fecha']}",
                font=('Arial', 10),
                bg=self.colores[self.tema_actual]["bg"],
                fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
        
        tk.Label(resumen_frame, text=f"Última conversión: {self.historial[-1]['fecha']}",
                font=('Arial', 10),
                bg=self.colores[self.tema_actual]["bg"],
                fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
        
        # Estadísticas Celsius → Fahrenheit
        cf_frame = tk.Frame(scrollable_frame, 
                           bg=self.colores[self.tema_actual]["bg"],
                           relief=tk.RIDGE, bd=2)
        cf_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(cf_frame, text="🌡️ CELSIUS → FAHRENHEIT",
                font=('Arial', 11, 'bold'),
                bg=self.colores[self.tema_actual]["bg"],
                fg="#4CAF50").pack(pady=5)
        
        tk.Label(cf_frame, text=f"Cantidad: {cf_count} ({cf_count/total*100:.1f}% del total)",
                font=('Arial', 10),
                bg=self.colores[self.tema_actual]["bg"],
                fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
        
        if cf_count > 0:
            tk.Label(cf_frame, text=f"Mínimo: {cf_min}°C → {round((cf_min * 9/5) + 32, 2)}°F",
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
            
            tk.Label(cf_frame, text=f"Máximo: {cf_max}°C → {round((cf_max * 9/5) + 32, 2)}°F",
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
            
            tk.Label(cf_frame, text=f"Promedio entrada: {cf_promedio_entrada:.2f}°C",
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
            
            tk.Label(cf_frame, text=f"Promedio salida: {cf_promedio_salida:.2f}°F",
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
        
        # Estadísticas Fahrenheit → Celsius
        fc_frame = tk.Frame(scrollable_frame, 
                           bg=self.colores[self.tema_actual]["bg"],
                           relief=tk.RIDGE, bd=2)
        fc_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(fc_frame, text="🌡️ FAHRENHEIT → CELSIUS",
                font=('Arial', 11, 'bold'),
                bg=self.colores[self.tema_actual]["bg"],
                fg="#2196F3").pack(pady=5)
        
        tk.Label(fc_frame, text=f"Cantidad: {fc_count} ({fc_count/total*100:.1f}% del total)",
                font=('Arial', 10),
                bg=self.colores[self.tema_actual]["bg"],
                fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
        
        if fc_count > 0:
            tk.Label(fc_frame, text=f"Mínimo: {fc_min}°F → {round((fc_min - 32) * 5/9, 2)}°C",
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
            
            tk.Label(fc_frame, text=f"Máximo: {fc_max}°F → {round((fc_max - 32) * 5/9, 2)}°C",
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
            
            tk.Label(fc_frame, text=f"Promedio entrada: {fc_promedio_entrada:.2f}°F",
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
            
            tk.Label(fc_frame, text=f"Promedio salida: {fc_promedio_salida:.2f}°C",
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(pady=2)
        
        # Consejos según el uso
        tips_frame = tk.Frame(scrollable_frame, 
                             bg=self.colores[self.tema_actual]["bg"],
                             relief=tk.RIDGE, bd=2)
        tips_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(tips_frame, text="💡 CONSEJOS PERSONALIZADOS",
                font=('Arial', 11, 'bold'),
                bg=self.colores[self.tema_actual]["bg"],
                fg="#FF9800").pack(pady=5)
        
        if total > 20:
            consejo = "🎉 ¡Excelente! Has realizado muchas conversiones. ¡Eres un experto!"
        elif total > 10:
            consejo = "👍 Buen trabajo. Sigue practicando para dominar las conversiones."
        elif total > 0:
            consejo = "📚 ¡Buen comienzo! Realiza más conversiones para ver tu progreso."
        else:
            consejo = "✨ ¡Anímate a hacer tu primera conversión!"
        
        if cf_count > fc_count:
            consejo += "\n🔍 Parece que prefieres convertir de Celsius a Fahrenheit."
        elif fc_count > cf_count:
            consejo += "\n🔍 Parece que prefieres convertir de Fahrenheit a Celsius."
        
        tk.Label(tips_frame, text=consejo,
                font=('Arial', 10),
                bg=self.colores[self.tema_actual]["bg"],
                fg=self.colores[self.tema_actual]["fg"],
                wraplength=480).pack(pady=10, padx=10)
        
        # Botón de cerrar
        btn_cerrar = tk.Button(scrollable_frame, text="Cerrar", 
                              command=stats_ventana.destroy,
                              bg=self.colores[self.tema_actual]["button"],
                              fg="white", font=('Arial', 10, 'bold'),
                              padx=30, pady=8, cursor="hand2")
        btn_cerrar.pack(pady=15)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada y resultados."""
        self.valor_celsius.set("")
        self.valor_fahrenheit.set("")
        self.resultado_celsius.set("")
        self.resultado_fahrenheit.set("")
        self.actualizar_barra("🧹 Todos los campos han sido limpiados")
    
    def cambiar_tema(self):
        """Cambia entre tema claro y oscuro."""
        self.tema_actual = "oscuro" if self.tema_actual == "claro" else "claro"
        self.aplicar_tema()
        
        # Actualizar colores de botones existentes
        colores_actual = self.colores[self.tema_actual]
        for widget in self.ventana.winfo_children():
            self.actualizar_colores_botones(widget, colores_actual)
        
        tema_texto = "oscuro" if self.tema_actual == "oscuro" else "claro"
        self.actualizar_barra(f"🌓 Tema cambiado a {tema_texto}")
    
    def actualizar_colores_botones(self, widget, colores):
        """Actualiza recursivamente los colores de los botones."""
        if isinstance(widget, tk.Button):
            widget.configure(bg=colores["button"])
        for child in widget.winfo_children():
            self.actualizar_colores_botones(child, colores)
    
    def mostrar_ayuda(self):
        """Muestra la ayuda de la aplicación con interfaz profesional."""
        
        # Crear ventana de ayuda personalizada
        ayuda_ventana = tk.Toplevel(self.ventana)
        ayuda_ventana.title("🎯 Guía Rápida - Conversor Profesional")
        ayuda_ventana.geometry("650x550")
        ayuda_ventana.configure(bg=self.colores[self.tema_actual]["bg"])
        
        # Centrar ventana
        ayuda_ventana.update_idletasks()
        x = (ayuda_ventana.winfo_screenwidth() // 2) - (650 // 2)
        y = (ayuda_ventana.winfo_screenheight() // 2) - (550 // 2)
        ayuda_ventana.geometry(f'650x550+{x}+{y}')
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(ayuda_ventana, bg=self.colores[self.tema_actual]["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg=self.colores[self.tema_actual]["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colores[self.tema_actual]["bg"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=630)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título principal
        titulo = tk.Label(scrollable_frame, 
                         text="🎯 GUÍA RÁPIDA DE USO",
                         font=('Arial', 18, 'bold'),
                         bg=self.colores[self.tema_actual]["bg"],
                         fg=self.colores[self.tema_actual]["fg"])
        titulo.pack(pady=20)
        
        # Línea decorativa
        tk.Frame(scrollable_frame, height=2, bg="#4CAF50").pack(fill=tk.X, padx=40, pady=5)
        
        # ========== SECCIÓN 1: CÓMO USAR ==========
        sec1_frame = tk.Frame(scrollable_frame, bg=self.colores[self.tema_actual]["bg"])
        sec1_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(sec1_frame, text="📝 CÓMO USAR EL CONVERSOR",
                font=('Arial', 13, 'bold'),
                bg=self.colores[self.tema_actual]["bg"],
                fg="#4CAF50").pack(anchor=tk.W, pady=5)
        
        pasos = [
            "1️Escribe un número en el campo de entrada",
            "2️Presiona el botón \"CONVERTIR\"",
            "3️¡El resultado aparece automáticamente!",
            "4️Se guarda en el historial para referencia futura"
        ]
        
        for paso in pasos:
            tk.Label(sec1_frame, text=paso,
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(anchor=tk.W, pady=3, padx=20)
        
        # ========== SECCIÓN 2: ATAJOS DE TECLADO ==========
        sec2_frame = tk.Frame(scrollable_frame, bg=self.colores[self.tema_actual]["bg"])
        sec2_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(sec2_frame, text="⌨️ ATAJOS DE TECLADO",
                font=('Arial', 13, 'bold'),
                bg=self.colores[self.tema_actual]["bg"],
                fg="#2196F3").pack(anchor=tk.W, pady=5)
        
        # Tabla de atajos
        atajos_frame = tk.Frame(sec2_frame, bg=self.colores[self.tema_actual]["bg"])
        atajos_frame.pack(padx=20)
        
        atajos = [
            ("↲ Enter", "Convertir (según campo activo)"),
            ("⌘ Ctrl + C", "Limpiar todos los campos"),
            ("⌘ Ctrl + H", "Ver historial de conversiones"),
            ("F1", "Abrir esta ayuda"),
            ("⎋ Escape", "Salir de la aplicación")
        ]
        
        for i, (tecla, accion) in enumerate(atajos):
            # Fila
            fila = tk.Frame(atajos_frame, bg=self.colores[self.tema_actual]["bg"])
            fila.pack(fill=tk.X, pady=4)
            
            # Tecla (con fondo)
            tecla_label = tk.Label(fila, text=tecla, 
                                  font=('Arial', 10, 'bold'),
                                  bg="#333333", fg="white",
                                  padx=10, pady=3, relief=tk.RAISED)
            tecla_label.pack(side=tk.LEFT, padx=(0, 15))
            
            # Acción
            tk.Label(fila, text=accion,
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(side=tk.LEFT)
        
        # ========== SECCIÓN 3: TIPS ÚTILES ==========
        sec3_frame = tk.Frame(scrollable_frame, bg=self.colores[self.tema_actual]["bg"])
        sec3_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(sec3_frame, text="💡 TIPS ÚTILES",
                font=('Arial', 13, 'bold'),
                bg=self.colores[self.tema_actual]["bg"],
                fg="#FF9800").pack(anchor=tk.W, pady=5)
        
        tips = [
            "✓ Puedes usar números decimales (ej: 23.5, -10.2, 37.8)",
            "✓ También números negativos (ej: -15, -40)",
            "✓ El historial se guarda automáticamente en un archivo JSON",
            "✓ Cambia el tema claro/oscuro cuando quieras",
            "✓ Exporta el historial a TXT para guardar tus registros",
            "✓ Limpia el historial cuando necesites empezar de cero"
        ]
        
        for tip in tips:
            tk.Label(sec3_frame, text=tip,
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(anchor=tk.W, pady=3, padx=20)
        
        # ========== SECCIÓN 4: REFERENCIAS RÁPIDAS ==========
        sec4_frame = tk.Frame(scrollable_frame, bg=self.colores[self.tema_actual]["bg"])
        sec4_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(sec4_frame, text="📚 REFERENCIAS RÁPIDAS",
                font=('Arial', 13, 'bold'),
                bg=self.colores[self.tema_actual]["bg"],
                fg="#9C27B0").pack(anchor=tk.W, pady=5)
        
        referencias_frame = tk.Frame(sec4_frame, bg=self.colores[self.tema_actual]["bg"])
        referencias_frame.pack(padx=20)
        
        referencias = [
            ("0°C", "32°F", "Congelación del agua"),
            ("100°C", "212°F", "Ebullición del agua"),
            ("37°C", "98.6°F", "Temperatura corporal"),
            ("20°C", "68°F", "Temperatura ambiente"),
            ("-40°C", "-40°F", "Punto de equivalencia")
        ]
        
        # Encabezados
        header_frame = tk.Frame(referencias_frame, bg=self.colores[self.tema_actual]["bg"])
        header_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(header_frame, text="Celsius", width=10, font=('Arial', 10, 'bold'),
                bg=self.colores[self.tema_actual]["bg"], fg="#4CAF50").pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="Fahrenheit", width=10, font=('Arial', 10, 'bold'),
                bg=self.colores[self.tema_actual]["bg"], fg="#2196F3").pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="Referencia", width=20, font=('Arial', 10, 'bold'),
                bg=self.colores[self.tema_actual]["bg"], fg="#FF9800").pack(side=tk.LEFT, padx=5)
        
        tk.Frame(referencias_frame, height=1, bg="#666").pack(fill=tk.X, pady=5)
        
        for celsius, fahrenheit, ref in referencias:
            fila = tk.Frame(referencias_frame, bg=self.colores[self.tema_actual]["bg"])
            fila.pack(fill=tk.X, pady=3)
            
            tk.Label(fila, text=celsius, width=10, font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"], fg=self.colores[self.tema_actual]["fg"]).pack(side=tk.LEFT, padx=5)
            tk.Label(fila, text=fahrenheit, width=10, font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"], fg=self.colores[self.tema_actual]["fg"]).pack(side=tk.LEFT, padx=5)
            tk.Label(fila, text=ref, width=20, font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"], fg=self.colores[self.tema_actual]["fg"]).pack(side=tk.LEFT, padx=5)
        
        # ========== SECCIÓN 5: CARACTERÍSTICAS ==========
        sec5_frame = tk.Frame(scrollable_frame, bg=self.colores[self.tema_actual]["bg"])
        sec5_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(sec5_frame, text="🎨 CARACTERÍSTICAS DEL PROGRAMA",
                font=('Arial', 13, 'bold'),
                bg=self.colores[self.tema_actual]["bg"],
                fg="#E91E63").pack(anchor=tk.W, pady=5)
        
        caracteristicas = [
            "• Interfaz profesional con dos paneles de conversión",
            "• Historial completo con fecha y hora",
            "• Exportación de historial a archivo TXT",
            "• Estadísticas detalladas de uso",
            "• Temas claro/oscuro intercambiables",
            "• Validación de errores amigable",
            "• Conversión en tiempo real al presionar el botón",
            "• Persistencia de datos (el historial no se pierde)"
        ]
        
        for carac in caracteristicas:
            tk.Label(sec5_frame, text=carac,
                    font=('Arial', 10),
                    bg=self.colores[self.tema_actual]["bg"],
                    fg=self.colores[self.tema_actual]["fg"]).pack(anchor=tk.W, pady=2, padx=20)
        
        # Línea decorativa final
        tk.Frame(scrollable_frame, height=2, bg="#4CAF50").pack(fill=tk.X, padx=40, pady=10)
        
        # Botón de cerrar
        btn_cerrar = tk.Button(scrollable_frame, text="✓ Entendido", 
                              command=ayuda_ventana.destroy,
                              bg="#4CAF50", fg="white", 
                              font=('Arial', 11, 'bold'),
                              padx=40, pady=10, cursor="hand2")
        btn_cerrar.pack(pady=20)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def actualizar_barra(self, mensaje):
        """Actualiza el mensaje de la barra de estado."""
        self.barra_estado.config(text=f"💡 {mensaje}")
        # Resetear después de 3 segundos
        self.ventana.after(3000, lambda: self.barra_estado.config(
            text="✅ Listo | F1=Ayuda | Enter=Convertir | Ctrl+H=Historial"))
    
    def confirmar_salida(self):
        """Confirma antes de cerrar la aplicación."""
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
            self.ventana.destroy()
    
    def ejecutar(self):
        """Inicia la aplicación."""
        self.ventana.mainloop()


# Punto de entrada
if __name__ == "__main__":
    try:
        app = ConversorTemperaturaPro()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presiona Enter para salir...")
