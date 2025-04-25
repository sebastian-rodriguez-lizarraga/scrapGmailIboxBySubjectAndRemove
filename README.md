# 🧹 Gmail Cleaner por Asunto

Este script en Python te permite **mover a la papelera automáticamente los correos cuyo asunto contenga una palabra clave específica**, de forma rápida y simple. Ideal si querés limpiar tu inbox de promociones, newsletters o spam acumulado.

---

## 🚀 ¿Cómo funciona?

El script:

1. Se conecta a tu cuenta de Gmail usando IMAP.
2. Revisa los últimos `N` correos (vos elegís cuántos).
3. Si encuentra la palabra clave en el asunto de un correo, lo **mueve a la papelera** y lo marca como eliminado.
4. Al final, **los elimina permanentemente** de tu bandeja de entrada.

---

## ⚙️ Configuración y Requisitos

Antes de correr el script, asegurate de hacer lo siguiente:

### 1. Activar la verificación en dos pasos (2FA) en tu cuenta de Gmail

🔐 [Cómo activar la 2FA (guía oficial de Google)](https://support.google.com/accounts/answer/185839?hl=es-419&co=GENIE.Platform%3DDesktop)

### 2. Crear una Contraseña de Aplicación

🔑 [Cómo crear una contraseña de aplicación](https://support.google.com/accounts/answer/185833?hl=es-419)

> **⚠️ No uses tu contraseña habitual de Gmail.**  
> Este script necesita una contraseña especial que se genera una vez que activás el 2FA.

---

### 3. Editá las siguientes variables del script:

```python
EMAIL = "tuCorreo@gmail.com"
PASSWORD = "tuContraseñaDeAplicación"  # no es la de tu Gmail común
PALABRA_CLAVE_ASUNTO = "asunto"  # palabra clave del asunto (no distingue mayúsculas)
CANTIDAD_A_REVISAR = 700  # cantidad de mails recientes a revisar
