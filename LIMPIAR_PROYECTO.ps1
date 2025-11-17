# ========================================
# Script de Limpieza del Proyecto Brain Rush
# ========================================

Write-Host "🧹 Iniciando limpieza del proyecto Brain Rush..." -ForegroundColor Cyan
Write-Host ""

# Crear carpeta de respaldo antes de eliminar
$backupFolder = ".\ARCHIVOS_OBSOLETOS_BACKUP_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupFolder -Force | Out-Null
Write-Host "📦 Carpeta de respaldo creada: $backupFolder" -ForegroundColor Green
Write-Host ""

# ========================================
# 1. SCRIPTS DE MIGRACIÓN SQL (ya aplicados)
# ========================================
$archivosSQLObsoletos = @(
    "agregar_cascada_eliminacion.sql",
    "agregar_cuestionario_recompensas.sql",
    "agregar_insignias_comprables.sql",
    "agregar_numero_grupo.sql",
    "agregar_onedrive_tokens.sql",
    "agregar_tiempo_pregunta.sql",
    "agregar_tipo_sala.sql",
    "crear_sistema_juego.sql",
    "crear_sistema_xp_insignias.sql",
    "crear_tabla_grupos_sala.sql",
    "crear_tabla_participantes_sala.sql",
    "crear_tienda_insignias.sql"
)

Write-Host "📂 Moviendo scripts SQL de migración obsoletos..." -ForegroundColor Yellow
foreach ($archivo in $archivosSQLObsoletos) {
    if (Test-Path $archivo) {
        Move-Item -Path $archivo -Destination $backupFolder -Force
        Write-Host "  ✓ Movido: $archivo" -ForegroundColor Gray
    }
}

# ========================================
# 2. SCRIPTS PYTHON DE MIGRACIÓN (ya ejecutados)
# ========================================
$archivosPythonMigracion = @(
    "agregar_tokens_simple.py",
    "ampliar_columna_pin_sala.py",
    "arreglar_fk_salas_juego.py",
    "configurar_cascada_eliminacion.py",
    "crear_tablas_xp.py",
    "crear_tienda_insignias.py",
    "demo_nivel_automatico.py",
    "ejecutar_agregar_tiempo.py",
    "ejecutar_migracion_recompensas.py",
    "ejecutar_sql.py",
    "inicializar_xp_estudiantes.py",
    "instalar_onedrive.py",
    "migracion_grupos.py",
    "migracion_sistema_juego.py",
    "migrar_numero_grupo.py",
    "obtener_tokens_onedrive.py",
    "obtener_tokens_simple.py",
    "recalcular_niveles.py",
    "recalcular_niveles_auto.py",
    "resetear_xp_estudiantes.py",
    "onedrive_auth.py"
)

Write-Host ""
Write-Host "📂 Moviendo scripts Python de migración obsoletos..." -ForegroundColor Yellow
foreach ($archivo in $archivosPythonMigracion) {
    if (Test-Path $archivo) {
        Move-Item -Path $archivo -Destination $backupFolder -Force
        Write-Host "  ✓ Movido: $archivo" -ForegroundColor Gray
    }
}

# ========================================
# 3. SCRIPTS DE PRUEBA (ya no necesarios)
# ========================================
$archivosPrueba = @(
    "probar_compra_insignia.py",
    "probar_conteo_insignias.py",
    "probar_deteccion_modo.py",
    "probar_eliminacion_cascada.py",
    "probar_generacion_pins.py",
    "probar_importacion_duplicados.py",
    "probar_nivel_automatico.py",
    "probar_progreso_insignias.py",
    "probar_sala_automatica.py",
    "probar_tienda_xp_acumulado.py",
    "probar_visualizacion_insignias.py",
    "prueba_final_nivel.py",
    "test_autenticacion.py",
    "test_control_acceso.py",
    "test_email.py",
    "test_jwt_auth.py",
    "test_jwt_automatico.py",
    "test_login.py",
    "verificar_estado_usuario.py",
    "verificar_onedrive.py",
    "verificar_pins_salas.py",
    "verificar_sistema_xp.py",
    "verificar_tiempos_preguntas.py",
    "verificar_y_arreglar_estado.py",
    "smtp_debug_server.py"
)

Write-Host ""
Write-Host "📂 Moviendo scripts de prueba obsoletos..." -ForegroundColor Yellow
foreach ($archivo in $archivosPrueba) {
    if (Test-Path $archivo) {
        Move-Item -Path $archivo -Destination $backupFolder -Force
        Write-Host "  ✓ Movido: $archivo" -ForegroundColor Gray
    }
}

# ========================================
# 4. DOCUMENTACIÓN OBSOLETA (ya completada)
# ========================================
$archivosDocObsoletos = @(
    "ACTUALIZACION_AUTENTICACION_COMPLETA.md",
    "AGREGAR_URLS_AZURE.md",
    "CONFIGURACION_ONEDRIVE_OAUTH2.md",
    "CONFIGURACION_ONEDRIVE_SISTEMA.md",
    "CONFIGURAR_CORREO_GMAIL.md",
    "CONFIGURAR_GMAIL.md",
    "CONFIGURAR_ONEDRIVE.md",
    "CONFIGURAR_ONEDRIVE_PYTHONANYWHERE.md",
    "CONTROL_ACCESO_RUTAS.md",
    "CORRECCION_ERRORES_AUTH.md",
    "CORRECCION_INSIGNIAS.txt",
    "EXPORTACION_GOOGLE_SHEETS.md",
    "EXPORTACION_ONEDRIVE_PYTHONANYWHERE.md",
    "GUIA_EXPORTACION_ONEDRIVE.md",
    "IMPLEMENTAR_DOS_MODOS_JUEGO.md",
    "IMPORTACION_EXCEL_PREGUNTAS.md",
    "INSTALACION_RAPIDA_EMAIL.md",
    "MIGRACION_COMPLETADA.md",
    "MIGRACION_JWT.md",
    "MIGRACION_JWT_EXTENDED_COMPLETA.md",
    "MIGRACION_ONEDRIVE.md",
    "OBTENER_TOKENS_ONEDRIVE.md",
    "RECOMPENSAS_AUTOMATICAS.md",
    "RENOVACION_AUTOMATICA_TOKENS.md",
    "RESUMEN_CAMBIOS.md",
    "RESUMEN_IMPLEMENTACION_ONEDRIVE.md",
    "RESUMEN_IMPLEMENTACION_ONEDRIVE.txt",
    "SISTEMA_PINS_AUTOMATICOS.txt"
)

Write-Host ""
Write-Host "📂 Moviendo documentación obsoleta..." -ForegroundColor Yellow
foreach ($archivo in $archivosDocObsoletos) {
    if (Test-Path $archivo) {
        Move-Item -Path $archivo -Destination $backupFolder -Force
        Write-Host "  ✓ Movido: $archivo" -ForegroundColor Gray
    }
}

# ========================================
# 5. COLECCIÓN ANTIGUA DE POSTMAN
# ========================================
Write-Host ""
Write-Host "📂 Moviendo colección antigua de Postman..." -ForegroundColor Yellow
if (Test-Path "Brain_Rush_API_Collection.postman_collection.json") {
    Move-Item -Path "Brain_Rush_API_Collection.postman_collection.json" -Destination $backupFolder -Force
    Write-Host "  ✓ Movido: Brain_Rush_API_Collection.postman_collection.json (usar Part1-4)" -ForegroundColor Gray
}

# ========================================
# 6. ARCHIVOS DE CONFIGURACIÓN TEMPORAL
# ========================================
$archivosConfigTemp = @(
    "comandos.txt",
    "requirements_onedrive.txt"
)

Write-Host ""
Write-Host "📂 Moviendo archivos de configuración temporal..." -ForegroundColor Yellow
foreach ($archivo in $archivosConfigTemp) {
    if (Test-Path $archivo) {
        Move-Item -Path $archivo -Destination $backupFolder -Force
        Write-Host "  ✓ Movido: $archivo" -ForegroundColor Gray
    }
}

# ========================================
# 7. LIMPIAR __pycache__ y VENV ANTIGUO
# ========================================
Write-Host ""
Write-Host "📂 Limpiando cache de Python..." -ForegroundColor Yellow

# Limpiar __pycache__
if (Test-Path "__pycache__") {
    Remove-Item -Path "__pycache__" -Recurse -Force
    Write-Host "  ✓ Eliminado: __pycache__" -ForegroundColor Gray
}

# Limpiar __pycache__ en controladores
if (Test-Path "controladores\__pycache__") {
    Remove-Item -Path "controladores\__pycache__" -Recurse -Force
    Write-Host "  ✓ Eliminado: controladores\__pycache__" -ForegroundColor Gray
}

# Advertencia sobre venv
if (Test-Path "venv") {
    Write-Host ""
    Write-Host "⚠️  ADVERTENCIA: Se encontró carpeta 'venv' (entorno virtual duplicado)" -ForegroundColor Red
    Write-Host "   Ya existe '.venv' como entorno principal." -ForegroundColor Yellow
    Write-Host "   Si no lo estás usando, puedes eliminarlo manualmente con:" -ForegroundColor Yellow
    Write-Host "   Remove-Item -Path venv -Recurse -Force" -ForegroundColor White
}

# ========================================
# 8. RESUMEN
# ========================================
Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "✅ LIMPIEZA COMPLETADA" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Resumen:" -ForegroundColor Cyan
Write-Host "  • Scripts SQL de migración: movidos" -ForegroundColor Gray
Write-Host "  • Scripts Python de migración: movidos" -ForegroundColor Gray
Write-Host "  • Scripts de prueba: movidos" -ForegroundColor Gray
Write-Host "  • Documentación obsoleta: movida" -ForegroundColor Gray
Write-Host "  • Colección Postman antigua: movida" -ForegroundColor Gray
Write-Host "  • Cache de Python: eliminado" -ForegroundColor Gray
Write-Host ""
Write-Host "📦 Todos los archivos movidos están en:" -ForegroundColor Yellow
Write-Host "   $backupFolder" -ForegroundColor White
Write-Host ""
Write-Host "📋 Archivos IMPORTANTES que se mantienen:" -ForegroundColor Green
Write-Host "  ✓ main.py, api_crud.py, bd.py, config.py, utils_auth.py, extensions.py" -ForegroundColor Gray
Write-Host "  ✓ requirements.txt, .env" -ForegroundColor Gray
Write-Host "  ✓ controladores/" -ForegroundColor Gray
Write-Host "  ✓ static/, Templates/" -ForegroundColor Gray
Write-Host "  ✓ Brain_Rush_API_Complete_Part1-4.postman_collection.json" -ForegroundColor Gray
Write-Host "  ✓ bd.sql, database_schema_complete.sql" -ForegroundColor Gray
Write-Host "  ✓ GUIA_INSIGNIAS.md, GUIA_NOTIFICACIONES.md, GUIA_POSTMAN_API_CRUD.md" -ForegroundColor Gray
Write-Host "  ✓ SISTEMA_JUEGO_README.md, SISTEMA_XP_INSIGNIAS.md" -ForegroundColor Gray
Write-Host "  ✓ PRUEBA_JWT_TOKEN.md" -ForegroundColor Gray
Write-Host ""
Write-Host "Restaurar archivos: Move-Item -Path CARPETA_BACKUP\archivo -Destination ." -ForegroundColor Cyan
Write-Host ""
