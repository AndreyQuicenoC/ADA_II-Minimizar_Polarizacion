"""
Estilos y configuración visual para la GUI de Minimizar Polarización
=====================================================================

Define la paleta de colores, estilos de widgets y configuración visual
para el Sistema de Minimización de Polarización.

Autores: Andrey Quiceño, Iván, Francesco, Jonathan
Fecha: Diciembre 2025
"""

from tkinter import ttk


class GUIStyles:
    """Clase que contiene todos los estilos visuales de la GUI"""
    
    # ===== PALETA DE COLORES MODERNA - TEMA PÚRPURA/AZUL =====
    COLORS = {
        'bg_dark': '#0d1117',           # Fondo principal muy oscuro (GitHub dark)
        'bg_medium': '#161b22',         # Fondo medio
        'bg_light': '#21262d',          # Fondo claro
        'accent': '#8b5cf6',            # Púrpura acento (violeta moderno)
        'accent_hover': '#a78bfa',      # Púrpura acento hover
        'accent_dark': '#6d28d9',       # Púrpura oscuro
        'button': '#7c3aed',            # Púrpura botones
        'button_hover': '#8b5cf6',      # Púrpura botones hover
        'text': '#f0f6fc',              # Texto claro
        'text_secondary': '#8b949e',    # Texto secundario
        'border': '#30363d',            # Bordes
        'border_active': '#8b5cf6',     # Bordes activos
        'error': '#f85149',             # Rojo error
        'success': '#3fb950',           # Verde éxito
        'warning': '#d29922',           # Amarillo advertencia
        'info': '#58a6ff',              # Azul info
        'frame_bg': '#161b22',          # Fondo de frames
        'card_bg': '#0d1117',           # Fondo de tarjetas
        'input_bg': '#0d1117',          # Fondo inputs
    }
    
    # ===== FUENTES =====
    FONTS = {
        'title': ('Segoe UI', 18, 'bold'),
        'subtitle': ('Segoe UI', 14, 'bold'),
        'heading': ('Segoe UI', 11, 'bold'),
        'normal': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'button': ('Segoe UI', 10, 'bold'),
        'mono': ('Cascadia Code', 9),
        'mono_bold': ('Cascadia Code', 10, 'bold'),
    }
    
    # ===== DIMENSIONES =====
    DIMENSIONS = {
        'window_width': 1100,
        'window_height': 750,
        'min_width': 900,
        'min_height': 600,
        'text_width': 100,
        'text_height': 25,
        'padding_large': 20,
        'padding_medium': 12,
        'padding_small': 6,
    }
    
    @staticmethod
    def configure_styles():
        """Configura todos los estilos ttk personalizados"""
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use('clam')
        
        # ===== ESTILOS PARA FRAMES =====
        style.configure('Dark.TFrame', 
                       background=GUIStyles.COLORS['bg_dark'])
        
        style.configure('Medium.TFrame',
                       background=GUIStyles.COLORS['bg_medium'])
        
        style.configure('Card.TFrame',
                       background=GUIStyles.COLORS['card_bg'],
                       relief='flat')
        
        # ===== ESTILOS PARA LABELS =====
        style.configure('Dark.TLabel',
                       background=GUIStyles.COLORS['bg_dark'],
                       foreground=GUIStyles.COLORS['text'],
                       font=GUIStyles.FONTS['normal'])
        
        style.configure('Title.TLabel',
                       background=GUIStyles.COLORS['bg_dark'],
                       foreground=GUIStyles.COLORS['text'],
                       font=GUIStyles.FONTS['title'])
        
        style.configure('Subtitle.TLabel',
                       background=GUIStyles.COLORS['bg_dark'],
                       foreground=GUIStyles.COLORS['accent'],
                       font=GUIStyles.FONTS['subtitle'])
        
        style.configure('Heading.TLabel',
                       background=GUIStyles.COLORS['bg_dark'],
                       foreground=GUIStyles.COLORS['text_secondary'],
                       font=GUIStyles.FONTS['heading'])
        
        style.configure('Info.TLabel',
                       background=GUIStyles.COLORS['bg_dark'],
                       foreground=GUIStyles.COLORS['info'],
                       font=GUIStyles.FONTS['small'])
        
        # ===== ESTILOS PARA LABELFRAME =====
        style.configure('Dark.TLabelframe',
                       background=GUIStyles.COLORS['frame_bg'],
                       foreground=GUIStyles.COLORS['text'],
                       bordercolor=GUIStyles.COLORS['border'],
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Dark.TLabelframe.Label',
                       background=GUIStyles.COLORS['frame_bg'],
                       foreground=GUIStyles.COLORS['accent'],
                       font=GUIStyles.FONTS['heading'])
        
        style.configure('Card.TLabelframe',
                       background=GUIStyles.COLORS['card_bg'],
                       foreground=GUIStyles.COLORS['text'],
                       bordercolor=GUIStyles.COLORS['border_active'],
                       relief='solid',
                       borderwidth=2)
        
        style.configure('Card.TLabelframe.Label',
                       background=GUIStyles.COLORS['card_bg'],
                       foreground=GUIStyles.COLORS['accent'],
                       font=GUIStyles.FONTS['subtitle'])
        
        # ===== ESTILOS PARA ENTRY =====
        style.configure('Dark.TEntry',
                       fieldbackground=GUIStyles.COLORS['input_bg'],
                       foreground=GUIStyles.COLORS['text'],
                       bordercolor=GUIStyles.COLORS['border'],
                       lightcolor=GUIStyles.COLORS['border_active'],
                       darkcolor=GUIStyles.COLORS['border'],
                       insertcolor=GUIStyles.COLORS['text'])
        
        # ===== ESTILOS PARA BOTONES PRINCIPALES =====
        style.configure('Accent.TButton',
                       background=GUIStyles.COLORS['button'],
                       foreground='white',
                       bordercolor=GUIStyles.COLORS['border_active'],
                       focuscolor=GUIStyles.COLORS['accent'],
                       font=GUIStyles.FONTS['button'],
                       padding=(16, 10))
        
        style.map('Accent.TButton',
                 background=[('active', GUIStyles.COLORS['button_hover']),
                           ('pressed', GUIStyles.COLORS['accent_dark']),
                           ('disabled', GUIStyles.COLORS['bg_light'])],
                 foreground=[('disabled', GUIStyles.COLORS['text_secondary'])])
        
        # ===== ESTILOS PARA BOTONES SECUNDARIOS =====
        style.configure('Secondary.TButton',
                       background=GUIStyles.COLORS['bg_light'],
                       foreground=GUIStyles.COLORS['text'],
                       bordercolor=GUIStyles.COLORS['border'],
                       font=GUIStyles.FONTS['normal'],
                       padding=(12, 8))
        
        style.map('Secondary.TButton',
                 background=[('active', GUIStyles.COLORS['bg_medium']),
                           ('disabled', GUIStyles.COLORS['bg_dark'])],
                 foreground=[('disabled', GUIStyles.COLORS['text_secondary'])])
        
        # ===== ESTILOS PARA BOTONES DE ÉXITO =====
        style.configure('Success.TButton',
                       background=GUIStyles.COLORS['success'],
                       foreground='white',
                       bordercolor=GUIStyles.COLORS['success'],
                       font=GUIStyles.FONTS['button'],
                       padding=(12, 8))
        
        style.map('Success.TButton',
                 background=[('active', '#4ade80'),
                           ('disabled', GUIStyles.COLORS['bg_light'])],
                 foreground=[('disabled', GUIStyles.COLORS['text_secondary'])])


class GUIIcons:
    """Iconos Unicode para la interfaz"""
    # Símbolos generales
    LOGO = "◆"
    FILE = "📄"
    FOLDER = "📁"
    SETTINGS = "⚙"
    PLAY = "▶"
    PAUSE = "⏸"
    STOP = "⏹"
    REFRESH = "↻"
    CLEAN = "🗑"
    
    # Estados
    SUCCESS = "✓"
    ERROR = "✗"
    WARNING = "⚠"
    INFO = "ℹ"
    LOADING = "⏳"
    
    # Análisis
    CHART = "📊"
    GRAPH = "📈"
    DATA = "📋"
    REPORT = "📑"
    
    # Acciones
    DOWNLOAD = "⬇"
    UPLOAD = "⬆"
    SAVE = "💾"
    OPEN = "📂"


class GUIMessages:
    """Clase que contiene los mensajes de la GUI"""
    
    # Títulos
    WINDOW_TITLE = "Sistema de Minimización de Polarización - Análisis de Algoritmos II"
    APP_TITLE = "Minimizar Polarización en Poblaciones"
    APP_SUBTITLE = "Optimización mediante Programación Entera Mixta"
    
    # Secciones
    SECTION_INPUT = "Configuración de Entrada"
    SECTION_PARAMS = "Parámetros del Problema"
    SECTION_EXECUTE = "Ejecución del Modelo"
    SECTION_OUTPUT = "Resultados de la Optimización"
    SECTION_ANALYSIS = "Análisis de la Solución"
    
    # Botones
    BTN_BROWSE = "Seleccionar archivo..."
    BTN_LOAD = "Cargar datos"
    BTN_EXECUTE = "Ejecutar MiniZinc"
    BTN_SAVE = "Guardar resultado"
    BTN_CLEAR = "Limpiar"
    BTN_EXPORT = "Exportar .dzn"
    BTN_VIEW_MODEL = "Ver modelo"
    
    # Estados
    STATUS_READY = "Sistema listo. Seleccione un archivo de entrada."
    STATUS_FILE_SELECTED = lambda filename: f"✓ Archivo seleccionado: {filename}"
    STATUS_LOADING = "Cargando datos de entrada..."
    STATUS_LOADED = lambda n, m: f"✓ Datos cargados: {n} personas, {m} opiniones"
    STATUS_RUNNING = "⏳ Ejecutando modelo de optimización..."
    STATUS_COMPLETED = lambda time, pol: f"✓ Optimización completada en {time:.2f}s | Polarización: {pol:.3f}"
    STATUS_ERROR = "✗ Error durante la ejecución"
    STATUS_SAVED = lambda file: f"✓ Resultado guardado en: {file}"
    STATUS_CLEANED = "Interfaz limpiada. Lista para nueva ejecución."
    
    # Información de parámetros
    INFO_N = "Número total de personas en la población"
    INFO_M = "Número de opiniones posibles"
    INFO_CT = "Costo total máximo permitido para los esfuerzos"
    INFO_MOVS = "Cantidad máxima de movimientos permitidos"
    INFO_POL = "Valor de polarización final (menor es mejor)"
    
    # Errores
    ERROR_NO_FILE = "Error: No se ha seleccionado ningún archivo"
    ERROR_INVALID_FILE = "Error: El archivo no tiene el formato correcto"
    ERROR_MINIZINC = "Error: MiniZinc no está instalado o no está en el PATH"
    ERROR_NO_SOLUTION = "Error: No se encontró ninguna solución"
    ERROR_TIMEOUT = "Error: Tiempo límite de ejecución excedido"
    ERROR_PARSE = lambda msg: f"Error al parsear entrada: {msg}"
    ERROR_SAVE = lambda msg: f"Error al guardar: {msg}"
    
    # Ayuda
    HELP_FORMAT = """
Formato del archivo de entrada (.txt):

Línea 1: n (número de personas)
Línea 2: m (número de opiniones)
Línea 3: distribución de personas por opinión (p₁,p₂,...,pₘ)
Línea 4: valores de las opiniones (v₁,v₂,...,vₘ)
Líneas 5 a 4+m: resistencias por opinión (bajo,medio,alto)
Línea 5+m: costo total máximo (ct)
Línea 6+m: movimientos máximos (maxMovs)
"""
    
    # Créditos
    CREDITS = "Andrey Quiceño • Iván • Francesco • Jonathan | Universidad del Valle | 2025"
