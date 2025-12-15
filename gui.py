"""
GUI Principal para el Sistema de Minimización de Polarización
==============================================================

Interfaz gráfica moderna y profesional para ejecutar el modelo de optimización
que minimiza la polarización en poblaciones.

Autores: Andrey Quiceño, Iván, Francesco, Jonathan
Fecha: Diciembre 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import sys
import os
from pathlib import Path
import subprocess
import threading
import time
from typing import Dict, Optional

# Importar estilos y configuración
from gui_styles import GUIStyles, GUIIcons, GUIMessages

# Agregar paths necesarios
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / 'input_output'))

# Importar módulos de I/O
from input_output.input import parse_input_file, txt_to_dzn
from input_output.output import parse_minizinc_output, generate_output_file


class PolarizationGUI:
    """Clase principal de la interfaz gráfica"""
    
    def __init__(self, root):
        """Inicializa la interfaz gráfica"""
        self.root = root
        self.root.title(GUIMessages.WINDOW_TITLE)
        self.root.geometry(f"{GUIStyles.DIMENSIONS['window_width']}x{GUIStyles.DIMENSIONS['window_height']}")
        self.root.minsize(GUIStyles.DIMENSIONS['min_width'], GUIStyles.DIMENSIONS['min_height'])
        
        # Configurar estilos
        GUIStyles.configure_styles()
        self.root.configure(bg=GUIStyles.COLORS['bg_dark'])
        
        # Variables de estado
        self.input_file = None
        self.params = None
        self.minizinc_output = None
        self.is_running = False
        
        # Crear interfaz
        self.create_widgets()
        self.update_status(GUIMessages.STATUS_READY)
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        # ==== HEADER ====
        self.create_header(main_frame)
        
        # ==== CONTENIDO PRINCIPAL ====
        content_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Frame izquierdo (Input y parámetros)
        left_frame = ttk.Frame(content_frame, style='Dark.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_input_section(left_frame)
        self.create_params_section(left_frame)
        self.create_execute_section(left_frame)
        
        # Frame derecho (Output)
        right_frame = ttk.Frame(content_frame, style='Dark.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.create_output_section(right_frame)
        
        # ==== FOOTER ====
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Crea el encabezado de la aplicación"""
        header_frame = ttk.Frame(parent, style='Dark.TFrame')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        # Logo y título
        title_frame = ttk.Frame(header_frame, style='Dark.TFrame')
        title_frame.pack(side='left')
        
        # Título principal
        title_label = ttk.Label(
            title_frame,
            text=f"{GUIIcons.LOGO} {GUIMessages.APP_TITLE}",
            style='Title.TLabel'
        )
        title_label.pack(anchor='w')
        
        # Subtítulo
        subtitle_label = ttk.Label(
            title_frame,
            text=GUIMessages.APP_SUBTITLE,
            style='Info.TLabel'
        )
        subtitle_label.pack(anchor='w', pady=(2, 0))
    
    def create_input_section(self, parent):
        """Crea la sección de entrada de archivo"""
        input_frame = ttk.LabelFrame(
            parent,
            text=f"{GUIIcons.FILE} {GUIMessages.SECTION_INPUT}",
            style='Card.TLabelframe',
            padding=15
        )
        input_frame.pack(fill='x', pady=(0, 15))
        
        # Frame para el selector de archivo
        file_frame = ttk.Frame(input_frame, style='Dark.TFrame')
        file_frame.pack(fill='x', pady=5)
        
        # Entry para mostrar el archivo
        self.file_entry = ttk.Entry(
            file_frame,
            style='Dark.TEntry',
            font=GUIStyles.FONTS['normal']
        )
        self.file_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Botón para buscar archivo
        browse_btn = ttk.Button(
            file_frame,
            text=GUIMessages.BTN_BROWSE,
            style='Secondary.TButton',
            command=self.browse_file
        )
        browse_btn.pack(side='right')
        
        # Botón para cargar datos
        load_btn = ttk.Button(
            input_frame,
            text=f"{GUIIcons.UPLOAD} {GUIMessages.BTN_LOAD}",
            style='Success.TButton',
            command=self.load_data
        )
        load_btn.pack(fill='x', pady=(10, 0))
    
    def create_params_section(self, parent):
        """Crea la sección de parámetros del problema"""
        params_frame = ttk.LabelFrame(
            parent,
            text=f"{GUIIcons.SETTINGS} {GUIMessages.SECTION_PARAMS}",
            style='Card.TLabelframe',
            padding=15
        )
        params_frame.pack(fill='x', pady=(0, 15))
        
        # Grid para mostrar parámetros
        params_grid = ttk.Frame(params_frame, style='Dark.TFrame')
        params_grid.pack(fill='x')
        
        # Configurar grid
        for i in range(2):
            params_grid.columnconfigure(i, weight=1)
        
        # Parámetro n
        self.create_param_display(params_grid, "n (personas):", 0, 0)
        self.n_value = ttk.Label(params_grid, text="-", style='Dark.TLabel', font=GUIStyles.FONTS['mono_bold'])
        self.n_value.grid(row=0, column=1, sticky='w', padx=5, pady=3)
        
        # Parámetro m
        self.create_param_display(params_grid, "m (opiniones):", 1, 0)
        self.m_value = ttk.Label(params_grid, text="-", style='Dark.TLabel', font=GUIStyles.FONTS['mono_bold'])
        self.m_value.grid(row=1, column=1, sticky='w', padx=5, pady=3)
        
        # Parámetro ct
        self.create_param_display(params_grid, "Costo máximo:", 2, 0)
        self.ct_value = ttk.Label(params_grid, text="-", style='Dark.TLabel', font=GUIStyles.FONTS['mono_bold'])
        self.ct_value.grid(row=2, column=1, sticky='w', padx=5, pady=3)
        
        # Parámetro maxMovs
        self.create_param_display(params_grid, "Movimientos máx:", 3, 0)
        self.maxmovs_value = ttk.Label(params_grid, text="-", style='Dark.TLabel', font=GUIStyles.FONTS['mono_bold'])
        self.maxmovs_value.grid(row=3, column=1, sticky='w', padx=5, pady=3)
    
    def create_param_display(self, parent, label_text, row, col):
        """Crea un label para un parámetro"""
        label = ttk.Label(
            parent,
            text=label_text,
            style='Heading.TLabel'
        )
        label.grid(row=row, column=col, sticky='e', padx=5, pady=3)
    
    def create_execute_section(self, parent):
        """Crea la sección de ejecución"""
        execute_frame = ttk.LabelFrame(
            parent,
            text=f"{GUIIcons.PLAY} {GUIMessages.SECTION_EXECUTE}",
            style='Card.TLabelframe',
            padding=15
        )
        execute_frame.pack(fill='x', pady=(0, 15))
        
        # Botón de ejecución
        self.execute_btn = ttk.Button(
            execute_frame,
            text=f"{GUIIcons.PLAY} {GUIMessages.BTN_EXECUTE}",
            style='Accent.TButton',
            command=self.execute_minizinc
        )
        self.execute_btn.pack(fill='x', pady=(0, 10))
        
        # Frame para botones secundarios
        buttons_frame = ttk.Frame(execute_frame, style='Dark.TFrame')
        buttons_frame.pack(fill='x')
        
        # Botón para guardar
        self.save_btn = ttk.Button(
            buttons_frame,
            text=f"{GUIIcons.SAVE} {GUIMessages.BTN_SAVE}",
            style='Secondary.TButton',
            command=self.save_output,
            state='disabled'
        )
        self.save_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        # Botón para limpiar
        clear_btn = ttk.Button(
            buttons_frame,
            text=f"{GUIIcons.CLEAN} {GUIMessages.BTN_CLEAR}",
            style='Secondary.TButton',
            command=self.clear_all
        )
        clear_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
    
    def create_output_section(self, parent):
        """Crea la sección de salida"""
        output_frame = ttk.LabelFrame(
            parent,
            text=f"{GUIIcons.REPORT} {GUIMessages.SECTION_OUTPUT}",
            style='Card.TLabelframe',
            padding=15
        )
        output_frame.pack(fill='both', expand=True)
        
        # Text widget para mostrar salida
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=GUIStyles.FONTS['mono'],
            bg=GUIStyles.COLORS['input_bg'],
            fg=GUIStyles.COLORS['text'],
            insertbackground=GUIStyles.COLORS['text'],
            selectbackground=GUIStyles.COLORS['accent'],
            selectforeground='white',
            width=GUIStyles.DIMENSIONS['text_width'],
            height=GUIStyles.DIMENSIONS['text_height'],
            relief='flat',
            borderwidth=0
        )
        self.output_text.pack(fill='both', expand=True)
        
        # Configurar tags para colores
        self.output_text.tag_config('success', foreground=GUIStyles.COLORS['success'], font=GUIStyles.FONTS['mono_bold'])
        self.output_text.tag_config('error', foreground=GUIStyles.COLORS['error'], font=GUIStyles.FONTS['mono_bold'])
        self.output_text.tag_config('warning', foreground=GUIStyles.COLORS['warning'])
        self.output_text.tag_config('info', foreground=GUIStyles.COLORS['info'])
        self.output_text.tag_config('accent', foreground=GUIStyles.COLORS['accent'], font=GUIStyles.FONTS['mono_bold'])
        self.output_text.tag_config('header', foreground=GUIStyles.COLORS['text'], font=GUIStyles.FONTS['mono_bold'])
    
    def create_footer(self, parent):
        """Crea el pie de página con la barra de estado"""
        footer_frame = ttk.Frame(parent, style='Medium.TFrame')
        footer_frame.pack(fill='x', side='bottom')
        
        # Barra de estado
        self.status_label = ttk.Label(
            footer_frame,
            text=GUIMessages.STATUS_READY,
            style='Dark.TLabel',
            font=GUIStyles.FONTS['small']
        )
        self.status_label.pack(side='left', padx=20, pady=8)
        
        # Créditos
        credits_label = ttk.Label(
            footer_frame,
            text=GUIMessages.CREDITS,
            font=GUIStyles.FONTS['small'],
            foreground=GUIStyles.COLORS['text_secondary'],
            background=GUIStyles.COLORS['bg_medium']
        )
        credits_label.pack(side='right', padx=20, pady=8)
    
    def browse_file(self):
        """Abre un diálogo para seleccionar archivo"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de entrada",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialdir=ROOT_DIR / "tests"
        )
        
        if filename:
            self.input_file = filename
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            self.update_status(GUIMessages.STATUS_FILE_SELECTED(Path(filename).name))
    
    def load_data(self):
        """Carga y parsea el archivo de entrada"""
        if not self.input_file:
            messagebox.showerror("Error", GUIMessages.ERROR_NO_FILE)
            return
        
        try:
            self.update_status(GUIMessages.STATUS_LOADING)
            self.params = parse_input_file(self.input_file)
            
            # Actualizar displays de parámetros
            self.n_value.config(text=str(self.params['n']))
            self.m_value.config(text=str(self.params['m']))
            self.ct_value.config(text=f"{self.params['ct']:.1f}")
            self.maxmovs_value.config(text=f"{self.params['maxMovs']:.1f}")
            
            # Mostrar información en la salida
            self.output_text.delete(1.0, tk.END)
            self.write_output("═" * 80 + "\n", 'header')
            self.write_output("DATOS DE ENTRADA CARGADOS\n", 'header')
            self.write_output("═" * 80 + "\n\n", 'header')
            
            self.write_output(f"Número de personas (n): ", 'info')
            self.write_output(f"{self.params['n']}\n", 'accent')
            
            self.write_output(f"Número de opiniones (m): ", 'info')
            self.write_output(f"{self.params['m']}\n", 'accent')
            
            self.write_output(f"\nDistribución de personas por opinión:\n", 'info')
            for i, p in enumerate(self.params['p'], 1):
                self.write_output(f"  Opinión {i}: {p} personas\n")
            
            self.write_output(f"\nValores de las opiniones:\n", 'info')
            for i, v in enumerate(self.params['v'], 1):
                self.write_output(f"  Opinión {i}: {v:.3f}\n")
            
            self.write_output(f"\nResistencias al cambio:\n", 'info')
            for i, resistances in enumerate(self.params['s'], 1):
                self.write_output(f"  Opinión {i}: Baja={resistances[0]}, Media={resistances[1]}, Alta={resistances[2]}\n")
            
            self.write_output(f"\nCosto total máximo: ", 'info')
            self.write_output(f"{self.params['ct']}\n", 'accent')
            
            self.write_output(f"Movimientos máximos: ", 'info')
            self.write_output(f"{self.params['maxMovs']}\n\n", 'accent')
            
            self.update_status(GUIMessages.STATUS_LOADED(self.params['n'], self.params['m']))
            
        except Exception as e:
            messagebox.showerror("Error", GUIMessages.ERROR_PARSE(str(e)))
            self.update_status(GUIMessages.STATUS_ERROR)
    
    def execute_minizinc(self):
        """Ejecuta el modelo de MiniZinc"""
        if not self.params:
            messagebox.showerror("Error", "Debe cargar los datos primero")
            return
        
        if self.is_running:
            messagebox.showwarning("Advertencia", "Ya hay una ejecución en curso")
            return
        
        # Ejecutar en un thread separado
        thread = threading.Thread(target=self._run_minizinc_thread, daemon=True)
        thread.start()
    
    def _run_minizinc_thread(self):
        """Thread para ejecutar MiniZinc sin bloquear la UI"""
        self.is_running = True
        self.execute_btn.config(state='disabled')
        self.root.after(0, lambda: self.update_status(GUIMessages.STATUS_RUNNING))
        
        try:
            # Verificar que MiniZinc esté instalado
            try:
                check_result = subprocess.run(
                    ['minizinc', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if check_result.returncode != 0:
                    raise FileNotFoundError("MiniZinc no responde correctamente")
            except (FileNotFoundError, subprocess.TimeoutExpired) as e:
                error_msg = (
                    "❌ MiniZinc no está instalado o no está en el PATH del sistema.\n\n"
                    "Por favor, sigue estos pasos:\n\n"
                    "1. Descarga MiniZinc desde: https://www.minizinc.org/\n"
                    "2. Instala MiniZinc en tu sistema\n"
                    "3. Asegúrate de marcar la opción 'Add to PATH' durante la instalación\n"
                    "4. Reinicia VS Code o tu terminal\n"
                    "5. Verifica la instalación ejecutando: minizinc --version\n\n"
                    "Si ya instalaste MiniZinc, es posible que necesites:\n"
                    "- Reiniciar tu computadora para que el PATH se actualice\n"
                    "- Agregar manualmente el directorio de MiniZinc al PATH del sistema"
                )
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("MiniZinc No Encontrado", msg))
                return
            
            # Generar archivo .dzn
            dzn_file = ROOT_DIR / "temp" / "DatosProyecto.dzn"
            dzn_file.parent.mkdir(exist_ok=True)
            txt_to_dzn(self.input_file, str(dzn_file))
            
            # Ejecutar MiniZinc
            mzn_file = ROOT_DIR / "model" / "Proyecto.mzn"
            
            # Verificar que el modelo existe
            if not mzn_file.exists():
                error_msg = f"El archivo del modelo no existe: {mzn_file}\n\nPor favor, verifica la estructura del proyecto."
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("Error", msg))
                return
            
            start_time = time.time()
            
            cmd = [
                'minizinc',
                '--solver', 'Gecode',
                '--time-limit', '300000',  # 5 minutos
                str(mzn_file),
                str(dzn_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=320
            )
            
            elapsed_time = time.time() - start_time
            
            if result.returncode == 0:
                self.minizinc_output = result.stdout
                self.root.after(0, lambda: self._display_results(elapsed_time))
            else:
                error_msg = result.stderr if result.stderr else "Error desconocido"
                self.root.after(0, lambda: self._display_error(error_msg))
                
        except subprocess.TimeoutExpired:
            self.root.after(0, lambda: messagebox.showerror("Error", GUIMessages.ERROR_TIMEOUT))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error inesperado: {str(e)}"))
        finally:
            self.is_running = False
            self.execute_btn.config(state='normal')
    
    def _display_results(self, elapsed_time):
        """Muestra los resultados de la optimización"""
        try:
            parsed = parse_minizinc_output(self.minizinc_output)
            pol = parsed.get('polarization', 0)
            
            self.output_text.delete(1.0, tk.END)
            
            self.write_output("═" * 80 + "\n", 'header')
            self.write_output("RESULTADOS DE LA OPTIMIZACIÓN\n", 'success')
            self.write_output("═" * 80 + "\n\n", 'header')
            
            self.write_output(f"✓ Polarización final: ", 'success')
            self.write_output(f"{pol:.3f}\n\n", 'accent')
            
            self.write_output(f"Tiempo de ejecución: {elapsed_time:.2f} segundos\n\n", 'info')
            
            if 'final_distribution' in parsed:
                self.write_output("Distribución final de personas:\n", 'info')
                for i, count in enumerate(parsed['final_distribution'], 1):
                    self.write_output(f"  Opinión {i}: {count} personas\n")
                self.write_output("\n")
            
            if 'median_value' in parsed:
                self.write_output(f"Valor de la mediana: {parsed['median_value']:.3f}\n\n", 'info')
            
            # Mostrar matrices de movimientos
            for k in range(1, 4):
                resistance_name = ['Baja', 'Media', 'Alta'][k-1]
                self.write_output(f"Movimientos (Resistencia {resistance_name}):\n", 'info')
                
                matrix = parsed.get(f'movements_k{k}', [])
                if matrix:
                    # Encabezado
                    header = "      " + "".join([f"Op{j+1:2d} " for j in range(len(matrix))])
                    self.write_output(header + "\n")
                    
                    for i, row in enumerate(matrix, 1):
                        row_str = f"  Op{i:2d} " + "".join([f"{val:3d} " for val in row])
                        self.write_output(row_str + "\n")
                    self.write_output("\n")
            
            self.update_status(GUIMessages.STATUS_COMPLETED(elapsed_time, pol))
            self.save_btn.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar resultados: {str(e)}")
    
    def _display_error(self, error_msg):
        """Muestra un error de ejecución"""
        self.output_text.delete(1.0, tk.END)
        self.write_output("═" * 80 + "\n", 'header')
        self.write_output("ERROR DE EJECUCIÓN\n", 'error')
        self.write_output("═" * 80 + "\n\n", 'header')
        self.write_output(error_msg, 'error')
        self.update_status(GUIMessages.STATUS_ERROR)
    
    def save_output(self):
        """Guarda la salida en un archivo .txt"""
        if not self.minizinc_output or not self.params:
            messagebox.showerror("Error", "No hay resultados para guardar")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Guardar resultado",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            try:
                generate_output_file(self.minizinc_output, filename, self.params['m'])
                messagebox.showinfo("Éxito", f"Resultado guardado en:\n{filename}")
                self.update_status(GUIMessages.STATUS_SAVED(Path(filename).name))
            except Exception as e:
                messagebox.showerror("Error", GUIMessages.ERROR_SAVE(str(e)))
    
    def clear_all(self):
        """Limpia la interfaz"""
        self.input_file = None
        self.params = None
        self.minizinc_output = None
        
        self.file_entry.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)
        
        self.n_value.config(text="-")
        self.m_value.config(text="-")
        self.ct_value.config(text="-")
        self.maxmovs_value.config(text="-")
        
        self.save_btn.config(state='disabled')
        self.update_status(GUIMessages.STATUS_CLEANED)
    
    def write_output(self, text, tag=None):
        """Escribe texto en el widget de salida con un tag opcional"""
        if tag:
            self.output_text.insert(tk.END, text, tag)
        else:
            self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
    
    def update_status(self, message):
        """Actualiza la barra de estado"""
        self.status_label.config(text=message)


def main():
    """Función principal"""
    root = tk.Tk()
    app = PolarizationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
