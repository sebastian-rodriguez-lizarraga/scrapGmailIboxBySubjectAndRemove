import imaplib
import email
from email.header import decode_header



#PARA CORRERLO DEBES INGRESAR LOS SIGUIENTES DATOS PARA QUE EL SCRAPPER PUEDA ACCEDER A TUS CORREOS 
EMAIL = "ingresaTuMail@gmail.com"
PASSWORD = "contraseña de aplicación" #sino sabes que es esto LEE LO DE ABAJO QUE TE EXPLICO
#No es la misma que la que usas para el mail, es una especial. Para sacarla tenes que habilitar 2FA en el gmail y crearla
#Te dejo los links para esto acá: 
#2fa: https://support.google.com/accounts/answer/185839?hl=es-419&co=GENIE.Platform%3DDesktop
#Crear la contraseña de aplicación https://support.google.com/accounts/answer/185833?hl=es-419 (si te trabas con esto escribime si queres)


SERVIDOR_IMAP = "imap.gmail.com" #si usas gmail esto no se toca

PALABRA_CLAVE_ASUNTO = "asunto"  # poné la palabra clave del asunto de los correos que quieras mover a la papelera (no es case sensitive (no importa si es mayusc/minusc))
#pone de a cuantos mails queres revisar, este número es un limite para que no tarde infinito en terminar (yo tenía 40k emails en bandeja)
CANTIDAD_A_REVISAR = 700



def conectar_mail():
    mail = imaplib.IMAP4_SSL(SERVIDOR_IMAP)
    mail.login(EMAIL, PASSWORD)
    return mail

def decodificar_asunto(subject_header):
    if subject_header is None:
        return "(Sin asunto)"

    asunto_final = ""
    for parte, cod in decode_header(subject_header):
        if isinstance(parte, bytes):
            if not cod or cod.lower() in ("unknown-8bit", "x-unknown", "8bit"):
                cod = chardet.detect(parte)["encoding"] or "utf-8"
            try:
                codecs.lookup(cod)  # valida cod
                parte = parte.decode(cod, errors="replace")
            except Exception:
                parte = parte.decode("utf-8", errors="replace")
        asunto_final += parte
    return asunto_final


def eliminar_por_asunto():
    mail = conectar_mail()
    mail.select("inbox")

    status, mensajes = mail.search(None, "ALL")
    ids = mensajes[0].split()
    ids_a_revisar = ids[-CANTIDAD_A_REVISAR:]  # Últimos N correos
    eliminados = 0

    for mail_id in reversed(ids_a_revisar):
        status, data = mail.fetch(mail_id, "(RFC822)")
        if status != "OK":
            continue

        try:
            msg = email.message_from_bytes(data[0][1])
        except Exception as e:
            print(f"Error al leer el correo: {e}")
            continue
        
        # Decodificar el asunto
        asunto = decodificar_asunto(msg["Subject"])
        # Comprobamos si contiene la palabra clave en el asunto
        if PALABRA_CLAVE_ASUNTO.lower() in asunto.lower():
            print(f"Moviendo a la papelera: {asunto}")
            # 1. Copiar a la papelera
            result = mail.copy(mail_id, "[Gmail]/Papelera")
            if result[0] == 'OK':
                # 2. Marcar como eliminado
                mail.store(mail_id, "+FLAGS", "\\Deleted")
                eliminados += 1
            else:
                print(f"❌ Error al mover a la papelera: {result}")

    mail.expunge()  # Elimina permanentemente
    mail.logout()
    print(f"\n✅ Total movidos a la papelera: {eliminados}")

if __name__ == "__main__":
    eliminar_por_asunto()
