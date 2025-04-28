import random

level_configs = [
    {
        "num_answers": 2,
        "items_per_answer": 1,
        "num_distractors": 0,
        "time_start_range": (20, 30),
    },
    {
        "num_answers": 3,
        "items_per_answer": 2,
        "num_distractors": 1,
        "time_start_range": (45, 55),
    },
    {
        "num_answers": 3,
        "items_per_answer": 3,
        "num_distractors": 2,
        "time_start_range": (55, 60),
    },
    {
        "num_answers": 4,
        "items_per_answer": 3,
        "num_distractors": 3,
        "time_start_range": (70, 90),
    },
    {
        "num_answers": 4,
        "items_per_answer": 4,
        "num_distractors": 4,
        "time_start_range": (85, 110),
    },
]

ITEMS_POOL = [
    # Boot basics
    {"label": "Realiza comprobaciones básicas de hardware al encender", "correct_answer": "POST"},
    {"label": "Inicializa configuraciones básicas de hardware", "correct_answer": "BIOS"},
    {"label": "Gestiona el arranque seguro y moderno de sistemas", "correct_answer": "UEFI"},
    {"label": "Selecciona el dispositivo de arranque según prioridades", "correct_answer": "Boot Priority"},
    {"label": "Carga la partición de arranque primaria del disco", "correct_answer": "MBR"},

    # Bootloaders
    {"label": "Carga el gestor que permitirá iniciar un sistema operativo", "correct_answer": "Bootloader"},
    {"label": "Muestra un menú para elegir entre múltiples sistemas", "correct_answer": "GRUB"},
    {"label": "Carga los archivos iniciales del sistema operativo", "correct_answer": "OS Loader"},

    # Kernel and early OS
    {"label": "Carga el núcleo del sistema operativo en la memoria RAM", "correct_answer": "Kernel"},
    {"label": "Expande módulos del núcleo necesarios para dispositivos", "correct_answer": "Kernel Modules"},
    {"label": "Monta el sistema de archivos raíz en memoria", "correct_answer": "File System Mount"},
    {"label": "Carga una imagen de disco temporal en la RAM", "correct_answer": "Initrd"},

    # Early system services
    {"label": "Ejecuta el primer proceso de espacio de usuario (init)", "correct_answer": "Init"},
    {"label": "Gestiona los servicios y procesos del sistema operativo moderno", "correct_answer": "Systemd"},
    {"label": "Inicia servicios esenciales como redes y discos", "correct_answer": "Startup Services"},
    {"label": "Monta automáticamente particiones adicionales", "correct_answer": "File System Mount"},

    # Drivers and Devices
    {"label": "Inicializa los controladores de dispositivos básicos", "correct_answer": "Device Drivers"},
    {"label": "Verifica la funcionalidad de la memoria RAM", "correct_answer": "Memory Check"},
    {"label": "Conecta dispositivos de entrada y salida (teclado, mouse)", "correct_answer": "Hardware Initialization"},

    # Security and Recovery
    {"label": "Valida firmas digitales antes de iniciar", "correct_answer": "Secure Boot"},
    {"label": "Carga herramientas de recuperación de sistema", "correct_answer": "Recovery Partition"},
    {"label": "Permite restaurar el sistema a un estado funcional", "correct_answer": "Recovery Partition"},

    # User Space and Login
    {"label": "Muestra la pantalla de login para ingresar al sistema", "correct_answer": "Login Manager"},
    {"label": "Inicia una consola o intérprete de comandos", "correct_answer": "Shell"},

    # Advanced checks
    {"label": "Verifica la integridad del disco duro en busca de errores", "correct_answer": "Disk Check"},
    {"label": "Comprueba dispositivos de almacenamiento conectados", "correct_answer": "Disk Check"},
    {"label": "Prepara el sistema de archivos para su uso", "correct_answer": "File System Mount"},

    # Specifics for Windows
    {"label": "Carga el gestor de arranque de Windows (winload.exe)", "correct_answer": "Bootloader"},
    {"label": "Inicializa el núcleo NT de Windows", "correct_answer": "Kernel"},

    # Additional system concepts
    {"label": "Asigna direcciones de memoria virtual", "correct_answer": "Kernel Modules"},
    {"label": "Detecta y enumera todos los dispositivos conectados", "correct_answer": "Hardware Initialization"},
    {"label": "Aplica configuraciones de arranque avanzadas", "correct_answer": "UEFI"},
    {"label": "Protege contra alteraciones en el sistema operativo", "correct_answer": "Secure Boot"},
    {"label": "Prepara variables de entorno iniciales del sistema", "correct_answer": "Init"},
    {"label": "Carga configuraciones de arranque predefinidas", "correct_answer": "BIOS"},

    # Fun/Extra ideas
    {"label": "Prepara los controladores gráficos para el entorno visual", "correct_answer": "Device Drivers"},
    {"label": "Inicializa los adaptadores de red durante el arranque", "correct_answer": "Startup Services"},
    {"label": "Carga configuración de fecha y hora del sistema", "correct_answer": "BIOS"},
    {"label": "Inicia procesos críticos del sistema en orden correcto", "correct_answer": "Systemd"},
]

def generate_random_level(num_answers=3, items_per_answer=2, num_distractors=2):
    # 1. Get all unique possible answers
    all_answers = list({item["correct_answer"] for item in ITEMS_POOL})
    selected_answers = random.sample(all_answers, num_answers)

    # 2. Build the answer list
    answers = selected_answers

    # 3. Build the item list
    items = []

    for answer in answers:
        # Get all matching items for that answer
        matching_items = [item for item in ITEMS_POOL if item["correct_answer"] == answer]

        # Pick up to 'items_per_answer' matching items (without replacement if possible)
        picked = random.sample(matching_items, min(len(matching_items), items_per_answer))
        items.extend(picked)

    # 4. Add distractor items
    distractor_pool = [item for item in ITEMS_POOL if item["correct_answer"] not in answers]
    distractors = random.sample(distractor_pool, min(len(distractor_pool), num_distractors))

    for dis in distractors:
        items.append({"label": dis["label"], "correct_answer": None})

    # 5. Shuffle the final list
    random.shuffle(items)

    return {
        "answers": answers,
        "items": items
    }