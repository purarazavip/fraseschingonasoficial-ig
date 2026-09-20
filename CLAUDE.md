# fraseschingonasoficial-ig

Repo que genera el contenido diario para @fraseschingonasoficial (Instagram): 4 posts de frases
(imagen 1080x1920, fondo negro, fuente Caveat embebida) + un carrusel de "facto" (2 imágenes
1080x1080, fondo blanco/rojo) con su propio caption. Todo lo genera `generar_lote.py`.

## Reglas para la corrida diaria automática (Routine "Frases Chingonas - posts diarios IG")

- **El facto NO es opcional.** `generar_lote.py N` genera automáticamente, además de las N frases,
  el carrusel de facto (`facto_1.png`, `facto_2.png`, `facto_caption.txt`) y actualiza
  `usadas_factos.json`. Al mandar el contenido del día al usuario con `SendUserFile`, incluye
  **siempre** esos 3 archivos junto con las imágenes/captions de frases — no hay que esperar a que
  el usuario lo pida ni preguntar si los quiere.
- Antes de generar, revisa disponibilidad en **ambos** bancos: `frases_banco.json` vs `usadas.json`
  (por categoría) y `factos_banco.json` vs `usadas_factos.json`. Si a cualquiera de los dos le
  quedan menos de 3 elementos sin usar en alguna categoría (o en el banco de factos), redacta 6-8
  originales nuevos en el mismo tono y agrégalos antes de correr el script.
- Chrome headless: revisa primero `/opt/pw-browsers/chromium-*/chrome-linux/chrome` (suele estar
  preinstalado en el entorno) antes de intentar instalar nada.
- `posts/` está en `.gitignore` a propósito — nunca lo subas a git.
- **Antes de hacer `git push`**, revisa si `HEAD` está detached o si la rama local quedó adelantada
  a `origin/main` por corridas anteriores cuyo push falló silenciosamente (esto ya pasó: se
  acumularon ~5 días de commits sin subir). Si es así, primero actualiza `main` a esos commits
  (fast-forward) y súbelos junto con el commit de hoy, no dejes que seguido se acumulen.
- Si el push final falla por permisos, no es un fallo fatal de la tarea, pero repórtalo igual.
