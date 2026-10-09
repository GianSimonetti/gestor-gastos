# PRD-001: Gestor Inteligente de Gastos Personales — Control colaborativo de gastos, disponible y ahorros por tablero

**Versión:** 2.0  
**Estado:** MVP — Módulo 1 AI-First Builders Lab 2026

## Contexto y Problema

El control manual de gastos mediante planillas requiere tiempo y es propenso a errores de carga y cálculo. A medida que aumenta la cantidad de gastos, resulta fácil perder el seguimiento del dinero disponible, especialmente cuando varias personas comparten gastos.

El monto pagado por una persona no siempre coincide con la parte del gasto que le corresponde. El producto debe distinguir el monto total que reduce el disponible mensual del tablero, la parte asignada a cada persona y los importes que las demás personas deben devolverle al pagador.

La aplicación busca simplificar este proceso mediante una carga rápida y revisable, sin perder la facilidad de consulta, modificación y corrección de una planilla. Cada usuario debe autenticarse para crear un tablero o incorporarse a uno mediante un código de invitación. Los datos financieros pertenecen al tablero y pueden ser operados por sus miembros.

### Personas

- **Usuario con cuenta:** persona autenticada que crea un tablero o se incorpora a uno mediante un código y opera sus datos.
- **Participante sin cuenta:** persona representada dentro de un tablero para distribuir gastos, sin acceso a la aplicación.

### Definiciones del MVP

- **Tablero:** contenedor al que pertenecen los gastos, participantes sin cuenta, disponible mensual y ahorros.
- **Miembro:** usuario con cuenta que pertenece al tablero. Todos los miembros pueden operar dentro de él; el MVP no define roles adicionales.
- **Persona del tablero:** miembro o participante sin cuenta que puede ser pagador o recibir una parte asignada de un gasto.
- **Período mensual:** mes calendario determinado con la zona horaria de Argentina.
- **Disponible base:** importe en ARS configurado para un período mensual del tablero.
- **Dinero consumido:** suma de los montos totales de los gastos y de los importes en ARS utilizados para comprar USD durante el período mensual.
- **Dinero restante:** disponible base menos dinero consumido. Puede ser negativo.
- **Parte asignada:** importe de un gasto que corresponde a una persona, separado del impacto total del gasto sobre el disponible.
- **Deuda con el pagador:** parte asignada a una persona distinta del pagador que debe devolverle a este. El MVP calcula esa deuda, pero no gestiona su liquidación.
- Los gastos y el disponible se expresan en ARS y admiten centavos. Los ahorros se expresan en USD.

## Objetivos

- O-01. Simplificar el control cotidiano de los gastos personales y compartidos.
- O-02. Reducir el tiempo y esfuerzo necesarios para registrar y mantener actualizado el control de gastos.
- O-03. Facilitar la comprensión de cómo se distribuyen los gastos para ayudar a planificar mejor los ahorros.
- O-04. Permitir diferenciar el dinero destinado a consumo del dinero destinado al ahorro.

## Requerimientos Funcionales

### RF-01 — Registro de cuenta

El sistema debe permitir registrar una cuenta mediante email y contraseña.

### RF-02 — Inicio de sesión

El sistema debe permitir iniciar sesión mediante email y contraseña.

### RF-03 — Cierre de sesión

El sistema debe permitir cerrar la sesión activa.

### RF-04 — Inicio de recuperación de acceso

El sistema debe enviar por email un mecanismo de recuperación de acceso a la cuenta solicitada.

### RF-05 — Restablecimiento de contraseña

El sistema debe permitir definir una nueva contraseña mediante un mecanismo de recuperación vigente.

### RF-06 — Creación de tablero

El sistema debe permitir a un usuario autenticado crear un tablero.

### RF-07 — Código de invitación

El sistema debe permitir que cualquier miembro obtenga el código de invitación del tablero para compartirlo.

### RF-08 — Incorporación a un tablero

El sistema debe permitir a un usuario autenticado incorporarse a un tablero mediante su código de invitación.

### RF-09 — Registro de participantes sin cuenta

El sistema debe permitir registrar un participante sin cuenta dentro de un tablero.

### RF-10 — Modificación de participantes sin cuenta

El sistema debe permitir modificar un participante sin cuenta del tablero.

### RF-11 — Eliminación de participantes sin cuenta

El sistema debe permitir eliminar un participante sin cuenta del tablero para futuros gastos.

### RF-12 — Registro de gastos

El sistema debe permitir registrar un gasto con nombre, monto total en ARS, categoría, fecha, pagador y una descripción opcional.

### RF-13 — Fecha predeterminada del gasto

El sistema debe asignar al gasto la fecha de creación en la zona horaria de Argentina cuando el usuario no indique una fecha.

### RF-14 — Tipo de gasto

El sistema debe permitir clasificar un gasto como personal, compartido en partes iguales o compartido con distribución personalizada.

### RF-15 — División equitativa

El sistema debe distribuir un gasto compartido en partes iguales entre las personas seleccionadas.

### RF-16 — Residuo de división equitativa

El sistema debe distribuir de forma determinista cualquier residuo de centavos producido por una división equitativa.

### RF-17 — División personalizada

El sistema debe permitir definir el importe correspondiente a cada persona en un gasto compartido.

### RF-18 — Validación de la división personalizada

El sistema debe rechazar una distribución personalizada que contenga importes negativos o cuya suma no coincida exactamente con el monto total del gasto.

### RF-19 — Partes asignadas

El sistema debe calcular la parte del gasto asignada a cada persona seleccionada.

### RF-20 — Deudas con el pagador

El sistema debe calcular cuánto debe devolverle al pagador cada persona distinta de este según su parte asignada.

### RF-21 — Consulta del listado de gastos

El sistema debe permitir consultar los gastos registrados en el tablero.

### RF-22 — Consulta del detalle de un gasto

El sistema debe permitir visualizar los datos de un gasto registrado en el tablero.

### RF-23 — Edición de gastos

El sistema debe permitir modificar los datos de un gasto registrado en el tablero.

### RF-24 — Eliminación de gastos

El sistema debe permitir eliminar un gasto registrado en el tablero únicamente después de que un miembro confirme la operación.

### RF-25 — Inicio del registro mediante audio

El sistema debe permitir iniciar la captura de audio para registrar un gasto.

### RF-26 — Extracción de datos del audio

El sistema debe intentar interpretar los datos relevantes presentes en el audio para registrar el gasto, incluidos, cuando correspondan, el tipo de gasto, el pagador y los participantes.

### RF-27 — Generación de propuesta desde audio

El sistema debe generar una propuesta de gasto con los datos extraídos del audio.

### RF-28 — Propuesta de audio incompleta

El sistema debe mostrar como editable una propuesta de audio aunque falte alguno de los datos obligatorios.

### RF-29 — Revisión de la propuesta de audio

El sistema debe permitir revisar toda propuesta generada desde el audio antes de registrarla.

### RF-30 — Modificación de la propuesta de audio

El sistema debe permitir modificar los datos de toda propuesta generada desde el audio.

### RF-31 — Confirmación de la propuesta de audio

El sistema debe permitir registrar como gasto una propuesta de audio que contenga todos los datos obligatorios válidos.

### RF-32 — Distribución gráfica por categoría

El sistema debe mostrar la distribución de los gastos del período mensual por categoría.

### RF-33 — Configuración del disponible mensual

El sistema debe permitir definir el disponible base en ARS de un tablero para un período mensual.

### RF-34 — Modificación del disponible mensual

El sistema debe permitir modificar el disponible base de un período mensual del tablero.

### RF-35 — Dinero consumido mensual

El sistema debe mostrar el dinero consumido del tablero durante el período mensual.

### RF-36 — Dinero restante mensual

El sistema debe mostrar el dinero restante del tablero durante el período mensual.

### RF-37 — Registro del ahorro inicial

El sistema debe permitir registrar el monto inicial de ahorros en USD del tablero.

### RF-38 — Edición del ahorro inicial

El sistema debe permitir modificar el registro de ahorro inicial en USD del tablero.

### RF-39 — Eliminación del ahorro inicial

El sistema debe permitir eliminar el registro de ahorro inicial en USD del tablero.

### RF-40 — Registro de compra de USD

El sistema debe permitir registrar una compra indicando la cantidad de USD adquiridos, el importe utilizado en ARS y la fecha.

### RF-41 — Fecha predeterminada de la compra de USD

El sistema debe asignar a una compra de USD la fecha de creación en la zona horaria de Argentina cuando el usuario no indique una fecha.

### RF-42 — Edición de compra de USD

El sistema debe permitir modificar una compra de USD registrada en el tablero.

### RF-43 — Eliminación de compra de USD

El sistema debe permitir eliminar una compra de USD registrada en el tablero.

### RF-44 — Impacto de la compra de USD

El sistema debe incluir el importe en ARS de cada compra de USD en el dinero consumido del período mensual correspondiente a su fecha.

### RF-45 — Total de ahorros

El sistema debe mostrar el total de USD ahorrados en el tablero.

### RF-46 — Compras de USD por período

El sistema debe mostrar las compras de USD del tablero correspondientes al período mensual consultado.

## Requerimientos No Funcionales

### RNF-01 — Persistencia de datos

El 100% de las cuentas, pertenencias a tableros, participantes, gastos, configuraciones mensuales del disponible y registros de ahorro confirmados debe conservarse después de reiniciar el backend y hasta que un miembro ejecute una operación explícita de modificación o eliminación sobre el dato correspondiente.

### RNF-02 — Accesibilidad de la carga

La acción para iniciar el registro de un nuevo gasto debe estar disponible desde la pantalla principal del tablero y requerir como máximo 1 interacción para abrir el formulario de carga.

### RNF-03 — Diseño responsive

El 100% de las pantallas necesarias para ejecutar los criterios de aceptación debe poder visualizarse y operarse sin desplazamiento horizontal, sin contenido cortado y con todos los controles visibles y utilizables en esta matriz fija de prueba del MVP: Safari en iOS 14 con un viewport de 390 × 844 píxeles CSS y Chrome en Android 12 con un viewport de 360 × 800 píxeles CSS, en ambos casos con orientación vertical y zoom del 100%.

### RNF-04 — Precisión de interpretación por audio

El sistema debe interpretar correctamente los datos relevantes presentes en al menos 12 de los 20 audios de un conjunto fijo de evaluación del MVP, equivalente a una precisión mínima del 60%. El conjunto debe definirse antes de ejecutar la prueba, usar español de Argentina, identificar para cada caso los datos relevantes expresados y sus valores esperados, y mantenerse sin cambios durante la evaluación. Los datos esperados deben incluir, cuando estén presentes en el audio, el tipo de gasto, el pagador y los participantes. Un caso cuenta como correcto únicamente si todos sus valores esperados coinciden con la interpretación del sistema.

### RNF-05 — Seguridad de credenciales

La cantidad de credenciales de autenticación almacenadas o expuestas en texto plano debe ser 0.

### RNF-06 — Rendimiento de autenticación

En una prueba de 100 inicios de sesión válidos ejecutada con 5 usuarios virtuales concurrentes, al menos 95 intentos deben completarse en un máximo de 4 segundos, medidos desde la recepción de la solicitud hasta la entrega de la respuesta HTTP completa. La prueba debe ejecutarse con el backend y SQLite en un entorno fijo de 2 vCPU y 4 GB de RAM, sin llamadas a servicios externos, después de 10 solicitudes de calentamiento excluidas de la medición.

## Criterios de Aceptación

### AC-01 (RF-01) — Registro de cuenta

Dado un email no registrado y una contraseña válida, cuando una persona confirma el registro, entonces debe existir exactamente una cuenta asociada a ese email.

### AC-02 (RF-02) — Inicio de sesión

Dada una cuenta registrada, cuando el usuario ingresa su email y contraseña válidos, entonces debe acceder a una sesión autenticada correspondiente a esa cuenta.

### AC-03 (RF-03) — Cierre de sesión

Dada una sesión autenticada, cuando el usuario cierra sesión, entonces la aplicación debe dejar de mostrar los datos de sus tableros y debe exigir autenticación para volver a acceder a ellos.

### AC-04 (RF-04) — Inicio de recuperación

Dada una cuenta registrada con un email accesible, cuando el usuario solicita recuperar el acceso, entonces debe recibirse en ese email un mecanismo de recuperación vigente asociado a la cuenta.

### AC-05 (RF-05) — Restablecimiento de contraseña

Dado un mecanismo de recuperación vigente, cuando el usuario define una nueva contraseña válida, entonces la contraseña anterior debe ser rechazada y la nueva debe permitir iniciar sesión.

### AC-06 (RF-06) — Creación de tablero

Dado un usuario autenticado sin un tablero llamado Hogar, cuando crea el tablero Hogar, entonces debe existir exactamente un tablero con ese nombre y el usuario debe figurar como miembro.

### AC-07 (RF-07) — Código de invitación

Dado cualquier miembro del tablero Hogar, cuando solicita su código de invitación, entonces el sistema debe mostrar un código asociado a ese tablero que el miembro pueda compartir.

### AC-08 (RF-08) — Incorporación mediante código

Dado un usuario autenticado que no pertenece a Hogar y un código de invitación asociado a ese tablero, cuando ingresa el código, entonces debe figurar como miembro de Hogar y poder consultar su listado de gastos.

### AC-09 (RF-09) — Alta de participante sin cuenta

Dado un miembro que opera el tablero Hogar, cuando registra un participante sin cuenta llamado Ana, entonces debe existir exactamente un participante llamado Ana disponible para nuevos gastos del tablero.

### AC-10 (RF-10) — Modificación de participante sin cuenta

Dado un participante sin cuenta llamado Ana, cuando un miembro cambia su nombre a Ana Pérez, entonces debe existir un único participante llamado Ana Pérez y los gastos históricos asociados deben conservar sus montos y distribuciones.

### AC-11 (RF-11) — Eliminación de participante sin cuenta

Dado un participante sin cuenta llamado Ana asociado a un gasto histórico, cuando un miembro lo elimina, entonces Ana no debe estar disponible para nuevos gastos y el gasto histórico debe conservar su monto y distribución.

### AC-12 (RF-12) — Registro de gasto

Dado el tablero Hogar y una persona del tablero seleccionada como pagador, cuando un miembro registra un gasto con nombre Supermercado, monto ARS 30.000,00, categoría Alimentos y fecha 15/01/2026, entonces debe existir exactamente un gasto con esos datos y ese pagador en el tablero.

### AC-13 (RF-13) — Fecha predeterminada del gasto

Dado que en Argentina es 15/01/2026, cuando un miembro registra un gasto sin indicar fecha, entonces el gasto debe quedar registrado con fecha 15/01/2026.

### AC-14 (RF-14) — Persistencia del tipo de gasto

Dado que un miembro registra un gasto, cuando selecciona el tipo personal, compartido en partes iguales o distribución personalizada y confirma el registro, entonces el gasto almacenado debe conservar exactamente el tipo seleccionado.

### AC-15 (RF-15) — División equitativa

Dado un gasto de ARS 30.000,00 y dos personas seleccionadas, cuando un miembro elige la división equitativa, entonces cada persona debe tener asignados ARS 15.000,00.

### AC-16 (RF-16) — Residuo determinista

Dado un gasto de ARS 100,00, tres personas seleccionadas en el mismo orden y la división equitativa, cuando se calcula la distribución más de una vez, entonces cada cálculo debe producir la misma asignación de centavos y la suma debe ser ARS 100,00.

### AC-17 (RF-17) — División personalizada

Dado un gasto de ARS 150.000,00, cuando un miembro asigna ARS 40.000,00 al pagador y ARS 110.000,00 a Ana, entonces la distribución guardada debe contener exactamente esos dos importes.

### AC-18 (RF-18) — Rechazo de división personalizada inválida

Dado un gasto de ARS 150.000,00, cuando un miembro intenta confirmarlo con una parte negativa o con partes cuya suma difiere de ARS 150.000,00, entonces no debe guardarse el gasto y el sistema debe identificar la distribución inválida.

### AC-19 (RF-19) — Consulta de partes asignadas

Dado un gasto de ARS 150.000,00 con ARS 40.000,00 asignados al pagador y ARS 110.000,00 a Ana, cuando un miembro consulta su distribución, entonces debe ver ARS 40.000,00 para el pagador y ARS 110.000,00 para Ana.

### AC-20 (RF-20) — Deuda con el pagador

Dado un gasto pagado por un miembro con ARS 40.000,00 asignados al pagador y ARS 110.000,00 a Ana, cuando se consulta la deuda del gasto, entonces el sistema debe mostrar que Ana debe devolver ARS 110.000,00 al pagador.

### AC-21 (RF-21) — Listado de gastos

Dado un gasto registrado con nombre Supermercado, monto ARS 30.000,00 y categoría Alimentos, cuando un miembro accede al listado de gastos del tablero, entonces debe mostrarse exactamente un gasto con esos valores.

### AC-22 (RF-22) — Detalle de gasto

Dado un gasto registrado con fecha, pagador, tipo y distribución, cuando un miembro abre su detalle, entonces debe ver esos cuatro datos con los valores almacenados.

### AC-23 (RF-23) — Edición de gasto

Dado un tablero con disponible base de ARS 500.000,00, ninguna compra de USD y un único gasto de ARS 30.000,00 en enero de 2026, cuando un miembro cambia el monto del gasto a ARS 35.000,00, entonces debe existir un único gasto por ARS 35.000,00 y el dinero restante de enero debe ser ARS 465.000,00.

### AC-24 (RF-24) — Eliminación de gasto

Dado un tablero con disponible base de ARS 500.000,00, ninguna compra de USD y un único gasto de ARS 30.000,00 en enero de 2026, cuando un miembro solicita eliminar el gasto y confirma la operación, entonces el gasto no debe aparecer en el listado y el dinero restante de enero debe ser ARS 500.000,00.

### AC-25 (RF-25) — Inicio de captura de audio

Dado que la captura de audio está inactiva, cuando un miembro inicia el registro mediante audio, entonces debe mostrarse un indicador de captura activa.

### AC-26 (RF-26) — Extracción de datos

Dado un audio del conjunto fijo cuyo resultado esperado contiene nombre Supermercado, monto ARS 30.000,00, categoría Alimentos, tipo compartido en partes iguales, pagador Carla y participantes Carla y Ana, cuando el sistema procesa el audio, entonces todos los valores interpretados deben coincidir con ese resultado esperado.

### AC-27 (RF-27) — Generación de propuesta

Dado un audio del que se interpretaron nombre Supermercado, monto ARS 30.000,00, categoría Alimentos, tipo compartido en partes iguales, pagador Carla y participantes Carla y Ana, cuando finaliza su procesamiento, entonces debe existir una propuesta no registrada con esos valores.

### AC-28 (RF-28) — Propuesta incompleta

Dado un audio del que solo se extrajeron el nombre Supermercado y el monto ARS 30.000,00, cuando finaliza su procesamiento, entonces debe mostrarse una propuesta editable con la categoría identificada como faltante y no debe existir un nuevo gasto.

### AC-29 (RF-29) — Revisión de propuesta

Dada una propuesta con nombre Supermercado, monto ARS 30.000,00, categoría Alimentos, tipo compartido en partes iguales, pagador Carla y participantes Carla y Ana, cuando un miembro accede a la revisión, entonces debe ver todos esos valores antes de confirmar el registro.

### AC-30 (RF-30) — Modificación de propuesta

Dada una propuesta con monto ARS 30.000,00, cuando un miembro cambia el monto a ARS 35.000,00, entonces la propuesta debe mostrar ARS 35.000,00 y no debe existir todavía un nuevo gasto.

### AC-31 (RF-31) — Confirmación de propuesta

Dada una propuesta revisada con todos los datos obligatorios válidos, cuando un miembro confirma el registro, entonces debe existir exactamente un nuevo gasto con los valores de la propuesta.

### AC-32 (RF-32) — Gráfico por categoría

Dado que en enero de 2026 existen gastos por ARS 40.000,00 en Alimentos y ARS 60.000,00 en Transporte, cuando un miembro consulta el gráfico de enero, entonces el gráfico debe mostrar ambas categorías con esos importes y un total de ARS 100.000,00.

### AC-33 (RF-33) — Configuración del disponible mensual

Dado un tablero sin disponible base para enero de 2026, cuando un miembro define ARS 500.000,00 para ese mes, entonces enero de 2026 debe tener un disponible base de ARS 500.000,00.

### AC-34 (RF-34) — Modificación del disponible mensual

Dado un disponible base de ARS 500.000,00, gastos por ARS 40.000,00 y compras de USD por ARS 150.000,00 en enero de 2026, cuando un miembro cambia el disponible base del mes a ARS 600.000,00, entonces el dinero restante de enero debe ser ARS 410.000,00.

### AC-35 (RF-35) — Dinero consumido mensual

Dado que en enero de 2026 el tablero tiene gastos totales por ARS 150.000,00 distribuidos entre varias personas y compras de USD por ARS 40.000,00, cuando un miembro consulta el dinero consumido de enero, entonces debe ver ARS 190.000,00, independientemente de la distribución de los gastos.

### AC-36 (RF-36) — Dinero restante negativo

Dado un disponible base de ARS 100.000,00 y gastos por ARS 120.000,00 en enero de 2026, cuando un miembro consulta el dinero restante de enero, entonces debe ver ARS -20.000,00.

### AC-37 (RF-37) — Ahorro inicial

Dado un tablero sin ahorro inicial, cuando un miembro registra USD 1.000,00, entonces el tablero debe mostrar USD 1.000,00 como ahorro inicial.

### AC-38 (RF-38) — Edición del ahorro inicial

Dado un ahorro inicial de USD 1.000,00, cuando un miembro lo modifica a USD 1.200,00, entonces debe existir un único registro de ahorro inicial por USD 1.200,00.

### AC-39 (RF-39) — Eliminación del ahorro inicial

Dado un ahorro inicial de USD 1.000,00 y ninguna compra de USD, cuando un miembro elimina el ahorro inicial, entonces el total de ahorros debe ser USD 0,00.

### AC-40 (RF-40) — Compra de USD

Dado un tablero con USD 1.000,00 ahorrados, cuando un miembro registra una compra de USD 100,00 por ARS 150.000,00 con fecha 15/01/2026, entonces debe existir exactamente una compra con esos valores y esa fecha.

### AC-41 (RF-41) — Fecha predeterminada de compra

Dado que en Argentina es 15/01/2026, cuando un miembro registra una compra de USD sin indicar fecha, entonces la compra debe quedar registrada con fecha 15/01/2026.

### AC-42 (RF-42) — Edición de compra

Dada una única compra de USD 100,00 por ARS 150.000,00 en enero de 2026, cuando un miembro la modifica a USD 120,00 por ARS 180.000,00, entonces debe existir una única compra con los nuevos importes y el dinero consumido de enero debe aumentar en ARS 30.000,00.

### AC-43 (RF-43) — Eliminación de compra

Dado un disponible base de ARS 500.000,00 y una única compra de USD 100,00 por ARS 150.000,00 en enero de 2026, cuando un miembro elimina la compra, entonces no debe aparecer en las compras de enero y el dinero restante del mes debe ser ARS 500.000,00.

### AC-44 (RF-44) — Impacto mensual de compra

Dado un disponible base de ARS 500.000,00 y ninguna otra operación en enero de 2026, cuando un miembro registra una compra de USD por ARS 150.000,00 con fecha de enero, entonces el dinero consumido de enero debe ser ARS 150.000,00 y el restante debe ser ARS 350.000,00.

### AC-45 (RF-45) — Total de ahorros

Dado un ahorro inicial de USD 1.000,00 y compras vigentes por USD 100,00, cuando un miembro consulta el total de ahorros, entonces debe ver USD 1.100,00.

### AC-46 (RF-46) — Compras mensuales de USD

Dada una compra de USD 100,00 con fecha de enero de 2026 y otra de USD 50,00 con fecha de febrero de 2026, cuando un miembro consulta enero de 2026, entonces debe mostrarse únicamente la compra de USD 100,00 y un total mensual de USD 100,00.

### AC-47 (RF-21) — Lectura de gastos por un no miembro

Dado un usuario autenticado que no pertenece al tablero Hogar, cuando intenta consultar su listado de gastos, entonces el sistema debe rechazar la solicitud y no debe devolver ningún gasto del tablero.

### AC-48 (RF-35, RF-36) — Lectura del disponible por un no miembro

Dado un usuario autenticado que no pertenece al tablero Hogar, cuando intenta consultar su resumen mensual, entonces el sistema debe rechazar la solicitud y no debe devolver el dinero consumido ni el dinero restante del tablero.

### AC-49 (RF-45, RF-46) — Lectura de ahorros por un no miembro

Dado un usuario autenticado que no pertenece al tablero Hogar, cuando intenta consultar sus ahorros, entonces el sistema debe rechazar la solicitud y no debe devolver el total ni las compras de USD del tablero.

### AC-50 (RF-34) — Modificación del disponible por un no miembro

Dado un usuario autenticado que no pertenece al tablero Hogar y un disponible base de ARS 500.000,00, cuando intenta cambiarlo a ARS 600.000,00, entonces el sistema debe rechazar la solicitud y el disponible base debe continuar en ARS 500.000,00.

### AC-51 (RF-23) — Modificación de gasto por un no miembro

Dado un usuario autenticado que no pertenece al tablero Hogar y un gasto de ARS 30.000,00, cuando intenta cambiarlo a ARS 35.000,00, entonces el sistema debe rechazar la solicitud y el gasto debe continuar en ARS 30.000,00.

### AC-52 (RF-10) — Modificación de participante por un no miembro

Dado un usuario autenticado que no pertenece al tablero Hogar y un participante llamado Ana, cuando intenta cambiar su nombre a Ana Pérez, entonces el sistema debe rechazar la solicitud y el participante debe continuar llamándose Ana.

### AC-53 (RF-24) — Eliminación de gasto por un no miembro

Dado un usuario autenticado que no pertenece al tablero Hogar y un gasto de ARS 30.000,00, cuando intenta eliminarlo, entonces el sistema debe rechazar la solicitud y el gasto debe continuar en el tablero.

### AC-54 (RF-11) — Eliminación de participante por un no miembro

Dado un usuario autenticado que no pertenece al tablero Hogar y un participante llamado Ana, cuando intenta eliminarlo, entonces el sistema debe rechazar la solicitud y el participante debe continuar disponible en el tablero.

### AC-55 (RNF-01) — Persistencia después de reinicio

Dado un conjunto confirmado con una cuenta, un tablero, un participante, un gasto, un disponible mensual y un registro de ahorro, cuando se reinicia el backend y se vuelve a consultar cada dato, entonces el 100% debe conservar los valores previos al reinicio.

### AC-56 (RNF-02) — Acceso a la carga

Dado un miembro en la pantalla principal del tablero, cuando realiza una interacción sobre la acción de nuevo gasto, entonces debe abrirse el formulario de carga.

### AC-57 (RNF-03) — Matriz responsive

Dadas todas las pantallas usadas por estos criterios, cuando se ejecutan en cada navegador y viewport de la matriz definida en RNF-03, entonces el 100% debe operar sin desplazamiento horizontal, contenido cortado ni controles inaccesibles.

### AC-58 (RNF-04) — Evaluación del audio

Dado el conjunto fijo de 20 audios definido antes de la prueba conforme a RNF-04, cuando el sistema procesa los 20 casos, entonces al menos 12 deben coincidir en todos los datos relevantes y valores esperados definidos para cada caso.

### AC-59 (RNF-05) — Ausencia de credenciales en texto plano

Dadas cuentas registradas y sesiones iniciadas durante la prueba, cuando se inspeccionan las credenciales de autenticación almacenadas o expuestas por el sistema, entonces deben encontrarse 0 credenciales de autenticación en texto plano.

### AC-60 (RNF-06) — Rendimiento del inicio de sesión

Dado el entorno, calentamiento, concurrencia y volumen definidos en RNF-06, cuando se ejecutan los 100 inicios de sesión válidos, entonces al menos 95 deben entregar la respuesta HTTP completa en un máximo de 4 segundos.

## Fuera de Alcance

Para este MVP quedan explícitamente fuera:

- Integración automática con bancos, tarjetas de crédito, billeteras virtuales o Mercado Pago.
- Gestión o recomendación de inversiones.
- Aplicaciones móviles nativas para iOS y Android.
- Obtención automática de cotizaciones del dólar en tiempo real.
- Conversión automática del patrimonio ahorrado en USD a su valor actualizado en ARS.
- Funcionalidades contables o impositivas avanzadas.
- Recomendaciones avanzadas mediante IA sobre cómo reducir gastos o mejorar hábitos financieros.
- Roles o niveles de permisos diferentes entre miembros de un tablero.
- Liquidación, compensación, cobro o registro de pagos de las deudas calculadas entre personas.
- Gestión avanzada de categorías.

La funcionalidad de IA del MVP se concentra en facilitar el registro de gastos mediante audio.

## Riesgos y Dependencias

### R-01 — Interpretación mediante audio

La interpretación incorrecta de los datos relevantes presentes en el audio puede generar propuestas incorrectas. Se mitiga mostrando siempre la propuesta para revisión y permitiendo editarla antes de exigir una confirmación para registrar el gasto.

### R-02 — Integridad de los datos

La pérdida o modificación incorrecta de gastos, disponible o ahorros puede afectar los totales históricos. Se mitiga verificando la persistencia después de reinicios y recalculando los valores derivados después de cada edición o eliminación.

### R-03 — Cálculos compartidos

Los errores en la distribución pueden producir partes o deudas incorrectas. Se mitiga exigiendo que las partes sumen el monto total, rechazando importes negativos y aplicando una distribución determinista de residuos.

### R-04 — Acceso entre tableros

Un error de autorización podría exponer o modificar datos de otro tablero. Se mitiga validando la pertenencia al tablero en cada operación y verificando por separado lectura, modificación y eliminación por parte de un no miembro.

### D-01 — Procesamiento de audio

La carga mediante voz depende de un mecanismo capaz de procesar entradas de audio y devolver datos estructurados.

### D-02 — Persistencia

La aplicación depende de un mecanismo de almacenamiento persistente para conservar cuentas, tableros, miembros, participantes, gastos, disponible y ahorros.

### D-03 — Autenticación

Las cuentas y sesiones dependen de un mecanismo de autenticación basado en JWT.

### D-04 — Recuperación por email

La recuperación de acceso depende de un mecanismo capaz de enviar emails al usuario.
