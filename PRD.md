# PRD-001: Gestor Inteligente de Gastos Personales — Control de gastos personales, compartidos y ahorros

**Versión:** 1.0  
**Estado:** MVP — Módulo 1 AI-First Builders Lab 2026

## Contexto y Problema

Actualmente, el control manual de gastos mediante planillas requiere tiempo y es propenso a errores de carga y cálculo. A medida que aumenta la cantidad de movimientos, resulta fácil perder el seguimiento de las cuentas, especialmente cuando existen gastos compartidos con otras personas.

Además, el monto pagado inicialmente no siempre representa el gasto personal real. Por ejemplo, una persona puede pagar una compra completa y luego recibir parte del dinero de otros participantes. El sistema de control debe permitir diferenciar cuánto se pagó, cuánto corresponde a cada participante y cuánto representa finalmente el gasto propio.

La aplicación busca simplificar este proceso mediante una carga de gastos más rápida e intuitiva, reduciendo el trabajo manual y las posibilidades de error, sin perder la facilidad de consulta, modificación y corrección que proporciona actualmente una planilla.

### Persona

Usuario principal: persona adulta que desea llevar un control cotidiano de sus gastos personales, compartidos y ahorros de una manera simple, rápida y con menor riesgo de errores que mediante un registro manual en una planilla.

## Objetivos

- O-01. Simplificar el control cotidiano de los gastos personales y compartidos.

- O-02. Reducir el tiempo y esfuerzo necesarios para registrar y mantener actualizado el control de gastos.

- O-03. Facilitar la comprensión de cómo se distribuyen los gastos del usuario para ayudarlo a planificar mejor sus ahorros.

- O-04. Permitir diferenciar el dinero destinado a consumo del dinero destinado al ahorro.

## Requerimientos Funcionales (RF-01, RF-02, …)

### RF-01 — Registro de gastos

El sistema debe permitir registrar un gasto indicando como mínimo nombre, monto y categoría, y opcionalmente una descripción.

### RF-02 — Tipo de gasto

El sistema debe permitir clasificar un gasto como personal, compartido en partes iguales o compartido con distribución personalizada.

### RF-03 — División equitativa

El sistema debe permitir dividir un gasto compartido en partes iguales entre los participantes seleccionados.

### RF-04 — División personalizada

El sistema debe permitir definir manualmente el monto correspondiente a cada participante de un gasto compartido.

### RF-05 — Gasto personal real

El sistema debe calcular automáticamente qué parte de un gasto corresponde realmente al usuario, independientemente del monto total que haya pagado.

### RF-06 — Configuración del dinero disponible

El sistema debe permitir al usuario definir el monto de dinero disponible para gastos.

### RF-07 — Modificación del dinero disponible

El sistema debe permitir al usuario modificar el monto de dinero disponible para gastos.

### RF-08 — Dinero consumido

El sistema debe mostrar cuánto del dinero disponible fue consumido, considerando únicamente la parte correspondiente al usuario en los gastos registrados y el dinero destinado a ahorro.

### RF-09 — Dinero restante

El sistema debe mostrar cuánto dinero permanece disponible, considerando únicamente la parte correspondiente al usuario en los gastos registrados y el dinero destinado a ahorro.

### RF-10 — Consulta de movimientos

El sistema debe permitir consultar los gastos registrados y visualizar sus datos.

### RF-11 — Edición de gastos

El sistema debe permitir modificar los datos de un gasto previamente registrado.

### RF-12 — Eliminación de gastos

El sistema debe permitir eliminar un gasto previamente registrado.

### RF-13 — Inicio del registro mediante audio

El sistema debe permitir iniciar el registro de un gasto mediante audio.

### RF-14 — Interpretación del audio

El sistema debe extraer del audio los datos necesarios para generar una propuesta de movimiento.

### RF-15 — Revisión de la propuesta de audio

El sistema debe permitir revisar los datos interpretados a partir del audio.

### RF-16 — Modificación de la propuesta de audio

El sistema debe permitir modificar los datos interpretados a partir del audio.

### RF-17 — Confirmación de la propuesta de audio

El sistema debe permitir confirmar el registro de la propuesta generada mediante audio.

### RF-18 — Visualización gráfica

El sistema debe presentar visualizaciones gráficas que permitan consultar la distribución de los gastos registrados.

### RF-19 — Recuperación de acceso

El sistema debe permitir al usuario iniciar un proceso de recuperación de acceso a su cuenta.

### RF-20 — Registro de participantes

El sistema debe permitir registrar participantes que puedan ser asociados a gastos compartidos.

### RF-21 — Modificación de participantes

El sistema debe permitir modificar participantes registrados.

### RF-22 — Eliminación de participantes

El sistema debe permitir eliminar participantes registrados.

### RF-23 — Configuración inicial de ahorros

El sistema debe permitir al usuario registrar el monto inicial de ahorros en USD que posee.

### RF-24 — Registro de ahorro en USD

El sistema debe permitir registrar una compra de USD indicando como mínimo la cantidad de USD adquiridos y el monto utilizado para realizar la compra.

### RF-25 — Impacto del ahorro sobre el disponible

El sistema debe descontar del dinero disponible el monto destinado a una compra de USD.

### RF-26 — Total de ahorros

El sistema debe mostrar el total de USD ahorrados.

### RF-27 — Compras de USD por período

El sistema debe mostrar las compras de USD realizadas durante cada período.

## Requerimientos No Funcionales (RNF-01, …)

### RNF-01 — Persistencia de datos

El 100% de los gastos y operaciones confirmados correctamente debe permanecer almacenado hasta que el usuario realice explícitamente una operación que provoque su eliminación.

### RNF-02 — Accesibilidad de la carga

La acción para iniciar el registro de un nuevo gasto debe estar disponible desde la pantalla principal y requerir como máximo una interacción para abrir el formulario de carga.

### RNF-03 — Diseño responsive

El 100% de las pantallas necesarias para ejecutar los criterios de aceptación debe poder visualizarse y operarse sin desplazamiento horizontal, sin contenido cortado y con todos los controles visibles y utilizables en esta matriz fija de prueba del MVP: Safari en iOS 14 con un viewport de 390 × 844 píxeles CSS y Chrome en Android 12 con un viewport de 360 × 800 píxeles CSS, en ambos casos con orientación vertical y zoom del 100%.

### RNF-04 — Precisión de interpretación por audio

El porcentaje de casos en los que el sistema interpreta correctamente los datos necesarios para registrar un gasto debe ser ≥ 60% sobre un conjunto fijo de 20 casos de prueba del MVP definidos para la entrada por audio; esto equivale a interpretar correctamente al menos 12 de los 20 casos.

### RNF-05 — Seguridad de credenciales

La cantidad de credenciales de autenticación almacenadas o expuestas en texto plano debe ser 0.

### RNF-06 — Rendimiento de autenticación

En una prueba de 100 inicios de sesión válidos ejecutada con 5 usuarios virtuales concurrentes, al menos 95 intentos deben completarse en un máximo de 4 segundos, medidos desde la recepción de la solicitud hasta la entrega de la respuesta HTTP completa. La prueba debe ejecutarse con el backend y SQLite en un entorno fijo de 2 vCPU y 4 GB de RAM, sin llamadas a servicios externos, después de 10 solicitudes de calentamiento excluidas de la medición.

## Criterios de Aceptación (AC-01 (RF-01): Dado / Cuando / Entonces)

### AC-01 (RF-01) — Registro válido

Dado que el usuario se encuentra registrando un gasto,
Cuando ingresa el nombre "Supermercado", el monto $30.000, la categoría "Alimentos" y confirma el registro,
Entonces debe existir exactamente un nuevo movimiento con nombre "Supermercado", monto $30.000 y categoría "Alimentos" en su listado de gastos.

### AC-02 (RF-01) — Campos obligatorios

Dado que el usuario se encuentra registrando un gasto,
Cuando intenta confirmar sin nombre, sin monto o sin categoría,
Entonces no debe crearse ningún movimiento y el sistema debe identificar cada campo obligatorio faltante.

### AC-03 (RF-02) — Selección del tipo

Dado que el usuario se encuentra registrando un gasto,
Cuando selecciona el tipo "personal", "compartido en partes iguales" o "distribución personalizada",
Entonces el gasto en edición debe conservar exactamente el tipo seleccionado.

### AC-04 (RF-03) — División equitativa

Dado que el usuario tiene $500.000 disponibles,
Cuando registra un gasto de $30.000 compartido en partes iguales entre él y otro participante,
Entonces el sistema debe asignar $15.000 a cada participante, considerar $15.000 como gasto personal real y mostrar $485.000 disponibles.

### AC-05 (RF-04) — Distribución personalizada

Dado un gasto de $150.000 y otro participante registrado,
Cuando el usuario asigna $40.000 a sí mismo y $110.000 al otro participante,
Entonces la distribución guardada debe contener exactamente $40.000 asignados al usuario y $110.000 al otro participante.

### AC-06 (RF-04) — Cálculo personalizado

Dado que el usuario tiene $500.000 disponibles,
Cuando registra un gasto de $150.000 asignando $40.000 al usuario y $110.000 a otro participante,
Entonces el sistema debe considerar $40.000 como gasto personal real y mostrar $460.000 disponibles.

### AC-07 (RF-05) — Gasto personal real

Dado un gasto compartido de $150.000 con $40.000 asignados al usuario y $110.000 a otro participante,
Cuando el sistema calcula el gasto personal real,
Entonces el resultado debe ser $40.000.

### AC-08 (RF-06) — Configuración del disponible

Dado que el usuario todavía no configuró su dinero disponible,
Cuando define un monto de $500.000,
Entonces el monto disponible base almacenado debe ser $500.000.

### AC-09 (RF-07) — Modificación del disponible

Dado que el usuario tiene configurado un monto disponible base de $500.000, gastos personales reales por $40.000 y compras de USD por $150.000,
Cuando modifica el monto disponible base a $600.000,
Entonces el monto disponible base almacenado debe ser $600.000, el dinero consumido debe ser $190.000 y el dinero restante debe ser $410.000.

### AC-10 (RF-08) — Dinero consumido

Dado un monto disponible base de $500.000, gastos personales reales por $40.000 y compras de USD por $150.000,
Cuando el usuario consulta el dinero consumido,
Entonces el sistema debe mostrar $190.000 consumidos.

### AC-11 (RF-09) — Dinero restante

Dado un monto disponible base de $500.000, gastos personales reales por $40.000 y compras de USD por $150.000,
Cuando el usuario consulta el dinero restante,
Entonces el sistema debe mostrar $310.000 disponibles.

### AC-12 (RF-10) — Consulta de movimientos

Dado un gasto registrado con nombre "Supermercado", monto $30.000 y categoría "Alimentos",
Cuando el usuario accede al listado de gastos,
Entonces debe mostrarse un movimiento con nombre "Supermercado", monto $30.000 y categoría "Alimentos".

### AC-13 (RF-11) — Edición

Dado un monto disponible base de $500.000, ningún monto destinado a ahorro y un único gasto personal registrado con nombre "Supermercado" y monto $30.000,
Cuando el usuario cambia el monto del gasto a $35.000 y confirma la modificación,
Entonces debe existir un único movimiento "Supermercado" con monto $35.000, el dinero consumido debe ser $35.000 y el dinero restante debe ser $465.000.

### AC-14 (RF-12) — Eliminación

Dado un monto disponible base de $500.000, ningún monto destinado a ahorro y un único gasto personal registrado con nombre "Supermercado" y monto $30.000,
Cuando el usuario confirma la eliminación del gasto,
Entonces no debe existir el movimiento "Supermercado" en su listado, el dinero consumido debe ser $0 y el dinero restante debe ser $500.000.

### AC-15 (RF-13) — Inicio del registro mediante audio

Dado que el usuario seleccionó la carga mediante audio y la captura todavía no está activa,
Cuando inicia la carga mediante audio,
Entonces el sistema debe mostrar un indicador visible de que la captura de audio está activa.

### AC-16 (RF-14) — Interpretación del audio

Dado un audio interpretable que indica un gasto de $30.000 en supermercado dentro de la categoría "Alimentos",
Cuando el sistema procesa el audio,
Entonces debe generar una propuesta con monto $30.000, nombre "Supermercado" y categoría "Alimentos".

### AC-17 (RF-15) — Revisión de la propuesta de audio

Dada una propuesta de audio con nombre "Supermercado", monto $30.000 y categoría "Alimentos",
Cuando el usuario accede a la revisión,
Entonces debe ver el nombre "Supermercado", el monto $30.000 y la categoría "Alimentos" antes de confirmar el registro.

### AC-18 (RF-16) — Modificación de la propuesta de audio

Dada una propuesta de audio con monto $30.000,
Cuando el usuario modifica el monto a $35.000,
Entonces la propuesta debe mostrar $35.000 y no debe existir todavía un nuevo movimiento registrado.

### AC-19 (RF-17) — Confirmación de la propuesta de audio

Dada una propuesta de audio revisada con nombre "Supermercado", monto $35.000 y categoría "Alimentos",
Cuando el usuario confirma el registro,
Entonces debe existir exactamente un nuevo movimiento con nombre "Supermercado", monto $35.000 y categoría "Alimentos".

### AC-20 (RF-18) — Visualizaciones

Dado que existen dos gastos registrados por $40.000 y $60.000,
Cuando el usuario accede a la distribución gráfica de sus gastos,
Entonces la visualización debe representar ambos gastos con sus respectivos valores de $40.000 y $60.000, que totalizan $100.000, sin exigir una agrupación específica.

### AC-21 (RF-19) — Recuperación de acceso

Dado que existe una cuenta a la que el usuario no puede acceder,
Cuando el usuario solicita iniciar el proceso de recuperación mediante el mecanismo disponible,
Entonces el sistema debe mostrar una confirmación visible de que el proceso de recuperación fue iniciado.

### AC-22 (RF-20) — Alta de participantes

Dado que el usuario administra sus participantes,
Cuando registra un participante con nombre "Ana",
Entonces debe existir exactamente un nuevo participante llamado "Ana" disponible para futuros gastos compartidos.

### AC-23 (RF-21) — Modificación de participantes

Dado un participante registrado con nombre "Ana",
Cuando el usuario cambia su nombre a "Ana Pérez",
Entonces debe existir un único participante con nombre "Ana Pérez" y los gastos históricos asociados deben conservar sus montos y distribuciones originales.

### AC-24 (RF-22) — Eliminación de participantes

Dado un participante registrado con nombre "Ana" asociado a un gasto histórico,
Cuando el usuario elimina al participante,
Entonces "Ana" no debe estar disponible para nuevos gastos y el gasto histórico debe conservar sus montos y distribución originales.

### AC-25 (RF-23) — Ahorro inicial

Dado que el usuario todavía no configuró sus ahorros,
Cuando registra un monto inicial de USD 1.000,
Entonces el sistema debe mostrar USD 1.000 como ahorro acumulado inicial.

### AC-26 (RF-24) — Compra de USD

Dado que el usuario tiene $500.000 disponibles y USD 1.000 ahorrados,
Cuando registra una compra de USD 100 utilizando $150.000,
Entonces debe existir exactamente una nueva compra de USD 100 por $150.000.

### AC-27 (RF-25) — Impacto sobre el disponible

Dado que el usuario tiene $500.000 disponibles,
Cuando registra una compra de USD utilizando $150.000,
Entonces el sistema debe mostrar $350.000 como monto disponible restante.

### AC-28 (RF-26) — Ahorro acumulado

Dado que el usuario posee USD 1.000 ahorrados,
Cuando registra una nueva compra de USD 100,
Entonces el sistema debe mostrar USD 1.100 como ahorro acumulado.

### AC-29 (RF-27) — Ahorro mensual

Dado que existe una compra de USD 100 en enero y otra de USD 50 en febrero,
Cuando el usuario consulta enero,
Entonces el sistema debe mostrar únicamente la compra de USD 100 realizada en enero y un total de USD 100 adquiridos durante ese mes.

### AC-30 (RF-08, RF-09, RF-10, RF-26, RF-27) — Consulta de datos de otro usuario

Dado que A está autenticado y B es otro usuario que posee gastos, dinero consumido y restante, un total de ahorros y compras de USD propios,
Cuando A intenta consultar los gastos, el dinero consumido y restante, el total de ahorros y las compras de USD de B,
Entonces el sistema debe rechazar cada intento y no debe devolver a A ninguno de los datos de B.

### AC-31 (RF-07, RF-11, RF-21) — Modificación de datos de otro usuario

Dado que A está autenticado y B es otro usuario que tiene un monto disponible base de $500.000, un gasto de $30.000 y un participante llamado "Ana",
Cuando A intenta cambiar el monto disponible base de B a $600.000, el gasto de B a $35.000 y el nombre del participante de B a "Ana Pérez",
Entonces el sistema debe rechazar cada intento y B debe conservar el monto disponible base de $500.000, el gasto de $30.000 y el participante llamado "Ana".

### AC-32 (RF-12, RF-22) — Eliminación de datos de otro usuario

Dado que A está autenticado y B es otro usuario que posee un gasto de $30.000 y un participante llamado "Ana",
Cuando A intenta eliminar el gasto y el participante de B,
Entonces el sistema debe rechazar ambos intentos y B debe conservar el gasto de $30.000 y el participante llamado "Ana".

## Fuera de Alcance

### MVP

Para esta primera versión quedan explícitamente fuera:

- Integración automática con bancos, tarjetas de crédito, billeteras virtuales o Mercado Pago.
- Gestión o recomendación de inversiones.
- Aplicaciones móviles nativas para iOS y Android.
- Obtención automática de cotizaciones del dólar en tiempo real.
- Conversión automática del patrimonio ahorrado en USD a su valor actualizado en ARS.
- Funcionalidades contables o impositivas avanzadas.
- Recomendaciones avanzadas mediante IA sobre cómo reducir gastos o mejorar los hábitos financieros.

La funcionalidad de IA del MVP se concentra principalmente en facilitar el registro de movimientos mediante audio.

## Riesgos y Dependencias

### R-01 — Interpretación mediante audio

La interpretación incorrecta de montos, categorías, tipos de gasto o participantes puede generar propuestas incorrectas. Los movimientos generados mediante audio deberán ser revisados y confirmados por el usuario antes de almacenarse definitivamente.

### R-02 — Integridad de los datos

La pérdida o modificación incorrecta de movimientos históricos puede afectar el cálculo de gastos, dinero disponible y ahorros.

### R-03 — Cálculos compartidos

Errores en las reglas de distribución de gastos pueden producir valores incorrectos de gasto personal y dinero disponible.

### D-01 — Procesamiento de audio

La carga mediante voz dependerá de un mecanismo capaz de procesar e interpretar entradas de audio.

### D-02 — Persistencia

La aplicación dependerá de un mecanismo de almacenamiento persistente para conservar usuarios, movimientos, participantes, configuración y ahorros.

### D-03 — Autenticación

Las cuentas individuales dependerán de un mecanismo de autenticación y recuperación de acceso.
