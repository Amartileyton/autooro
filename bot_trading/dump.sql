BEGIN TRANSACTION;
CREATE TABLE news_interactions (
	id INTEGER NOT NULL, 
	news_id VARCHAR(128) NOT NULL, 
	news_title VARCHAR(300) NOT NULL, 
	news_url VARCHAR(500), 
	news_asset VARCHAR(60), 
	action_type VARCHAR(30) NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE raw_telegram_messages (
	id INTEGER NOT NULL, 
	message_id INTEGER, 
	channel_id INTEGER, 
	channel_name VARCHAR(120), 
	raw_text TEXT NOT NULL, 
	parsed_success BOOLEAN NOT NULL, 
	parser_used VARCHAR(30) NOT NULL, 
	error_reason VARCHAR(255), 
	received_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "raw_telegram_messages" VALUES(1,7909,-1002763662248,'Chartoro FX Señales Gratis','**DIRECTO A LAS GANANCIAS **⚡️

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Sesión recién iniciada y el movimiento llegó rápido.__',0,'NONE',NULL,'2026-08-21 03:42:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(2,7908,-1002763662248,'Chartoro FX Señales Gratis','**EL PRECIO EMPIEZA A IMPULSAR ****👀**',0,'NONE',NULL,'2026-08-21 03:40:50.000000');
INSERT INTO "raw_telegram_messages" VALUES(3,7907,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4532
**⛔️ Stop Loss (SL): **4540

**🏆 TP1: **4529
**🏆 TP2:** 4524
**🏆 TP3:** 4516

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-21 03:30:48.000000');
INSERT INTO "raw_telegram_messages" VALUES(4,7906,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4532
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-21 03:28:55.000000');
INSERT INTO "raw_telegram_messages" VALUES(5,7904,-1002763662248,'Chartoro FX Señales Gratis','Profit profe muchas gracias',0,'NONE',NULL,'2026-08-21 03:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(6,7903,-1002763662248,'Chartoro FX Señales Gratis','__No solo recibes señales y transparencia...__

**TAMBIÉN OBTIENES MI MENTORÍA Y MATERIAL EDUCATIVO QUE TE AYUDARÁN AL 100% A CONVERTIRTE EN UN MEJOR TRADER, SIN IMPORTAR QUÉ!** 📈📈📈**
**
[**HAZ CLIC AQUÍ PARA SABER MÁS**](https://t.me/m/q3-XLmhBNmY0) ⚡️',0,'NONE',NULL,'2026-08-21 02:54:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(7,7902,-1002763662248,'Chartoro FX Señales Gratis','❌ **SL HIT**

No todos los setups saldrán a nuestro favor, y desafortunadamente este terminó en pérdida.

Mantenemos la **transparencia con cada resultado**, tanto en las ganancias como en las pérdidas. Una correcta gestión del riesgo nos mantiene protegidos y preparados para la próxima oportunidad. 💪🏻

**__Aprendemos, reiniciamos y seguimos avanzando.__**',0,'NONE',NULL,'2026-08-21 02:46:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(8,7901,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4527
**⛔️ Stop Loss (SL): **4535

**🏆 TP1: **4524
**🏆 TP2:** 4519
**🏆 TP3:** 4511

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-21 02:36:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(9,7900,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4527
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-21 02:34:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(10,7899,-1002763662248,'Chartoro FX Señales Gratis','__Algunos entrarán con guía.
Otros entrarán adivinando.__

**El VIP está abierto para quienes ya no quieren adivinar.**

💎 [**HAZ CLIC AQUÍ PARA ACCESO GRATIS AL VIP**](https://t.me/m/q3-XLmhBNmY0) 💎',0,'NONE',NULL,'2026-08-21 02:24:16.000000');
INSERT INTO "raw_telegram_messages" VALUES(11,7898,-1002763662248,'Chartoro FX Señales Gratis','**Por qué conformarte con una señal al día cuando puedes recibir 4-8 SEÑALES DIARIAS EN EL VIP** ⁉️⁉️⁉️',0,'NONE',NULL,'2026-08-21 00:01:38.000000');
INSERT INTO "raw_telegram_messages" VALUES(12,7896,-1002763662248,'Chartoro FX Señales Gratis','**Para quién es el VIP?**

Para cualquiera listo para:
✅ Copiar señales reales
✅Aprender mientras gana
✅Operar con confianza',0,'NONE',NULL,'2026-08-20 18:22:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(13,7895,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA OPERAR CONMIGO**](https://t.me/m/q3-XLmhBNmY0) 📈📈📈',0,'NONE',NULL,'2026-08-20 16:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(14,7894,-1002763662248,'Chartoro FX Señales Gratis','🏆 **EL VIP INCLUYE:**

✔️ De 4 a 8 señales diarias de trading de alta calidad
✔️ Curso completo de trading
✔️ Guía completa A-a-Z para construir bases sólidas
✔️ Rendimiento comprobado de las señales basado en resultados reales
✔️ Soporte y mentoría 24/7
 
🚀 [**RECLAMA TU ACCESO AL VIP AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 🚀',0,'NONE',NULL,'2026-08-20 14:19:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(15,7893,-1002763662248,'Chartoro FX Señales Gratis','**TODO A FONDO… SIN VUELTA ATRÁS 🚀

****#XAUUSD**** TP3 HIT, +200 Pips 🏆**

__Desde una entrada temprana hasta una dominación total.__',0,'NONE',NULL,'2026-08-20 13:03:52.000000');
INSERT INTO "raw_telegram_messages" VALUES(16,7892,-1002763662248,'Chartoro FX Señales Gratis','**Y AHORA ESTÁ EN MODO PERSECUCIÓN TOTAL 🏃‍♂️

****#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El impulso se está saliendo de control.__',0,'NONE',NULL,'2026-08-20 12:53:12.000000');
INSERT INTO "raw_telegram_messages" VALUES(17,7891,-1002763662248,'Chartoro FX Señales Gratis','**Y EXPLOTÓ… RÁPIDO 💥**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Parpadeas y ya desapareció.__',0,'NONE',NULL,'2026-08-20 12:45:44.000000');
INSERT INTO "raw_telegram_messages" VALUES(18,7890,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4463.20

🏆**TP1**: 4466.20
🏆**TP2**: 4473.20
🏆**TP3**: 4483.20

**⛔️ Stop Loss (SL)**: 4453.20

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-20 12:41:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(19,7889,-1002763662248,'Chartoro FX Señales Gratis','❓__Te gustaría tener acceso a estrategias de trading exclusivas?__',0,'NONE',NULL,'2026-08-20 12:02:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(20,7888,-1002763662248,'Chartoro FX Señales Gratis','**BUENOS DIAS CHARTORO TRADERS** 👑',0,'NONE',NULL,'2026-08-20 10:17:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(21,7887,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA UNIRTE AL MÁS REAL DE LOS GRUPOS VIP**](https://t.me/m/q3-XLmhBNmY0)  💎',0,'NONE',NULL,'2026-08-20 06:34:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(22,7886,-1002763662248,'Chartoro FX Señales Gratis','**Dónde has visto este nivel de transparencia en un grupo de señales?**

__Si encuentras un grupo que afirma tener un 100% de aciertos, mejor sal corriendo... __ 🏃',0,'NONE',NULL,'2026-08-20 06:34:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(23,7885,-1002763662248,'Chartoro FX Señales Gratis','**❌ SL HIT**

Darle más espacio a la operación no ayudó esta vez.

No pasa nada — seguiré buscando una nueva configuración clara 🔎

Manténganse pacientes, equipo. Operamos con inteligencia, no con prisas. ✅',0,'NONE',NULL,'2026-08-20 04:35:40.000000');
INSERT INTO "raw_telegram_messages" VALUES(24,7884,-1002763662248,'Chartoro FX Señales Gratis','Move SL to 4488',1,'REGEX',NULL,'2026-08-20 04:29:30.000000');
INSERT INTO "raw_telegram_messages" VALUES(25,7883,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point:** 4498
**⛔️ Stop Loss (SL): **4490

**🏆 TP1: **4501
**🏆 TP2:** 4506
**🏆 TP3:** 4514

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-20 04:03:35.000000');
INSERT INTO "raw_telegram_messages" VALUES(26,7882,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4498
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-20 04:01:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(27,7880,-1002763662248,'Chartoro FX Señales Gratis','**GANANCIAS TEMPRANAS ASEGURADAS ****🔥****

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Reacción rápida, toma limpia ____💰__',0,'NONE',NULL,'2026-08-20 03:14:25.000000');
INSERT INTO "raw_telegram_messages" VALUES(28,7879,-1002763662248,'Chartoro FX Señales Gratis','**TP1 CARGANDO… VAMOS! ****🚀**',0,'NONE',NULL,'2026-08-20 03:12:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(29,7878,-1002763662248,'Chartoro FX Señales Gratis','Move SL to 4501',1,'REGEX',NULL,'2026-08-20 03:05:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(30,7877,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4491
**⛔️ Stop Loss (SL): **4499

**🏆 TP1: **4488
**🏆 TP2:** 4483
**🏆 TP3:** 4475

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-20 02:47:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(31,7876,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4491
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-20 02:47:19.000000');
INSERT INTO "raw_telegram_messages" VALUES(32,7875,-1002763662248,'Chartoro FX Señales Gratis','🔠 **SEÑALES VIP GRATIS**

**🔠** **MATERIAL EDUCATIVO GRATIS**

**🔠** **MENTORÍA GRATIS**

[**RECLAMA AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-20 02:14:20.000000');
INSERT INTO "raw_telegram_messages" VALUES(33,7874,-1002763662248,'Chartoro FX Señales Gratis','**Copiar las señales dentro del VIP y empezar a ganar de inmediato** 💵💵💵

👑 [**HAZ CLIC AQUÍ PARA UNIRTE AHORA**](https://t.me/m/q3-XLmhBNmY0) 👑',0,'NONE',NULL,'2026-08-19 22:38:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(34,7873,-1002763662248,'Chartoro FX Señales Gratis','Muchas gracias ❤️',0,'NONE',NULL,'2026-08-19 21:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(35,7872,-1002763662248,'Chartoro FX Señales Gratis','1️⃣ Copiar

2️⃣ Pegar

3️⃣ **GANAR DINERO** 💵💵💵

**DE VERDAD VAS A RECHAZAR ESO??? ****🤯****🤯**',0,'NONE',NULL,'2026-08-19 19:04:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(36,7871,-1002763662248,'Chartoro FX Señales Gratis','❓ **Ya tienes un mentor de trading?**',0,'NONE',NULL,'2026-08-19 17:10:30.000000');
INSERT INTO "raw_telegram_messages" VALUES(37,6982,-1002763662248,'Chartoro FX Señales Gratis','**VAMOS TRADERSSSS **💰',0,'NONE',NULL,'2026-07-23 02:12:19.000000');
INSERT INTO "raw_telegram_messages" VALUES(38,6983,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4125
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-07-23 02:53:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(39,6984,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4125
**⛔️ Stop Loss (SL): **4117

**🏆 TP1: **4128
**🏆 TP2:** 4133
**🏆 TP3:** 4141

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-23 02:55:42.000000');
INSERT INTO "raw_telegram_messages" VALUES(40,6985,-1002763662248,'Chartoro FX Señales Gratis','**🔥 LOS BENEFICIOS HAN LLEGADO OTRA VEZ!**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Estructura clara, ejecución limpia, resultados reales 💰__',0,'NONE',NULL,'2026-07-23 02:57:14.000000');
INSERT INTO "raw_telegram_messages" VALUES(41,6986,-1002763662248,'Chartoro FX Señales Gratis','👀👀👀',0,'NONE',NULL,'2026-07-23 03:07:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(42,6987,-1002763662248,'Chartoro FX Señales Gratis','**TP2 está a solo un paso ****🔥**',0,'NONE',NULL,'2026-07-23 03:23:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(43,6988,-1002763662248,'Chartoro FX Señales Gratis','**SIGUE AVANZANDO **🔥

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__El movimiento fue limpio y conforme al plan.__',0,'NONE',NULL,'2026-07-23 03:24:54.000000');
INSERT INTO "raw_telegram_messages" VALUES(44,6989,-1002763662248,'Chartoro FX Señales Gratis','**QUIERES CONSEGUIR MÚLTIPLES VICTORIAS COMO ESTAS? **💎💎',0,'NONE',NULL,'2026-07-23 03:48:52.000000');
INSERT INTO "raw_telegram_messages" VALUES(45,6990,-1002763662248,'Chartoro FX Señales Gratis','**IMAGINA ATRAPAR ESTO TODOS LOS DÍAS **👀',0,'NONE',NULL,'2026-07-23 03:50:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(46,6991,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA OBTENER MÁS**](https://t.me/m/q3-XLmhBNmY0) 💵💵💵',0,'NONE',NULL,'2026-07-23 03:50:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(47,6992,-1002763662248,'Chartoro FX Señales Gratis','**Para quién es el VIP?**

Para cualquiera listo para:
✅ Copiar señales reales
✅Aprender mientras gana
✅Operar con confianza',0,'NONE',NULL,'2026-07-23 06:19:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(48,6994,-1002763662248,'Chartoro FX Señales Gratis','🚀 **ESTÁS LISTO PARA GANAR HOY?**',0,'NONE',NULL,'2026-07-23 10:24:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(49,6995,-1002763662248,'Chartoro FX Señales Gratis','De a poquito se llena el saquito, gracias.',0,'NONE',NULL,'2026-07-23 11:01:38.000000');
INSERT INTO "raw_telegram_messages" VALUES(50,6996,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4085.50

🏆**TP1**: 4088.50
🏆**TP2**: 4095.50
🏆**TP3**: 4105.50

**⛔️ Stop Loss (SL)**: 4075.50

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Same as the original idea',1,'REGEX',NULL,'2026-07-23 11:59:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(51,6997,-1002763662248,'Chartoro FX Señales Gratis','Desafortunadamente, esta operación alcanzó el Stop Loss después de que el precio no lograra mantenerse por encima de nuestra zona de entrada.

La vela martillo inicialmente mostró una posible reacción alcista, pero los compradores no tuvieron el impulso suficiente para confirmar el movimiento. En su lugar, el mercado continuó cayendo, lo que podría haber sido otra búsqueda de liquidez para barrer los Stop Loss antes de mostrar la dirección real. Este tipo de movimientos son comunes en mercados con alta volatilidad.

Nuestra idea principal aún no queda completamente invalidada. Si el precio recupera nuevamente la zona de entrada con confirmaciones más sólidas y una mejor estructura de mercado, no dudaremos en volver a tomar la operación.

Por ahora, la paciencia sigue siendo nuestra mejor herramienta. Esperaremos las confirmaciones adecuadas antes de enviar una nueva señal. Proteger el capital y priorizar operaciones de alta probabilidad siempre será más importante que forzar entradas. 💪📈',0,'NONE',NULL,'2026-07-23 12:19:51.000000');
INSERT INTO "raw_telegram_messages" VALUES(52,6998,-1002763662248,'Chartoro FX Señales Gratis','**TRANSPARENCIA ANTE TODO** 💯',0,'NONE',NULL,'2026-07-23 13:43:40.000000');
INSERT INTO "raw_telegram_messages" VALUES(53,7000,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4053.75

🏆**TP1**: 4056.75
🏆**TP2**: 4063.75
🏆**TP3**: 4073.75

**⛔️ Stop Loss (SL)**: 4043.75

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-23 14:29:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(54,7001,-1002763662248,'Chartoro FX Señales Gratis','**EL MERCADO INMEDIATAMENTE ABRIÓ EL CAMINO! ****🔥****

****#XAUUSD**** TP1 HIT, +30 Pips ****🏆**

__La vela inicial dio una señal fuerte, el momentum se aseguró de inmediato antes de que el mercado se expandiera.__',0,'NONE',NULL,'2026-07-23 14:31:24.000000');
INSERT INTO "raw_telegram_messages" VALUES(55,7002,-1002763662248,'Chartoro FX Señales Gratis','__Como ya saben, el trading cambió mi vida...__

🪙 Me dio el poder de ganar dinero a mi manera
🪙 Me ayudó a salir de la rutina del 9 a 5
🪙 Y me dio verdadera libertad financiera

⏳  [**HAZ CLIC AQUÍ PARA TRANSFORMAR TU VIDA TAMBIÉN**](https://t.me/m/q3-XLmhBNmY0) ⏳',0,'NONE',NULL,'2026-07-23 15:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(56,7003,-1002763662248,'Chartoro FX Señales Gratis','⏩ [**RECLAMA ACCESO VIP GRATIS Y BENEFICIOS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-23 15:23:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(57,7004,-1002763662248,'Chartoro FX Señales Gratis','⭐️ **BENEFICIOS VIP** ⭐️

⏩ 4–8 señales de trading de alta calidad al día
⏩ Un curso completo de trading
⏩ Una guía completa de la A a la Z para que sepas por qué funcionan las operaciones
⏩ Mentoría y acompañamiento real
⏩ Resultados comprobados que puedes seguir paso a paso',0,'NONE',NULL,'2026-07-23 15:45:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(58,7005,-1002763662248,'Chartoro FX Señales Gratis','__Las señales te ponen dentro

                     ____⬇️____

La educación te mantiene constante

                     ____⬇️____

La mentoría te mantiene enfocado__

🎉 **El VIP no es solo una cosa, ES TODO EL SISTEMA** 🎉',0,'NONE',NULL,'2026-07-23 16:22:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(59,7006,-1002763662248,'Chartoro FX Señales Gratis','Ya viste a los miembros sacando ganancias de:

🤑 $200
🤑 $500
🤑 $700 **EN UNA SOLA SEMANA** 🤑🤑🤑

Y todavía lo estás pensando? 🤔',0,'NONE',NULL,'2026-07-23 17:11:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(60,7007,-1002763662248,'Chartoro FX Señales Gratis','Hola Luis, que señal tan excelente',0,'NONE',NULL,'2026-07-23 18:22:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(61,7008,-1002763662248,'Chartoro FX Señales Gratis','🟣__ SEÑALES VIP GRATIS 

🟣 MATERIAL EDUCATIVO GRATIS 

🟣 MENTORÍA GRATIS __


✈️  [**RECLAMA AQUÍ**](https://t.me/m/q3-XLmhBNmY0) ✈️',0,'NONE',NULL,'2026-07-23 19:03:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(62,7009,-1002763662248,'Chartoro FX Señales Gratis','Pero que es eso!!!!! Estoy muy feliz!',0,'NONE',NULL,'2026-07-23 20:44:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(63,7010,-1002763662248,'Chartoro FX Señales Gratis','📣 [**RECLAMA UN LUGAR VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)  📣',0,'NONE',NULL,'2026-07-23 22:19:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(64,7011,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4049
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-07-24 00:45:29.000000');
INSERT INTO "raw_telegram_messages" VALUES(65,7012,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4049
**⛔️ Stop Loss (SL): **4041

**🏆 TP1: **4052
**🏆 TP2:** 4057
**🏆 TP3:** 4065

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-24 00:48:16.000000');
INSERT INTO "raw_telegram_messages" VALUES(66,7013,-1002763662248,'Chartoro FX Señales Gratis','✨ [ **ESTA ES TU SEÑAL PARA GANAR MÁS** ](https://t.me/m/q3-XLmhBNmY0)✨',0,'NONE',NULL,'2026-07-24 02:14:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(67,7014,-1002763662248,'Chartoro FX Señales Gratis','**❌ SL HIT**

Darle más espacio a la operación no ayudó esta vez.

No pasa nada — seguiré buscando una nueva configuración clara 🔎

Manténganse pacientes, equipo. Operamos con inteligencia, no con prisas. ✅',0,'NONE',NULL,'2026-07-24 02:18:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(68,7015,-1002763662248,'Chartoro FX Señales Gratis','Pero que es eso!!!!! Estoy muy feliz!',0,'NONE',NULL,'2026-07-24 02:41:23.000000');
INSERT INTO "raw_telegram_messages" VALUES(69,7016,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4030
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-07-24 02:51:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(70,7017,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4030
**⛔️ Stop Loss (SL): **4038

**🏆 TP1: **4027
**🏆 TP2:** 4022
**🏆 TP3:** 4014

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-24 02:52:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(71,7018,-1002763662248,'Chartoro FX Señales Gratis','**COMIENZO CALIENTE DEL DÍA! 🔥**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Ganancia instantánea, precisión y sincronización perfectas! ____💪__',0,'NONE',NULL,'2026-07-24 02:53:58.000000');
INSERT INTO "raw_telegram_messages" VALUES(72,7019,-1002763662248,'Chartoro FX Señales Gratis','**EL MOMENTO SE FORTALECE! ****⚡️**

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__Ejecución impecable, análisis preciso, las ganancias se acumulan rápido hoy! ____💰__',0,'NONE',NULL,'2026-07-24 05:57:22.000000');
INSERT INTO "raw_telegram_messages" VALUES(73,7020,-1002763662248,'Chartoro FX Señales Gratis','Ya estoy 360 en mi primera semana , casi duplicó mi primer depósito',0,'NONE',NULL,'2026-07-24 07:40:26.000000');
INSERT INTO "raw_telegram_messages" VALUES(74,7021,-1002763662248,'Chartoro FX Señales Gratis','**BUENOS DÍAS TRADERS!** 🌞🌞🌞',0,'NONE',NULL,'2026-07-24 10:26:25.000000');
INSERT INTO "raw_telegram_messages" VALUES(75,7022,-1002763662248,'Chartoro FX Señales Gratis','__Están listos para el último impulso de esta semana?__',0,'NONE',NULL,'2026-07-24 10:26:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(76,7023,-1002763662248,'Chartoro FX Señales Gratis','...__me siento generoso__ 🤩🤩

**BONO DE DOBLE DEPÓSITO EXTENDIDO POR 1 SEMANA MÁS!!!!**',0,'NONE',NULL,'2026-07-24 11:18:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(77,7024,-1002763662248,'Chartoro FX Señales Gratis','⚠️ 🚨 **ESTA ES LA ÚLTIMA LLAMADA!** 🚨⚠️',0,'NONE',NULL,'2026-07-24 11:19:22.000000');
INSERT INTO "raw_telegram_messages" VALUES(78,7025,-1002763662248,'Chartoro FX Señales Gratis','2 días de VIP y ya tenemos duplicada la cuenta 🤩😮‍💨',0,'NONE',NULL,'2026-07-24 12:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(79,7026,-1002763662248,'Chartoro FX Señales Gratis','Me fui tranquilo ☺️ a Dormir',0,'NONE',NULL,'2026-07-24 12:22:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(80,7027,-1002763662248,'Chartoro FX Señales Gratis','Doble un dia de mi trabajo en minutos',0,'NONE',NULL,'2026-07-24 12:22:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(81,7028,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4059.70

🏆**TP1**: 4062.70
🏆**TP2**: 4069.70
🏆**TP3**: 4079.70

**⛔️ Stop Loss (SL)**: 4049.70

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Price breakout the vib line after correction',1,'REGEX',NULL,'2026-07-24 13:58:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(82,7029,-1002763662248,'Chartoro FX Señales Gratis','**COMENZANDO EL DÍA CON MÁXIMA POTENCIA **🔥

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Reacción del precio rápida y precisa.__',0,'NONE',NULL,'2026-07-24 14:00:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(83,7030,-1002763662248,'Chartoro FX Señales Gratis','**LA TENDENCIA CONTINÚA SIN DUDAS **🚀

**#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El precio se movió de forma fluida, siguiendo perfectamente el escenario.__',0,'NONE',NULL,'2026-07-24 14:02:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(84,7031,-1002763662248,'Chartoro FX Señales Gratis','Claro que el viernes vamos a hacer que llueva dinero! 😉

Quieres más operaciones como esta????',0,'NONE',NULL,'2026-07-24 14:27:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(85,7032,-1002763662248,'Chartoro FX Señales Gratis','🚨 [RECLAMA TU ACCESO GRATIS AHORA Y DUPLICARÉ TU DEPÓSITO](http://t.me/SoporteChartoroFX) 🚨',0,'NONE',NULL,'2026-07-24 14:28:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(86,7034,-1002763662248,'Chartoro FX Señales Gratis','**CIERRE FUERTE **👑

**#XAUUSD**** TP3 HIT, +200 Pips 🏆**

__Ejecución disciplinada + condiciones de mercado favorables = resultados máximos.__',0,'NONE',NULL,'2026-07-24 15:19:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(87,7035,-1002763662248,'Chartoro FX Señales Gratis','Gracias Luis, estoy operando contigo ya casi 3 semanas y ya subí más de 300$ mi cuenta',0,'NONE',NULL,'2026-07-24 15:45:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(88,7036,-1002763662248,'Chartoro FX Señales Gratis','🔠🔠🔠   🔠🔠🔠🔠🔠🔠',0,'NONE',NULL,'2026-07-24 16:15:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(89,7037,-1002763662248,'Chartoro FX Señales Gratis','**DENTRO DEL VIP, NO TIENES QUE ELEGIR ENTRE APRENDER O GANAR** 😉

Copias señales reales mientras aprendes por qué funcionan.
**Así es como los traders evolucionan rápido.**

❌ __Sin adivinar
____❌__ __Sin apostar
____❌__ __Sin falsa confianza__

[**HAZ CLIC AQUÍ PARA APRENDER Y GANAR CON EL VIP**](https://t.me/m/q3-XLmhBNmY0) 🚀',0,'NONE',NULL,'2026-07-24 18:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(90,7038,-1002763662248,'Chartoro FX Señales Gratis','**De verdad vas a dejar que termine la semana sin tomar acción? 🤔**',0,'NONE',NULL,'2026-07-24 19:47:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(91,7039,-1002763662248,'Chartoro FX Señales Gratis','**O por fin vas a dar el paso que puede cambiar tu vida? La decisión es tuya** 👉 @SoporteChartoroFX',0,'NONE',NULL,'2026-07-24 19:50:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(92,7041,-1002763662248,'Chartoro FX Señales Gratis','Otro día Victorioso 
Vamoooos ❤️‍🔥',0,'NONE',NULL,'2026-07-24 22:17:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(93,7042,-1002763662248,'Chartoro FX Señales Gratis','⬇️         ⬇️         ⬇️         ⬇️         ⬇️

                   **   **[**VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-25 01:10:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(94,7043,-1002763662248,'Chartoro FX Señales Gratis','💡**TIP DE TRADING** 

Tu mayor arrepentimiento no será una pérdida, serán las ganancias que nunca tomaste.

**TU FUTURO EMPIEZA AQUÍ** 🚀👉 @SoporteChartoroFX',0,'NONE',NULL,'2026-07-25 03:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(95,7044,-1002763662248,'Chartoro FX Señales Gratis','🌞 **BUENOS DÍAS TRADERS!**

Los mercados pueden estar cerrados, pero el crecimiento nunca se toma un día libre.

__Aprovechen este fin de semana para revisar sus operaciones, fortalecer su mentalidad y prepararse para la semana que viene. __

**Los mejores traders se forman cuando los gráficos están apagados**  💪',0,'NONE',NULL,'2026-07-25 10:55:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(96,7045,-1002763662248,'Chartoro FX Señales Gratis','**TE GUSTARÍA VER LO QUE GANARON LOS MIEMBROS VIP ESTE MES? **💵💵💵',0,'NONE',NULL,'2026-07-25 11:48:39.000000');
INSERT INTO "raw_telegram_messages" VALUES(97,7047,-1002763662248,'Chartoro FX Señales Gratis','volvimos asegurar otra entrada, excelente señal, gracias!!!!',0,'NONE',NULL,'2026-07-25 12:03:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(98,7048,-1002763662248,'Chartoro FX Señales Gratis','Empezamos profit',0,'NONE',NULL,'2026-07-25 12:05:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(99,7049,-1002763662248,'Chartoro FX Señales Gratis','Mis resultados de hoy hermano',0,'NONE',NULL,'2026-07-25 12:15:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(100,7050,-1002763662248,'Chartoro FX Señales Gratis','Entre despues porque no vi la señal cuando la mandaste pero aun así se lograron',0,'NONE',NULL,'2026-07-25 12:15:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(101,7051,-1002763662248,'Chartoro FX Señales Gratis','Uff.. gracias, que buena señal, seguimos Profit.!!',0,'NONE',NULL,'2026-07-25 12:20:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(102,7052,-1002763662248,'Chartoro FX Señales Gratis','Te comparto la ganancia que tuve hoy gracias a tus señales',0,'NONE',NULL,'2026-07-25 12:25:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(103,7054,-1002763662248,'Chartoro FX Señales Gratis','Ganando desde tempranito',0,'NONE',NULL,'2026-07-25 12:35:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(104,7055,-1002763662248,'Chartoro FX Señales Gratis','Las mejores señales Enverdad',0,'NONE',NULL,'2026-07-25 12:40:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(105,7057,-1002763662248,'Chartoro FX Señales Gratis','Hola hace poco volví a operar y voy siguiendo tus operación . 
Hoy fue la primera que seguí , la verdad una hermosura . Gracias genios',0,'NONE',NULL,'2026-07-25 12:45:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(106,7058,-1002763662248,'Chartoro FX Señales Gratis','**__…Y APENAS ESTAMOS EMPEZANDO__**',0,'NONE',NULL,'2026-07-25 13:04:20.000000');
INSERT INTO "raw_telegram_messages" VALUES(107,7059,-1002763662248,'Chartoro FX Señales Gratis','👉 [**HAZ CLIC AQUÍ PARA TERMINAR JULIO CON GANANCIAS**](https://t.me/m/q3-XLmhBNmY0)**  **🤑',0,'NONE',NULL,'2026-07-25 13:05:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(108,7060,-1002763662248,'Chartoro FX Señales Gratis','[**Y HAZ CLIC AQUÍ SI QUIERES QUE DUPLIQUE TU DEPÓSITO ANTES DE QUE TERMINE MI PROMOCIÓN**](https://t.me/m/q3-XLmhBNmY0)** **💯💯',0,'NONE',NULL,'2026-07-25 13:34:22.000000');
INSERT INTO "raw_telegram_messages" VALUES(109,7061,-1002763662248,'Chartoro FX Señales Gratis','Gracias Luis... Más de 140 USD de Profit en estos días..
Eres el mejor trader que eh conocido, cómo no te conocí antes para forrarme con tus entradas jejeje. 👍💪💪
El mejor grupo VIP...',0,'NONE',NULL,'2026-07-25 14:01:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(110,7062,-1002763662248,'Chartoro FX Señales Gratis','Nos fuimos profit TP2 XAUSD',0,'NONE',NULL,'2026-07-25 14:15:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(111,7063,-1002763662248,'Chartoro FX Señales Gratis','Lindooo... Gracias  😍',0,'NONE',NULL,'2026-07-25 14:33:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(112,7064,-1002763662248,'Chartoro FX Señales Gratis','Mi primera operación🥳 muchas gracias Luis 🤩',0,'NONE',NULL,'2026-07-25 14:45:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(113,7065,-1002763662248,'Chartoro FX Señales Gratis','🔼**HAS VISTO TODAS LAS GANANCIAS QUE MI VIP ME ENVIÓ ARRIBA?**

**TÚ TAMBIÉN PUEDES GANAR ESO!** 🫵

👉 [**OBTÉN SEÑALES VIP AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-07-25 14:50:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(114,7066,-1002763662248,'Chartoro FX Señales Gratis','ⓘ[ Has sido mencionado por el propietario de este canal](https://t.me/m/q3-XLmhBNmY0).',0,'NONE',NULL,'2026-07-25 15:11:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(115,7067,-1002763662248,'Chartoro FX Señales Gratis','Reclama tu BONO DE DEPÓSITO 100% ahora y empieza a multiplicar tus resultados  ↗️

💵 [**BONO VIP DE DEPÓSITO DOBLE**](https://t.me/m/q3-XLmhBNmY0) 💵',0,'NONE',NULL,'2026-07-25 15:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(116,7068,-1002763662248,'Chartoro FX Señales Gratis','Ya llevo casi 300 usd de ganancia!',0,'NONE',NULL,'2026-07-25 15:35:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(117,7070,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA RECLAMAR EL BONO DE DOBLE DEPÓSITO**](https://t.me/m/q3-XLmhBNmY0) ‼️‼️',0,'NONE',NULL,'2026-07-25 15:44:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(118,7071,-1002763662248,'Chartoro FX Señales Gratis','En dos semanas logré duplicar mi capital 🤑🤑',0,'NONE',NULL,'2026-07-25 15:55:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(119,7072,-1002763662248,'Chartoro FX Señales Gratis','➡️➡️➡️ [**ÚNETE AHORA Y DUPLICO TU DEPÓSITO**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-25 16:28:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(120,7073,-1002763662248,'Chartoro FX Señales Gratis','Espectacular entrada 💪👌',0,'NONE',NULL,'2026-07-25 18:18:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(121,7074,-1002763662248,'Chartoro FX Señales Gratis','**LOS MIEMBROS QUE SE UNAN HOY RECIBIRÁN EL DOBLE DE CAPITAL** 💰💯

🔠🔠 [**RECLÁMALO AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-25 19:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(122,7076,-1002763662248,'Chartoro FX Señales Gratis','Gracias Luis por tu señales positivas',0,'NONE',NULL,'2026-07-25 20:15:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(123,7078,-1002763662248,'Chartoro FX Señales Gratis','Los 3TP cazados 💪',0,'NONE',NULL,'2026-07-25 20:45:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(124,7080,-1002763662248,'Chartoro FX Señales Gratis','[**GANA COMO UN VIP TÚ TAMBIÉN!**](https://t.me/m/q3-XLmhBNmY0) 💰💰💰',0,'NONE',NULL,'2026-07-25 21:15:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(125,7081,-1002763662248,'Chartoro FX Señales Gratis','La cuenta sigue creciendo, muy agradecido....
Mi cuenta de 200 USD lleva 180 USD de crecimiento al día de hoy, total 380 uff .
Eres un crack, gracias..',0,'NONE',NULL,'2026-07-25 22:32:21.000000');
INSERT INTO "raw_telegram_messages" VALUES(126,7082,-1002763662248,'Chartoro FX Señales Gratis','**Imagina convertir $500 en $1000 al instante ****💰****💰****💰**

**💰** **$300 a $600 
****💰**** $400 a $800 **

[**VAMOS CON TODO! **](https://t.me/m/q3-XLmhBNmY0)🚀',0,'NONE',NULL,'2026-07-25 23:21:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(127,7083,-1002763662248,'Chartoro FX Señales Gratis','[**Ⓘ LUIS TE MENCIONÓ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-26 00:18:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(128,7084,-1002763662248,'Chartoro FX Señales Gratis','Uff... Super agradecido. Otro TP más. Ganando prácticamente desde mi cama jaja.
40 USD más lo que ganó en dos días de trabajo lo gano en 15 min con una señal tuya.. muy agradecido 💪👍',0,'NONE',NULL,'2026-07-26 00:44:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(129,7085,-1002763662248,'Chartoro FX Señales Gratis','__ESAS SON SOLO ALGUNAS DE LAS GANANCIAS DE UNA SOLA SEMANA!__ 💵💵💵',0,'NONE',NULL,'2026-07-26 01:07:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(130,7086,-1002763662248,'Chartoro FX Señales Gratis','💰 [**HAZ CLIC AQUÍ SI QUIERES UNA NUEVA FUENTE DE INGRESOS**](https://t.me/m/q3-XLmhBNmY0) 💰',0,'NONE',NULL,'2026-07-26 01:16:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(131,7087,-1002763662248,'Chartoro FX Señales Gratis','**EL VIP TE DA:**

🟢 Señales VIP
🟢 Un curso de trading de 5 horas
🟢 Un sistema comprobado
🟢 Mentoría

💵 [**SUBE DE NIVEL CON VIP**](https://t.me/m/q3-XLmhBNmY0)  💵',0,'NONE',NULL,'2026-07-26 02:16:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(132,7088,-1002763662248,'Chartoro FX Señales Gratis','Las mejores señales en verdad me alegro aver entrado al vip gracias Luis por tu señales',0,'NONE',NULL,'2026-07-26 02:41:14.000000');
INSERT INTO "raw_telegram_messages" VALUES(133,7089,-1002763662248,'Chartoro FX Señales Gratis','Buenas noches!
muchas gracias ya cerré la operación del xauusd con un 20% de ganancia de mi depósito 🤑🤑 muchas gracias',0,'NONE',NULL,'2026-07-26 02:44:42.000000');
INSERT INTO "raw_telegram_messages" VALUES(134,7090,-1002763662248,'Chartoro FX Señales Gratis','Gracias mi hermano muchas bendiciones 👍🤝',0,'NONE',NULL,'2026-07-26 02:50:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(135,7091,-1002763662248,'Chartoro FX Señales Gratis','Gracias Luis, estoy operando contigo ya casi 3 semanas y ya subí más de 300$ mi cuenta',0,'NONE',NULL,'2026-07-26 02:55:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(136,7092,-1002763662248,'Chartoro FX Señales Gratis','💰 **VICTORA TRAS VICTORIA **💰

En el VIP no paramos de cerrar trades verdes ✅
Y tú sigues mirando desde afuera 👀',0,'NONE',NULL,'2026-07-26 03:15:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(137,7093,-1002763662248,'Chartoro FX Señales Gratis','💵 [**HAZ CLIC AQUÍ PARA GANAR DINERO**](https://t.me/m/q3-XLmhBNmY0) 💵',0,'NONE',NULL,'2026-07-26 03:31:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(138,7094,-1002763662248,'Chartoro FX Señales Gratis','Esto es hoy 😍',0,'NONE',NULL,'2026-07-26 04:11:58.000000');
INSERT INTO "raw_telegram_messages" VALUES(139,7095,-1002763662248,'Chartoro FX Señales Gratis','Seguimos Profit Luis.. muy agradecido,, ayer hubo turbulencias pero es parte de. Y hoy ya vamos super Profit 425 USD va la cuenta 💪👌',0,'NONE',NULL,'2026-07-26 04:15:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(140,7097,-1002763662248,'Chartoro FX Señales Gratis','Estás han sido las ganancias que obtuve con tus alertas, muchas gracias!',0,'NONE',NULL,'2026-07-26 04:31:50.000000');
INSERT INTO "raw_telegram_messages" VALUES(141,7098,-1002763662248,'Chartoro FX Señales Gratis','__El bono de depósito al doble todavía está disponible!!!__

👉 [**RECLÁMALO AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-26 04:45:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(142,7100,-1002763662248,'Chartoro FX Señales Gratis','Estás han sido las ganancias que obtuve con tus alertas, muchas gracias!',0,'NONE',NULL,'2026-07-26 05:02:47.000000');
INSERT INTO "raw_telegram_messages" VALUES(143,7101,-1002763662248,'Chartoro FX Señales Gratis','**DE VERDAD TE VAS A PERDER ESTAS GANANCIAS?** 💰💰💰',0,'NONE',NULL,'2026-07-26 05:25:32.000000');
INSERT INTO "raw_telegram_messages" VALUES(144,7102,-1002763662248,'Chartoro FX Señales Gratis','💎 [**HAZ CLIC AQUÍ PARA RECIBIR DE 4 A 8 SEÑALES VIP DIARIAS**](https://t.me/m/q3-XLmhBNmY0) 💎',0,'NONE',NULL,'2026-07-26 06:45:41.000000');
INSERT INTO "raw_telegram_messages" VALUES(145,7104,-1002763662248,'Chartoro FX Señales Gratis','❓ **TE GUSTARÍA TENER ACCESO A ESTRATEGIAS DE TRADING EXCLUSIVAS?**',0,'NONE',NULL,'2026-07-26 11:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(146,7105,-1002763662248,'Chartoro FX Señales Gratis','💥 4–8 señales de alta calidad diarias
💥 Curso completo de trading
💥 Resultados y ganancias respaldados por rendimiento
💥 Soporte 24/7 cuando lo necesites

‼️ [**HAZ CLIC AQUÍ PARA ASEGURAR TU CUPO**](https://t.me/m/q3-XLmhBNmY0)  ‼️',0,'NONE',NULL,'2026-07-26 12:21:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(147,7106,-1002763662248,'Chartoro FX Señales Gratis','Suuuupeeeer bien! En una semana casi recupere el 50% de la inversión! Así que vamos bien',0,'NONE',NULL,'2026-07-26 13:01:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(148,7107,-1002763662248,'Chartoro FX Señales Gratis','🔥',0,'NONE',NULL,'2026-07-26 13:15:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(149,7108,-1002763662248,'Chartoro FX Señales Gratis','Estás modo fuego bro 
Muchas gracias ❤️‍🔥',0,'NONE',NULL,'2026-07-26 13:34:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(150,7109,-1002763662248,'Chartoro FX Señales Gratis','Usted un crack para hacer dinero las mejores señales 💪',0,'NONE',NULL,'2026-07-26 13:45:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(151,7110,-1002763662248,'Chartoro FX Señales Gratis','⬆️ **MIEMBROS VIP APRENDAN Y GANEN AL MISMO TIEMPO**',0,'NONE',NULL,'2026-07-26 14:04:35.000000');
INSERT INTO "raw_telegram_messages" VALUES(152,7111,-1002763662248,'Chartoro FX Señales Gratis','Copiar ➕ Pegar 🟰 **GANAR DINERO** 💰💰💰

👉 [**HAZ CLIC AQUÍ PARA OBTENER GANANCIAS**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-07-26 14:34:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(153,7112,-1002763662248,'Chartoro FX Señales Gratis','❌ __Las señales no esperan.
____❌__ __Las oportunidades no esperan.
____❌__ __El crecimiento no espera.__

Lo único que está en pausa ahora mismo… eres tú  🫵

**QUITA LA PAUSA** 

Envíame un mensaje y te guío para empezar antes de que llegue el lunes 👉 @SoporteChartoroFX 🏆',0,'NONE',NULL,'2026-07-26 15:07:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(154,7113,-1002763662248,'Chartoro FX Señales Gratis','Ve lo que gane con la señal de la mañana, excelente',0,'NONE',NULL,'2026-07-26 15:28:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(155,7115,-1002763662248,'Chartoro FX Señales Gratis','Muchas gracias Luis por esas magníficas señales. Sigo de a poquito pero segura. Recomiendo ingresar al VIP 👌💰💸',0,'NONE',NULL,'2026-07-26 15:45:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(156,7116,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA ACCEDER A LA ESTRATEGIA GANADORA**](https://t.me/m/q3-XLmhBNmY0) 💪',0,'NONE',NULL,'2026-07-26 15:58:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(157,7117,-1002763662248,'Chartoro FX Señales Gratis','**CÓMO VA TU FIN DE SEMANA?**',0,'NONE',NULL,'2026-07-26 16:19:39.000000');
INSERT INTO "raw_telegram_messages" VALUES(158,7118,-1002763662248,'Chartoro FX Señales Gratis','Quieres algo para revisar durante el fin de semana antes de que el mercado abra de nuevo?

📖 [**OBTÉN MATERIALES EDUCATIVOS GRATUITOS AQUÍ!**](https://t.me/m/q3-XLmhBNmY0) 📖',0,'NONE',NULL,'2026-07-26 17:08:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(159,7119,-1002763662248,'Chartoro FX Señales Gratis','Señales VIP? **DIARIAS**
Curso de trading? **CURSO DE TRADING DE 5 HORAS**
Precisión? **80%**
Soporte? **LAS 24 HORAS**

**ESCRÍBEME SI QUIERES TODO ESTO** 🔠 @SoporteChartoroFX',0,'NONE',NULL,'2026-07-26 18:15:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(160,7120,-1002763662248,'Chartoro FX Señales Gratis','**Los nuevos miembros VIP ya están leyendo y viendo el curso antes de que abran los mercados el Lunes ****📚**',0,'NONE',NULL,'2026-07-26 18:41:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(161,7121,-1002763662248,'Chartoro FX Señales Gratis','Enserio necesito estar en tu VIP 🤑',0,'NONE',NULL,'2026-07-26 19:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(162,7122,-1002763662248,'Chartoro FX Señales Gratis','⬆️ **OBTÉN GANANCIAS INCLUSO AQUÍ EN EL GRUPO PRINCIPAL!**',0,'NONE',NULL,'2026-07-26 19:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(163,7123,-1002763662248,'Chartoro FX Señales Gratis','__CANSADO DE PERDER?__
➡️ [**TOCA AQUÍ PARA UNIRTE A UN GRUPO GANADOR CON PRUEBAS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-26 19:31:16.000000');
INSERT INTO "raw_telegram_messages" VALUES(164,7124,-1002763662248,'Chartoro FX Señales Gratis','Que buena señal, crack, ya cerré la de 0.30 la otra la dejo hasta TP 3 💥',0,'NONE',NULL,'2026-07-26 20:10:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(165,7125,-1002763662248,'Chartoro FX Señales Gratis','Muy emocionada muchas gracias 🙌🏻',0,'NONE',NULL,'2026-07-26 20:33:48.000000');
INSERT INTO "raw_telegram_messages" VALUES(166,7126,-1002763662248,'Chartoro FX Señales Gratis','Los resultados de ayer con las señales gratuitas. Una locura germano! (La que esta en negativo fue un análisis mio) ahora solo opero con tus señales.',0,'NONE',NULL,'2026-07-26 21:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(167,7127,-1002763662248,'Chartoro FX Señales Gratis','🔴 [**ENTRA AL VIP ANTES DE QUE SALGA UNA NUEVA SEÑAL**](https://t.me/m/q3-XLmhBNmY0) 🔴',0,'NONE',NULL,'2026-07-26 22:19:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(168,7128,-1002763662248,'Chartoro FX Señales Gratis','Amigo Luis ya mi cuenta la eh duplicado muchas gracias',0,'NONE',NULL,'2026-07-26 23:11:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(169,7129,-1002763662248,'Chartoro FX Señales Gratis','Reclama tu BONO DE DEPÓSITO 100% ahora y empieza a multiplicar tus resultados  ↗️

💵 [**BONO VIP DE DEPÓSITO DOBLE**](https://t.me/m/q3-XLmhBNmY0) 💵',0,'NONE',NULL,'2026-07-26 23:50:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(170,7130,-1002763662248,'Chartoro FX Señales Gratis','A 1 mes que empecé, trabajando parcialmente. estando al pendiente 1 o 2 horas al día. En algunas he perdido pero la mayoría se ha ganado',0,'NONE',NULL,'2026-07-27 00:37:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(171,7131,-1002763662248,'Chartoro FX Señales Gratis','🔼**YA HAS VISTO RESULTADO TRAS RESULTADO!** 💵💵
**
QUÉ ESTÁS ESPERANDO?**',0,'NONE',NULL,'2026-07-27 00:44:52.000000');
INSERT INTO "raw_telegram_messages" VALUES(172,7132,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA GANAR COMO ELLOS TAMBIÉN **](https://t.me/m/q3-XLmhBNmY0)🫵',0,'NONE',NULL,'2026-07-27 00:55:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(173,7133,-1002763662248,'Chartoro FX Señales Gratis','**ASÍ ES COMO LOS MIEMBROS VIP SE MANTIENEN EN LA CIMA:**

✅ 4–8 señales premium todos los días
✅ Profundizando en el curso completo de trading de 5 horas
✅ Señales confiables con 80% de efectividad
✅ Soporte 24/7 para que nunca te quedes solo

**QUIERES ESTAR EN LA CIMA?** 
🏆 [**HAZ CLIC AQUÍ PARA RECLAMAR TODOS LOS BENEFICIOS VIP**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-07-27 01:16:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(174,7134,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA RECLAMAR EL BONO DE DOBLE DEPÓSITO**](https://t.me/m/q3-XLmhBNmY0) ‼️‼️',0,'NONE',NULL,'2026-07-27 02:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(175,7136,-1002763662248,'Chartoro FX Señales Gratis','Otro día Victorioso 
Vamoooos ❤️‍🔥',0,'NONE',NULL,'2026-07-27 02:45:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(176,7137,-1002763662248,'Chartoro FX Señales Gratis','Deja de intentar hacerlo solo — te está costando ganancias cada semana 💸
El equipo correcto, la guía correcta y las entradas correctas = **RESULTADOS** 📈

Únete a quienes ya descubrieron cómo hacerlo 😉😉

⚠️** **[**RECLAMA ACCESO VIP GRATIS + BONO DE DEPÓSITO DOBLE AQUÍ**](http://t.me/SoporteChartoroFX) ⚠️',0,'NONE',NULL,'2026-07-27 02:50:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(177,7138,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4096
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-07-27 02:50:23.000000');
INSERT INTO "raw_telegram_messages" VALUES(178,7139,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 ****#XAUUSD**** **

**Direction: 📈 ****#SELL**** **

** Entry Point: **4096
**⛔️ Stop Loss (SL): **4104

**🏆 TP1: **4093
**🏆 TP2:** 4088
**🏆 TP3:** 4080

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-27 02:53:47.000000');
INSERT INTO "raw_telegram_messages" VALUES(179,7140,-1002763662248,'Chartoro FX Señales Gratis','**DIRECTO AL AZUL ****💙**',0,'NONE',NULL,'2026-07-27 03:03:44.000000');
INSERT INTO "raw_telegram_messages" VALUES(180,7141,-1002763662248,'Chartoro FX Señales Gratis','**EL MERCADO ABRE Y DE INMEDIATO SE VUELVE PRODUCTIVO! ****⚡️****

****#XAUUSD**** TP1 HIT, +30 Pips 🏆
**
__Ganancia rápida para mantener el ritmo fuerte al inicio de la semana!__',0,'NONE',NULL,'2026-07-27 03:05:35.000000');
INSERT INTO "raw_telegram_messages" VALUES(181,7143,-1002763662248,'Chartoro FX Señales Gratis','TP2 **CASI ALCANZADO **🔥',0,'NONE',NULL,'2026-07-27 03:27:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(182,7144,-1002763662248,'Chartoro FX Señales Gratis','**LA ESTRUCTURA A NUESTRO FAVOR, LAS GANANCIAS FLUYEN! **

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__El mercado se movió según lo planeado. Sin ruido, sin dudas, solo una ejecución limpia.__',0,'NONE',NULL,'2026-07-27 03:28:48.000000');
INSERT INTO "raw_telegram_messages" VALUES(183,7146,-1002763662248,'Chartoro FX Señales Gratis','**PUDISTE CACHAR ESO??? **💥💥',0,'NONE',NULL,'2026-07-27 04:03:29.000000');
INSERT INTO "raw_telegram_messages" VALUES(184,7147,-1002763662248,'Chartoro FX Señales Gratis','**ASÍ ES COMO LO HACEMOS EN EL VIP** 🔥

[**ÚNETE AHORA **](https://t.me/m/q3-XLmhBNmY0)🚀',0,'NONE',NULL,'2026-07-27 04:04:41.000000');
INSERT INTO "raw_telegram_messages" VALUES(185,7148,-1002763662248,'Chartoro FX Señales Gratis','💎 [**HAZ CLIC AQUÍ PARA RECIBIR DE 4 A 8 SEÑALES VIP DIARIAS**](https://t.me/m/q3-XLmhBNmY0) 💎',0,'NONE',NULL,'2026-07-27 04:31:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(186,7149,-1002763662248,'Chartoro FX Señales Gratis','Esto fue de las señales de Oro de hace poco....gracias !!! 🤗 Voy a paso lento pero segura',0,'NONE',NULL,'2026-07-27 05:25:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(187,7150,-1002763662248,'Chartoro FX Señales Gratis','**LOS MIEMBROS DEL VIP ESTÁN GANANDO ESTO EN CUESTIÓN DE MINUTOS!** 🤑🤑',0,'NONE',NULL,'2026-07-27 05:26:53.000000');
INSERT INTO "raw_telegram_messages" VALUES(188,7151,-1002763662248,'Chartoro FX Señales Gratis','🏆 [**SÉ PARTE DE LA COMUNIDAD VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-07-27 05:31:19.000000');
INSERT INTO "raw_telegram_messages" VALUES(189,7152,-1002763662248,'Chartoro FX Señales Gratis','🔈 **SOLO QUEDA UN LUGAR PARA EL VIP GRATIS!!!!**',0,'NONE',NULL,'2026-07-27 06:17:16.000000');
INSERT INTO "raw_telegram_messages" VALUES(190,7153,-1002763662248,'Chartoro FX Señales Gratis','⚠️ [**ASEGURA EL ÚLTIMO LUGAR AQUÍ**](https://t.me/m/q3-XLmhBNmY0) ⚠️',0,'NONE',NULL,'2026-07-27 06:30:55.000000');
INSERT INTO "raw_telegram_messages" VALUES(191,7156,-1002763662248,'Chartoro FX Señales Gratis','**YA TIENES ACTIVADAS TUS NOTIFICACIONES?** 🔔',0,'NONE',NULL,'2026-07-27 11:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(192,7157,-1002763662248,'Chartoro FX Señales Gratis','💥 **NUEVA SEMANA, NUEVAS GANANCIAS** 💥

Envíame un mensaje ahora y recibe señales **VIP GRATIS**! 💯',0,'NONE',NULL,'2026-07-27 12:05:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(193,7158,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📈#XAUUSD📈

**Direction:📈** **#SELL**
**Entry Point**: 4086.95

🏆**TP1**: 4083.95
🏆**TP2**: 4076.95
🏆**TP3**: 4066.95

**⛔️ Stop Loss (SL)**: 4096.95

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Same as the original idea',1,'REGEX',NULL,'2026-07-27 12:19:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(194,7159,-1002763662248,'Chartoro FX Señales Gratis','**EL ORO YA ESTÁ CORRIENDO ****👀****

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Captura rápida desde el inicio.__',0,'NONE',NULL,'2026-07-27 12:22:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(195,7160,-1002763662248,'Chartoro FX Señales Gratis','👀👀👀',0,'NONE',NULL,'2026-07-27 12:39:22.000000');
INSERT INTO "raw_telegram_messages" VALUES(196,7161,-1002763662248,'Chartoro FX Señales Gratis','**ESTÁS LISTO PARA VER LOS RESULTADOS DE LA SEMANA PASADA?** 🤫',0,'NONE',NULL,'2026-07-27 12:58:39.000000');
INSERT INTO "raw_telegram_messages" VALUES(197,7162,-1002763662248,'Chartoro FX Señales Gratis','📈** RESULTADOS SEMANALES DE SEÑALES** 📈
__20 de Julio – 24 de Julio, 2026__

💰 TOTAL: **+916 PIPS GANADOS** 💰

✔️ Win Ratio: 74% (19 ganadas / 7 perdidas)
✔️ Operaciones totales: 26 setups
✔️ Buy vs Sell: 18 compras / 8 ventas
✔️ XAUUSD volvió a ser uno de los pares con mejor rendimiento durante la semana
✔️ Lunes (+363 pips), martes (+323 pips) y viernes (+300 pips) lideraron las ganancias
✔️ Otra semana consistente aprovechando las mejores oportunidades del mercado FOREX y GOLD

🤑 **QUÉ SIGNIFICA ESTO EN DINERO REAL?**

• 0.01 lote → ~$9.16 USD
• 0.10 lote → ~$91.60 USD
• 1.00 lote → ~**$916+ USD EN UNA SEMANA**

🔥 **+916 PIPS EN SOLO UNA SEMANA**

__ESCRÍBEME AHORA Y DESCUBRE CÓMO RECIBIR LAS SEÑALES VIP GRATIS__ 🚀',0,'NONE',NULL,'2026-07-27 13:16:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(198,7164,-1002763662248,'Chartoro FX Señales Gratis','**EL MOMENTUM ESTÁ ENTRANDO ****🚀****

****#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El oro se mueve limpio y fuerte.__',0,'NONE',NULL,'2026-07-27 13:32:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(199,7165,-1002763662248,'Chartoro FX Señales Gratis','**Y ESE ES TODO EL MOVIMIENTO ****🤯****

****#XAUUSD**** TP3 HIT, +200 Pips 🏆
**
__Un seguimiento hermoso.__',0,'NONE',NULL,'2026-07-27 14:32:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(200,7167,-1002763662248,'Chartoro FX Señales Gratis','**GANANCIA TRAS GANANCIA, TRAS GANANCIA! **🚀',0,'NONE',NULL,'2026-07-27 17:39:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(201,7168,-1002763662248,'Chartoro FX Señales Gratis','👉 [**HAZ CLIC AQUÍ PARA OBTENER MÁS**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-07-27 17:39:55.000000');
INSERT INTO "raw_telegram_messages" VALUES(202,7169,-1002763662248,'Chartoro FX Señales Gratis','Lo mejor 🏆🤩',0,'NONE',NULL,'2026-07-27 18:16:47.000000');
INSERT INTO "raw_telegram_messages" VALUES(203,7170,-1002763662248,'Chartoro FX Señales Gratis','**QUIERES ESTO TAMBIÉN?** 👆

[**EMPIEZA HOY Y DUPLICARÉ TU DEPÓSITO!!!**](https://t.me/m/q3-XLmhBNmY0) 🔤2️⃣',0,'NONE',NULL,'2026-07-27 18:19:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(204,7171,-1002763662248,'Chartoro FX Señales Gratis','⬆️⬆️ **MIRA LAS GANANCIAS QUE TE PERDISTE LA SEMANA PASADA POR NO UNIRTE A NOSOTROS!**',0,'NONE',NULL,'2026-07-27 18:40:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(205,7172,-1002763662248,'Chartoro FX Señales Gratis','[**Ⓘ LUIS TE MENCIONÓ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-27 18:50:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(206,7173,-1002763662248,'Chartoro FX Señales Gratis','Ya estoy 360 en mi primera semana , casi duplicó mi primer depósito',0,'NONE',NULL,'2026-07-27 19:01:38.000000');
INSERT INTO "raw_telegram_messages" VALUES(207,7175,-1002763662248,'Chartoro FX Señales Gratis','💎 **SEÑALES VIP GRATIS
****💎**** MATERIAL EDUCATIVO GRATIS
****💎**** MENTORÍA GRATIS**

🏆[** RECLAMA AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-07-27 19:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(208,7176,-1002763662248,'Chartoro FX Señales Gratis','**COPIAR **➕** PEGAR **🟰** INGRESOS DIARIOS** 💰🔥

👉 [**HAZ CLIC AQUÍ Y APROVECHA **](https://t.me/m/q3-XLmhBNmY0)👈',0,'NONE',NULL,'2026-07-27 20:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(209,7177,-1002763662248,'Chartoro FX Señales Gratis','Solo 20 minutos al día. Eso es todo lo que necesitas.

Operar no se trata de trabajar más duro, sino de trabajar con más inteligencia. 📈💯

Pasa menos tiempo persiguiendo el dinero y más tiempo disfrutando la vida. 🤔

Envíame un mensaje hoy, tus 20 minutos podrían cambiarlo todo! 🔥

🏆[** VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-07-27 21:05:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(210,7179,-1002763662248,'Chartoro FX Señales Gratis','Hola Luis, paso a mostrar las ganancias, con esta última operación ya he triplicado mi depósito de 100Usd en menos de un mes 

Vamos por maaaaas',0,'NONE',NULL,'2026-07-27 22:35:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(211,7180,-1002763662248,'Chartoro FX Señales Gratis','⬆️ __YA TRIPLICASTE TU DINERO? __

[**TOCA AQUÍ Y EMPIEZA A GANAR CON NOSOTROS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-27 22:45:35.000000');
INSERT INTO "raw_telegram_messages" VALUES(212,7181,-1002763662248,'Chartoro FX Señales Gratis','Para unirte solo necesitas:
🔴 Un teléfono
🔴 Internet
🔴 20 minutos al día

❌ NO SE NECESITA EXPERIENCIA ❌

[**ÚNETE GRATIS AL VIP**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-27 23:26:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(213,7182,-1002763662248,'Chartoro FX Señales Gratis','Poco a poquito creciendo. Más que feliz. Muchas gracias Luis',0,'NONE',NULL,'2026-07-27 23:45:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(214,7183,-1002763662248,'Chartoro FX Señales Gratis','**COPIAR** ➡️  **PEGAR**  **➡️****GANAR**',0,'NONE',NULL,'2026-07-28 00:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(215,7184,-1002763662248,'Chartoro FX Señales Gratis','[**CAMBIA TU VIDA HOY Y GANA DINERO DESDE TU CELULAR! **](https://t.me/m/q3-XLmhBNmY0)📱',0,'NONE',NULL,'2026-07-28 00:32:42.000000');
INSERT INTO "raw_telegram_messages" VALUES(216,7185,-1002763662248,'Chartoro FX Señales Gratis','__Como ya saben, el trading cambió mi vida...__

🪙 Me dio el poder de ganar dinero a mi manera
🪙 Me ayudó a salir de la rutina del 9 a 5
🪙 Y me dio verdadera libertad financiera

⏳  [**HAZ CLIC AQUÍ PARA TRANSFORMAR TU VIDA TAMBIÉN**](https://t.me/m/q3-XLmhBNmY0) ⏳',0,'NONE',NULL,'2026-07-28 00:51:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(217,7186,-1002763662248,'Chartoro FX Señales Gratis','Ya viste a los miembros sacando ganancias de:

💰 $200
💰 $500
💰 $700 **EN UNA SOLA SEMANA** 🤑🤑🤑

Y todavía lo estás pensando? 🤔',0,'NONE',NULL,'2026-07-28 01:21:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(218,7188,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4044
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-07-28 02:04:39.000000');
INSERT INTO "raw_telegram_messages" VALUES(219,7189,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4044
**⛔️ Stop Loss (SL): **4052

**🏆 TP1: **4041
**🏆 TP2:** 4036
**🏆 TP3:** 4028

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-28 02:07:48.000000');
INSERT INTO "raw_telegram_messages" VALUES(220,7190,-1002763662248,'Chartoro FX Señales Gratis','Hola Luis, que señal tan excelente',0,'NONE',NULL,'2026-07-28 02:45:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(221,7191,-1002763662248,'Chartoro FX Señales Gratis','**ESTO ES LO QUE PUEDES GANAR EN MINUTOS **📈📈',0,'NONE',NULL,'2026-07-28 02:49:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(222,7192,-1002763662248,'Chartoro FX Señales Gratis','ⓘ[__ Luis te mencionó__](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-28 02:53:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(223,7193,-1002763662248,'Chartoro FX Señales Gratis','**PRIMER TOQUE EN CAMINO ****🔥**',0,'NONE',NULL,'2026-07-28 02:56:58.000000');
INSERT INTO "raw_telegram_messages" VALUES(224,7194,-1002763662248,'Chartoro FX Señales Gratis','**EL ORO SE MOVIÓ PRIMERO **😎

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Golpe rápido, ganancia instantánea ____💰__',0,'NONE',NULL,'2026-07-28 02:59:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(225,7197,-1002763662248,'Chartoro FX Señales Gratis','ESTÁS DISFRUTANDO LOS BLUES? 💙📈',0,'NONE',NULL,'2026-07-28 03:31:12.000000');
INSERT INTO "raw_telegram_messages" VALUES(226,7198,-1002763662248,'Chartoro FX Señales Gratis','🏆 [**HAZ CLIC AQUÍ PARA OBTENER MÁS SEÑALES**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-07-28 03:31:39.000000');
INSERT INTO "raw_telegram_messages" VALUES(227,7200,-1002763662248,'Chartoro FX Señales Gratis','**LUEGO ACELERÓ ****🚀**

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__Extensión limpia, sin dudas ____👀__',0,'NONE',NULL,'2026-07-28 05:39:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(228,7202,-1002763662248,'Chartoro FX Señales Gratis','**VAMOSSSS **⚡️⚡️',0,'NONE',NULL,'2026-07-28 06:09:15.000000');
INSERT INTO "raw_telegram_messages" VALUES(229,7204,-1002763662248,'Chartoro FX Señales Gratis','**JULIO YA CASI TERMINA!!!**
Estás listo para cerrar el mes con ganancias? 📈',0,'NONE',NULL,'2026-07-28 11:06:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(230,7205,-1002763662248,'Chartoro FX Señales Gratis','__Te preguntas cómo unirte al VIP?
Te preguntas cómo funcionan las señales?
Te preguntas qué es lo que recibes dentro?__

**MÁNDAME UN DM Y TE AYUDO A ENTRAR AL VIP**
👉👉 [@SoporteChartoroFX](https://t.me/SoporteChartoroFX)',0,'NONE',NULL,'2026-07-28 11:38:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(231,7206,-1002763662248,'Chartoro FX Señales Gratis','**EL VIP ESTÁ CAMBIANDO VIDAS!** 🔼

[**HAZ CLIC AQUÍ Y EMPIEZA AGOSTO CON EL PIE DERECHO!**](https://t.me/m/q3-XLmhBNmY0) 🚀',0,'NONE',NULL,'2026-07-28 12:21:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(232,7207,-1002763662248,'Chartoro FX Señales Gratis','🏆 **BENEFICIOS VIP** 🏆

✔️ 4–8 señales de trading de alta calidad al día
✔️ Un curso completo de trading
✔️ Una guía completa de la A a la Z para que sepas por qué funcionan las operaciones
✔️ Mentoría y acompañamiento real
✔️ Resultados comprobados que puedes seguir paso a paso',0,'NONE',NULL,'2026-07-28 13:00:26.000000');
INSERT INTO "raw_telegram_messages" VALUES(233,7208,-1002763662248,'Chartoro FX Señales Gratis','[**‼️**](https://t.me/m/q3-XLmhBNmY0) [**HAZ CLIC AQUÍ ANTES DE QUE SALGA LA PRÓXIMA SEÑAL VIP ‼️**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-28 13:15:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(234,7209,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4026.27

🏆**TP1**: 4029.27
🏆**TP2**: 4036.27
🏆**TP3**: 4046.27

**⛔️ Stop Loss (SL)**: 4016.27

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Same as the original idea',1,'REGEX',NULL,'2026-07-28 14:05:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(235,7210,-1002763662248,'Chartoro FX Señales Gratis','**CLARA RESPUESTA DESDE LA APERTURA ****👀****

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Movimiento inmediato, la lectura inicial se valida.__',0,'NONE',NULL,'2026-07-28 14:07:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(236,7211,-1002763662248,'Chartoro FX Señales Gratis','🔤🔤🔤    🔤🔤🔤🔤🔤🔤',0,'NONE',NULL,'2026-07-28 15:23:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(237,7212,-1002763662248,'Chartoro FX Señales Gratis','⏩ [**RECLAMA ACCESO VIP GRATIS Y BENEFICIOS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-28 16:16:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(238,7213,-1002763662248,'Chartoro FX Señales Gratis','COPIAR OPERACIONES 
              ➕
APRENDER EL SISTEMA
              ➕
HACER PREGUNTAS EN CUALQUIER MOMENTO 
              ➕
CONSTRUIR CONFIANZA 
              ➕
GANAR MIENTRAS APRENDES 

              🟰
              
        🏆 [**VIP**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-07-28 17:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(239,7214,-1002763662248,'Chartoro FX Señales Gratis','[**TOCA AQUÍ SI ERES PRINCIPIANTE Y BUSCAS UN MENTOR PROFESIONAL Y MATERIAL DE TRADING GRATIS**](https://t.me/m/q3-XLmhBNmY0) 📚📈',0,'NONE',NULL,'2026-07-28 19:03:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(240,7215,-1002763662248,'Chartoro FX Señales Gratis','Si hubieras empezado hace 2 semanas, ya tendrías:

✔️ 2 semanas de setups guiados 
✔️ Más de 20 operaciones ejecutadas 
✔️ Ganancias reales para mostrar 

En cambio, estás en el día 14 de “pensarlo” 🤔🤔
No te falta tiempo… **__te falta compromiso__**.

⚠️  Únete antes de que otra semana se te escape 👉 [**VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-28 20:29:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(241,7216,-1002763662248,'Chartoro FX Señales Gratis','**📖**** **[**RECLAMA TU E-BOOK DE TRADING GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)** ****📖**',0,'NONE',NULL,'2026-07-28 23:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(242,7217,-1002763662248,'Chartoro FX Señales Gratis','⚠️ **EL VIP NO ES SOLO PARA PRINCIPIANTES** ⚠️

Esto también es para:
Traders **CANSADOS DE PERDER** y traders que quieren **LLEVAR SU NIVEL AL MÁXIMO**  🌡

**📊** [**HAZ CLIC AQUÍ PARA CAMBIAR TU JUEGO**](https://t.me/m/q3-XLmhBNmY0) **📊**',0,'NONE',NULL,'2026-07-29 01:34:17.000000');
INSERT INTO "raw_telegram_messages" VALUES(243,7218,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4031
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-07-29 02:29:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(244,7219,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4031
**⛔️ Stop Loss (SL): **4023

**🏆 TP1: **4034
**🏆 TP2:** 4039
**🏆 TP3:** 4047

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-29 02:35:56.000000');
INSERT INTO "raw_telegram_messages" VALUES(245,7222,-1002763662248,'Chartoro FX Señales Gratis','**Y EXPLOTÓ AL INSTANTE ****💥**

**#XAUUSD**** TP1 HIT, +30 Pips ****🏆**

__La ruptura fue limpia y precisa.__',0,'NONE',NULL,'2026-07-29 02:36:36.000000');
INSERT INTO "raw_telegram_messages" VALUES(246,7224,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4023
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-07-29 04:01:37.000000');
INSERT INTO "raw_telegram_messages" VALUES(247,7225,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4023
**⛔️ Stop Loss (SL): **4031

**🏆 TP1: **4020
**🏆 TP2:** 4015
**🏆 TP3:** 4007

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-29 04:03:18.000000');
INSERT INTO "raw_telegram_messages" VALUES(248,7226,-1002763662248,'Chartoro FX Señales Gratis','**❌ SL HIT**

Darle más espacio a la operación no ayudó esta vez.

No pasa nada — seguiré buscando una nueva configuración clara 🔎

Manténganse pacientes, equipo. Operamos con inteligencia, no con prisas. ✅',0,'NONE',NULL,'2026-07-29 05:16:56.000000');
INSERT INTO "raw_telegram_messages" VALUES(249,7227,-1002763662248,'Chartoro FX Señales Gratis','Ya estoy 360 en mi primera semana , casi duplicó mi primer depósito',0,'NONE',NULL,'2026-07-29 07:11:25.000000');
INSERT INTO "raw_telegram_messages" VALUES(250,7228,-1002763662248,'Chartoro FX Señales Gratis','Hace unos días esta fue mi ganancia, en un solo día 💪🏻',0,'NONE',NULL,'2026-07-29 07:25:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(251,7230,-1002763662248,'Chartoro FX Señales Gratis','❓ __Quieres guía gratuita?__',0,'NONE',NULL,'2026-07-29 11:15:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(252,7231,-1002763662248,'Chartoro FX Señales Gratis','✅** SÍ, __recibirás de 4 a 8 señales diarias__
****✅**** SÍ, __tendrás mi guía y acompañamiento__
****✅**** SÍ, __recibirás mis materiales educativos__**

❗️ [**RECLAMA TODO AHORA**](https://t.me/m/q3-XLmhBNmY0) ❗️',0,'NONE',NULL,'2026-07-29 13:44:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(253,7232,-1002763662248,'Chartoro FX Señales Gratis','[**Y SI TE DIJERA QUE PUEDES GANAR DINERO CON SOLO UN SIMPLE COPIAR Y PEGAR????**](https://t.me/m/q3-XLmhBNmY0) 💵💵💵',0,'NONE',NULL,'2026-07-29 15:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(254,7233,-1002763662248,'Chartoro FX Señales Gratis','1️⃣ Copiar

2️⃣ Pegar

3️⃣ **GANAR DINERO** 💵💵💵',0,'NONE',NULL,'2026-07-29 17:24:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(255,7234,-1002763662248,'Chartoro FX Señales Gratis','Muchas personas se quedan en grupos gratis esperando…
__refrescando la pantalla por una señal, tal vez dos.__

**DENTRO DEL VIP, ES DIFERENTE** 😉
🏆4–8 señales de alta calidad al día.
➡️Más setups.
➡️Más oportunidades para ejecutar.
➡️Más espacio para gestionar el riesgo y construir consistencia.',0,'NONE',NULL,'2026-07-29 19:20:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(256,7235,-1002763662248,'Chartoro FX Señales Gratis','🔓  [**TOCA AQUÍ PARA OBTENER ACCESO GRATIS A LAS SEÑALES VIP**](https://t.me/m/q3-XLmhBNmY0)  🔓',0,'NONE',NULL,'2026-07-29 22:25:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(257,7236,-1002763662248,'Chartoro FX Señales Gratis','Pasas 20 minutos scrolleando? No ganas nada. 

Pasas 20 minutos operando? **GENERAS INGRESOS EXTRA.** 💰',0,'NONE',NULL,'2026-07-30 01:28:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(258,7237,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4068
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-07-30 03:02:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(259,7238,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4068
**⛔️ Stop Loss (SL): **4076

**🏆 TP1: **4065
**🏆 TP2:** 4060
**🏆 TP3:** 4052

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-30 03:05:30.000000');
INSERT INTO "raw_telegram_messages" VALUES(260,7239,-1002763662248,'Chartoro FX Señales Gratis','**EL PRECIO EMPIEZA A MOVERSE **👀',0,'NONE',NULL,'2026-07-30 03:10:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(261,7242,-1002763662248,'Chartoro FX Señales Gratis','**EL MERCADO HIZO EL PRIMER MOVIMIENTO **👀**

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**
**
**__Simplemente aceptamos la invitación __💰',0,'NONE',NULL,'2026-07-30 03:12:22.000000');
INSERT INTO "raw_telegram_messages" VALUES(262,7244,-1002763662248,'Chartoro FX Señales Gratis','**EL MOMENTUM ESTÁ ENTRANDO **🚀',0,'NONE',NULL,'2026-07-30 03:19:42.000000');
INSERT INTO "raw_telegram_messages" VALUES(263,7245,-1002763662248,'Chartoro FX Señales Gratis','**LUEGO LLEGÓ EL IMPULSO REAL **

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__El momentum tomó el control__',0,'NONE',NULL,'2026-07-30 03:21:16.000000');
INSERT INTO "raw_telegram_messages" VALUES(264,7247,-1002763662248,'Chartoro FX Señales Gratis','**OBJETIVO FINAL A LA VISTA **🤯',0,'NONE',NULL,'2026-07-30 03:31:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(265,7248,-1002763662248,'Chartoro FX Señales Gratis','**Y LA CARRERA SE COMPLETÓ **💣**

****#XAUUSD**** TP3 HIT, +160 Pips 🏆**
**
**__Seguimiento perfecto ____👑__',0,'NONE',NULL,'2026-07-30 03:32:56.000000');
INSERT INTO "raw_telegram_messages" VALUES(266,7250,-1002763662248,'Chartoro FX Señales Gratis','No necesitas “__ser bueno__” para entrar al VIP.
**ENTRAS PARA VOLVERTE BUENO** 💪

**Copias operaciones, aprendes por qué funcionan y desarrollas habilidad al mismo tiempo.**

Así es como los principiantes realmente **SUBEN DE NIVEL** 🔼

SI ERES PRINCIPIANTE, [**HAZ CLIC AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-07-30 04:23:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(267,7251,-1002763662248,'Chartoro FX Señales Gratis','**HOLA TRADERS!!!!** 🔔🔔🔔',0,'NONE',NULL,'2026-07-30 09:23:18.000000');
INSERT INTO "raw_telegram_messages" VALUES(268,7252,-1002763662248,'Chartoro FX Señales Gratis','‼️ __Estás cansado de resultados inconsistentes y quieres cambiar eso?__',0,'NONE',NULL,'2026-07-30 11:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(269,7253,-1002763662248,'Chartoro FX Señales Gratis','Listo y agradecido por las señales',0,'NONE',NULL,'2026-07-30 12:47:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(270,7254,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4093.85

🏆**TP1**: 4096.85
🏆**TP2**: 4103.85
🏆**TP3**: 4113.85

**⛔️ Stop Loss (SL)**: 4083.85

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Price about to breakout the major resistance',1,'REGEX',NULL,'2026-07-30 13:43:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(271,7255,-1002763662248,'Chartoro FX Señales Gratis','**EL MERCADO HIZO EL PRIMER MOVIMIENTO **👀**

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**
**
**__Simplemente aceptamos la invitación __💰',0,'NONE',NULL,'2026-07-30 13:49:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(272,7256,-1002763662248,'Chartoro FX Señales Gratis','**LUEGO LLEGÓ EL IMPULSO REAL **🚀**

****#XAUUSD**** TP2 HIT, +100 Pips 🏆**
**
**__El momentum tomó el control__',0,'NONE',NULL,'2026-07-30 13:57:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(273,7257,-1002763662248,'Chartoro FX Señales Gratis','**Y LA CARRERA SE COMPLETÓ **💣**

****#XAUUSD**** TP3 HIT, +200 Pips 🏆**
**
**__Seguimiento perfecto ____👑__',0,'NONE',NULL,'2026-07-30 14:03:20.000000');
INSERT INTO "raw_telegram_messages" VALUES(274,7258,-1002763662248,'Chartoro FX Señales Gratis','🔴 Señales VIP? **DIARIAS**
🔴 Curso de trading? **CURSO DE TRADING DE 5 HORAS**
🔴 Precisión? **80%**
🔴 Soporte? **LAS 24 HORAS**

**ESCRÍBEME SI QUIERES TODO ESTO** 🔠 @SoporteChartoroFX',0,'NONE',NULL,'2026-07-30 14:25:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(275,7259,-1002763662248,'Chartoro FX Señales Gratis','**NECESITAS AYUDA CON EL TRADING?** 

👉👉 [__HAZ CLIC AQUÍ PARA RECIBIR APOYO__](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-30 17:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(276,7260,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ SI QUIERES SER RENTABLE**](https://t.me/m/q3-XLmhBNmY0) 💵💵💵',0,'NONE',NULL,'2026-07-30 19:45:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(277,7261,-1002763662248,'Chartoro FX Señales Gratis','Ya pasas horas en tu teléfono... 
Mejor haz que te pague?💸

[**HAZ CLIC AQUÍ PARA GANAR BENEFICIOS VÍA TELÉFONO**](https://t.me/m/q3-XLmhBNmY0) 📱',0,'NONE',NULL,'2026-07-30 22:50:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(278,7263,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4086
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-07-31 01:57:50.000000');
INSERT INTO "raw_telegram_messages" VALUES(279,7264,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4086
**⛔️ Stop Loss (SL): **4078

**🏆 TP1: **4089
**🏆 TP2:** 4094
**🏆 TP3:** 4102

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-31 01:59:58.000000');
INSERT INTO "raw_telegram_messages" VALUES(280,7265,-1002763662248,'Chartoro FX Señales Gratis','👀 **EL PRECIO TOCANDO LA PUERTA**',0,'NONE',NULL,'2026-07-31 02:07:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(281,7266,-1002763662248,'Chartoro FX Señales Gratis','**🔥 LOS BENEFICIOS HAN LLEGADO OTRA VEZ!**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Estructura clara, ejecución limpia, resultados reales 💰__',0,'NONE',NULL,'2026-07-31 02:10:32.000000');
INSERT INTO "raw_telegram_messages" VALUES(282,7268,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4076
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-07-31 03:02:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(283,7269,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4076
**⛔️ Stop Loss (SL): **4085

**🏆 TP1: **4073
**🏆 TP2:** 4068
**🏆 TP3:** 4060

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-07-31 03:04:18.000000');
INSERT INTO "raw_telegram_messages" VALUES(284,7270,-1002763662248,'Chartoro FX Señales Gratis','**🔥**** VAMOS EQUIPO!**',0,'NONE',NULL,'2026-07-31 03:12:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(285,7271,-1002763662248,'Chartoro FX Señales Gratis','**🔥 LOS BENEFICIOS HAN LLEGADO OTRA VEZ!**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Estructura clara, ejecución limpia, resultados reales 💰__',0,'NONE',NULL,'2026-07-31 03:13:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(286,7272,-1002763662248,'Chartoro FX Señales Gratis','🆘 QUEDA 1 CUPO PARA EL BONO DE DEPÓSITO DOBLE — **última llamada**! 🆘',0,'NONE',NULL,'2026-07-31 04:20:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(287,7273,-1002763662248,'Chartoro FX Señales Gratis','Que entrada bro👍',0,'NONE',NULL,'2026-07-31 08:52:58.000000');
INSERT INTO "raw_telegram_messages" VALUES(288,7274,-1002763662248,'Chartoro FX Señales Gratis','__BUENOS DÍAS TRADERS__

**ESTÁN LISTOS PARA UN NUEVO DÍA?** 🚀🚀🚀',0,'NONE',NULL,'2026-07-31 10:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(289,7275,-1002763662248,'Chartoro FX Señales Gratis','🔝 **VIP NO ES SOLO UNA SALA DE SEÑALES** 🔝

Es:
🔸 4–8 señales diarias de alta calidad
🔸 Un curso completo de trading
🔸 Rendimiento probado y transparente
🔸 Mentoría 24/7 cuando las decisiones realmente importan

Esa combinación es rara.
**POR ESO FUNCIONA ****✔️**',0,'NONE',NULL,'2026-07-31 13:12:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(290,7276,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4031.45

🏆**TP1**: 4034.45
🏆**TP2**: 4041.45
🏆**TP3**: 4051.45

**⛔️ Stop Loss (SL)**: 4021.45

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Same as the original idea',1,'REGEX',NULL,'2026-07-31 14:15:26.000000');
INSERT INTO "raw_telegram_messages" VALUES(291,7277,-1002763662248,'Chartoro FX Señales Gratis','**COMENZANDO EL DÍA CON MÁXIMA POTENCIA **🔥

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Reacción del precio rápida y precisa.__',0,'NONE',NULL,'2026-07-31 14:19:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(292,7278,-1002763662248,'Chartoro FX Señales Gratis','**LA TENDENCIA CONTINÚA SIN DUDAS **🚀

**#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El precio se movió de forma fluida, siguiendo perfectamente el escenario.__',0,'NONE',NULL,'2026-07-31 14:36:49.000000');
INSERT INTO "raw_telegram_messages" VALUES(293,7279,-1002763662248,'Chartoro FX Señales Gratis','**IMAGINA ATRAPAR ESTO TODOS LOS DÍAS ****👀**',0,'NONE',NULL,'2026-07-31 14:50:54.000000');
INSERT INTO "raw_telegram_messages" VALUES(294,7280,-1002763662248,'Chartoro FX Señales Gratis','**CIERRE FUERTE **👑

**#XAUUSD**** TP3 HIT, +200 Pips 🏆**

__Ejecución disciplinada + condiciones de mercado favorables = resultados máximos.__',0,'NONE',NULL,'2026-07-31 15:18:29.000000');
INSERT INTO "raw_telegram_messages" VALUES(295,7281,-1002763662248,'Chartoro FX Señales Gratis','**Casi** entraste.
**Casi **tomaste ese movimiento.
**Casi** obtuviste esa ganancia.

⚠️ **Pero “casi” no paga las cuentas** ⚠️

Lo único peor que perder es saber que ni siquiera lo intentaste, mientras otros con el mismo setup ya están ganando 🙄🙄

Decide si ya estás cansado de **CASI **ganar.
👉 [VIP GRATIS AHORA](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-07-31 16:53:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(296,7282,-1002763662248,'Chartoro FX Señales Gratis','👑  [**ACCESO VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)   👑',0,'NONE',NULL,'2026-07-31 19:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(297,7283,-1002763662248,'Chartoro FX Señales Gratis','Para ser el primer dia, en mi cuenta pequeña un 20% es un monton!
Esa señal salio como cohete! 
Gracias luis!',0,'NONE',NULL,'2026-07-31 22:15:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(298,7284,-1002763662248,'Chartoro FX Señales Gratis','**ERES PRINCIPIANTE?

OBTÉN TODOS MIS TIPS Y TRUCOS EN EL VIP Y TE CONVERTIRÁS EN UN TRADER PRO EN POCO TIEMPO **🚀🚀🚀

➡️ [**ACCESO VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-01 01:16:35.000000');
INSERT INTO "raw_telegram_messages" VALUES(299,7285,-1002763662248,'Chartoro FX Señales Gratis','Si todavía estás adivinando tus operaciones, no estás haciendo trading — **estás apostando** ❌

**Dentro del VIP, cada movimiento está calculado y respaldado por estructura.**

**EMPIEZA A APRENDER, NO A ADIVINAR **‼️',0,'NONE',NULL,'2026-08-01 04:16:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(300,7286,-1002763662248,'Chartoro FX Señales Gratis','✨  [**__HAZ CLIC AQUÍ PARA GENERAR NUEVOS INGRESOS ESTE AGOSTO__**](https://t.me/m/q3-XLmhBNmY0)  ✨',0,'NONE',NULL,'2026-08-01 07:22:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(301,7288,-1002763662248,'Chartoro FX Señales Gratis','❓ __Cómo va tu trading hasta ahora?__',0,'NONE',NULL,'2026-08-01 11:45:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(302,7289,-1002763662248,'Chartoro FX Señales Gratis','🏆 **EL VIP INCLUYE:**

✔️ De 4 a 8 señales diarias de trading de alta calidad
✔️ Curso completo de trading
✔️ Guía completa A-a-Z para construir bases sólidas
✔️ Rendimiento comprobado de las señales basado en resultados reales
✔️ Soporte y mentoría 24/7

**QUÉ MÁS PODRÍAS PEDIR** **⁉️****⁉️**
 
🚀 [**RECLAMA TU ACCESO AL VIP AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 🚀',0,'NONE',NULL,'2026-08-01 13:45:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(303,7290,-1002763662248,'Chartoro FX Señales Gratis','🏆🏆**LOS NUEVOS MIEMBROS VIP YA ESTÁN REVISANDO MIS MATERIALES…**

Cómo se ven tus planes para el sábado?? 🤔🤔',0,'NONE',NULL,'2026-08-01 15:33:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(304,7291,-1002763662248,'Chartoro FX Señales Gratis','Si llevas meses operando pero todavía te cuesta ser rentable...

**ESTA ES TU SEÑAL PARA SUBIR DE NIVEL EN EL VIP** 💰💰💰',0,'NONE',NULL,'2026-08-01 17:35:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(305,7294,-1002763662248,'Chartoro FX Señales Gratis','❌ __Las señales no esperan.
____❌__ __Las oportunidades no esperan.
____❌__ __El crecimiento no espera.__

Lo único que está en pausa ahora mismo… eres tú  🫵

**QUITA LA PAUSA** 

Envíame un mensaje y te guío para empezar antes de que llegue el lunes 👉 @SoporteChartoroFX 🏆',0,'NONE',NULL,'2026-08-01 21:37:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(306,7295,-1002763662248,'Chartoro FX Señales Gratis','Luis de verdad que Dios lo bendiga mucho, me siento súper feliz es la primera operación y ya gané $61 apenas iniciando',0,'NONE',NULL,'2026-08-01 23:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(307,7296,-1002763662248,'Chartoro FX Señales Gratis','[**TOCA PARA OBTENER LOS BENEFICIOS VIP**](https://t.me/m/q3-XLmhBNmY0) 👑',0,'NONE',NULL,'2026-08-02 00:05:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(308,7297,-1002763662248,'Chartoro FX Señales Gratis','**3 hábitos que todo trader rentable tiene:**

👉 Aparecen incluso cuando es aburrido.
📚 Estudian lo que otros pasan por alto.
⚡ Actúan mientras los demás dudan.

Esa es la diferencia entre mirar gráficos y sacar ganancias reales 👀💰

💸 El fin de semana casi termina — decide cuál eres tú.


🔽    🔽    🔽    🔽    🔽

[ACCESO VIP GRATIS AQUÍ](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-02 02:37:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(309,7298,-1002763662248,'Chartoro FX Señales Gratis','💎 **SEÑALES VIP GRATIS
****💎**** MATERIAL EDUCATIVO GRATIS
****💎**** MENTORÍA GRATIS**

🏆[** RECLAMA AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-08-02 03:44:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(310,7300,-1002763662248,'Chartoro FX Señales Gratis','❓ **QUIERES GUÍA GRATUITA?**',0,'NONE',NULL,'2026-08-02 11:10:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(311,7301,-1002763662248,'Chartoro FX Señales Gratis','Es domingo 🍀

O te unes al **VIP GRATIS** y usas el material para llegar preparado al lunes…
o no haces nada y el mercado te agarra igual 

**TU ELECCIÓN** 🫵',0,'NONE',NULL,'2026-08-02 12:23:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(312,7302,-1002763662248,'Chartoro FX Señales Gratis','**POR QUÉ CONFORMARSE CON 1-2 SEÑALES AL DÍA CUANDO PUEDES TENER 4-8 DIARIAS?**',0,'NONE',NULL,'2026-08-02 13:21:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(313,7303,-1002763662248,'Chartoro FX Señales Gratis','**ASÍ ES COMO LOS MIEMBROS VIP SE MANTIENEN EN LA CIMA:**

✔️ 4–8 señales premium todos los días
✔️ Profundizando en el curso completo de trading de 5 horas
✔️ Señales confiables con 80% de efectividad
✔️ Soporte 24/7 para que nunca te quedes solo

🟢 [**HAZ CLIC AQUÍ PARA RECLAMAR TODOS LOS BENEFICIOS VIP **](https://t.me/m/q3-XLmhBNmY0)🟢',0,'NONE',NULL,'2026-08-02 14:29:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(314,7304,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA UNIRTE AL VIP ANTES DE QUE ABRA EL MERCADO**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-08-02 16:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(315,7305,-1002763662248,'Chartoro FX Señales Gratis','❓ **QUIERES CONVERTIR EL TRADING EN INGRESOS CONSISTENTES?**',0,'NONE',NULL,'2026-08-02 17:36:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(316,7306,-1002763662248,'Chartoro FX Señales Gratis','**LO ÚNICO QUE NECESITAS ES:

****💬**** TU CELULAR
****🌐**** INTERNET
****⏱️**** 3 MINUTOS PARA COPIAR Y PEGAR**',0,'NONE',NULL,'2026-08-02 18:22:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(317,7307,-1002763662248,'Chartoro FX Señales Gratis','📈 [**APRENDE A HACER TRADING AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 📈',0,'NONE',NULL,'2026-08-02 19:40:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(318,7308,-1002763662248,'Chartoro FX Señales Gratis','Es fácil dudar desde afuera.
Pero cuando entras al VIP, ves la diferencia: 
✔️ **señales reales**
✔️ **análisis reales**
✔️ **resultados reales** 

 🟢 [**SÉ PARTE DEL VIP**](https://t.me/m/q3-XLmhBNmY0) 🟢',0,'NONE',NULL,'2026-08-02 20:20:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(319,7309,-1002763662248,'Chartoro FX Señales Gratis','[**TOCA AQUÍ PARA OBTENER SEÑALES VIP**](https://t.me/m/q3-XLmhBNmY0)  👑',0,'NONE',NULL,'2026-08-02 21:15:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(320,7310,-1002763662248,'Chartoro FX Señales Gratis','**Quién entra? **
👑 @SoporteChartoroFX',0,'NONE',NULL,'2026-08-02 22:44:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(321,7311,-1002763662248,'Chartoro FX Señales Gratis','Luis, entre un poco o tarde, pero salí en verde, gracias ✌🏻',0,'NONE',NULL,'2026-08-02 23:35:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(322,7313,-1002763662248,'Chartoro FX Señales Gratis','Súper!!',0,'NONE',NULL,'2026-08-03 00:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(323,7314,-1002763662248,'Chartoro FX Señales Gratis','Voy x el tp3',0,'NONE',NULL,'2026-08-03 00:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(324,7315,-1002763662248,'Chartoro FX Señales Gratis','Foto de DAN ROBERT',0,'NONE',NULL,'2026-08-03 00:31:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(325,7316,-1002763662248,'Chartoro FX Señales Gratis','Mi Resultado de hoy . Gracias ChartoroFax',0,'NONE',NULL,'2026-08-03 00:31:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(326,7317,-1002763662248,'Chartoro FX Señales Gratis','🔼**HAS VISTO TODAS LAS GANANCIAS QUE MI VIP ME ENVIÓ ARRIBA?**

**TÚ TAMBIÉN PUEDES GANAR ESO!** 🫵

👉 [**OBTÉN SEÑALES VIP AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-08-03 01:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(327,7318,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4060
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-03 01:02:32.000000');
INSERT INTO "raw_telegram_messages" VALUES(328,7319,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4060
**⛔️ Stop Loss (SL): **4052

**🏆 TP1: **4063
**🏆 TP2:** 4068
**🏆 TP3:** 4076

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-03 01:04:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(329,7320,-1002763662248,'Chartoro FX Señales Gratis','**❌ SL HIT**

Darle más espacio a la operación no ayudó esta vez.

No pasa nada — seguiré buscando una nueva configuración clara 🔎

Manténganse pacientes, equipo. Operamos con inteligencia, no con prisas. ✅',0,'NONE',NULL,'2026-08-03 01:18:41.000000');
INSERT INTO "raw_telegram_messages" VALUES(330,7321,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4056
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-03 01:36:51.000000');
INSERT INTO "raw_telegram_messages" VALUES(331,7322,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4056
**⛔️ Stop Loss (SL): **4048

**🏆 TP1: **4059
**🏆 TP2:** 4064
**🏆 TP3:** 4072

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-03 01:38:16.000000');
INSERT INTO "raw_telegram_messages" VALUES(332,7323,-1002763662248,'Chartoro FX Señales Gratis','Move SL to 4046',1,'REGEX',NULL,'2026-08-03 01:41:52.000000');
INSERT INTO "raw_telegram_messages" VALUES(333,7324,-1002763662248,'Chartoro FX Señales Gratis','**AHÍ VAMOOOOS! **🚀',0,'NONE',NULL,'2026-08-03 02:01:47.000000');
INSERT INTO "raw_telegram_messages" VALUES(334,7325,-1002763662248,'Chartoro FX Señales Gratis','**ESTAMOS DE VUELTA EN EL CAMINO ****💥****💥**

**#XAUUSD**** TP1 HIT, +30 Pips ****🏆**

En camino a la recuperación, chicos — **NO LOS VOY A DECEPCIONAR ****❤️‍🩹**',0,'NONE',NULL,'2026-08-03 02:03:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(335,7326,-1002763662248,'Chartoro FX Señales Gratis','**🚀**** LA TENDENCIA ESTÁ CUMPLIENDO!

****#XAUUSD**** TP2 HIT, +80 Pips 🏆
**
__El impulso está haciendo el trabajo.__',0,'NONE',NULL,'2026-08-03 02:51:31.000000');
INSERT INTO "raw_telegram_messages" VALUES(336,7327,-1002763662248,'Chartoro FX Señales Gratis','HAY QUE AMAR ESOS BLUES! 💙',0,'NONE',NULL,'2026-08-03 03:38:35.000000');
INSERT INTO "raw_telegram_messages" VALUES(337,7328,-1002763662248,'Chartoro FX Señales Gratis','⬇️         ⬇️         ⬇️         ⬇️         ⬇️

                   **   **[**VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-03 03:41:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(338,7329,-1002763662248,'Chartoro FX Señales Gratis','**🚨**** LOS OBJETIVOS ESTÁN CADA VEZ MÁS CERCA**',0,'NONE',NULL,'2026-08-03 04:49:50.000000');
INSERT INTO "raw_telegram_messages" VALUES(339,7330,-1002763662248,'Chartoro FX Señales Gratis','**🤯**** QUÉ RECORRIDO!

****#XAUUSD**** TP3 HIT, +160 Pips 🏆**

__Directo desde la entrada hasta el objetivo final__',0,'NONE',NULL,'2026-08-03 04:52:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(340,7331,-1002763662248,'Chartoro FX Señales Gratis','**Y ASÍ ES COMO LO HACEMOS EN EL VIP** 🔥

__QUÉ ESTÁS ESPERANDO?__
[**ÚNETE AHORA **](https://t.me/m/q3-XLmhBNmY0)🚀',0,'NONE',NULL,'2026-08-03 05:06:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(341,7332,-1002763662248,'Chartoro FX Señales Gratis','[**ENTRA AL VIP ANTES DE QUE SALGA LA PRÓXIMA SEÑAL**](https://t.me/m/q3-XLmhBNmY0) 🚨🚨',0,'NONE',NULL,'2026-08-03 06:02:54.000000');
INSERT INTO "raw_telegram_messages" VALUES(342,7334,-1002763662248,'Chartoro FX Señales Gratis','**YA TIENES UN MENTOR DE TRADING****❓**',0,'NONE',NULL,'2026-08-03 11:30:42.000000');
INSERT INTO "raw_telegram_messages" VALUES(343,7335,-1002763662248,'Chartoro FX Señales Gratis','__No solo recibes señales y transparencia...__

**TAMBIÉN OBTIENES MI MENTORÍA Y MATERIAL EDUCATIVO QUE TE AYUDARÁN AL 100% A CONVERTIRTE EN UN MEJOR TRADER, SIN IMPORTAR QUÉ!** 📈📈📈**
**
[**HAZ CLIC AQUÍ PARA SABER MÁS**](https://t.me/m/q3-XLmhBNmY0) ⚡️',0,'NONE',NULL,'2026-08-03 12:20:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(344,7336,-1002763662248,'Chartoro FX Señales Gratis','Mi profit hoy',0,'NONE',NULL,'2026-08-03 12:59:16.000000');
INSERT INTO "raw_telegram_messages" VALUES(345,7337,-1002763662248,'Chartoro FX Señales Gratis','Muchas gracias excelente señal',0,'NONE',NULL,'2026-08-03 13:15:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(346,7338,-1002763662248,'Chartoro FX Señales Gratis','**QUIERES VER LOS RESULTADOS DE LA SEMANA PASADA?** 💯',0,'NONE',NULL,'2026-08-03 13:25:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(347,7339,-1002763662248,'Chartoro FX Señales Gratis','__Ya publiqué una señal en el grupo VIP!__

[**HAZ CLIC AQUÍ PARA VERLA**](https://t.me/m/q3-XLmhBNmY0) 👀',0,'NONE',NULL,'2026-08-03 13:56:22.000000');
INSERT INTO "raw_telegram_messages" VALUES(348,7340,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4032.78

🏆**TP1**: 4035.78
🏆**TP2**: 4042.78
🏆**TP3**: 4052.78

**⛔️ Stop Loss (SL)**: 4022.78

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__
...',1,'REGEX',NULL,'2026-08-03 13:59:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(349,7341,-1002763662248,'Chartoro FX Señales Gratis','**EL ORO SE MOVIÓ LIMPIO 😎

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Sin estrés, solo ganancias ____💰__',0,'NONE',NULL,'2026-08-03 14:04:42.000000');
INSERT INTO "raw_telegram_messages" VALUES(350,7342,-1002763662248,'Chartoro FX Señales Gratis','⚡️⚡️⚡️',0,'NONE',NULL,'2026-08-03 14:05:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(351,7343,-1002763662248,'Chartoro FX Señales Gratis','**Para quién es el VIP?**

Para cualquiera listo para:
✅ Copiar señales reales
✅Aprender mientras gana
✅Operar con confianza',0,'NONE',NULL,'2026-08-03 14:29:35.000000');
INSERT INTO "raw_telegram_messages" VALUES(352,7344,-1002763662248,'Chartoro FX Señales Gratis','📈** RESULTADOS SEMANALES DE SEÑALES** 📈
__27 de Julio – 31 de Julio, 2026__

💰 TOTAL: **+1153 PIPS GANADOS** 💰

✔️ Win Ratio: 85% (16 ganadas / 3 perdidas)
✔️ Operaciones totales: 19 setups
✔️ Buy vs Sell: 10 compras / 9 ventas
✔️ XAUUSD volvió a ser el activo con mejor rendimiento durante la semana
✔️ Lunes (+401 pips), jueves (+325 pips) y viernes (+260 pips) lideraron las ganancias
✔️ Otra semana consistente aprovechando las mejores oportunidades del mercado FOREX y GOLD

🤑 **QUÉ SIGNIFICA ESTO EN DINERO REAL?**

• 0.01 lote → ~$11.53 USD
• 0.10 lote → ~$115.30 USD
• 1.00 lote → ~**$1,153+ USD EN UNA SEMANA**

🔥 **+1153 PIPS EN SOLO UNA SEMANA**

**ÚNETE AL GRUPO VIP Y NO TE PIERDAS LA PRÓXIMA SEÑAL**  💰',0,'NONE',NULL,'2026-08-03 15:10:58.000000');
INSERT INTO "raw_telegram_messages" VALUES(353,7346,-1002763662248,'Chartoro FX Señales Gratis','**TE PERDISTE +1,153 PIPS EN SOLO UNA SEMANA LA SEMANA PASADA** 🤯🤯🤯',0,'NONE',NULL,'2026-08-03 15:22:54.000000');
INSERT INTO "raw_telegram_messages" VALUES(354,7347,-1002763662248,'Chartoro FX Señales Gratis','**NUEVA SEÑAL EN EL VIP RECIÉN PUBLICADA!** 🤫',0,'NONE',NULL,'2026-08-03 15:29:25.000000');
INSERT INTO "raw_telegram_messages" VALUES(355,7348,-1002763662248,'Chartoro FX Señales Gratis','⚡️ [**RECLAMA UN LUGAR VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0) ⚡️',0,'NONE',NULL,'2026-08-03 16:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(356,7349,-1002763662248,'Chartoro FX Señales Gratis','__Yo también fui principiante alguna vez, **así que te entiendo...**__

**MÁNDAME UN DM Y CON GUSTO TE GUÍO EN TU CAMINO COMO TRADER** ➡️ [@SoporteChartoroFX](https://t.me/SoporteChartoroFX)',0,'NONE',NULL,'2026-08-03 18:22:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(357,7350,-1002763662248,'Chartoro FX Señales Gratis','**LA ESTRUCTURA A NUESTRO FAVOR, LAS GANANCIAS FLUYEN! 📊

****#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El mercado se movió según lo planeado. Sin ruido, sin dudas, solo una ejecución limpia.__',0,'NONE',NULL,'2026-08-03 18:53:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(358,7351,-1002763662248,'Chartoro FX Señales Gratis','**INICIO FUERTE DE LA SEMANA! **💰

**#XAUUSD**** TP3 HIT, +200 Pips 🏆**

__Movimiento limpio, resultados impresionantes __🚀',0,'NONE',NULL,'2026-08-03 19:26:51.000000');
INSERT INTO "raw_telegram_messages" VALUES(359,7352,-1002763662248,'Chartoro FX Señales Gratis','⚡** SEÑALES VIP GRATIS

****📕**** MATERIAL EDUCATIVO GRATIS

**🧠** MENTORÍA GRATIS**


👉 [** RECLAMA AQUÍ 👈**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-03 20:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(360,7353,-1002763662248,'Chartoro FX Señales Gratis','**🔈 Ganancias con señales y aprendizaje a través de materiales educativos y mentoría

ESO ES LO QUE OBTIENES DENTRO DEL **[**VIP**](https://t.me/m/q3-XLmhBNmY0)  👑',0,'NONE',NULL,'2026-08-03 22:24:36.000000');
INSERT INTO "raw_telegram_messages" VALUES(361,7354,-1002763662248,'Chartoro FX Señales Gratis','**PODRÍAS HABER GANADO $1,153 LA SEMANA PASADA SI HUBIERAS ESTADO EN EL VIP** ⚠️',0,'NONE',NULL,'2026-08-03 22:35:18.000000');
INSERT INTO "raw_telegram_messages" VALUES(362,7355,-1002763662248,'Chartoro FX Señales Gratis','ⓘ[__ Luis te mencionó__](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-03 22:44:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(363,7357,-1002763662248,'Chartoro FX Señales Gratis','Mis ganancias del día de hoy , cerré antes pero fueron ganancias , gracias por tus señales amigo',0,'NONE',NULL,'2026-08-03 23:16:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(364,7358,-1002763662248,'Chartoro FX Señales Gratis','Ahí vamos amigo Luis, paso a paso',0,'NONE',NULL,'2026-08-03 23:40:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(365,7359,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA GANAR COMO ELLOS**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-08-04 00:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(366,7360,-1002763662248,'Chartoro FX Señales Gratis','**COPIAR** ➡️  **PEGAR**  **➡️****GANAR**',0,'NONE',NULL,'2026-08-04 01:10:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(367,7361,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4060
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-04 01:57:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(368,7362,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#SELL ** **

** Entry Point: **4060
**⛔️ Stop Loss (SL): **4068

**🏆 TP1: **4057
**🏆 TP2:** 4052
**🏆 TP3:** 4044

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-04 01:58:56.000000');
INSERT INTO "raw_telegram_messages" VALUES(369,7363,-1002763662248,'Chartoro FX Señales Gratis','**PRIMER TOQUE EN CAMINO ****🔥**',0,'NONE',NULL,'2026-08-04 02:05:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(370,7364,-1002763662248,'Chartoro FX Señales Gratis','**EL ORO VINO A DOMINAR **😎🔥

**#XAUUSD**** TP1 HIT, +30 Pips 🏆
**
__Ganancia fácil ____💰__',0,'NONE',NULL,'2026-08-04 02:07:53.000000');
INSERT INTO "raw_telegram_messages" VALUES(371,7366,-1002763662248,'Chartoro FX Señales Gratis','Hace unos días esta fue mi ganancia, en un solo día 💪🏻',0,'NONE',NULL,'2026-08-04 03:25:47.000000');
INSERT INTO "raw_telegram_messages" VALUES(372,7367,-1002763662248,'Chartoro FX Señales Gratis','💎 [**HAZ CLIC AQUÍ PARA RECIBIR DE 4 A 8 SEÑALES VIP DIARIAS**](https://t.me/m/q3-XLmhBNmY0) 💎',0,'NONE',NULL,'2026-08-04 03:30:41.000000');
INSERT INTO "raw_telegram_messages" VALUES(373,7368,-1002763662248,'Chartoro FX Señales Gratis','**LA PRESIÓN ESTÁ AUMENTANDO…**',0,'NONE',NULL,'2026-08-04 04:02:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(374,7369,-1002763662248,'Chartoro FX Señales Gratis','**MOMENTUM DESATADO 🚀**

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__Movimiento limpio, sin retrocesos__',0,'NONE',NULL,'2026-08-04 04:05:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(375,7371,-1002763662248,'Chartoro FX Señales Gratis','**VAMOS TRADERSSSS **⚡️',0,'NONE',NULL,'2026-08-04 04:11:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(376,7372,-1002763662248,'Chartoro FX Señales Gratis','Copiar ➕Pegar 🟰 **GANAR DINERO** 💰💰💰

👉 [**HAZ CLIC AQUÍ PARA OBTENER GANANCIAS**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-08-04 05:29:56.000000');
INSERT INTO "raw_telegram_messages" VALUES(377,7373,-1002763662248,'Chartoro FX Señales Gratis','👏✅',0,'NONE',NULL,'2026-08-04 09:17:36.000000');
INSERT INTO "raw_telegram_messages" VALUES(378,7374,-1002763662248,'Chartoro FX Señales Gratis','**BUENOS DÍAS TRADERS! **🚀
__Pudieron aprovechar las señales de ayer?__',0,'NONE',NULL,'2026-08-04 10:10:20.000000');
INSERT INTO "raw_telegram_messages" VALUES(379,7375,-1002763662248,'Chartoro FX Señales Gratis','**ESTÁN LISTOS PARA MÁS HOY?** 💯',0,'NONE',NULL,'2026-08-04 10:18:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(380,7376,-1002763662248,'Chartoro FX Señales Gratis','🏆 **DENTRO DEL VIP** 🏆

👉 4–8 señales diarias
👉 un curso de trading paso a paso
👉 mentoría a demanda

💰 [**RECLAMA LOS BENEFICIOS VIP AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 💰',0,'NONE',NULL,'2026-08-04 12:10:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(381,7377,-1002763662248,'Chartoro FX Señales Gratis','⚠️ **EL VIP NO ES SOLO PARA PRINCIPIANTES** ⚠️

Esto también es para:
Traders **CANSADOS DE PERDER** y traders que quieren **LLEVAR SU NIVEL AL MÁXIMO**  🌡

**📊** [**HAZ CLIC AQUÍ PARA CAMBIAR TU JUEGO**](https://t.me/m/q3-XLmhBNmY0) **📊**',0,'NONE',NULL,'2026-08-04 13:02:47.000000');
INSERT INTO "raw_telegram_messages" VALUES(382,7378,-1002763662248,'Chartoro FX Señales Gratis','🙌🏻🙏',0,'NONE',NULL,'2026-08-04 13:24:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(383,7379,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4079.81

🏆**TP1**: 4082.81
🏆**TP2**: 4089.81
🏆**TP3**: 4099.81

**⛔️ Stop Loss (SL)**: 4069.81

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Same as the original idea',1,'REGEX',NULL,'2026-08-04 13:27:37.000000');
INSERT INTO "raw_telegram_messages" VALUES(384,7380,-1002763662248,'Chartoro FX Señales Gratis','**EL PRIMER MOVIMIENTO DE LA SESIÓN SE CUMPLIÓ **⚡️

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__El oro reaccionó justo desde ese nivel.__',0,'NONE',NULL,'2026-08-04 13:32:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(385,7381,-1002763662248,'Chartoro FX Señales Gratis','**EL MERCADO SIGUIÓ EMPUJANDO **🚀

**#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El trade fluyó exactamente como lo habíamos planeado.__',0,'NONE',NULL,'2026-08-04 13:42:32.000000');
INSERT INTO "raw_telegram_messages" VALUES(386,7382,-1002763662248,'Chartoro FX Señales Gratis','Que entrada bro👍',0,'NONE',NULL,'2026-08-04 14:16:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(387,7383,-1002763662248,'Chartoro FX Señales Gratis','**__Aquí en Chartoro, estás bien atendido.__** **Y lo más importante, VERÁS POR TI MISMO QUE UN WIN RATE DEL 70 AL 80% ES REALMENTE ALCANZABLE, no solo palabras**  🥂',0,'NONE',NULL,'2026-08-04 15:09:41.000000');
INSERT INTO "raw_telegram_messages" VALUES(388,7384,-1002763662248,'Chartoro FX Señales Gratis','💵⭐️ [**TOCA AQUÍ PARA CAMBIAR TU VIDA PARA MEJOR**](https://t.me/m/q3-XLmhBNmY0) ⭐️💵',0,'NONE',NULL,'2026-08-04 15:35:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(389,7385,-1002763662248,'Chartoro FX Señales Gratis','Mira bro esta ganancia en mi cuenta de 100',0,'NONE',NULL,'2026-08-04 16:04:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(390,7386,-1002763662248,'Chartoro FX Señales Gratis','Mi primera operación🥳 muchas gracias Luis 🤩',0,'NONE',NULL,'2026-08-04 16:12:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(391,7387,-1002763662248,'Chartoro FX Señales Gratis','**FINALIZANDO FUERTE! ****💎**

**#XAUUSD**** TP3 HIT, +200 Pips ****🏆**

__Estructura respetada de inicio a fin. Así es como operamos.__',0,'NONE',NULL,'2026-08-04 17:06:47.000000');
INSERT INTO "raw_telegram_messages" VALUES(392,7389,-1002763662248,'Chartoro FX Señales Gratis','Vamos mejorando',0,'NONE',NULL,'2026-08-04 22:20:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(393,7390,-1002763662248,'Chartoro FX Señales Gratis','Estamos por buen camino',0,'NONE',NULL,'2026-08-04 22:20:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(394,7391,-1002763662248,'Chartoro FX Señales Gratis','Gracias de verdad',0,'NONE',NULL,'2026-08-04 22:20:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(395,7392,-1002763662248,'Chartoro FX Señales Gratis','**QUÉ OTRA PRUEBA NECESITAS?**
**LA GENTE EN EL VIP ESTÁ GANANDO POR TODAS PARTES**  💵💵💵',0,'NONE',NULL,'2026-08-04 22:28:19.000000');
INSERT INTO "raw_telegram_messages" VALUES(396,7393,-1002763662248,'Chartoro FX Señales Gratis','⏳ [**RECLAMA AQUÍ EL ÚLTIMO CUPO VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-04 23:05:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(397,7394,-1002763662248,'Chartoro FX Señales Gratis','**__Te preguntas cómo unirte al VIP?__**
**__Te preguntas cómo funcionan las señales?__**
**__Te preguntas qué recibes dentro?__**

‼️ **ENTONCES PREGUNTA** ‼️

Quedarte callado es la forma más rápida de quedarte afuera 🙄🙄

Envíame un mensaje para poder ayudarte 👉@SoporteChartoroFX',0,'NONE',NULL,'2026-08-05 00:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(398,7395,-1002763662248,'Chartoro FX Señales Gratis','**2 NUEVOS MIEMBROS VIP ACABAN DE ELEGIR GANAR INGRESOS ADICIONALES MEDIANTE EL TRADING. VAMOS!** 🤑🤑🤑',0,'NONE',NULL,'2026-08-05 01:01:42.000000');
INSERT INTO "raw_telegram_messages" VALUES(399,7396,-1002763662248,'Chartoro FX Señales Gratis','🚨 **BUSCANDO 5 TRADERS PRINCIPIANTES → **[**ACCESO VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 💥',0,'NONE',NULL,'2026-08-05 01:28:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(400,7397,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4097
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-05 02:06:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(401,7398,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point:** 4097
**⛔️ Stop Loss (SL): **4089

**🏆 TP1: **4100
**🏆 TP2:** 4105
**🏆 TP3:** 4113

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-05 02:08:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(402,7399,-1002763662248,'Chartoro FX Señales Gratis','**MODO MERCADO: EN LLAMAS! ****🔥**

**#XAUUSD**** TP1 HIT, +30 Pips ****🏆**

__Breakout válido, timing perfecto, ganancia inmediata.__',0,'NONE',NULL,'2026-08-05 02:13:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(403,7402,-1002763662248,'Chartoro FX Señales Gratis','👌👌👌👌',0,'NONE',NULL,'2026-08-05 02:15:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(404,7403,-1002763662248,'Chartoro FX Señales Gratis','**MOVIÉNDONOS AL SIGUIENTE OBJETIVO ****🚀**',0,'NONE',NULL,'2026-08-05 02:27:41.000000');
INSERT INTO "raw_telegram_messages" VALUES(405,7404,-1002763662248,'Chartoro FX Señales Gratis','**TENDENCIA BAJO CONTROL ****📈**

**#XAUUSD**** TP2 HIT, +80 Pips ****🏆**

__El precio se movió limpio según lo planeado. La disciplina paga.__',0,'NONE',NULL,'2026-08-05 02:30:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(406,7406,-1002763662248,'Chartoro FX Señales Gratis','**EL OBJETIVO FINAL NOS ESPERA ****🎯**',0,'NONE',NULL,'2026-08-05 02:37:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(407,7408,-1002763662248,'Chartoro FX Señales Gratis','**FINALIZANDO FUERTE! ****💎**

**#XAUUSD**** TP3 HIT, +160 Pips ****🏆**

__Estructura respetada de inicio a fin. Así es como operamos.__',0,'NONE',NULL,'2026-08-05 02:40:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(408,7409,-1002763662248,'Chartoro FX Señales Gratis','**Las ganancias siguen llegando, ESTAMOS EN LLAMAS! ****🔥**
**🟠**** **[**HAZ CLIC AQUÍ PARA UNIRTE AHORA**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-05 02:55:52.000000');
INSERT INTO "raw_telegram_messages" VALUES(409,7410,-1002763662248,'Chartoro FX Señales Gratis','Quiero compartir esto Luis! Todo empezó por tí y tú guía y consejos. Esto en una semana siguiéndote',0,'NONE',NULL,'2026-08-05 03:26:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(410,7411,-1002763662248,'Chartoro FX Señales Gratis','**MIRA TODO LO QUE TE ESTÁS PERDIENDO **🔝',0,'NONE',NULL,'2026-08-05 03:29:44.000000');
INSERT INTO "raw_telegram_messages" VALUES(411,7412,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA RECIBIR SEÑALES DE ÉXITO**](https://t.me/m/q3-XLmhBNmY0)** **💵💵💵',0,'NONE',NULL,'2026-08-05 03:45:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(412,7415,-1002763662248,'Chartoro FX Señales Gratis','__Te gustaría operar con confianza utilizando señales profesionales__ ❓',0,'NONE',NULL,'2026-08-05 11:02:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(413,7416,-1002763662248,'Chartoro FX Señales Gratis','__Yo también fui principiante alguna vez, **así que te entiendo...**__

**MÁNDAME UN DM Y CON GUSTO TE GUÍO EN TU CAMINO COMO TRADER** ➡️ @[SoporteChartoroFX](https://t.me/SoporteChartoroFX)',0,'NONE',NULL,'2026-08-05 12:03:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(414,7417,-1002763662248,'Chartoro FX Señales Gratis','💥 4–8 señales de alta calidad diarias
💥 Curso completo de trading
💥 Resultados y ganancias respaldados por rendimiento
💥 Soporte 24/7 cuando lo necesites

‼️ [**HAZ CLIC AQUÍ PARA ASEGURAR TU CUPO**](https://t.me/m/q3-XLmhBNmY0)  ‼️',0,'NONE',NULL,'2026-08-05 13:02:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(415,7418,-1002763662248,'Chartoro FX Señales Gratis','Muchas gracias excelente señal',0,'NONE',NULL,'2026-08-05 14:04:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(416,7419,-1002763662248,'Chartoro FX Señales Gratis','**PODRÍAS HABER GANADO MÁS DE $1,153 USD LA SEMANA PASADA!** 💰📈',0,'NONE',NULL,'2026-08-05 14:08:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(417,7420,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA GENERAR GANANCIAS ESTA SEMANA**](https://t.me/m/q3-XLmhBNmY0) 🤑🤑🤑',0,'NONE',NULL,'2026-08-05 14:12:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(418,7421,-1002763662248,'Chartoro FX Señales Gratis','**YA PUBLIQUÉ 2 SEÑALES EN EL **[**VIP**](https://t.me/m/q3-XLmhBNmY0)** ****‼️****‼️****‼️**',0,'NONE',NULL,'2026-08-05 15:50:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(419,7422,-1002763662248,'Chartoro FX Señales Gratis','**POR QUÉ CONFORMARSE CON 1-2 SEÑALES AL DÍA CUANDO PUEDES TENER 4-8 DIARIAS?** 🤯🤯🤯🤯',0,'NONE',NULL,'2026-08-05 15:52:41.000000');
INSERT INTO "raw_telegram_messages" VALUES(420,7423,-1002763662248,'Chartoro FX Señales Gratis','**YA ESTAMOS LLEGANDO A LOS TP!!
TE LO ESTÁS PERDIENDO AHORA MISMO** 💸💸',0,'NONE',NULL,'2026-08-05 16:00:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(421,7425,-1002763662248,'Chartoro FX Señales Gratis','__No solo recibes señales y transparencia...__

**TAMBIÉN OBTIENES MI MENTORÍA Y MATERIAL EDUCATIVO QUE TE AYUDARÁN AL 100% A CONVERTIRTE EN UN MEJOR TRADER, SIN IMPORTAR QUÉ!** 📈📈📈**
**
[**HAZ CLIC AQUÍ PARA SABER MÁS**](https://t.me/m/q3-XLmhBNmY0) ⚡️',0,'NONE',NULL,'2026-08-05 18:03:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(422,7426,-1002763662248,'Chartoro FX Señales Gratis','Muchas gracias luis!! Un dia excelente',0,'NONE',NULL,'2026-08-05 23:51:49.000000');
INSERT INTO "raw_telegram_messages" VALUES(423,7427,-1002763662248,'Chartoro FX Señales Gratis','Buenos días, queria agradecerle con las señales, de momento me fue bien ayer con el oro',0,'NONE',NULL,'2026-08-06 00:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(424,7429,-1002763662248,'Chartoro FX Señales Gratis','En 5 días. ¡Eres muy grande!',0,'NONE',NULL,'2026-08-06 00:16:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(425,7430,-1002763662248,'Chartoro FX Señales Gratis','⤴️ **QUIERES GANAR ESO TAMBIÉN?** 🤑🤑🤑',0,'NONE',NULL,'2026-08-06 00:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(426,7431,-1002763662248,'Chartoro FX Señales Gratis','⚡️ [**HAZ CLIC AQUÍ ANTES DE QUE SALGA LA PRÓXIMA SEÑAL**](https://t.me/m/q3-XLmhBNmY0) ⚡️',0,'NONE',NULL,'2026-08-06 00:25:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(427,7432,-1002763662248,'Chartoro FX Señales Gratis','**NECESITAS AYUDA CON EL TRADING?** 📈📈

👉👉 [__HAZ CLIC AQUÍ PARA RECIBIR APOYO__](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-06 01:13:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(428,7433,-1002763662248,'Chartoro FX Señales Gratis','En 5 días. ¡Eres muy grande!',0,'NONE',NULL,'2026-08-06 01:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(429,7434,-1002763662248,'Chartoro FX Señales Gratis','Nuestros miembros están obteniendo entre $200 y $1,000 POR DÍA — lo has visto tú mismo! 💰🔥

 **COPIA, PEGA Y GANA **✔️✔️',0,'NONE',NULL,'2026-08-06 01:40:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(430,7435,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4288
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-06 01:48:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(431,7436,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4288
**⛔️ Stop Loss (SL): **4280

**🏆 TP1: **4291
**🏆 TP2:** 4296
**🏆 TP3:** 4304

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-06 01:49:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(432,7437,-1002763662248,'Chartoro FX Señales Gratis','**VAMOOOOSSSS ORROOOO** 🚀

#XAUUSD **TP1 HIT, +30 Pips** 🏆
#XAUUSD **TP2 HIT, +80 Pips** 🏆',0,'NONE',NULL,'2026-08-06 01:55:24.000000');
INSERT INTO "raw_telegram_messages" VALUES(433,7438,-1002763662248,'Chartoro FX Señales Gratis','**LETSGOOOOO** 🍾🍾

#XAUUSD **TP3 Hit, +160 Pips **🏆',0,'NONE',NULL,'2026-08-06 02:07:20.000000');
INSERT INTO "raw_telegram_messages" VALUES(434,7439,-1002763662248,'Chartoro FX Señales Gratis','**VISTE EL TRADE?**

Dale a ❤️
👇',0,'NONE',NULL,'2026-08-06 02:11:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(435,7440,-1002763662248,'Chartoro FX Señales Gratis','__TE GUSTA LO QUE ESTÁS OBTENIENDO AQUÍ?__
**DISFRUTA DE AÚN MÁS GANANCIAS EN EL **[**VIP**](https://t.me/m/q3-XLmhBNmY0)** **🤑🤑🤑',0,'NONE',NULL,'2026-08-06 02:33:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(436,7441,-1002763662248,'Chartoro FX Señales Gratis','**UN GRAN COMIENZO PARA UN AGOSTO PRÓSPERO PARA LOS TRADERS DE CHARTOROFX **💫💫',0,'NONE',NULL,'2026-08-06 03:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(437,7442,-1002763662248,'Chartoro FX Señales Gratis','❌ **Operar solo convierte pequeños errores en lecciones caras.** ❌

Operar con orientación los convierte en correcciones rápidas ✔️✔️✔️

**ESA ES LA VERDADERA VENTAJA DE TENER UN MENTOR**

👉 [**ÚNETE AL VIP PARA MENTORÍA GRATIS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-06 03:39:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(438,7443,-1002763662248,'Chartoro FX Señales Gratis','🔓  [**TOCA AQUÍ PARA OBTENER ACCESO GRATIS A LAS SEÑALES VIP**](https://t.me/m/q3-XLmhBNmY0)  🔓',0,'NONE',NULL,'2026-08-06 04:12:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(439,7446,-1002763662248,'Chartoro FX Señales Gratis','**ESTÁS LISTO PARA GANAR HOY?** 🤩🤩🤩',0,'NONE',NULL,'2026-08-06 10:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(440,7447,-1002763662248,'Chartoro FX Señales Gratis','**El grupo VIP de CHARTOROFX ha estado creciendo y creciendo ****📈****📈****📈**
__Gracias a todos por ser parte de nuestra comunidad __🙏',0,'NONE',NULL,'2026-08-06 12:10:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(441,7448,-1002763662248,'Chartoro FX Señales Gratis','Listo',0,'NONE',NULL,'2026-08-06 13:20:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(442,7449,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4269.03

🏆**TP1**: 4272.03
🏆**TP2**: 4279.03
🏆**TP3**: 4289.03

**⛔️ Stop Loss (SL)**: 4259.03

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Price about to breakout the vib line',1,'REGEX',NULL,'2026-08-06 13:48:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(443,7450,-1002763662248,'Chartoro FX Señales Gratis','**EL ORO EMPEZÓ FUERTE **🔥

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Toque rápido, dinero instantáneo __💰',0,'NONE',NULL,'2026-08-06 14:13:24.000000');
INSERT INTO "raw_telegram_messages" VALUES(444,7451,-1002763662248,'Chartoro FX Señales Gratis','[**TOCA AQUÍ SI YA ESTÁS LISTO PARA UNIRTE A NOSOTROS**](https://t.me/m/q3-XLmhBNmY0)

👉 x4 SEÑALES
👉 x4 POTENCIAL DE GANANCIAS
👉 MENTORÍA DE ALTA CALIDAD
👉 CURSO DE 5 HORAS DE ALTA CALIDAD',0,'NONE',NULL,'2026-08-06 14:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(445,7453,-1002763662248,'Chartoro FX Señales Gratis','👉 [**TOCA AQUÍ SI ERES UN TRADER PRINCIPIANTE**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-08-06 15:45:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(446,7454,-1002763662248,'Chartoro FX Señales Gratis','🚨 **VIP NO ES SOLO UNA SALA DE SEÑALES** 🚨

Es:
🔴 4–8 señales diarias de alta calidad
🔴 Un curso completo de trading
🔴 Rendimiento probado y transparente
🔴 Mentoría 24/7 cuando las decisiones realmente importan

Esa combinación es rara.
**POR ESO FUNCIONA ****❗️**

💥 [**ENTRA AL VIP AHORA**](https://t.me/m/q3-XLmhBNmY0) 💥',0,'NONE',NULL,'2026-08-06 16:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(447,7455,-1002763662248,'Chartoro FX Señales Gratis','**LA CHECKLIST PARA TRADERS REALES**

✅ __Mentalidad basada en la paciencia, no en el pánico
____✅____ Plan de riesgo más firme que tus excusas
____✅____ Mentor que realmente opera, no solo habla__',0,'NONE',NULL,'2026-08-06 17:55:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(448,7456,-1002763662248,'Chartoro FX Señales Gratis','Aquí te paso las últimas. 
Hoy fue un buen día.

Lastimosamente tuve que cerrar las últimas porque no podía supervisarlas, pero gracias a Dios y a tu ayuda, cerramos en positivos.',0,'NONE',NULL,'2026-08-06 18:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(449,7457,-1002763662248,'Chartoro FX Señales Gratis','Una operación a la vez, las ganancias se siguen acumulando 

✅ Sin adivinar
✅ Sin estrés
✅ Solo siguiendo el plan

**TÚ PODRÍAS ESTAR EN LA PRÓXIMA CAPTURA** 🫵',0,'NONE',NULL,'2026-08-06 19:44:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(450,7458,-1002763662248,'Chartoro FX Señales Gratis','Fueron más de 70 dólares, gracias...',0,'NONE',NULL,'2026-08-06 21:53:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(451,7459,-1002763662248,'Chartoro FX Señales Gratis','El VIP no es “**estudiar para siempre**” ni “**copiar a ciegas**”

Es:
💎 Copiar mientras aprendes
💎 Ganar mientras subes de nivel
💎 Construir confianza a través de la ejecución

**ASÍ ES COMO SE FORMAN LOS TRADERS REALES** 📊

[**CONVIÉRTETE EN UN TRADER VIP AHORA**](https://t.me/m/q3-XLmhBNmY0) 🚀🚀',0,'NONE',NULL,'2026-08-06 22:47:21.000000');
INSERT INTO "raw_telegram_messages" VALUES(452,7460,-1002763662248,'Chartoro FX Señales Gratis','🏆 **DENTRO DEL VIP** 🏆

👉 4–8 señales diarias
👉 un curso de trading paso a paso
👉 mentoría a demanda

💰 [**RECLAMA LOS BENEFICIOS VIP AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 💰',0,'NONE',NULL,'2026-08-07 00:08:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(453,7461,-1002763662248,'Chartoro FX Señales Gratis','Gracias por señales',0,'NONE',NULL,'2026-08-07 00:26:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(454,7462,-1002763662248,'Chartoro FX Señales Gratis','Hola Luis, a veces es mejor asegurar🤭 vale más pájaro en la mano que 100 volando',0,'NONE',NULL,'2026-08-07 00:27:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(455,7463,-1002763662248,'Chartoro FX Señales Gratis','Gracias por tu señal Luis excelente!',0,'NONE',NULL,'2026-08-07 00:27:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(456,7464,-1002763662248,'Chartoro FX Señales Gratis','⬆️ **TÚ TAMBIÉN PUEDES GANAR ESTO!** 🤑🤑🤑',0,'NONE',NULL,'2026-08-07 00:50:15.000000');
INSERT INTO "raw_telegram_messages" VALUES(457,7465,-1002763662248,'Chartoro FX Señales Gratis','👉 [**HAZ CLIC AQUÍ SI TAMBIÉN QUIERES GANAR ESO USANDO TU TELÉFONO**](https://t.me/m/q3-XLmhBNmY0)  👈',0,'NONE',NULL,'2026-08-07 00:52:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(458,7466,-1002763662248,'Chartoro FX Señales Gratis','**ACABAMOS DE HACER UN SORTEO EN EL VIP! **🤫🤫🤫

[**HAZ CLIC AQUÍ PARA UNIRTE A NOSOTROS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-07 02:13:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(459,7467,-1002763662248,'Chartoro FX Señales Gratis','**LA CHECKLIST PARA TRADERS REALES**

✅ __Mentalidad basada en la paciencia, no en el pánico
____✅____ Plan de riesgo más firme que tus excusas
____✅____ Mentor que realmente opera, no solo habla__',0,'NONE',NULL,'2026-08-07 03:10:20.000000');
INSERT INTO "raw_telegram_messages" VALUES(460,7468,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4254
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-07 03:15:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(461,7469,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4254
**⛔️ Stop Loss (SL): **4246

**🏆 TP1: **4257
**🏆 TP2:** 4262
**🏆 TP3:** 4270

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-07 03:17:23.000000');
INSERT INTO "raw_telegram_messages" VALUES(462,7470,-1002763662248,'Chartoro FX Señales Gratis','**EL PRECIO YA SE VE “HAMBRIENTO” ****🔥**',0,'NONE',NULL,'2026-08-07 03:26:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(463,7471,-1002763662248,'Chartoro FX Señales Gratis','**Y GOLPEÓ INMEDIATAMENTE ****💥**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__El mercado entró agresivo desde el inicio.__',0,'NONE',NULL,'2026-08-07 03:28:54.000000');
INSERT INTO "raw_telegram_messages" VALUES(464,7473,-1002763662248,'Chartoro FX Señales Gratis','**AHORA ESTÁ GANANDO VELOCIDAD ****🚀**',0,'NONE',NULL,'2026-08-07 03:58:26.000000');
INSERT INTO "raw_telegram_messages" VALUES(465,7474,-1002763662248,'Chartoro FX Señales Gratis','**Y AHORA SE ESTÁ CONVIRTIENDO EN UNA CARRERA 🏃‍♂️**

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**
__
El momentum está creciendo con fuerza.__',0,'NONE',NULL,'2026-08-07 04:00:26.000000');
INSERT INTO "raw_telegram_messages" VALUES(466,7476,-1002763662248,'Chartoro FX Señales Gratis','👀👀👀',0,'NONE',NULL,'2026-08-07 04:35:40.000000');
INSERT INTO "raw_telegram_messages" VALUES(467,7477,-1002763662248,'Chartoro FX Señales Gratis','**ESTO SE ESTÁ SALIENDO DE CONTROL ****🤯**',0,'NONE',NULL,'2026-08-07 05:12:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(468,7478,-1002763662248,'Chartoro FX Señales Gratis','**Y ESO… FUE UN DOMINIO TOTAL DE LA SESIÓN ****👑**

**#XAUUSD**** TP3 HIT, +160 Pips ****🏆**

__El mercado no dio ni un respiro ____💰__',0,'NONE',NULL,'2026-08-07 05:14:49.000000');
INSERT INTO "raw_telegram_messages" VALUES(469,7480,-1002763662248,'Chartoro FX Señales Gratis','[**OBTÉN MUCHO MÁS DE ESTO EN EL VIP**](https://t.me/m/q3-XLmhBNmY0)  ⬆️',0,'NONE',NULL,'2026-08-07 05:39:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(470,7482,-1002763662248,'Chartoro FX Señales Gratis','**LISTO PARA LLEVAR TU TRADING AL SIGUIENTE NIVEL?** 📈📈📈',0,'NONE',NULL,'2026-08-07 11:33:58.000000');
INSERT INTO "raw_telegram_messages" VALUES(471,7483,-1002763662248,'Chartoro FX Señales Gratis','⚠️ **EL VIP NO ES SOLO PARA PRINCIPIANTES** ⚠️

Esto también es para:
Traders **CANSADOS DE PERDER** y traders que quieren **LLEVAR SU NIVEL AL MÁXIMO**  🌡

**📊** [**HAZ CLIC AQUÍ PARA CAMBIAR TU JUEGO**](https://t.me/m/q3-XLmhBNmY0) **📊**',0,'NONE',NULL,'2026-08-07 12:15:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(472,7484,-1002763662248,'Chartoro FX Señales Gratis','__LOS MIEMBROS VIP SE VIENEN CON UN MES MUY ABUNDANTE__ 🤑🤑🤑',0,'NONE',NULL,'2026-08-07 13:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(473,7485,-1002763662248,'Chartoro FX Señales Gratis','⭐️ **BENEFICIOS VIP** ⭐️

⏩ 4–8 señales de trading de alta calidad al día
⏩ Un curso completo de trading
⏩ Una guía completa de la A a la Z para que sepas por qué funcionan las operaciones
⏩ Mentoría y acompañamiento real
⏩ Resultados comprobados que puedes seguir paso a paso',0,'NONE',NULL,'2026-08-07 14:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(474,7486,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4337.39

🏆**TP1**: 4340.39
🏆**TP2**: 4347.39
🏆**TP3**: 4357.39

**⛔️ Stop Loss (SL)**: 4327.39

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Price bounced from support zone',1,'REGEX',NULL,'2026-08-07 14:09:48.000000');
INSERT INTO "raw_telegram_messages" VALUES(475,7487,-1002763662248,'Chartoro FX Señales Gratis','**PRECISIÓN EN ACCIÓN! ****⚡️**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__ganancias aseguradas desde el inicio ____💰__',0,'NONE',NULL,'2026-08-07 14:11:54.000000');
INSERT INTO "raw_telegram_messages" VALUES(476,7488,-1002763662248,'Chartoro FX Señales Gratis','**MOMENTUM DESATADO! ****🚀****

****#XAUUSD**** TP2 HIT, +100 Pips 🏆**

análisis preciso, resultados reales 📈',0,'NONE',NULL,'2026-08-07 14:22:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(477,7489,-1002763662248,'Chartoro FX Señales Gratis','**VAMOSSSS!!!!**',0,'NONE',NULL,'2026-08-07 14:35:44.000000');
INSERT INTO "raw_telegram_messages" VALUES(478,7490,-1002763662248,'Chartoro FX Señales Gratis','Aquí en el VIP, buscamos el **ÉXITO A LARGO PLAZO** 📈

Esto es más que solo una buena operación,
se trata de ganar de manera consistente cada mes 🤑🤑🤑

[**ÉXITO VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-07 14:38:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(479,7491,-1002763662248,'Chartoro FX Señales Gratis','💵 [**HAZ CLIC AQUÍ PARA GANAR DINERO**](https://t.me/m/q3-XLmhBNmY0) 💵',0,'NONE',NULL,'2026-08-07 15:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(480,7492,-1002763662248,'Chartoro FX Señales Gratis','**ÚLTIMO MOVIMIENTO, DAÑO MASIVO 💥**

**#XAUUSD**** TP3 HIT, +200 Pips 🏆**

__El mismo plan, pago máximo ____💰__',0,'NONE',NULL,'2026-08-07 15:25:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(481,7493,-1002763662248,'Chartoro FX Señales Gratis','🔤🔤🔤🔤❗️❗️❗️',0,'NONE',NULL,'2026-08-07 15:35:20.000000');
INSERT INTO "raw_telegram_messages" VALUES(482,7494,-1002763662248,'Chartoro FX Señales Gratis','**Y esto es solo un SABOR GRATIS de lo que el VIP ve todos los días **💵💵💵',0,'NONE',NULL,'2026-08-07 15:36:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(483,7495,-1002763662248,'Chartoro FX Señales Gratis','⚡️ [**HAZ CLIC AQUÍ ANTES DE QUE SALGA LA PRÓXIMA SEÑAL**](https://t.me/m/q3-XLmhBNmY0) ⚡️',0,'NONE',NULL,'2026-08-07 15:36:55.000000');
INSERT INTO "raw_telegram_messages" VALUES(484,7496,-1002763662248,'Chartoro FX Señales Gratis','👑
👑
👑',0,'NONE',NULL,'2026-08-07 16:05:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(485,7497,-1002763662248,'Chartoro FX Señales Gratis','Señales VIP? **DIARIAS**
Curso de trading? **CURSO DE TRADING DE 5 HORAS**
Precisión? **80%**
Soporte? **LAS 24 HORAS**

**ESCRÍBEME SI QUIERES TODO ESTO** 🔠 @SoporteChartoroFX',0,'NONE',NULL,'2026-08-07 16:44:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(486,7498,-1002763662248,'Chartoro FX Señales Gratis','[**TOCA AQUÍ PARA ENTRAR GRATIS AL VIP**](https://t.me/m/q3-XLmhBNmY0) 🚀',0,'NONE',NULL,'2026-08-07 17:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(487,7499,-1002763662248,'Chartoro FX Señales Gratis','**Imagina despertar y solo copiar mis operaciones en vez de ir a trabajar por el mismo sueldo **🤯🤯

**ESO ES LO QUE CIENTOS DE PERSONAS YA ESTÁN HACIENDO DENTRO DEL VIP ****💯**',0,'NONE',NULL,'2026-08-07 18:12:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(488,7501,-1002763662248,'Chartoro FX Señales Gratis','🔝 **VIP NO ES SOLO UNA SALA DE SEÑALES** 🔝

Es:
🔸 4–8 señales diarias de alta calidad
🔸 Un curso completo de trading
🔸 Rendimiento probado y transparente
🔸 Mentoría 24/7 cuando las decisiones realmente importan

Esa combinación es rara.
**POR ESO FUNCIONA ****✔️**',0,'NONE',NULL,'2026-08-07 21:53:22.000000');
INSERT INTO "raw_telegram_messages" VALUES(489,7502,-1002763662248,'Chartoro FX Señales Gratis','**A este punto, ya has visto los resultados.**
Has visto el crecimiento 📈
Has visto la prueba 💵

Esto no se trata de convencerte —
se trata de que decidas dejar de ver cómo los demás avanzan 🫵

😎 [**HAZ CLIC AQUÍ PARA SUBIR DE NIVEL CON EL VIP**](https://t.me/m/q3-XLmhBNmY0) 😎',0,'NONE',NULL,'2026-08-07 23:33:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(490,7503,-1002763662248,'Chartoro FX Señales Gratis','Gracias por señales',0,'NONE',NULL,'2026-08-08 00:45:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(491,7504,-1002763662248,'Chartoro FX Señales Gratis','Compartir',0,'NONE',NULL,'2026-08-08 00:46:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(492,7505,-1002763662248,'Chartoro FX Señales Gratis','**⬆️**** BUSCANDO A LAS ÚLTIMAS 3 PERSONAS QUE QUIERAN SER COMO ELLOS!!!!**',0,'NONE',NULL,'2026-08-08 01:57:31.000000');
INSERT INTO "raw_telegram_messages" VALUES(493,7506,-1002763662248,'Chartoro FX Señales Gratis','**NECESITAS AYUDA CON EL TRADING?** 📈📈

👉👉 [__HAZ CLIC AQUÍ PARA RECIBIR APOYO__](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-08 02:34:48.000000');
INSERT INTO "raw_telegram_messages" VALUES(494,7507,-1002763662248,'Chartoro FX Señales Gratis','Para unirte solo necesitas:
🔴 Un teléfono
🔴 Internet
🔴 20 minutos al día

❌ NO SE NECESITA EXPERIENCIA ❌',0,'NONE',NULL,'2026-08-08 03:50:52.000000');
INSERT INTO "raw_telegram_messages" VALUES(495,7509,-1002763662248,'Chartoro FX Señales Gratis','Gracias hermano',0,'NONE',NULL,'2026-08-08 04:12:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(496,7510,-1002763662248,'Chartoro FX Señales Gratis','Hermosa señal Luis',0,'NONE',NULL,'2026-08-08 04:31:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(497,7511,-1002763662248,'Chartoro FX Señales Gratis','**QUIERES SER COMO ELLOS?** ☝️',0,'NONE',NULL,'2026-08-08 05:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(498,7514,-1002763662248,'Chartoro FX Señales Gratis','❓ **Tienes planes para el fin de semana?**',0,'NONE',NULL,'2026-08-08 11:21:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(499,7515,-1002763662248,'Chartoro FX Señales Gratis','**Estoy recopilando los resultados de la semana pasada** 💰💰💰

__Estás listo para saber cuánto te perdiste por no estar en el VIP la semana pasada?__ 🤨',0,'NONE',NULL,'2026-08-08 12:44:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(500,7516,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA GANAR SOLO COPIANDO Y PEGANDO**](https://t.me/m/q3-XLmhBNmY0) 🤯🤯🤯',0,'NONE',NULL,'2026-08-08 13:15:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(501,7518,-1002763662248,'Chartoro FX Señales Gratis','‼️ **SABÍAS QUE?**

__También hacemos sorteos aleatorios en el VIP __😉',0,'NONE',NULL,'2026-08-08 14:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(502,7519,-1002763662248,'Chartoro FX Señales Gratis','8**__ meses consecutivos en ganancias __**📈**__ __**📈**__ __**📈

**POR QUÉ AÚN NO ESTÁS EN EL VIP?**',0,'NONE',NULL,'2026-08-08 15:33:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(503,7520,-1002763662248,'Chartoro FX Señales Gratis','[**SÉ PARTE DEL EQUIPO GANADOR GRATIS**](https://t.me/m/q3-XLmhBNmY0) 🤑',0,'NONE',NULL,'2026-08-08 15:47:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(504,7521,-1002763662248,'Chartoro FX Señales Gratis','❗️ [**HAZ CLIC AQUÍ SI ERES UN TRADER PRINCIPIANTE Y NECESITAS AYUDA**](https://t.me/m/q3-XLmhBNmY0) ❗️',0,'NONE',NULL,'2026-08-08 17:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(505,7522,-1002763662248,'Chartoro FX Señales Gratis','Lo de hoy en menos de 10 minutos . Gracias Luis',0,'NONE',NULL,'2026-08-08 18:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(506,7524,-1002763662248,'Chartoro FX Señales Gratis','Luis genio!',0,'NONE',NULL,'2026-08-08 19:03:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(507,7525,-1002763662248,'Chartoro FX Señales Gratis','Vamos muy bien',0,'NONE',NULL,'2026-08-08 19:03:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(508,7526,-1002763662248,'Chartoro FX Señales Gratis','Esas operaciones están siendo espectaculares',0,'NONE',NULL,'2026-08-08 19:03:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(509,7527,-1002763662248,'Chartoro FX Señales Gratis','Gracias a Dios',0,'NONE',NULL,'2026-08-08 19:03:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(510,7528,-1002763662248,'Chartoro FX Señales Gratis','**QUÉ OTRA PRUEBA NECESITAS?** 🤑🤑**
**[**GANA GRATIS ESTE AGOSTO!**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-08 19:20:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(511,7529,-1002763662248,'Chartoro FX Señales Gratis','**📖**** **[**RECLAMA TU E-BOOK DE TRADING GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)** ****📖**',0,'NONE',NULL,'2026-08-08 20:10:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(512,7530,-1002763662248,'Chartoro FX Señales Gratis','🏆 **BENEFICIOS VIP** 🏆

✔️ 4–8 señales de trading de alta calidad al día
✔️ Un curso completo de trading
✔️ Una guía completa de la A a la Z para que sepas por qué funcionan las operaciones
✔️ Mentoría y acompañamiento real
✔️ Resultados comprobados que puedes seguir paso a paso',0,'NONE',NULL,'2026-08-08 21:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(513,7531,-1002763662248,'Chartoro FX Señales Gratis','**CÓMO VA TU FIN DE SEMANA HASTA AHORA?**',0,'NONE',NULL,'2026-08-08 22:16:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(514,7533,-1002763662248,'Chartoro FX Señales Gratis','💎 [**ÚNETE AL VIP AHORA ANTES DE QUE ABRA EL MERCADO!!!**](https://t.me/m/q3-XLmhBNmY0) 💎',0,'NONE',NULL,'2026-08-09 00:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(515,7534,-1002763662248,'Chartoro FX Señales Gratis','El mercado está en pausa, pero el plan no.
**Hoy es el día perfecto para ajustar tu estrategia y fortalecer tu mentalidad.**

✔️ Analiza
✔️ Corrige errores
✔️ Prepárate para la semana

**LA CONSISTENCIA SE CONSTRUYE FUERA DEL MERCADO** 💪

💰 [**HAZ CLIC AQUÍ PARA ACCEDER AL VIP GRATIS** ](https://t.me/m/q3-XLmhBNmY0)💰',0,'NONE',NULL,'2026-08-09 01:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(516,7535,-1002763662248,'Chartoro FX Señales Gratis','Hola Luis, a veces es mejor asegurar🤭 vale más pájaro en la mano que 100 volando',0,'NONE',NULL,'2026-08-09 02:23:32.000000');
INSERT INTO "raw_telegram_messages" VALUES(517,7536,-1002763662248,'Chartoro FX Señales Gratis','Quieres algo para revisar durante el fin de semana antes de que el mercado abra de nuevo?

📖 [**OBTÉN MATERIALES EDUCATIVOS GRATUITOS AQUÍ!**](https://t.me/m/q3-XLmhBNmY0) 📖',0,'NONE',NULL,'2026-08-09 02:40:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(518,7537,-1002763662248,'Chartoro FX Señales Gratis','Compartir',0,'NONE',NULL,'2026-08-09 04:44:47.000000');
INSERT INTO "raw_telegram_messages" VALUES(519,7538,-1002763662248,'Chartoro FX Señales Gratis','🔓  [**TOCA AQUÍ PARA OBTENER ACCESO GRATIS A LAS SEÑALES VIP**](https://t.me/m/q3-XLmhBNmY0)  🔓',0,'NONE',NULL,'2026-08-09 05:37:12.000000');
INSERT INTO "raw_telegram_messages" VALUES(520,7539,-1002763662248,'Chartoro FX Señales Gratis','🚨🚨 [**ÚLTIMO CUPO GRATIS EN EL VIP**](https://t.me/m/q3-XLmhBNmY0) 🚨🚨',0,'NONE',NULL,'2026-08-09 06:15:12.000000');
INSERT INTO "raw_telegram_messages" VALUES(521,7540,-1002763662248,'Chartoro FX Señales Gratis','**NUEVO EN EL TRADING?** Nosotros te ayudamos 👇

✅ 4–8 señales de alta calidad al día
✅ Guía ideal para principiantes
✅ Análisis en vivo del mercado
✅ Soporte dedicado 24/7

**100% GRATIS** para empezar!',0,'NONE',NULL,'2026-08-09 12:11:19.000000');
INSERT INTO "raw_telegram_messages" VALUES(522,7541,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ SI QUIERES APRENDER CÓMO HACER TRADING ESTE FIN DE SEMANA**](https://t.me/m/q3-XLmhBNmY0) ↗️',0,'NONE',NULL,'2026-08-09 13:37:16.000000');
INSERT INTO "raw_telegram_messages" VALUES(523,7542,-1002763662248,'Chartoro FX Señales Gratis','💭 **REFLEXIÓN DE FIN DE SEMANA:**

Recuerdo cuando no tenía dirección y cada operación se sentía como una apuesta—__realmente no sabía lo que estaba haciendo.__ **No obtuve resultados de la noche a la mañana.** Tuve pérdidas, aprendí de la manera difícil __y seguí adelante.__

**Las cosas solo cambiaron cuando me lo tomé en serio y empecé a construir disciplina real, INCLUSO LOS FINES DE SEMANA.** 

**POR ESO SÉ EXACTAMENTE LO QUE SE NECESITA PARA GANAR AHORA** 🤑 🤑

Comparte tus experiencias [**AQUÍ **](https://t.me/m/q3-XLmhBNmY0)también!',0,'NONE',NULL,'2026-08-09 16:02:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(524,7544,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ SI QUIERES SEÑALES VIP GRATIS ESTA SEMANA**](https://t.me/m/q3-XLmhBNmY0) 💪',0,'NONE',NULL,'2026-08-09 18:51:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(525,7545,-1002763662248,'Chartoro FX Señales Gratis','Quiero compartir esto Luis! Todo empezó por tí y tú guía y consejos. Esto en una semana siguiéndote',0,'NONE',NULL,'2026-08-09 19:12:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(526,7546,-1002763662248,'Chartoro FX Señales Gratis','En 5 días. ¡Eres muy grande!',0,'NONE',NULL,'2026-08-09 19:33:32.000000');
INSERT INTO "raw_telegram_messages" VALUES(527,7547,-1002763662248,'Chartoro FX Señales Gratis','🔼**HAS VISTO TODAS LAS GANANCIAS QUE MI VIP ME ENVIÓ ARRIBA?**

**TÚ TAMBIÉN PUEDES GANAR ESO!** 🫵',0,'NONE',NULL,'2026-08-09 19:45:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(528,7548,-1002763662248,'Chartoro FX Señales Gratis','Siempre es la misma historia:
Ves las ganancias. Dices “__la próxima semana__.”
Y esa próxima semana se convierte en el próximo mes 🙄

Mientras tanto, otros se unieron el fin de semana pasado…**y cerraron la semana con ganancias** 💰💰💰

No esperes al lunes para desear haber empezado hoy.
👉 [VIP GRATIS AQUÍ](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-09 21:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(529,7549,-1002763662248,'Chartoro FX Señales Gratis','🏆 [**SEÑALES VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-08-09 22:07:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(530,7551,-1002763662248,'Chartoro FX Señales Gratis','Cada persona de alto ingreso que he entrenado comenzó con una cosa:

**__una pregunta__** ❓**__
un mensaje__** ✉️**__
un momento de claridad__**  🧠

Si alguna vez te has preguntado “**__Cómo funciona?__”**...
**PREGUNTA AHORA** > [@SoporteChartoroFX](https://t.me/SoporteChartoroFX) 😉

⚠️ **Las personas que se retrasan son las mismas que se quedan en la quiebra** ⚠️',0,'NONE',NULL,'2026-08-10 00:25:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(531,7552,-1002763662248,'Chartoro FX Señales Gratis','__CANSADO DE PERDER?__
➡️ [**TOCA AQUÍ PARA UNIRTE A UN GRUPO GANADOR CON PRUEBAS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-10 01:29:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(532,7553,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4320
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-10 01:36:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(533,7554,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point:** 4320
**⛔️ Stop Loss (SL): **4328

**🏆 TP1: **4317
**🏆 TP2:** 4312
**🏆 TP3:** 4304

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-10 01:41:35.000000');
INSERT INTO "raw_telegram_messages" VALUES(534,7555,-1002763662248,'Chartoro FX Señales Gratis','**DIRECTO AL AZUL ****💙**',0,'NONE',NULL,'2026-08-10 01:43:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(535,7556,-1002763662248,'Chartoro FX Señales Gratis','**EL MERCADO ABRE Y DE INMEDIATO SE VUELVE PRODUCTIVO! ****⚡️****

****#XAUUSD**** TP1 HIT, +30 Pips 🏆
**
__Ganancia rápida para mantener el ritmo fuerte al inicio de la semana!__',0,'NONE',NULL,'2026-08-10 01:44:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(536,7559,-1002763662248,'Chartoro FX Señales Gratis','💵⭐️ [**TOCA AQUÍ PARA CAMBIAR TU VIDA PARA MEJOR**](https://t.me/m/q3-XLmhBNmY0) ⭐️💵',0,'NONE',NULL,'2026-08-10 03:11:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(537,7560,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4319
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-10 03:12:32.000000');
INSERT INTO "raw_telegram_messages" VALUES(538,7561,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4319
**⛔️ Stop Loss (SL): **4327

**🏆 TP1: **4316
**🏆 TP2:** 4311
**🏆 TP3:** 4303

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-10 03:13:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(539,7562,-1002763662248,'Chartoro FX Señales Gratis','Move SL to 4329',1,'REGEX',NULL,'2026-08-10 03:21:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(540,7563,-1002763662248,'Chartoro FX Señales Gratis','**❌ SL HIT**

Darle más espacio a la operación no ayudó esta vez.

No pasa nada — seguiré buscando una nueva configuración clara 🔎

Manténganse pacientes, equipo. Operamos con inteligencia, no con prisas. ✅',0,'NONE',NULL,'2026-08-10 03:43:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(541,7564,-1002763662248,'Chartoro FX Señales Gratis','🚨 **EL VERDADERO CÓDIGO SECRETO?**

__No es solo copiar señales…__
**sino aprender por qué funcionan mientras ganas con ellas** 📈

**EL VIP TE DA LAS SEÑALES Y LA GUÍA COMPLETA DE LA A–Z PARA QUE EVOLUCIONES MIENTRAS GENERAS BENEFICIOS** 💵💵💵',0,'NONE',NULL,'2026-08-10 04:15:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(542,7565,-1002763662248,'Chartoro FX Señales Gratis','Si sigues operando sin mentoría un lunes...
**ESTÁS ELIGIENDO EL MODO MÁS DIFÍCIL DE ESTE JUEGO** ‼️

**No hay excusas para eso** 🙄
**ÚNETE AL VIP GRATIS**  ➡️ @SoporteChartoroFX',0,'NONE',NULL,'2026-08-10 04:46:26.000000');
INSERT INTO "raw_telegram_messages" VALUES(543,7567,-1002763662248,'Chartoro FX Señales Gratis','**GRACIAS A TODOS POR CONFIAR EN CHARTORO** 🙏🙏',0,'NONE',NULL,'2026-08-10 08:01:47.000000');
INSERT INTO "raw_telegram_messages" VALUES(544,7569,-1002763662248,'Chartoro FX Señales Gratis','**YA TIENES ACTIVADAS LAS NOTIFICACIONES?** 🔔🔔',0,'NONE',NULL,'2026-08-10 10:40:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(545,7570,-1002763662248,'Chartoro FX Señales Gratis','**Cero experiencia en trading?** No importa.
Con nosotros:

📈 4–8 señales todos los días
📖 Explicaciones simples
🎯 Análisis + educación
🙌 Soporte constante

**Todo esto GRATIS**',0,'NONE',NULL,'2026-08-10 11:21:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(546,7571,-1002763662248,'Chartoro FX Señales Gratis','⚡️ [**RECLAMA UN LUGAR VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-10 12:21:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(547,7572,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📈#XAUUSD📈

**Direction:📈** **#SELL**
**Entry Point**: 4332.94

🏆**TP1**: 4329.94
🏆**TP2**: 4322.94
🏆**TP3**: 4312.94

**⛔️ Stop Loss (SL)**: 4342.94

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Same as the original idea',1,'REGEX',NULL,'2026-08-10 13:28:15.000000');
INSERT INTO "raw_telegram_messages" VALUES(548,7573,-1002763662248,'Chartoro FX Señales Gratis','**ENCENDIÓ… Y EXPLOTÓ ****💥****

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Ese primer movimiento llegó con fuerza.__',0,'NONE',NULL,'2026-08-10 13:47:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(549,7574,-1002763662248,'Chartoro FX Señales Gratis','**Y AHORA ESTÁN OBLIGADOS A PERSEGUIR 🏃‍♂️**

**#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El momentum subió a otro nivel.__',0,'NONE',NULL,'2026-08-10 13:53:42.000000');
INSERT INTO "raw_telegram_messages" VALUES(550,7575,-1002763662248,'Chartoro FX Señales Gratis','**VAMOSSSS** 🎯🎯',0,'NONE',NULL,'2026-08-10 14:08:44.000000');
INSERT INTO "raw_telegram_messages" VALUES(551,7576,-1002763662248,'Chartoro FX Señales Gratis','**ACABO DE SOLTAR OTRA SEÑAL EN EL VIP!**',0,'NONE',NULL,'2026-08-10 14:39:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(552,7577,-1002763662248,'Chartoro FX Señales Gratis','🚨 **VIP NO ES SOLO UNA SALA DE SEÑALES** 🚨

Es:
🔴 4–8 señales diarias de alta calidad
🔴 Un curso completo de trading
🔴 Rendimiento probado y transparente
🔴 Mentoría 24/7 cuando las decisiones realmente importan

Esa combinación es rara.
**POR ESO FUNCIONA ****❗️**

💥 [**ENTRA AL VIP AHORA**](https://t.me/m/q3-XLmhBNmY0) 💥',0,'NONE',NULL,'2026-08-10 15:23:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(553,7579,-1002763662248,'Chartoro FX Señales Gratis','Gracias a tus señales hoy comenzamos con esta ganancia',0,'NONE',NULL,'2026-08-10 16:22:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(554,7580,-1002763662248,'Chartoro FX Señales Gratis','❓ **QUIERES UNIRTE A UNA COMUNIDAD DE TRADERS GANADORES?**',0,'NONE',NULL,'2026-08-10 17:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(555,7581,-1002763662248,'Chartoro FX Señales Gratis','**SEAMOS HONESTOS:**

No estarías aquí, leyendo esto,
si no quisieras los resultados que están obteniendo los miembros del VIP 🙄🙄

Ya viste suficiente para unirte.
📊 [**AHORA HAZ CLIC AQUÍ PARA UNIRTE**](https://t.me/m/q3-XLmhBNmY0) 📊',0,'NONE',NULL,'2026-08-10 18:25:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(556,7582,-1002763662248,'Chartoro FX Señales Gratis','Compartir',0,'NONE',NULL,'2026-08-10 19:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(557,7583,-1002763662248,'Chartoro FX Señales Gratis','Vamos por más luis... graciias...',0,'NONE',NULL,'2026-08-10 19:22:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(558,7584,-1002763662248,'Chartoro FX Señales Gratis','💵 [**HAZ CLIC AQUÍ PARA GANAR DINERO**](https://t.me/m/q3-XLmhBNmY0) 💵',0,'NONE',NULL,'2026-08-10 20:26:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(559,7585,-1002763662248,'Chartoro FX Señales Gratis','Gracias!',0,'NONE',NULL,'2026-08-10 22:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(560,7586,-1002763662248,'Chartoro FX Señales Gratis','COPIAR OPERACIONES 
              ➕
APRENDER EL SISTEMA
              ➕
HACER PREGUNTAS EN CUALQUIER MOMENTO 
              ➕
CONSTRUIR CONFIANZA 
              ➕
GANAR MIENTRAS APRENDES 

              🟰
              
        🏆 [**VIP**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-08-10 23:27:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(561,7587,-1002763662248,'Chartoro FX Señales Gratis','[**CAMBIA TU VIDA HOY Y GANA DINERO DESDE TU CELULAR! **](https://t.me/m/q3-XLmhBNmY0)📱',0,'NONE',NULL,'2026-08-11 00:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(562,7588,-1002763662248,'Chartoro FX Señales Gratis','Muy buena Luis.
Empezamos con todo hoy Lunes.
Gracias, buen día 💪',0,'NONE',NULL,'2026-08-11 01:23:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(563,7589,-1002763662248,'Chartoro FX Señales Gratis','💰 **VICTORA TRAS VICTORIA **💰

En el VIP no paramos de cerrar trades verdes ✅
Y tú sigues mirando desde afuera 👀',0,'NONE',NULL,'2026-08-11 02:30:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(564,7590,-1002763662248,'Chartoro FX Señales Gratis','🏆 [**SÉ PARTE DE LA COMUNIDAD VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-08-11 02:45:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(565,7591,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4419
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-11 03:38:36.000000');
INSERT INTO "raw_telegram_messages" VALUES(566,7592,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4419
**⛔️ Stop Loss (SL): **4427

**🏆 TP1: **4416
**🏆 TP2:** 4411
**🏆 TP3:** 4403

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-11 03:40:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(567,7593,-1002763662248,'Chartoro FX Señales Gratis','**EL PRECIO SE ESTÁ COMPRIMIENDO FUERTEMENTE ****🔥**',0,'NONE',NULL,'2026-08-11 03:45:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(568,7594,-1002763662248,'Chartoro FX Señales Gratis','**ENCENDIÓ… Y EXPLOTÓ ****💥****

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Ese primer movimiento llegó con fuerza.__',0,'NONE',NULL,'2026-08-11 03:47:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(569,7596,-1002763662248,'Chartoro FX Señales Gratis','**LA PRESIÓN SE ACUMULA RÁPIDO ****🚀**',0,'NONE',NULL,'2026-08-11 04:21:24.000000');
INSERT INTO "raw_telegram_messages" VALUES(570,7597,-1002763662248,'Chartoro FX Señales Gratis','**Y AHORA ESTÁN OBLIGADOS A PERSEGUIR 🏃‍♂️**

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__El momentum subió a otro nivel.__',0,'NONE',NULL,'2026-08-11 04:23:24.000000');
INSERT INTO "raw_telegram_messages" VALUES(571,7599,-1002763662248,'Chartoro FX Señales Gratis','**AQUÍ ES DONDE SE VUELVE PARABÓLICO ****🤯**',0,'NONE',NULL,'2026-08-11 05:06:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(572,7600,-1002763662248,'Chartoro FX Señales Gratis','**Y ESO… FUE UN RALLY DE RUPTURA TOTAL ****🚀****💥**

**#XAUUSD**** TP3 HIT, +160 Pips 🏆**

__Eso es un dominio total del mercado__',0,'NONE',NULL,'2026-08-11 05:09:29.000000');
INSERT INTO "raw_telegram_messages" VALUES(573,7602,-1002763662248,'Chartoro FX Señales Gratis','__TE GUSTA LO QUE ESTÁS OBTENIENDO AQUÍ?__
**DISFRUTA DE AÚN MÁS GANANCIAS EN EL **[**VIP**](https://t.me/m/q3-XLmhBNmY0)** **🤑🤑🤑',0,'NONE',NULL,'2026-08-11 05:56:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(574,7603,-1002763662248,'Chartoro FX Señales Gratis','🔓  [**TOCA AQUÍ PARA OBTENER ACCESO GRATIS A LAS SEÑALES VIP**](https://t.me/m/q3-XLmhBNmY0)  🔓',0,'NONE',NULL,'2026-08-11 06:15:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(575,7604,-1002763662248,'Chartoro FX Señales Gratis','👑 __JULIO 2026 __👑
**RESUMEN MENSUAL DE RENDIMIENTO**

📈 +6,139 pips
🎯 82.65% de win rate (81/98 trades)
📊 Un mes sólido y consistente, con un rendimiento especialmente destacado durante los lunes, martes y jueves.

🏆 __81 operaciones ganadoras frente a solo 17 pérdidas, demostrando una ejecución disciplinada y resultados consistentes durante todo el mes.__

**RESULTADOS REALES, CONSISTENCIA REAL** 🔥

Listo para formar parte de la próxima historia de resultados?
Escríbeme ➡️ @SoporteChartoroFX 🚀',0,'NONE',NULL,'2026-08-11 09:26:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(576,7605,-1002763662248,'Chartoro FX Señales Gratis','**BUENOS DÍAS TRADERS!!! **☀️📈

👆👆👆 __YA VIERON LO QUE SE PERDIERON EL MES PASADO? __👀🔥

El mercado estuvo en movimiento, las oportunidades estaban por todos lados...
**Hagamos que este mes sea aún mejor!** 🚀',0,'NONE',NULL,'2026-08-11 10:28:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(577,7606,-1002763662248,'Chartoro FX Señales Gratis','**ES HORA DE UNIRTE POR FIN A LA COMUNIDAD DE TRADING CORRECTA! ** 💯',0,'NONE',NULL,'2026-08-11 11:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(578,7607,-1002763662248,'Chartoro FX Señales Gratis','**TODAVÍA NO PUEDES CREERLO?**
Déjame mostrarte lo que podrías haber ganado **SOLO LA SEMANA PASADA**  💰',0,'NONE',NULL,'2026-08-11 11:44:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(579,7608,-1002763662248,'Chartoro FX Señales Gratis','📈 **RESULTADOS SEMANALES DE SEÑALES **📈
__03 de Agosto – 07 de Agosto, 2026__

💰 **TOTAL: +1,346 PIPS GANADOS **💰

✔️ Win Ratio: 85% (17 ganadas / 3 perdidas)
✔️ Operaciones totales: 20 setups
✔️ Buy vs Sell: 15 compras / 5 ventas
✔️ XAUUSD volvió a destacar entre los instrumentos con mejor rendimiento durante la semana
✔️ Martes (+402 pips), lunes (+327 pips) y viernes (+325 pips) lideraron los resultados
✔️ Una semana más de ejecución consistente, aprovechando oportunidades en FOREX y GOLD

🤑 **QUÉ SIGNIFICA ESTO EN DINERO REAL?**

• 0.01 lote → el valor depende del instrumento y del tamaño del contrato
• 0.10 lote → el valor depende del instrumento y del tamaño del contrato
• 1.00 lote → el valor depende del instrumento y del tamaño del contrato

💰** +1,346 PIPS EN SOLO UNA SEMANA**

**ESCRÍBEME AHORA Y DESCUBRE CÓMO RECIBIR LAS SEÑALES VIP GRATIS!!!**',0,'NONE',NULL,'2026-08-11 12:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(580,7610,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📈#XAUUSD📈

**Direction:📈** **#SELL**
**Entry Point**: 4389.89

🏆**TP1**: 4386.89
🏆**TP2**: 4379.89
🏆**TP3**: 4369.89

**⛔️ Stop Loss (SL)**: 4399.89

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__...',1,'REGEX',NULL,'2026-08-11 12:26:22.000000');
INSERT INTO "raw_telegram_messages" VALUES(581,7611,-1002763662248,'Chartoro FX Señales Gratis','**#XAUUSD**** SL Hit  ❌**

Lamentablemente,  después de que las noticias generaran una fuerte volatilidad. El precio rompió el límite superior del canal ascendente con un movimiento impulsivo, invalidando la idea de venta antes de que los vendedores pudieran tomar el control.

La buena noticia es que nuestra idea bajista aún no ha sido descartada por completo. Si esta ruptura termina siendo un falso rompimiento y el precio vuelve a entrar dentro del canal con confirmaciones claras, podríamos tener una nueva oportunidad de venta de alta probabilidad. Esperaremos la confirmación antes de enviar otra operación.

Recuerden que ninguna estrategia gana todas las operaciones. Una pérdida después de una larga racha de ganancias es parte del trading profesional. Lo más importante es mantener una buena gestión del riesgo y seguir siendo disciplinados.

Mantengan la paciencia, protejan su capital y esperen las mejores oportunidades. La consistencia siempre vence a las emociones. 💪📉',0,'NONE',NULL,'2026-08-11 12:50:32.000000');
INSERT INTO "raw_telegram_messages" VALUES(582,7613,-1002763662248,'Chartoro FX Señales Gratis','**Dónde has visto este nivel de transparencia en un grupo de señales?**

__Si encuentras un grupo que afirma tener un 100% de aciertos, mejor sal corriendo... __ 🏃',0,'NONE',NULL,'2026-08-11 13:04:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(583,7614,-1002763662248,'Chartoro FX Señales Gratis','**DE AQUÍ SOLO PODEMOS IR HACIA ARRIBA!**  🔝',0,'NONE',NULL,'2026-08-11 13:04:25.000000');
INSERT INTO "raw_telegram_messages" VALUES(584,7615,-1002763662248,'Chartoro FX Señales Gratis','Genio💞💞💞💞💞',0,'NONE',NULL,'2026-08-11 13:15:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(585,7616,-1002763662248,'Chartoro FX Señales Gratis','De esta mañana mi bro gracias 🙏🏻',0,'NONE',NULL,'2026-08-11 13:31:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(586,7617,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📈#XAUUSD📈

**Direction:📈** **#SELL**
**Entry Point**: 4383.69

🏆**TP1**: 4380.69
🏆**TP2**: 4373.69
🏆**TP3**: 4363.69

**⛔️ Stop Loss (SL)**: 4393.69

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Same as the last idea',1,'REGEX',NULL,'2026-08-11 14:19:18.000000');
INSERT INTO "raw_telegram_messages" VALUES(587,7618,-1002763662248,'Chartoro FX Señales Gratis','**Cerrar el setup de GOLD.**
El precio ha vuelto a entrar dentro del canal, invalidando el setup. Cerramos la operación y esperaremos una nueva oportunidad con confirmación.',1,'REGEX',NULL,'2026-08-11 14:34:25.000000');
INSERT INTO "raw_telegram_messages" VALUES(588,7619,-1002763662248,'Chartoro FX Señales Gratis','⚠️ **QUIÉN QUIERE ENTRAR AL VIP GRATIS?**

**MÁNDAME DM AHORA** ➡️ @SoporteChartoroFX',0,'NONE',NULL,'2026-08-11 14:47:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(589,7620,-1002763662248,'Chartoro FX Señales Gratis','✨ [ **ESTA ES TU SEÑAL PARA GANAR MÁS** ](https://t.me/m/q3-XLmhBNmY0)✨',0,'NONE',NULL,'2026-08-11 15:14:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(590,7621,-1002763662248,'Chartoro FX Señales Gratis','🩷🩷🩷🩷🩷🩷🩷',0,'NONE',NULL,'2026-08-11 15:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(591,7622,-1002763662248,'Chartoro FX Señales Gratis','TP2',0,'NONE',NULL,'2026-08-11 15:42:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(592,7623,-1002763662248,'Chartoro FX Señales Gratis','[**VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0)

🔼  🔼  🔼',0,'NONE',NULL,'2026-08-11 15:50:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(593,7624,-1002763662248,'Chartoro FX Señales Gratis','🔝 **VIP NO ES SOLO UNA SALA DE SEÑALES** 🔝

Es:
🔸 4–8 señales diarias de alta calidad
🔸 Un curso completo de trading
🔸 Rendimiento probado y transparente
🔸 Mentoría 24/7 cuando las decisiones realmente importan

Esa combinación es rara.
**POR ESO FUNCIONA ****✔️**',0,'NONE',NULL,'2026-08-11 16:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(594,7625,-1002763662248,'Chartoro FX Señales Gratis','[**TOCA PARA OBTENER LOS BENEFICIOS VIP**](https://t.me/m/q3-XLmhBNmY0) 👑',0,'NONE',NULL,'2026-08-11 17:18:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(595,7626,-1002763662248,'Chartoro FX Señales Gratis','**LA CHECKLIST PARA TRADERS REALES**

✅ __Mentalidad basada en la paciencia, no en el pánico
____✅____ Plan de riesgo más firme que tus excusas
____✅____ Mentor que realmente opera, no solo habla__',0,'NONE',NULL,'2026-08-11 18:17:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(596,7627,-1002763662248,'Chartoro FX Señales Gratis','Muchas gracias ❤️',0,'NONE',NULL,'2026-08-11 19:20:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(597,7628,-1002763662248,'Chartoro FX Señales Gratis','**Imagina despertar y solo copiar mis operaciones en vez de ir a trabajar por el mismo sueldo **🤯🤯

**ESO ES LO QUE CIENTOS DE PERSONAS YA ESTÁN HACIENDO DENTRO DEL VIP ****💯**',0,'NONE',NULL,'2026-08-11 19:51:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(598,7630,-1002763662248,'Chartoro FX Señales Gratis','🚨 **BUSCANDO 5 TRADERS PRINCIPIANTES → **[**ACCESO VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 💥',0,'NONE',NULL,'2026-08-11 22:23:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(599,7631,-1002763662248,'Chartoro FX Señales Gratis','__EL VIP NO ES SOLO PARA PRINCIPIANTES__

**LOS TRADERS PRO QUE QUIERAN SUBIR DE NIVEL TAMBIÉN SON BIENVENIDOS! **🚀',0,'NONE',NULL,'2026-08-12 00:34:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(600,7633,-1002763662248,'Chartoro FX Señales Gratis','TP2',0,'NONE',NULL,'2026-08-12 01:08:49.000000');
INSERT INTO "raw_telegram_messages" VALUES(601,7634,-1002763662248,'Chartoro FX Señales Gratis','**+6139 ** **🤯****🤯****🤯**',0,'NONE',NULL,'2026-08-12 01:15:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(602,7635,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4391
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-12 01:22:38.000000');
INSERT INTO "raw_telegram_messages" VALUES(603,7636,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4391
**⛔️ Stop Loss (SL): **4399

**🏆 TP1: **4388
**🏆 TP2:** 4383
**🏆 TP3:** 4375

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-12 01:24:54.000000');
INSERT INTO "raw_telegram_messages" VALUES(604,7637,-1002763662248,'Chartoro FX Señales Gratis','**PRIMER TOQUE EN CAMINO ****🔥**',0,'NONE',NULL,'2026-08-12 01:33:58.000000');
INSERT INTO "raw_telegram_messages" VALUES(605,7638,-1002763662248,'Chartoro FX Señales Gratis','**EL ORO SE MOVIÓ PRIMERO **😎

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Golpe rápido, ganancia instantánea ____💰__',0,'NONE',NULL,'2026-08-12 01:35:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(606,7640,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4399
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-12 02:13:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(607,7641,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4399
**⛔️ Stop Loss (SL): **4391

**🏆 TP1: **4402
**🏆 TP2:** 4407
**🏆 TP3:** 4415

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-12 02:14:49.000000');
INSERT INTO "raw_telegram_messages" VALUES(608,7642,-1002763662248,'Chartoro FX Señales Gratis','**LA PRECISIÓN VUELVE A GOLPEAR **⚡️

**#XAUUSD**** TP1 HIT, +30 Pips 🏆
**
__Entrada inteligente, timing perfecto, beneficio asegurado desde temprano! ____💼__',0,'NONE',NULL,'2026-08-12 02:16:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(609,7643,-1002763662248,'Chartoro FX Señales Gratis','**LUEGO ACELERÓ ****🚀**

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__Extensión limpia, sin dudas ____👀__',0,'NONE',NULL,'2026-08-12 02:45:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(610,7644,-1002763662248,'Chartoro FX Señales Gratis','**SE VIENE UN GRAN IMPULSO ****🚀**',0,'NONE',NULL,'2026-08-12 03:09:30.000000');
INSERT INTO "raw_telegram_messages" VALUES(611,7645,-1002763662248,'Chartoro FX Señales Gratis','**TERMINÓ CON AUTORIDAD ****👑**

**#XAUUSD**** TP3 HIT, +160 Pips 🏆**

__Barrida completa, gran ganancia ____💰__',0,'NONE',NULL,'2026-08-12 03:11:38.000000');
INSERT INTO "raw_telegram_messages" VALUES(612,7646,-1002763662248,'Chartoro FX Señales Gratis','🔴 [**ENTRA AL VIP ANTES DE QUE SALGA UNA NUEVA SEÑAL**](https://t.me/m/q3-XLmhBNmY0) 🔴',0,'NONE',NULL,'2026-08-12 03:43:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(613,7647,-1002763662248,'Chartoro FX Señales Gratis','__Pudiste tomar algunas de las señales de muestra aquí en el grupo principal la semana pasada?__

[**ESTÁS LISTO PARA OBTENER MÁS EN EL VIP?**](https://t.me/m/q3-XLmhBNmY0) 🚀',0,'NONE',NULL,'2026-08-12 05:39:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(614,7648,-1002763662248,'Chartoro FX Señales Gratis','Listo hermano',0,'NONE',NULL,'2026-08-12 06:07:17.000000');
INSERT INTO "raw_telegram_messages" VALUES(615,7650,-1002763662248,'Chartoro FX Señales Gratis','**CUÁL HA SIDO TU MAYOR GANANCIA HASTA AHORA?** 🤑',0,'NONE',NULL,'2026-08-12 10:47:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(616,7651,-1002763662248,'Chartoro FX Señales Gratis','__CANSADO DE PERDER?__
➡️ [**TOCA AQUÍ PARA UNIRTE A UN GRUPO GANADOR CON PRUEBAS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-12 11:21:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(617,7652,-1002763662248,'Chartoro FX Señales Gratis','✅** SÍ, __recibirás de 4 a 8 señales diarias__
****✅**** SÍ, __tendrás mi guía y acompañamiento__
****✅**** SÍ, __recibirás mis materiales educativos__**

❗️ [**RECLAMA TODO AHORA**](https://t.me/m/q3-XLmhBNmY0) ❗️',0,'NONE',NULL,'2026-08-12 12:12:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(618,7654,-1002763662248,'Chartoro FX Señales Gratis','__Estoy buscando una oportunidad para el VIP...__',0,'NONE',NULL,'2026-08-12 13:47:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(619,7655,-1002763662248,'Chartoro FX Señales Gratis','⚠️ **Ten en cuenta que envío de 4 a 8 señales DIARIAS en el VIP.**

[**ÚNETE AQUÍ**](https://t.me/m/q3-XLmhBNmY0) __para que no te pierdas ninguna__ ‼️‼️‼️',0,'NONE',NULL,'2026-08-12 13:55:26.000000');
INSERT INTO "raw_telegram_messages" VALUES(620,7656,-1002763662248,'Chartoro FX Señales Gratis','Luis tus señales son muy buenas, gracias por la oportunidad',0,'NONE',NULL,'2026-08-12 14:57:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(621,7657,-1002763662248,'Chartoro FX Señales Gratis','🔠 [**OBTÉN MÁS SEÑALES AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-12 15:03:40.000000');
INSERT INTO "raw_telegram_messages" VALUES(622,7658,-1002763662248,'Chartoro FX Señales Gratis','🔤🔤🔤   🔤🔤🔤🔤🔤🔤',0,'NONE',NULL,'2026-08-12 16:16:24.000000');
INSERT INTO "raw_telegram_messages" VALUES(623,7659,-1002763662248,'Chartoro FX Señales Gratis','Cortemos el cuento:

Llevas horas deslizando.
Y cuánto te dejó eso? 🙄

**EXACTO.**
**ENTRA AL VIP Y CAMBIA TU VIDA** 💎

Mándame un mensaje para poder ayudarte 👉 [@SoporteChartoroFX](https://t.me/SoporteChartoroFX)',0,'NONE',NULL,'2026-08-12 16:51:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(624,7660,-1002763662248,'Chartoro FX Señales Gratis','El dinero que quieres ya lo están ganando personas que empezaron ESTA SEMANA 🤑🤑

__Sí — principiantes.
Sí — gente sin experiencia.
Sí — **solo siguieron las señales y cobraron.**__

❌ No es que no tengas suerte.
**ES QUE NO ESTÁS EN EL VIP** ‼️

👑 [**HAZ CLIC AQUÍ PARA ENTRAR AL VIP**](https://t.me/m/q3-XLmhBNmY0) 👑',0,'NONE',NULL,'2026-08-12 17:51:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(625,7661,-1002763662248,'Chartoro FX Señales Gratis','**YA VISTE LOS RESULTADOS DE LA SEMANA PASADA?** 🤑🤑🤑',0,'NONE',NULL,'2026-08-12 18:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(626,7662,-1002763662248,'Chartoro FX Señales Gratis','Gracias a tus señales amigo , hoy me fui con casi 10 dólares , hubieran sido más pero creo que no se puso la otra alerta que puse , gracias',0,'NONE',NULL,'2026-08-12 19:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(627,7663,-1002763662248,'Chartoro FX Señales Gratis','⚠️ **QUIÉN QUIERE ENTRAR AL VIP GRATIS?**

**MÁNDAME DM AHORA** ➡️ @SoporteChartoroFX',0,'NONE',NULL,'2026-08-12 19:50:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(628,7664,-1002763662248,'Chartoro FX Señales Gratis','Mi hermano que señal 🔥🔥🔥👌🏻👌🏻👌🏻',0,'NONE',NULL,'2026-08-12 21:55:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(629,7665,-1002763662248,'Chartoro FX Señales Gratis','💶 Ya recibiste tu sueldo o está por llegar? 💵

La pregunta es: lo vas a gastar en tragos y tonterías otra vez… ❌

O por fin vas a invertir una pequeña parte y empezar a cambiar tu vida para siempre? 🏆
 Esto es solo para tomadores de acción. 🚀

Únete [GRATIS](https://t.me/m/q3-XLmhBNmY0) aquí.',0,'NONE',NULL,'2026-08-12 22:57:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(630,7666,-1002763662248,'Chartoro FX Señales Gratis','📈 [**HAZ CLIC AQUÍ PARA APRENDER A OPERAR**](https://t.me/m/q3-XLmhBNmY0) 📈',0,'NONE',NULL,'2026-08-12 23:27:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(631,7667,-1002763662248,'Chartoro FX Señales Gratis','Puedes pasar otra semana buscando “__la estrategia perfecta__”…
**o puedes unirte a un equipo que ya usa una que funciona** 🔥

[**ACCESO GRATIS A MI GRUPO VIP**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-13 00:58:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(632,7668,-1002763662248,'Chartoro FX Señales Gratis','Si puedes copiar y pegar...
**PUEDES GANAR DINERO** 💰💰💰',0,'NONE',NULL,'2026-08-13 01:29:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(633,7669,-1002763662248,'Chartoro FX Señales Gratis','🔔 **3 COSAS QUE TODO TRADER PRINCIPIANTE DEBERÍA SABER**

1️⃣ No necesitas muchos trades… solo los correctos.
2️⃣ Proteger tu capital es más importante que ganar rápido.
3️⃣ La mayoría pierde porque opera sin un plan.

__Por eso muchos traders buscan una comunidad y guía real.__
**ÚNETE A LA NUESTRA AQUÍ > **@SoporteChartoroFX 🚀',0,'NONE',NULL,'2026-08-13 02:51:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(634,7670,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4409
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-13 03:31:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(635,7671,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 ****#XAUUSD**** **

**Direction: 📉 ****#BUY**** **

** Entry Point: **4409
**⛔️ Stop Loss (SL): **4401

**🏆 TP1: **4412
**🏆 TP2:** 4417
**🏆 TP3:** 4425

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-13 03:35:26.000000');
INSERT INTO "raw_telegram_messages" VALUES(636,7672,-1002763662248,'Chartoro FX Señales Gratis','**❌ SL HIT**

Darle más espacio a la operación no ayudó esta vez.

No pasa nada — seguiré buscando una nueva configuración clara 🔎

Manténganse pacientes, equipo. Operamos con inteligencia, no con prisas. ✅',0,'NONE',NULL,'2026-08-13 03:58:24.000000');
INSERT INTO "raw_telegram_messages" VALUES(637,7673,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4396
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-13 04:04:56.000000');
INSERT INTO "raw_telegram_messages" VALUES(638,7674,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4396
**⛔️ Stop Loss (SL): **4404

**🏆 TP1: **4393
**🏆 TP2:** 4388
**🏆 TP3:** 4380

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-13 04:06:54.000000');
INSERT INTO "raw_telegram_messages" VALUES(639,7675,-1002763662248,'Chartoro FX Señales Gratis','**PRIMER OBJETIVO AL ALCANCE **🔥',0,'NONE',NULL,'2026-08-13 04:11:50.000000');
INSERT INTO "raw_telegram_messages" VALUES(640,7676,-1002763662248,'Chartoro FX Señales Gratis','**ESTAMOS DE VUELTA EN EL CAMINO ****💥****💥**

**#XAUUSD**** TP1 HIT, +30 Pips ****🏆**

En camino a la recuperación, chicos — **NO LOS VOY A DECEPCIONAR ****❤️‍🩹**',0,'NONE',NULL,'2026-08-13 04:13:18.000000');
INSERT INTO "raw_telegram_messages" VALUES(641,7677,-1002763662248,'Chartoro FX Señales Gratis','**VAMOS TRADERSSSSS **🚀🚀',0,'NONE',NULL,'2026-08-13 04:52:52.000000');
INSERT INTO "raw_telegram_messages" VALUES(642,7678,-1002763662248,'Chartoro FX Señales Gratis','Compartir',0,'NONE',NULL,'2026-08-13 06:48:25.000000');
INSERT INTO "raw_telegram_messages" VALUES(643,7679,-1002763662248,'Chartoro FX Señales Gratis','**GÁNATE ESO EN MINUTOS** ⬆️',0,'NONE',NULL,'2026-08-13 09:15:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(644,7681,-1002763662248,'Chartoro FX Señales Gratis','❓ **Quieres saber cómo nuestros miembros están generando ganancias consistentes?**',0,'NONE',NULL,'2026-08-13 11:33:40.000000');
INSERT INTO "raw_telegram_messages" VALUES(645,7682,-1002763662248,'Chartoro FX Señales Gratis','No necesitas “__ser bueno__” para entrar al VIP.
**ENTRAS PARA VOLVERTE BUENO** 💪

**Copias operaciones, aprendes por qué funcionan y desarrollas habilidad al mismo tiempo.**

Así es como los principiantes realmente **SUBEN DE NIVEL** 🔼

SI ERES PRINCIPIANTE, [**HAZ CLIC AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-08-13 12:41:48.000000');
INSERT INTO "raw_telegram_messages" VALUES(646,7683,-1002763662248,'Chartoro FX Señales Gratis','Señales VIP? **DIARIAS**
Curso de trading? **CURSO DE TRADING DE 5 HORAS**
Precisión? **80%**
Soporte? **LAS 24 HORAS**

**ESCRÍBEME SI QUIERES TODO ESTO** 🔠 @SoporteChartoroFX',0,'NONE',NULL,'2026-08-13 13:31:47.000000');
INSERT INTO "raw_telegram_messages" VALUES(647,7684,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📈#XAUUSD📈

**Direction:📈** **#SELL**
**Entry Point**: 4385.11

🏆**TP1**: 4382.11
🏆**TP2**: 4375.11
🏆**TP3**: 4365.11

**⛔️ Stop Loss (SL)**: 4395.11

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__...',1,'REGEX',NULL,'2026-08-13 13:33:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(648,7685,-1002763662248,'Chartoro FX Señales Gratis','**LA PRIMERA REACCIÓN SE DIO JUSTO A TIEMPO **⚡️

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Buen comienzo… el mercado está respetando.__',0,'NONE',NULL,'2026-08-13 13:35:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(649,7686,-1002763662248,'Chartoro FX Señales Gratis','**Y LUEGO EMPEZÓ A FLUIR **🚀

**#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El trade se movió exactamente como lo imaginamos.__',0,'NONE',NULL,'2026-08-13 13:53:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(650,7687,-1002763662248,'Chartoro FX Señales Gratis','Mi hermano que señal 🔥🔥🔥👌🏻👌🏻👌🏻',0,'NONE',NULL,'2026-08-13 14:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(651,7689,-1002763662248,'Chartoro FX Señales Gratis','**MOVIMIENTO COMPLETO… LIMPIO **🤯

**#XAUUSD**** TP3 HIT, +200 Pips 🏆**

__Todo dio resultado en este trade 💰__',0,'NONE',NULL,'2026-08-13 14:32:51.000000');
INSERT INTO "raw_telegram_messages" VALUES(652,7690,-1002763662248,'Chartoro FX Señales Gratis','**Y esto es solo un SABOR GRATIS de lo que el VIP ve todos los días ****💵****💵****💵**',0,'NONE',NULL,'2026-08-13 14:38:51.000000');
INSERT INTO "raw_telegram_messages" VALUES(653,7691,-1002763662248,'Chartoro FX Señales Gratis','**De pérdidas constantes a mejores resultados** 📈

__Se unió al VIP Room de Chartoro y empezó a notar la diferencia en su camino como trader.__ 🔥

👉 [**ÚNETE AL VIP ROOM AHORA**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-13 14:47:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(654,7692,-1002763662248,'Chartoro FX Señales Gratis','🚨 [**HAZ CLIC AQUÍ PARA VER LA NUEVA SEÑAL VIP QUE PUBLIQUÉ**](https://t.me/m/q3-XLmhBNmY0) 🚨',0,'NONE',NULL,'2026-08-13 14:50:50.000000');
INSERT INTO "raw_telegram_messages" VALUES(655,7693,-1002763662248,'Chartoro FX Señales Gratis','De esta mañana mi bro gracias 🙏🏻',0,'NONE',NULL,'2026-08-13 15:44:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(656,7694,-1002763662248,'Chartoro FX Señales Gratis','**DE ESTO SE TRATA LA EXPERIENCIA VIP! ****🔥**',0,'NONE',NULL,'2026-08-13 17:10:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(657,7695,-1002763662248,'Chartoro FX Señales Gratis','💥 4–8 señales de alta calidad diarias
💥 Curso completo de trading
💥 Resultados y ganancias respaldados por rendimiento
💥 Soporte 24/7 cuando lo necesites',0,'NONE',NULL,'2026-08-13 18:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(658,7696,-1002763662248,'Chartoro FX Señales Gratis','Luis buen día, esas fueron mis ganancias está semana, excelente tus señales',0,'NONE',NULL,'2026-08-13 20:01:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(659,7697,-1002763662248,'Chartoro FX Señales Gratis','**LOS NUEVOS MIEMBROS VIP YA ESTÁN REVISANDO MIS MATERIALES** 🏆🏆🏆',0,'NONE',NULL,'2026-08-13 23:43:17.000000');
INSERT INTO "raw_telegram_messages" VALUES(660,7698,-1002763662248,'Chartoro FX Señales Gratis','‼️ [**TOCA AQUÍ PARA APROVECHAR ESTA OPORTUNIDAD**](https://t.me/m/q3-XLmhBNmY0) ‼️',0,'NONE',NULL,'2026-08-14 00:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(661,7699,-1002763662248,'Chartoro FX Señales Gratis','Para unirte solo necesitas:
🔴 Un teléfono
🔴 Internet
🔴 20 minutos al día

❌ NO SE NECESITA EXPERIENCIA ❌

[**ÚNETE GRATIS AL VIP**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-14 02:06:42.000000');
INSERT INTO "raw_telegram_messages" VALUES(662,7700,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4316
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-14 02:22:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(663,7701,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4316
**⛔️ Stop Loss (SL): **4324

**🏆 TP1: **4313
**🏆 TP2:** 4308
**🏆 TP3:** 4300

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-14 02:24:36.000000');
INSERT INTO "raw_telegram_messages" VALUES(664,7702,-1002763662248,'Chartoro FX Señales Gratis','**VAMOS EQUIPO! ****🔥**',0,'NONE',NULL,'2026-08-14 02:30:36.000000');
INSERT INTO "raw_telegram_messages" VALUES(665,7703,-1002763662248,'Chartoro FX Señales Gratis','**VAMOS CON TODOOOO! **🚀🚀

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__De vuelta a las ganancias, sigamos con el impulso! 🔥__',0,'NONE',NULL,'2026-08-14 02:34:18.000000');
INSERT INTO "raw_telegram_messages" VALUES(666,7705,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4325
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-14 03:31:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(667,7706,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4325
**⛔️ Stop Loss (SL): **4317

**🏆 TP1: **4328
**🏆 TP2:** 4333
**🏆 TP3:** 4341

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-14 03:33:12.000000');
INSERT INTO "raw_telegram_messages" VALUES(668,7708,-1002763662248,'Chartoro FX Señales Gratis','**ALLÍ VAMOS OTRA VEZ! **🔥🔥',0,'NONE',NULL,'2026-08-14 03:35:20.000000');
INSERT INTO "raw_telegram_messages" VALUES(669,7709,-1002763662248,'Chartoro FX Señales Gratis','**EL DÍA COMIENZA CON FUEGO ****🔥**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Entrada rápida, ganancias rápidas — directo a la bolsa ____💰__',0,'NONE',NULL,'2026-08-14 03:37:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(670,7711,-1002763662248,'Chartoro FX Señales Gratis','☀️ **BUENOS DÍAS TRADERS** ☀️

Llegaste al final de la semana, y eso ya demuestra disciplina, esfuerzo y crecimiento.

Cada gráfico que estudiaste, cada setup que esperaste, cada emoción que controlaste…
todo cuenta 💯

El progreso no siempre es ruidoso.
A veces simplemente se refleja en que operaste mejor que la semana pasada 📈

👉 ÚNETE GRATIS AL VIP @SoporteChartoroFX',0,'NONE',NULL,'2026-08-14 10:59:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(671,7712,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📈#XAUUSD📈

**Direction:📈** **#SELL**
**Entry Point**: 4386.20

🏆**TP1**: 4383.20
🏆**TP2**: 4376.20
🏆**TP3**: 4366.20

**⛔️ Stop Loss (SL)**: 4396.20

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-14 12:32:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(672,7713,-1002763662248,'Chartoro FX Señales Gratis','**Y GOLPEÓ INMEDIATAMENTE ****💥**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__El mercado entró agresivo desde el inicio.__',0,'NONE',NULL,'2026-08-14 12:34:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(673,7714,-1002763662248,'Chartoro FX Señales Gratis','**ESTRUCTURA CONFIRMADA, LAS GANANCIAS CONTINÚAN! ****📈**

**#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El mercado siguió el plan, ejecución limpia, los resultados hablan por sí solos ____🔥__',0,'NONE',NULL,'2026-08-14 12:42:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(674,7715,-1002763662248,'Chartoro FX Señales Gratis','👀👀',0,'NONE',NULL,'2026-08-14 13:25:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(675,7716,-1002763662248,'Chartoro FX Señales Gratis','💡 **TIP DE TRADING** 

Tu mayor arrepentimiento no será una pérdida, **SERÁN LAS GANANCIAS QUE NUNCA TOMASTE.**

**TU FUTURO EMPIEZA AQUÍ **👉 @SoporteChartoroFX',0,'NONE',NULL,'2026-08-14 13:50:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(676,7717,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA OPERAR CONMIGO**](https://t.me/m/q3-XLmhBNmY0) 📈📈📈',0,'NONE',NULL,'2026-08-14 14:22:18.000000');
INSERT INTO "raw_telegram_messages" VALUES(677,7718,-1002763662248,'Chartoro FX Señales Gratis','🏆 **EL VIP INCLUYE:**

✔️ De 4 a 8 señales diarias de trading de alta calidad
✔️ Curso completo de trading
✔️ Guía completa A-a-Z para construir bases sólidas
✔️ Rendimiento comprobado de las señales basado en resultados reales
✔️ Soporte y mentoría 24/7
 
🚀 [**RECLAMA TU ACCESO AL VIP AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 🚀',0,'NONE',NULL,'2026-08-14 14:57:23.000000');
INSERT INTO "raw_telegram_messages" VALUES(678,7719,-1002763662248,'Chartoro FX Señales Gratis','Fueron más de 70 dólares, gracias...',0,'NONE',NULL,'2026-08-14 15:28:44.000000');
INSERT INTO "raw_telegram_messages" VALUES(679,7720,-1002763662248,'Chartoro FX Señales Gratis','Quiero compartir esto Luis! Todo empezó por tí y tú guía y consejos. Esto en una semana siguiéndote',0,'NONE',NULL,'2026-08-14 15:39:31.000000');
INSERT INTO "raw_telegram_messages" VALUES(680,7721,-1002763662248,'Chartoro FX Señales Gratis','**QUIERES VIVIR LA EXPERIENCIA VIP? ****🔝**🔥',0,'NONE',NULL,'2026-08-14 16:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(681,7722,-1002763662248,'Chartoro FX Señales Gratis','Las señales te dan ganancias  💵
El curso te hace independiente 💪
La mentoría 24/7 te hace consistente  📈

**CUÁNTO TIEMPO MÁS VAS A QUEDARTE FUERA?**

🚀 [**APRENDE Y GANA EN EL VIP AHORA**](https://t.me/m/q3-XLmhBNmY0) 🚀',0,'NONE',NULL,'2026-08-14 17:16:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(682,7723,-1002763662248,'Chartoro FX Señales Gratis','‼️** TE IMAGINAS LO QUE ESTAS CANTIDADES PUEDEN HACER POR TU VIDA? **‼️ 😮🤔

SEMANA TRAS SEMANA. SIN FALTAR. 🏆

Solo necesitas dar el salto y empezar a tomar acción. 🚀

💰 [**HAZ CLIC AQUÍ PARA EMPEZAR A GANAR AHORA**](https://t.me/m/q3-XLmhBNmY0) 💰',0,'NONE',NULL,'2026-08-14 18:17:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(683,7725,-1002763662248,'Chartoro FX Señales Gratis','💎  [**SEÑALES VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)  💎',0,'NONE',NULL,'2026-08-14 22:01:40.000000');
INSERT INTO "raw_telegram_messages" VALUES(684,7726,-1002763662248,'Chartoro FX Señales Gratis','**Las personas llegan al VIP por diferentes razones.**

Algunos quieren ganancias diarias 💰
Otros quieren mejorar sus habilidades 📈

**EL VIP LES DA AMBAS**, señales de alta calidad y el tipo de entrenamiento que realmente eleva a los traders 💪

‼️ [**OBTÉN AMBAS AHORA**](https://t.me/m/q3-XLmhBNmY0) ‼️',0,'NONE',NULL,'2026-08-15 00:18:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(685,7728,-1002763662248,'Chartoro FX Señales Gratis','**Cuánto ganaste esta semana?** 🤔',0,'NONE',NULL,'2026-08-15 02:55:37.000000');
INSERT INTO "raw_telegram_messages" VALUES(686,7729,-1002763662248,'Chartoro FX Señales Gratis','🚨 **EL VERDADERO CÓDIGO SECRETO?**

__No es solo copiar señales…__
**sino aprender por qué funcionan mientras ganas con ellas** 📈

**EL VIP TE DA LAS SEÑALES Y LA GUÍA COMPLETA DE LA A–Z PARA QUE EVOLUCIONES MIENTRAS GENERAS BENEFICIOS** 💵💵💵',0,'NONE',NULL,'2026-08-15 03:51:19.000000');
INSERT INTO "raw_telegram_messages" VALUES(687,7732,-1002763662248,'Chartoro FX Señales Gratis','🚀 **HORA DE Q&A!** 🚀

Estoy respondiendo todas las preguntas VIP ahora mismo.
**Envíalas aquí → ****@SoporteChartoroFX**',0,'NONE',NULL,'2026-08-15 11:01:51.000000');
INSERT INTO "raw_telegram_messages" VALUES(688,7733,-1002763662248,'Chartoro FX Señales Gratis','🎯 **PRECISIÓN, DISCIPLINA Y SOPORTE**

En el VIP obtienes:
✔️ Setups listos para ejecutar
✔️ Explicación detrás de cada entrada
✔️ Gestión de riesgo clara
✔️ Acompañamiento diario

🚀 [**ACCESO DISPONIBLE**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-15 13:10:18.000000');
INSERT INTO "raw_telegram_messages" VALUES(689,7734,-1002763662248,'Chartoro FX Señales Gratis','✨ [**RECLAMA ACCESO VIP GRATIS Y BENEFICIOS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)  ✨',0,'NONE',NULL,'2026-08-15 14:30:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(690,7735,-1002763662248,'Chartoro FX Señales Gratis','"**LUIS, ESTO ES UNA ESTAFA?**” ⚠️

__Esta es una pregunta que recibo mucho...__
**Déjame mostrarte cuánto han ganado algunos miembros del VIP solo en estas primeras dos semanas del mes** ⬇️⬇️⬇️',0,'NONE',NULL,'2026-08-15 15:19:29.000000');
INSERT INTO "raw_telegram_messages" VALUES(691,7736,-1002763662248,'Chartoro FX Señales Gratis','Foto de DAN ROBERT',0,'NONE',NULL,'2026-08-15 15:24:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(692,7737,-1002763662248,'Chartoro FX Señales Gratis','Mi Resultado de hoy . Gracias ChartoroFax',0,'NONE',NULL,'2026-08-15 15:24:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(693,7739,-1002763662248,'Chartoro FX Señales Gratis','Súper!!',0,'NONE',NULL,'2026-08-15 15:27:54.000000');
INSERT INTO "raw_telegram_messages" VALUES(694,7740,-1002763662248,'Chartoro FX Señales Gratis','Muchas gracias excelente señal',0,'NONE',NULL,'2026-08-15 15:28:53.000000');
INSERT INTO "raw_telegram_messages" VALUES(695,7741,-1002763662248,'Chartoro FX Señales Gratis','Mi profit hoy',0,'NONE',NULL,'2026-08-15 15:30:03.000000');
INSERT INTO "raw_telegram_messages" VALUES(696,7743,-1002763662248,'Chartoro FX Señales Gratis','Mis ganancias del día de hoy , cerré antes pero fueron ganancias , gracias por tus señales amigo',0,'NONE',NULL,'2026-08-15 15:32:36.000000');
INSERT INTO "raw_telegram_messages" VALUES(697,7744,-1002763662248,'Chartoro FX Señales Gratis','Ahí vamos amigo Luis, paso a paso',0,'NONE',NULL,'2026-08-15 15:35:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(698,7745,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA GANAR COMO ELLOS**](https://t.me/m/q3-XLmhBNmY0) 🔼💵',0,'NONE',NULL,'2026-08-15 15:39:18.000000');
INSERT INTO "raw_telegram_messages" VALUES(699,7747,-1002763662248,'Chartoro FX Señales Gratis','Vamos mejorando',0,'NONE',NULL,'2026-08-15 21:11:36.000000');
INSERT INTO "raw_telegram_messages" VALUES(700,7748,-1002763662248,'Chartoro FX Señales Gratis','Estamos por buen camino',0,'NONE',NULL,'2026-08-15 21:11:36.000000');
INSERT INTO "raw_telegram_messages" VALUES(701,7749,-1002763662248,'Chartoro FX Señales Gratis','Gracias de verdad',0,'NONE',NULL,'2026-08-15 21:11:37.000000');
INSERT INTO "raw_telegram_messages" VALUES(702,7751,-1002763662248,'Chartoro FX Señales Gratis','Quiero compartir esto Luis! Todo empezó por tí y tú guía y consejos. Esto en una semana siguiéndote',0,'NONE',NULL,'2026-08-15 21:23:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(703,7752,-1002763662248,'Chartoro FX Señales Gratis','Muchas gracias luis!! Un dia excelente',0,'NONE',NULL,'2026-08-15 21:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(704,7753,-1002763662248,'Chartoro FX Señales Gratis','En 5 días. ¡Eres muy grande!',0,'NONE',NULL,'2026-08-15 21:31:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(705,7754,-1002763662248,'Chartoro FX Señales Gratis','**TÚ TAMBIÉN PODRÍAS ESTAR GANANDO ESTO **🔥',0,'NONE',NULL,'2026-08-16 00:32:14.000000');
INSERT INTO "raw_telegram_messages" VALUES(706,7755,-1002763662248,'Chartoro FX Señales Gratis','**QUIERES GANANCIAS COMO ESTAS?**  💵💵💵

‼️ [**HAZ CLIC AQUÍ PARA RECLAMAR VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0) ‼️',0,'NONE',NULL,'2026-08-16 00:33:54.000000');
INSERT INTO "raw_telegram_messages" VALUES(707,7756,-1002763662248,'Chartoro FX Señales Gratis','__Esto es lo que hace que todo valga la pena.__ 🚀 

De pasar por una situación difícil a ver resultados en el trading **que pueden ayudar con los gastos del hogar.** 🙏📈

🔥 **DEJA DE MIRAR DESDE AFUERA!** [**ÚNETE AL VIP AHORA Y EMPIEZA A GANAR!**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-16 01:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(708,7757,-1002763662248,'Chartoro FX Señales Gratis','[**Ⓘ LUIS TE MENCIONÓ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-16 02:58:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(709,7758,-1002763662248,'Chartoro FX Señales Gratis','⭐️ **BENEFICIOS VIP** ⭐️

⏩ 4–8 señales de trading de alta calidad al día
⏩ Un curso completo de trading
⏩ Una guía completa de la A a la Z para que sepas por qué funcionan las operaciones
⏩ Mentoría y acompañamiento real
⏩ Resultados comprobados que puedes seguir paso a paso',0,'NONE',NULL,'2026-08-16 03:22:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(710,7760,-1002763662248,'Chartoro FX Señales Gratis','Buenos días, queria agradecerle con las señales, de momento me fue bien ayer con el oro',0,'NONE',NULL,'2026-08-16 04:56:29.000000');
INSERT INTO "raw_telegram_messages" VALUES(711,7762,-1002763662248,'Chartoro FX Señales Gratis','Fueron más de 70 dólares, gracias...',0,'NONE',NULL,'2026-08-16 04:56:53.000000');
INSERT INTO "raw_telegram_messages" VALUES(712,7764,-1002763662248,'Chartoro FX Señales Gratis','**GANANCIAS REALES DE LOS VIPS DE CHARTORO** 💰👆

Muchos de ellos hicieron trading por primera vez este mes… **TÚ PODRÍAS SER EL PRÓXIMO!** 🫵',0,'NONE',NULL,'2026-08-16 04:59:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(713,7765,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ Y EMPIEZA A GANAR DINERO DESDE TU CELULAR AHORA**](https://t.me/m/q3-XLmhBNmY0) ‼️‼️',0,'NONE',NULL,'2026-08-16 05:01:38.000000');
INSERT INTO "raw_telegram_messages" VALUES(714,7766,-1002763662248,'Chartoro FX Señales Gratis','**Quieres ver los resultados de la semana pasada?** 🤔🤔',0,'NONE',NULL,'2026-08-16 06:36:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(715,7767,-1002763662248,'Chartoro FX Señales Gratis','**BUENOS DIAS TRADERS!!!**
__Publicando los resultados en…__',0,'NONE',NULL,'2026-08-16 10:13:29.000000');
INSERT INTO "raw_telegram_messages" VALUES(716,7768,-1002763662248,'Chartoro FX Señales Gratis','3️⃣',0,'NONE',NULL,'2026-08-16 10:18:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(717,7769,-1002763662248,'Chartoro FX Señales Gratis','2️⃣',0,'NONE',NULL,'2026-08-16 10:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(718,7770,-1002763662248,'Chartoro FX Señales Gratis','1️⃣',0,'NONE',NULL,'2026-08-16 10:33:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(719,7771,-1002763662248,'Chartoro FX Señales Gratis','📈 **RESULTADOS SEMANALES DE SEÑALES **📈
__10 de Agosto – 14 de Agosto, 2026__

💰 TOTAL: **+585 PIPS GANADOS** 💰

✔️ Win Ratio: 66% (16 ganadas / 7 perdidas)
✔️ Operaciones totales: 23 setups
✔️ Buy vs Sell: 6 compras / 17 ventas
✔️ XAUUSD volvió a destacar como uno de los instrumentos principales de la semana
✔️ Jueves (+165 pips), miércoles (+155 pips) y viernes (+125 pips) lideraron los resultados
✔️ Una semana más generando oportunidades en FOREX, GOLD y otros instrumentos

💰 **QUÉ SIGNIFICA ESTO EN DINERO REAL?**

• 0.01 lote → el valor depende del instrumento y del tamaño del contrato
• 0.10 lote → el valor depende del instrumento y del tamaño del contrato
• 1.00 lote → el valor depende del instrumento y del tamaño del contrato

💰 **+585 PIPS EN SOLO UNA SEMANA**

**QUIERES FORMAR PARTE DE LA COMUNIDAD Y RECIBIR LAS PRÓXIMAS SEÑALES?**

ESCRÍBEME “[**VIP**](https://t.me/m/q3-XLmhBNmY0)” POR PRIVADO Y TE EXPLICO CÓMO ACCEDER 🤑',0,'NONE',NULL,'2026-08-16 10:36:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(720,7773,-1002763662248,'Chartoro FX Señales Gratis','🚨 **VIP NO ES SOLO UNA SALA DE SEÑALES** 🚨

Es:
🔴 4–8 señales diarias de alta calidad
🔴 Un curso completo de trading
🔴 Rendimiento probado y transparente
🔴 Mentoría 24/7 cuando las decisiones realmente importan

Esa combinación es rara.
**POR ESO FUNCIONA ****❗️**

💥 [**ENTRA AL VIP AHORA**](https://t.me/m/q3-XLmhBNmY0) 💥',0,'NONE',NULL,'2026-08-16 12:29:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(721,7775,-1002763662248,'Chartoro FX Señales Gratis','El lunes no es estrés cuando operas con inteligencia — **es oportunidad **😎

Mientras la mayoría teme los lunes, **los traders VIP los esperan con ganas **📈
Ese es el poder de estar preparado.

‼️ [**HAZTE TRADER VIP AQUÍ**](https://t.me/m/q3-XLmhBNmY0) ‼️',0,'NONE',NULL,'2026-08-16 14:19:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(722,7776,-1002763662248,'Chartoro FX Señales Gratis','Corte y volvi a seguir la señal. Estuvo buenisimo. Logre un poco mas con tu señal. No es mucho pero crecer de apoco es lo ideal💪 vamos por mas',0,'NONE',NULL,'2026-08-16 16:03:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(723,7778,-1002763662248,'Chartoro FX Señales Gratis','Hermosa señal Luis',0,'NONE',NULL,'2026-08-16 16:03:30.000000');
INSERT INTO "raw_telegram_messages" VALUES(724,7779,-1002763662248,'Chartoro FX Señales Gratis','👀 Ver ganancias es una cosa 
**Ganarlas tú mismo es algo completamente diferente** 💰

**El VIP** es la diferencia entre ver y ganar 🤑

👉 [**HAZ CLIC AQUÍ PARA EMPEZAR A GANAR**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-08-16 16:05:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(725,7780,-1002763662248,'Chartoro FX Señales Gratis','**La oportunidad más simple que vas a encontrar está aquí** 

**SEÑALES + GUÍA = GANANCIAS INSTANTÁNEAS ****💵****💵****💵**

De verdad vas a quedarte fuera?

📊 [**RECLAMA SEÑALES Y GUÍA GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 📊',0,'NONE',NULL,'2026-08-16 17:04:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(726,7781,-1002763662248,'Chartoro FX Señales Gratis','No solo estás perdiendo ganancias…
**Estás perdiendo un sistema completo que a muchas personas les cuesta años descubrir:**

✔️ 4-8 señales de alta calidad diarias
✔️ Un curso de trading completo
✔️ Una guía de fundamentos de A a Z
✔️ Resultados respaldados por un rendimiento real
✔️ Soporte 24/7 cuando necesites orientación

Lo único que te está deteniendo es estar mirando desde afuera 👀

💎 [**ENTRA AL VIP AHORA**](https://t.me/m/q3-XLmhBNmY0)** **💎',0,'NONE',NULL,'2026-08-16 18:05:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(727,7782,-1002763662248,'Chartoro FX Señales Gratis','**Los nuevos miembros VIP ya están leyendo y viendo el curso antes de que abran los mercados el Lunes ****📚**',0,'NONE',NULL,'2026-08-16 19:08:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(728,7784,-1002763662248,'Chartoro FX Señales Gratis','Hola Luis, a veces es mejor asegurar🤭 vale más pájaro en la mano que 100 volando',0,'NONE',NULL,'2026-08-16 20:09:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(729,7786,-1002763662248,'Chartoro FX Señales Gratis','Gracias por tu señal Luis excelente!',0,'NONE',NULL,'2026-08-16 20:10:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(730,7787,-1002763662248,'Chartoro FX Señales Gratis','[**Y SI TE DIJERA QUE PUEDES GANAR DINERO CON SOLO UN SIMPLE COPIAR Y PEGAR????**](https://t.me/m/q3-XLmhBNmY0) 💵💵💵',0,'NONE',NULL,'2026-08-16 20:12:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(731,7788,-1002763662248,'Chartoro FX Señales Gratis','1️⃣ Copiar

2️⃣ Pegar

3️⃣ **GANAR DINERO** 💵💵💵',0,'NONE',NULL,'2026-08-16 21:05:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(732,7789,-1002763662248,'Chartoro FX Señales Gratis','Muchas personas se quedan en grupos gratis esperando…
__refrescando la pantalla por una señal, tal vez dos.__

**DENTRO DEL VIP, ES DIFERENTE** 😉
🏆4–8 señales de alta calidad al día.
➡️Más setups.
➡️Más oportunidades para ejecutar.
➡️Más espacio para gestionar el riesgo y construir consistencia.',0,'NONE',NULL,'2026-08-16 22:12:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(733,7790,-1002763662248,'Chartoro FX Señales Gratis','🔓  [**TOCA AQUÍ PARA OBTENER ACCESO GRATIS A LAS SEÑALES VIP**](https://t.me/m/q3-XLmhBNmY0)  🔓',0,'NONE',NULL,'2026-08-16 23:07:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(734,7791,-1002763662248,'Chartoro FX Señales Gratis','Pasas 20 minutos scrolleando? No ganas nada. 

Pasas 20 minutos operando? **GENERAS INGRESOS EXTRA.** 💰',0,'NONE',NULL,'2026-08-17 00:14:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(735,7792,-1002763662248,'Chartoro FX Señales Gratis','Gracias por señales',0,'NONE',NULL,'2026-08-17 01:03:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(736,7794,-1002763662248,'Chartoro FX Señales Gratis','Compartir',0,'NONE',NULL,'2026-08-17 01:07:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(737,7795,-1002763662248,'Chartoro FX Señales Gratis','‼️ [**OBTÉN SEÑALES GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0) ‼️',0,'NONE',NULL,'2026-08-17 01:32:24.000000');
INSERT INTO "raw_telegram_messages" VALUES(738,7796,-1002763662248,'Chartoro FX Señales Gratis','**SE HONESTO**… cuántas capturas has guardado “__por motivación__”?

**Mientras tanto, los miembros VIP están guardando sus propias capturas de ganancias** 💰💰

Puedes seguir siendo un espectador 👀
o puedes empezar a recoger las ganancias tú mismo 🤑

🫵 Tú decides 🫵

💵 [**HAZ CLICK AQUÍ PARA GANAR PROFIT**](https://t.me/m/q3-XLmhBNmY0) 💵',0,'NONE',NULL,'2026-08-17 02:02:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(739,7798,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4390
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-17 03:18:30.000000');
INSERT INTO "raw_telegram_messages" VALUES(740,7799,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#**XAUUSD**** **

**Direction: 📉 **#**BUY**** **

** Entry Point: **4390
**⛔️ Stop Loss (SL): **4382

**🏆 TP1: **4393
**🏆 TP2:** 4398
**🏆 TP3:** 4406

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-17 03:20:44.000000');
INSERT INTO "raw_telegram_messages" VALUES(741,7800,-1002763662248,'Chartoro FX Señales Gratis','**COMENZANDO EL DÍA CON MÁXIMA POTENCIA **🔥

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Reacción del precio rápida y precisa.__',0,'NONE',NULL,'2026-08-17 03:33:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(742,7802,-1002763662248,'Chartoro FX Señales Gratis','👀👀👀',0,'NONE',NULL,'2026-08-17 03:44:51.000000');
INSERT INTO "raw_telegram_messages" VALUES(743,7803,-1002763662248,'Chartoro FX Señales Gratis','**EL MOMENTUM ESTÁ EMPUJANDO CON FUERZA AHORA**',0,'NONE',NULL,'2026-08-17 04:02:35.000000');
INSERT INTO "raw_telegram_messages" VALUES(744,7804,-1002763662248,'Chartoro FX Señales Gratis','**LA TENDENCIA CONTINÚA SIN DUDAS **🚀

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__El precio se movió de forma fluida, siguiendo perfectamente el escenario.__',0,'NONE',NULL,'2026-08-17 04:04:53.000000');
INSERT INTO "raw_telegram_messages" VALUES(745,7806,-1002763662248,'Chartoro FX Señales Gratis','**VAMOSSSSS** 🤑🤑🤑',0,'NONE',NULL,'2026-08-17 04:07:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(746,7807,-1002763662248,'Chartoro FX Señales Gratis','[**TOCA PARA RECIBIR MÁS SEÑALES**](https://t.me/m/q3-XLmhBNmY0) 📲',0,'NONE',NULL,'2026-08-17 04:22:30.000000');
INSERT INTO "raw_telegram_messages" VALUES(747,7808,-1002763662248,'Chartoro FX Señales Gratis','Si sigues operando sin mentoría un lunes...
**ESTÁS ELIGIENDO EL MODO MÁS DIFÍCIL DE ESTE JUEGO** ‼️

**No hay excusas para eso** 🙄
**ÚNETE AL VIP GRATIS**  ➡️ @SoporteChartoroFX',0,'NONE',NULL,'2026-08-17 05:00:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(748,7809,-1002763662248,'Chartoro FX Señales Gratis','**CIERRE FUERTE **👑

**#XAUUSD**** TP3 HIT, +160 Pips 🏆**

__Ejecución disciplinada + condiciones de mercado favorables = resultados máximos.__',0,'NONE',NULL,'2026-08-17 07:33:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(749,7811,-1002763662248,'Chartoro FX Señales Gratis','**QUIERES CONSEGUIR MÚLTIPLES VICTORIAS COMO ESTAS? ** ⬆️⬆️',0,'NONE',NULL,'2026-08-17 09:58:20.000000');
INSERT INTO "raw_telegram_messages" VALUES(750,7812,-1002763662248,'Chartoro FX Señales Gratis','**EMPECEMOS BIEN EL DÍA **🚀🚀🚀',0,'NONE',NULL,'2026-08-17 10:20:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(751,7813,-1002763662248,'Chartoro FX Señales Gratis','Si llevas meses operando pero todavía te cuesta ser rentable...

**ESTA ES TU SEÑAL PARA SUBIR DE NIVEL EN EL VIP** 💰💰💰',0,'NONE',NULL,'2026-08-17 11:53:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(752,7814,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📈#XAUUSD📈

**Direction:📈** **#SELL**
**Entry Point**: 4396.69

🏆**TP1**: 4393.69
🏆**TP2**: 4386.69
🏆**TP3**: 4376.69

**⛔️ Stop Loss (SL)**: 4406.69

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Price about to breakout the vib line',1,'REGEX',NULL,'2026-08-17 11:55:36.000000');
INSERT INTO "raw_telegram_messages" VALUES(753,7815,-1002763662248,'Chartoro FX Señales Gratis','**EL ORO SE DESPERTÓ VIOLENTO **🔥**
**
**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Snipe rápido, dinero instantáneo __💰',0,'NONE',NULL,'2026-08-17 12:07:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(754,7816,-1002763662248,'Chartoro FX Señales Gratis','**SIN FRENOS EN ESTE MOVIMIENTO **🚀**
**
**#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__Rally directo, sin drama __👀',0,'NONE',NULL,'2026-08-17 12:29:38.000000');
INSERT INTO "raw_telegram_messages" VALUES(755,7817,-1002763662248,'Chartoro FX Señales Gratis','🚀 **BENEFICIOS VIP:**

✔️ 4–8 señales de trading de alta calidad al día
✔️ Un curso completo de trading
✔️ Una guía completa de la A a la Z para que sepas por qué funcionan las operaciones
✔️ Mentoría y acompañamiento real
✔️ Resultados comprobados que puedes seguir paso a paso

[**HAZ CLIC AQUÍ PARA OBTENER ESTOS BENEFICIOS**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-08-17 12:53:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(756,7818,-1002763662248,'Chartoro FX Señales Gratis','Si hubieras empezado hace 2 semanas, ya tendrías:

✔️ 2 semanas de setups guiados 
✔️ Más de 20 operaciones ejecutadas 
✔️ Ganancias reales para mostrar 

En cambio, estás en el día 14 de “pensarlo” 🤔🤔
No te falta tiempo… **__te falta compromiso__**.

⚠️  Únete antes de que otra semana se te escape 👉 [**VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-17 14:08:29.000000');
INSERT INTO "raw_telegram_messages" VALUES(757,7819,-1002763662248,'Chartoro FX Señales Gratis','**ACABO DE ENVIAR UNA SEÑAL EN EL VIP! **🚨📈',0,'NONE',NULL,'2026-08-17 15:29:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(758,7821,-1002763662248,'Chartoro FX Señales Gratis','Cada día guío a traders que alguna vez dudaron de que podían lograrlo.
Ahora son constantes, seguros y tienen estructura 💪💰

La única diferencia entre ellos y tú?
**ELLOS EMPEZARON.**

💎 [**EMPIEZA AHORA CON GUÍA VIP**](https://t.me/m/q3-XLmhBNmY0) 💎',0,'NONE',NULL,'2026-08-17 17:06:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(759,7822,-1002763662248,'Chartoro FX Señales Gratis','📈 [**APRENDE A HACER TRADING AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 📈',0,'NONE',NULL,'2026-08-17 18:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(760,7823,-1002763662248,'Chartoro FX Señales Gratis','Si tus resultados no están mejorando, es porque tus hábitos tampoco lo están 🥲

VIP te da los hábitos primero — las ganancias siguen después 💰💰💰

[**VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-17 19:07:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(761,7824,-1002763662248,'Chartoro FX Señales Gratis','TEAM PROFIT',0,'NONE',NULL,'2026-08-17 20:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(762,7825,-1002763662248,'Chartoro FX Señales Gratis','**Las señales**__ te ponen dentro...__
**La educación **__te mantiene constante__
**La mentoría** __te mantiene enfocado__

El VIP no es solo una cosa — **ES TODO EL SISTEMA** 💯

👉  [**HAZ CLIC AQUÍ PARA RECLAMAR UN CUPO GRATIS EN EL VIP**](https://t.me/m/q3-XLmhBNmY0) 👈',0,'NONE',NULL,'2026-08-17 21:08:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(763,7826,-1002763662248,'Chartoro FX Señales Gratis','Puedes pasar otra semana buscando “__la estrategia perfecta__”…
**o puedes unirte a un equipo que ya usa una que funciona** 🔥',0,'NONE',NULL,'2026-08-17 22:05:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(764,7827,-1002763662248,'Chartoro FX Señales Gratis','**CANSADO DE VIVIR DE QUINCENA EN QUINCENA?**  😫😫

✨ [**CAMBIA TU VIDA HOY**](https://t.me/m/q3-XLmhBNmY0) ✨',0,'NONE',NULL,'2026-08-17 22:23:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(765,7828,-1002763662248,'Chartoro FX Señales Gratis','__La mayoría de los miembros del VIP empezaron como principiantes.__..

Simplemente copiaron la primera señal y se dieron cuenta de lo **RIDÍCULAMENTE FÁCIL **que es 🤑🤑

Ahora te toca a ti — [**HAZ CLIC AQUÍ PARA COPIAR LAS SEÑALES VIP**](https://t.me/m/q3-XLmhBNmY0) 🕯',0,'NONE',NULL,'2026-08-17 23:10:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(766,7830,-1002763662248,'Chartoro FX Señales Gratis','💰 [**OBTÉN SEÑALES VIP AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 💰',0,'NONE',NULL,'2026-08-18 00:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(767,7831,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4430
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-18 00:34:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(768,7832,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point: **4430
**⛔️ Stop Loss (SL): **4422

**🏆 TP1: **4433
**🏆 TP2:** 4438
**🏆 TP3:** 4446

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-18 00:37:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(769,7833,-1002763662248,'Chartoro FX Señales Gratis','**PRIMER TOQUE EN CAMINO ****🔥**',0,'NONE',NULL,'2026-08-18 00:39:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(770,7834,-1002763662248,'Chartoro FX Señales Gratis','**EL CHART HIZO SU TRABAJO **😎

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Ganancia fácil __💰',0,'NONE',NULL,'2026-08-18 00:42:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(771,7836,-1002763662248,'Chartoro FX Señales Gratis','Esto ya es otra cosa!!! 👌💰💸🙌',0,'NONE',NULL,'2026-08-18 01:03:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(772,7837,-1002763662248,'Chartoro FX Señales Gratis','❗️ [**HAZ CLIC AQUÍ SI ERES UN TRADER PRINCIPIANTE Y NECESITAS AYUDA**](https://t.me/m/q3-XLmhBNmY0) ❗️',0,'NONE',NULL,'2026-08-18 01:40:08.000000');
INSERT INTO "raw_telegram_messages" VALUES(773,7838,-1002763662248,'Chartoro FX Señales Gratis','**ESTO NO ES SUERTE. ES UN SISTEMA.** 💯

Si te tomas en serio mejorar tu consistencia y operar con estructura, mándame un mensaje ➡️ @SoporteChartoroFX',0,'NONE',NULL,'2026-08-18 02:30:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(774,7839,-1002763662248,'Chartoro FX Señales Gratis','COPIAR OPERACIONES 
              ➕
APRENDER EL SISTEMA
              ➕
HACER PREGUNTAS EN CUALQUIER MOMENTO 
              ➕
CONSTRUIR CONFIANZA 
              ➕
GANAR MIENTRAS APRENDES 

              🟰
              
        🏆 [**VIP**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-08-18 03:15:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(775,7841,-1002763662248,'Chartoro FX Señales Gratis','**El grupo VIP de CHARTOROFX ha estado creciendo y creciendo ****📈****📈****📈**
__Gracias a todos por ser parte de nuestra comunidad __🙏',0,'NONE',NULL,'2026-08-18 06:25:48.000000');
INSERT INTO "raw_telegram_messages" VALUES(776,7843,-1002763662248,'Chartoro FX Señales Gratis','❓ **PREGUNTA RÁPIDA: **__Cuánto tiempo dedicas al trading cada semana?__',0,'NONE',NULL,'2026-08-18 11:57:24.000000');
INSERT INTO "raw_telegram_messages" VALUES(777,7844,-1002763662248,'Chartoro FX Señales Gratis','**ASÍ ES COMO LOS MIEMBROS VIP SE MANTIENEN EN LA CIMA:**

✅ 4–8 señales premium todos los días
✅ Profundizando en el curso completo de trading de 5 horas
✅ Señales confiables con 80% de efectividad
✅ Soporte 24/7 para que nunca te quedes solo

**QUIERES ESTAR EN LA CIMA?** 
🏆 [**HAZ CLIC AQUÍ PARA RECLAMAR TODOS LOS BENEFICIOS VIP**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-08-18 12:28:42.000000');
INSERT INTO "raw_telegram_messages" VALUES(778,7845,-1002763662248,'Chartoro FX Señales Gratis','**YA TIENES LAS NOTIFICACIONES ACTIVADAS? **🔔🔔🔔',0,'NONE',NULL,'2026-08-18 14:01:14.000000');
INSERT INTO "raw_telegram_messages" VALUES(779,7847,-1002763662248,'Chartoro FX Señales Gratis','Mi hermano que señal 🔥🔥🔥👌🏻👌🏻👌🏻',0,'NONE',NULL,'2026-08-18 15:21:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(780,7848,-1002763662248,'Chartoro FX Señales Gratis','[**‼️**](https://t.me/m/q3-XLmhBNmY0) [**HAZ CLIC AQUÍ ANTES DE QUE SALGA LA PRÓXIMA SEÑAL VIP ‼️**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-18 15:22:21.000000');
INSERT INTO "raw_telegram_messages" VALUES(781,7849,-1002763662248,'Chartoro FX Señales Gratis','🚨 **ALERTA DE OPERACIÓN VIP! **🚨',0,'NONE',NULL,'2026-08-18 15:25:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(782,7850,-1002763662248,'Chartoro FX Señales Gratis','➡️ [**HAZ CLIC AQUÍ PARA VER**](https://t.me/m/q3-XLmhBNmY0)  👀',0,'NONE',NULL,'2026-08-18 15:26:28.000000');
INSERT INTO "raw_telegram_messages" VALUES(783,7851,-1002763662248,'Chartoro FX Señales Gratis','__OTRA SEÑAL ACABA DE SALIR EN EL VIP!!!!__ 🔥
**TE LA ESTÁS PERDIENDO!!**',0,'NONE',NULL,'2026-08-18 15:33:46.000000');
INSERT INTO "raw_telegram_messages" VALUES(784,7852,-1002763662248,'Chartoro FX Señales Gratis','No espero que lo sepas todo...
**ESE ES MI TRABAJO** 📈😎

Tu trabajo dentro del VIP es simple:
**sigue las señales,
aprende el sistema,
haz preguntas cuando tengas dudas.**

👑 [**SÉ VIP**](https://t.me/m/q3-XLmhBNmY0) 👑',0,'NONE',NULL,'2026-08-18 17:22:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(785,7853,-1002763662248,'Chartoro FX Señales Gratis','🔤🔤🔤   🔤🔤🔤🔤🔤🔤🔤 9️⃣',0,'NONE',NULL,'2026-08-18 19:23:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(786,7854,-1002763662248,'Chartoro FX Señales Gratis','⚡** SEÑALES VIP GRATIS

****📕**** MATERIAL EDUCATIVO GRATIS

**🧠** MENTORÍA GRATIS**


👉 [** RECLAMA AQUÍ 👈**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-18 21:27:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(787,7855,-1002763662248,'Chartoro FX Señales Gratis','🔤🔤🔤   🔤🔤🔤🔤🔤🔤🔤 6️⃣',0,'NONE',NULL,'2026-08-18 23:07:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(788,7856,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4330
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-19 01:03:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(789,7857,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4330
**⛔️ Stop Loss (SL): **4338

**🏆 TP1: **4327
**🏆 TP2:** 4322
**🏆 TP3:** 4314

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-19 01:05:21.000000');
INSERT INTO "raw_telegram_messages" VALUES(790,7858,-1002763662248,'Chartoro FX Señales Gratis','**EL MERCADO SUSURRÓ… NOSOTROS ESCUCHAMOS 👀

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Entrada suave, reacción instantánea __💰',0,'NONE',NULL,'2026-08-19 01:06:40.000000');
INSERT INTO "raw_telegram_messages" VALUES(791,7859,-1002763662248,'Chartoro FX Señales Gratis','[**__HAZ CLIC AQUÍ PARA GENERAR NUEVOS INGRESOS ESTE AGOSTO__**](https://t.me/m/q3-XLmhBNmY0)  ✨',0,'NONE',NULL,'2026-08-19 01:29:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(792,7860,-1002763662248,'Chartoro FX Señales Gratis','**ERES PRINCIPIANTE?

OBTÉN TODOS MIS TIPS Y TRUCOS EN EL VIP Y TE CONVERTIRÁS EN UN TRADER PRO EN POCO TIEMPO **🚀🚀🚀

➡️ [**ACCESO VIP GRATIS AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-19 03:11:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(793,7861,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4358
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-19 03:38:30.000000');
INSERT INTO "raw_telegram_messages" VALUES(794,7862,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#**XAUUSD**** **

**Direction: 📉 **#**BUY**** **

** Entry Point: **4358
**⛔️ Stop Loss (SL): **4349

**🏆 TP1: **4361
**🏆 TP2: **4366
**🏆 TP3:** 4374

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-19 03:43:31.000000');
INSERT INTO "raw_telegram_messages" VALUES(795,7863,-1002763662248,'Chartoro FX Señales Gratis','**❌ SL HIT**

Darle más espacio a la operación no ayudó esta vez.

No pasa nada — seguiré buscando una nueva configuración clara 🔎

Manténganse pacientes, equipo. Operamos con inteligencia, no con prisas. ✅',0,'NONE',NULL,'2026-08-19 04:40:51.000000');
INSERT INTO "raw_telegram_messages" VALUES(796,7864,-1002763662248,'Chartoro FX Señales Gratis','🔤🔤🔤   🔤🔤🔤🔤🔤🔤🔤 1️⃣',0,'NONE',NULL,'2026-08-19 04:45:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(797,7865,-1002763662248,'Chartoro FX Señales Gratis','**Imagina esto:** dentro de 90 días, tu cuenta ha crecido de manera constante siguiendo exactamente las operaciones que enviamos cada día en VIP 📈💰

O dentro de 90 días, sigues atrapado en el grupo gratuito viendo cómo otros avanzan y te dejan atrás 🤔

👉 @SoporteChartoroFX',0,'NONE',NULL,'2026-08-19 06:20:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(798,7867,-1002763662248,'Chartoro FX Señales Gratis','Si estás confundido con el trading, abrumado
o atrapado viendo cómo otros ganan…
**AHORA es el mejor momento para cambiar eso** 😉

❓ __Haz las preguntas.
____👨‍🏫__ __Recibe la guía.__
**Únete a personas que realmente están aprendiendo y ganando al mismo tiempo** 💰💰💰

SI QUIERES MENTORÍA, [**HAZ CLICK AQUÍ**](https://t.me/m/q3-XLmhBNmY0)! 👈',0,'NONE',NULL,'2026-08-19 09:53:14.000000');
INSERT INTO "raw_telegram_messages" VALUES(799,7868,-1002763662248,'Chartoro FX Señales Gratis','TEAM PROFIT',0,'NONE',NULL,'2026-08-19 11:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(800,7869,-1002763662248,'Chartoro FX Señales Gratis','**Los miembros VIP ya tienen:**

✅ 4–8 señales premium hoy
✅ Configuraciones con 80% de efectividad
✅ Acceso completo al curso
✅ Soporte 24/7',0,'NONE',NULL,'2026-08-19 13:21:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(801,7870,-1002763662248,'Chartoro FX Señales Gratis','⚠️ **La mitad de la semana se fue.**
**LA MITAD DE LAS OPORTUNIDADES TAMBIÉN** ‼️

Pero los miembros VIP ya aprovecharon las suyas — y anotaron una y otra vez 📈📈📈
Y tú qué hiciste? 🙄

🏆 [**HAZ CLICK AQUÍ PARA ACCESO VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0) 🏆',0,'NONE',NULL,'2026-08-19 15:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(802,7871,-1002763662248,'Chartoro FX Señales Gratis','❓ **Ya tienes un mentor de trading?**',0,'NONE',NULL,'2026-08-19 17:10:30.000000');
INSERT INTO "raw_telegram_messages" VALUES(803,7872,-1002763662248,'Chartoro FX Señales Gratis','1️⃣ Copiar

2️⃣ Pegar

3️⃣ **GANAR DINERO** 💵💵💵

**DE VERDAD VAS A RECHAZAR ESO??? ****🤯****🤯**',0,'NONE',NULL,'2026-08-19 19:04:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(804,7873,-1002763662248,'Chartoro FX Señales Gratis','Muchas gracias ❤️',0,'NONE',NULL,'2026-08-19 21:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(805,7874,-1002763662248,'Chartoro FX Señales Gratis','**Copiar las señales dentro del VIP y empezar a ganar de inmediato** 💵💵💵

👑 [**HAZ CLIC AQUÍ PARA UNIRTE AHORA**](https://t.me/m/q3-XLmhBNmY0) 👑',0,'NONE',NULL,'2026-08-19 22:38:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(806,7875,-1002763662248,'Chartoro FX Señales Gratis','🔠 **SEÑALES VIP GRATIS**

**🔠** **MATERIAL EDUCATIVO GRATIS**

**🔠** **MENTORÍA GRATIS**

[**RECLAMA AQUÍ**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-20 02:14:20.000000');
INSERT INTO "raw_telegram_messages" VALUES(807,7876,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4491
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-20 02:47:19.000000');
INSERT INTO "raw_telegram_messages" VALUES(808,7877,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4491
**⛔️ Stop Loss (SL): **4499

**🏆 TP1: **4488
**🏆 TP2:** 4483
**🏆 TP3:** 4475

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-20 02:47:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(809,7878,-1002763662248,'Chartoro FX Señales Gratis','Move SL to 4501',1,'REGEX',NULL,'2026-08-20 03:05:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(810,7879,-1002763662248,'Chartoro FX Señales Gratis','**TP1 CARGANDO… VAMOS! ****🚀**',0,'NONE',NULL,'2026-08-20 03:12:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(811,7880,-1002763662248,'Chartoro FX Señales Gratis','**GANANCIAS TEMPRANAS ASEGURADAS ****🔥****

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Reacción rápida, toma limpia ____💰__',0,'NONE',NULL,'2026-08-20 03:14:25.000000');
INSERT INTO "raw_telegram_messages" VALUES(812,7882,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD BUY NOW 4498
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-20 04:01:10.000000');
INSERT INTO "raw_telegram_messages" VALUES(813,7883,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📉 **#BUY** **

** Entry Point:** 4498
**⛔️ Stop Loss (SL): **4490

**🏆 TP1: **4501
**🏆 TP2:** 4506
**🏆 TP3:** 4514

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-20 04:03:35.000000');
INSERT INTO "raw_telegram_messages" VALUES(814,7884,-1002763662248,'Chartoro FX Señales Gratis','Move SL to 4488',1,'REGEX',NULL,'2026-08-20 04:29:30.000000');
INSERT INTO "raw_telegram_messages" VALUES(815,7885,-1002763662248,'Chartoro FX Señales Gratis','**❌ SL HIT**

Darle más espacio a la operación no ayudó esta vez.

No pasa nada — seguiré buscando una nueva configuración clara 🔎

Manténganse pacientes, equipo. Operamos con inteligencia, no con prisas. ✅',0,'NONE',NULL,'2026-08-20 04:35:40.000000');
INSERT INTO "raw_telegram_messages" VALUES(816,7886,-1002763662248,'Chartoro FX Señales Gratis','**Dónde has visto este nivel de transparencia en un grupo de señales?**

__Si encuentras un grupo que afirma tener un 100% de aciertos, mejor sal corriendo... __ 🏃',0,'NONE',NULL,'2026-08-20 06:34:06.000000');
INSERT INTO "raw_telegram_messages" VALUES(817,7887,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA UNIRTE AL MÁS REAL DE LOS GRUPOS VIP**](https://t.me/m/q3-XLmhBNmY0)  💎',0,'NONE',NULL,'2026-08-20 06:34:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(818,7888,-1002763662248,'Chartoro FX Señales Gratis','**BUENOS DIAS CHARTORO TRADERS** 👑',0,'NONE',NULL,'2026-08-20 10:17:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(819,7889,-1002763662248,'Chartoro FX Señales Gratis','❓__Te gustaría tener acceso a estrategias de trading exclusivas?__',0,'NONE',NULL,'2026-08-20 12:02:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(820,7890,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4463.20

🏆**TP1**: 4466.20
🏆**TP2**: 4473.20
🏆**TP3**: 4483.20

**⛔️ Stop Loss (SL)**: 4453.20

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-20 12:41:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(821,7891,-1002763662248,'Chartoro FX Señales Gratis','**Y EXPLOTÓ… RÁPIDO 💥**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Parpadeas y ya desapareció.__',0,'NONE',NULL,'2026-08-20 12:45:44.000000');
INSERT INTO "raw_telegram_messages" VALUES(822,7892,-1002763662248,'Chartoro FX Señales Gratis','**Y AHORA ESTÁ EN MODO PERSECUCIÓN TOTAL 🏃‍♂️

****#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El impulso se está saliendo de control.__',0,'NONE',NULL,'2026-08-20 12:53:12.000000');
INSERT INTO "raw_telegram_messages" VALUES(823,7893,-1002763662248,'Chartoro FX Señales Gratis','**TODO A FONDO… SIN VUELTA ATRÁS 🚀

****#XAUUSD**** TP3 HIT, +200 Pips 🏆**

__Desde una entrada temprana hasta una dominación total.__',0,'NONE',NULL,'2026-08-20 13:03:52.000000');
INSERT INTO "raw_telegram_messages" VALUES(824,7894,-1002763662248,'Chartoro FX Señales Gratis','🏆 **EL VIP INCLUYE:**

✔️ De 4 a 8 señales diarias de trading de alta calidad
✔️ Curso completo de trading
✔️ Guía completa A-a-Z para construir bases sólidas
✔️ Rendimiento comprobado de las señales basado en resultados reales
✔️ Soporte y mentoría 24/7
 
🚀 [**RECLAMA TU ACCESO AL VIP AQUÍ**](https://t.me/m/q3-XLmhBNmY0) 🚀',0,'NONE',NULL,'2026-08-20 14:19:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(825,7895,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA OPERAR CONMIGO**](https://t.me/m/q3-XLmhBNmY0) 📈📈📈',0,'NONE',NULL,'2026-08-20 16:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(826,7896,-1002763662248,'Chartoro FX Señales Gratis','**Para quién es el VIP?**

Para cualquiera listo para:
✅ Copiar señales reales
✅Aprender mientras gana
✅Operar con confianza',0,'NONE',NULL,'2026-08-20 18:22:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(827,7898,-1002763662248,'Chartoro FX Señales Gratis','**Por qué conformarte con una señal al día cuando puedes recibir 4-8 SEÑALES DIARIAS EN EL VIP** ⁉️⁉️⁉️',0,'NONE',NULL,'2026-08-21 00:01:38.000000');
INSERT INTO "raw_telegram_messages" VALUES(828,7899,-1002763662248,'Chartoro FX Señales Gratis','__Algunos entrarán con guía.
Otros entrarán adivinando.__

**El VIP está abierto para quienes ya no quieren adivinar.**

💎 [**HAZ CLIC AQUÍ PARA ACCESO GRATIS AL VIP**](https://t.me/m/q3-XLmhBNmY0) 💎',0,'NONE',NULL,'2026-08-21 02:24:16.000000');
INSERT INTO "raw_telegram_messages" VALUES(829,7900,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4527
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-21 02:34:27.000000');
INSERT INTO "raw_telegram_messages" VALUES(830,7901,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4527
**⛔️ Stop Loss (SL): **4535

**🏆 TP1: **4524
**🏆 TP2:** 4519
**🏆 TP3:** 4511

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-21 02:36:43.000000');
INSERT INTO "raw_telegram_messages" VALUES(831,7902,-1002763662248,'Chartoro FX Señales Gratis','❌ **SL HIT**

No todos los setups saldrán a nuestro favor, y desafortunadamente este terminó en pérdida.

Mantenemos la **transparencia con cada resultado**, tanto en las ganancias como en las pérdidas. Una correcta gestión del riesgo nos mantiene protegidos y preparados para la próxima oportunidad. 💪🏻

**__Aprendemos, reiniciamos y seguimos avanzando.__**',0,'NONE',NULL,'2026-08-21 02:46:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(832,7903,-1002763662248,'Chartoro FX Señales Gratis','__No solo recibes señales y transparencia...__

**TAMBIÉN OBTIENES MI MENTORÍA Y MATERIAL EDUCATIVO QUE TE AYUDARÁN AL 100% A CONVERTIRTE EN UN MEJOR TRADER, SIN IMPORTAR QUÉ!** 📈📈📈**
**
[**HAZ CLIC AQUÍ PARA SABER MÁS**](https://t.me/m/q3-XLmhBNmY0) ⚡️',0,'NONE',NULL,'2026-08-21 02:54:45.000000');
INSERT INTO "raw_telegram_messages" VALUES(833,7904,-1002763662248,'Chartoro FX Señales Gratis','Profit profe muchas gracias',0,'NONE',NULL,'2026-08-21 03:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(834,7906,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4532
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-21 03:28:55.000000');
INSERT INTO "raw_telegram_messages" VALUES(835,7907,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4532
**⛔️ Stop Loss (SL): **4540

**🏆 TP1: **4529
**🏆 TP2:** 4524
**🏆 TP3:** 4516

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-21 03:30:48.000000');
INSERT INTO "raw_telegram_messages" VALUES(836,7908,-1002763662248,'Chartoro FX Señales Gratis','**EL PRECIO EMPIEZA A IMPULSAR ****👀**',0,'NONE',NULL,'2026-08-21 03:40:50.000000');
INSERT INTO "raw_telegram_messages" VALUES(837,7909,-1002763662248,'Chartoro FX Señales Gratis','**DIRECTO A LAS GANANCIAS **⚡️

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Sesión recién iniciada y el movimiento llegó rápido.__',0,'NONE',NULL,'2026-08-21 03:42:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(838,7910,-1002763662248,'Chartoro FX Señales Gratis','👀👀👀',0,'NONE',NULL,'2026-08-21 05:02:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(839,7911,-1002763662248,'Chartoro FX Señales Gratis','**BUENOS DÍAS TRADERS!**

Cada operación es una pieza de tu crecimiento:

✔ Sigue tu plan aunque no veas resultados inmediatos
✔ Celebra las pequeñas victorias — son la base de las grandes
✔ No compares tu progreso con otros, compáralo con tu “yo” de ayer

**Tu objetivo no es ser perfecto, es ser consistente.**

Únete al VIP y construyamos esa confianza juntos
👉 @SoporteChartoroFX',0,'NONE',NULL,'2026-08-21 10:36:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(840,7912,-1002763662248,'Chartoro FX Señales Gratis','No necesitas operar más, **necesitas operar mejor** 🎯🎯🎯

Los miembros VIP se enfocan en setups de calidad, no en el ruido.
Por eso ganamos cuando otros entran en pánico.

➡️➡️ [GANA CON EL VIP](http://t.me/SoporteChartoroFX)',0,'NONE',NULL,'2026-08-21 12:22:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(841,7913,-1002763662248,'Chartoro FX Señales Gratis','🔤🔤🔤   🔤🔤🔤🔤🔤🔤',0,'NONE',NULL,'2026-08-21 14:15:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(842,7914,-1002763662248,'Chartoro FX Señales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4590.47

🏆**TP1**: 4593.47
🏆**TP2**: 4600.47
🏆**TP3**: 4610.47

**⛔️ Stop Loss (SL)**: 4580.47

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Same as the original idea',1,'REGEX',NULL,'2026-08-21 14:53:40.000000');
INSERT INTO "raw_telegram_messages" VALUES(843,7915,-1002763662248,'Chartoro FX Señales Gratis','**🔥 LOS BENEFICIOS HAN LLEGADO OTRA VEZ!**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Estructura clara, ejecución limpia, resultados reales 💰__',0,'NONE',NULL,'2026-08-21 15:05:41.000000');
INSERT INTO "raw_telegram_messages" VALUES(844,7917,-1002763662248,'Chartoro FX Señales Gratis','**EL MOVIMIENTO SIGUE CRECIENDO 🚀

****#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El impulso ahora está entrando con mucha fuerza.__',0,'NONE',NULL,'2026-08-21 15:25:19.000000');
INSERT INTO "raw_telegram_messages" VALUES(845,7918,-1002763662248,'Chartoro FX Señales Gratis','**Y BOOM… OBJETIVO FINAL ALCANZADO ****🤯****

****#XAUUSD**** TP3 HIT, +200 Pips 🏆**

__La paciencia dio grandes resultados ____💰__',0,'NONE',NULL,'2026-08-21 15:46:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(846,7920,-1002763662248,'Chartoro FX Señales Gratis','🔝 **VIP NO ES SOLO UNA SALA DE SEÑALES** 🔝

Es:
🔸 4–8 señales diarias de alta calidad
🔸 Un curso completo de trading
🔸 Rendimiento probado y transparente
🔸 Mentoría 24/7 cuando las decisiones realmente importan

Esa combinación es rara.
**POR ESO FUNCIONA ****✔️**',0,'NONE',NULL,'2026-08-21 18:20:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(847,7921,-1002763662248,'Chartoro FX Señales Gratis','❓ __Cuál ha sido tu mayor ganancia hasta ahora?__',0,'NONE',NULL,'2026-08-21 21:06:12.000000');
INSERT INTO "raw_telegram_messages" VALUES(848,7922,-1002763662248,'Chartoro FX Señales Gratis','Ningún trader logró ser consistente adivinando.
Por eso nos enfocamos en la estructura, el riesgo y la ejecución 💪🏼

Quieres resultados? **APRENDE CÓMO LO HACEMOS DENTRO DEL VIP** 🤑🤑🤑',0,'NONE',NULL,'2026-08-21 23:30:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(849,7924,-1002763662248,'Chartoro FX Señales Gratis','**2 NUEVOS MIEMBROS VIP ACABAN DE ELEGIR GANAR INGRESOS ADICIONALES MEDIANTE EL TRADING. VAMOS!** 🤑🤑🤑',0,'NONE',NULL,'2026-08-22 06:14:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(850,7926,-1002763662248,'Chartoro FX Señales Gratis','**CÓMO VA TU FIN DE SEMANA?**',0,'NONE',NULL,'2026-08-22 11:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(851,7927,-1002763662248,'Chartoro FX Señales Gratis','1️⃣ Copiar

2️⃣ Pegar

3️⃣ **GANAR DINERO** 💵💵💵',0,'NONE',NULL,'2026-08-22 13:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(852,7928,-1002763662248,'Chartoro FX Señales Gratis','🚀 **DENTRO DEL VIP, NO TIENES QUE ELEGIR ENTRE APRENDER O GANAR**

Copias de 4 a 8 señales diarias comprobadas mientras completas un curso de trading, y tienes acceso 24/7 a mentoría — para que cada operación construya habilidad, no solo ganancias.

**Si quieres progreso real, no victorias temporales, aquí es donde sucede** ✨

⬇️         ⬇️         ⬇️          ⬇️         ⬇️         ⬇️         ⬇️         ⬇️

[**HAZ CLIC AQUÍ PARA RECLAMAR TU ACCESO GRATIS AL VIP**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-22 15:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(853,7929,-1002763662248,'Chartoro FX Señales Gratis','💭 **REFLEXIÓN DE FIN DE SEMANA:**

Recuerdo cuando no tenía dirección y cada operación se sentía como una apuesta—__realmente no sabía lo que estaba haciendo.__ **No obtuve resultados de la noche a la mañana.** Tuve pérdidas, aprendí de la manera difícil __y seguí adelante.__

**Las cosas solo cambiaron cuando me lo tomé en serio y empecé a construir disciplina real, INCLUSO LOS FINES DE SEMANA.** 

**POR ESO SÉ EXACTAMENTE LO QUE SE NECESITA PARA GANAR AHORA** 🤑 🤑

Comparte tus experiencias [**AQUÍ **](https://t.me/m/q3-XLmhBNmY0)también!',0,'NONE',NULL,'2026-08-22 19:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(854,7930,-1002763662248,'Chartoro FX Señales Gratis','Así nos fue esta semana 🫡🫡🫡🫡',0,'NONE',NULL,'2026-08-22 21:45:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(855,7931,-1002763662248,'Chartoro FX Señales Gratis','**EL VIP TE DA:**

🟢 Señales VIP
🟢 Un curso de trading de 5 horas
🟢 Un sistema comprobado
🟢 Mentoría

💵 [**SUBE DE NIVEL CON VIP**](https://t.me/m/q3-XLmhBNmY0)  💵',0,'NONE',NULL,'2026-08-22 23:17:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(856,7932,-1002763662248,'Chartoro FX Señales Gratis','**QUIÉN AQUÍ AMA OPERAR ORO? ** **✨**',0,'NONE',NULL,'2026-08-23 01:10:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(857,7933,-1002763662248,'Chartoro FX Señales Gratis','👑 👑 👑',0,'NONE',NULL,'2026-08-23 03:11:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(858,7934,-1002763662248,'Chartoro FX Señales Gratis','Sabías que existe un grupo VIP donde comparto todas mis operaciones para que las copies GRATIS? ✅💵

Puedes acceder a mi grupo TOTALMENTE GRATIS ‼️

Envíame un mensaje 👉🏼 @SoporteChartoroFX',0,'NONE',NULL,'2026-08-23 05:02:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(859,7935,-1002763662248,'Chartoro FX Señales Gratis','[**⚠️**](https://t.me/m/q3-XLmhBNmY0) [**HAZ CLIC AQUÍ PARA RECIBIR DE 4 A 8 SEÑALES DIARIAS**](https://t.me/m/q3-XLmhBNmY0) [**⚠️**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-23 08:27:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(860,7936,-1002763662248,'Chartoro FX Señales Gratis','☀️ **BUENOS DÍAS TRADERS!** ☀️

__El descanso también es parte del plan.__

✔ Usa el fin de semana para revisar tus operaciones
✔ Ajusta tu mentalidad, no solo tus gráficos
✔ La claridad mental genera mejores decisiones el lunes

Hoy no se opera, pero sí se crece. 🌱
__Ya hiciste tu revisión semanal?__',0,'NONE',NULL,'2026-08-23 10:43:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(861,7937,-1002763662248,'Chartoro FX Señales Gratis','❓ __Cuánto tiempo dedicas al trading cada semana?__',0,'NONE',NULL,'2026-08-23 12:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(862,7938,-1002763662248,'Chartoro FX Señales Gratis','Qué pasaría si tu teléfono pudiera hacerte ganar dinero?

✅ 4–8 señales diarias para copiar y pegar
✅ Educación y soporte sencillos
✅ 100% gratis para unirte

No solo veas cómo otros ganan, empieza hoy 🚀💰',0,'NONE',NULL,'2026-08-23 13:00:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(863,7939,-1002763662248,'Chartoro FX Señales Gratis','**ESTÁS LISTO PARA VER LOS RESULTADOS DE LA SEMANA PASADA? **🔥📈',0,'NONE',NULL,'2026-08-23 16:14:23.000000');
INSERT INTO "raw_telegram_messages" VALUES(864,7940,-1002763662248,'Chartoro FX Señales Gratis','📈 **RESULTADOS SEMANALES DE SEÑALES **📈
__17 de Agosto – 21 de Agosto, 2026__

💰 TOTAL: **+732 PIPS GANADOS **💰

✔️ Win Ratio: 85% (16 ganadas / 3 perdidas)
✔️ Operaciones totales: 19 setups
✔️ Buy vs Sell: 10 compras / 9 ventas
✔️ XAUUSD volvió a destacar como uno de los instrumentos principales de la semana
✔️ Lunes (+321 pips), martes (+175 pips) y jueves (+160 pips) lideraron los resultados
✔️ Una semana más generando oportunidades en FOREX, GOLD y otros instrumentos

🤑 **QUÉ SIGNIFICA ESTO EN DINERO REAL?**

• 0.01 lote → el valor depende del instrumento y del tamaño del contrato
• 0.10 lote → el valor depende del instrumento y del tamaño del contrato
• 1.00 lote → el valor depende del instrumento y del tamaño del contrato

💰 **+732 PIPS EN SOLO UNA SEMANA**

__QUIERES RECIBIR LAS PRÓXIMAS SEÑALES Y SER PARTE DE LA COMUNIDAD?__',0,'NONE',NULL,'2026-08-23 18:32:23.000000');
INSERT INTO "raw_telegram_messages" VALUES(865,7942,-1002763662248,'Chartoro FX Señales Gratis','[**HAZ CLIC AQUÍ PARA GANAR COMO ELLOS**](https://t.me/m/q3-XLmhBNmY0)  🤑🤑🤑',0,'NONE',NULL,'2026-08-23 19:45:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(866,7943,-1002763662248,'Chartoro FX Señales Gratis','Pasas 20 minutos scrolleando? No ganas nada. 

Pasas 20 minutos operando? **GENERAS INGRESOS EXTRA.** 💰',0,'NONE',NULL,'2026-08-23 21:45:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(867,7945,-1002763662248,'Chartoro FX Señales Gratis','⬇️         ⬇️         ⬇️         ⬇️         ⬇️

                   **   **[**VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-24 01:02:37.000000');
INSERT INTO "raw_telegram_messages" VALUES(868,7946,-1002763662248,'Chartoro FX Señales Gratis','XAUUSD SELL NOW 4637
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-24 02:46:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(869,7947,-1002763662248,'Chartoro FX Señales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4637
**⛔️ Stop Loss (SL): **4645

**🏆 TP1: **4634
**🏆 TP2:** 4629
**🏆 TP3:** 4621

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-24 02:47:53.000000');
INSERT INTO "raw_telegram_messages" VALUES(870,7948,-1002763662248,'Chartoro FX Señales Gratis','**LA PRECISIÓN ENTREGA UNA VEZ MÁS ****⚡️**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__La paciencia fue recompensada, beneficios asegurados temprano ____🔥__',0,'NONE',NULL,'2026-08-24 02:51:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(871,7949,-1002763662248,'Chartoro FX Señales Gratis','**MOMENTUM A TODO RITMO ****💥**

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__Sin ruido, solo ejecución limpia ____😎__',0,'NONE',NULL,'2026-08-24 02:54:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(872,7950,-1002763662248,'Chartoro FX Señales Gratis','💵 [**HAZ CLIC AQUÍ PARA GANAR DINERO**](https://t.me/m/q3-XLmhBNmY0) 💵',0,'NONE',NULL,'2026-08-24 03:49:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(873,7951,-1002763662248,'Chartoro FX Señales Gratis','Así nos fue esta semana 🫡🫡🫡🫡',0,'NONE',NULL,'2026-08-24 06:38:17.000000');
INSERT INTO "raw_telegram_messages" VALUES(904,7918,-1002763662248,'Chartoro FX Señales Gratis','**DIRECTO A LAS GANANCIAS **⚡️

**#XAUUSD**** TP1 HIT, +68 Pips 🏆**

__Sesión de madrugada completada con éxito.__',0,'NONE',NULL,'2026-08-24 07:28:15.000000');
INSERT INTO "raw_telegram_messages" VALUES(905,7906,-1002763662248,'Chartoro FX Se?ales Gratis','XAUUSD SELL NOW 4532
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-21 03:28:55.000000');
INSERT INTO "raw_telegram_messages" VALUES(906,7907,-1002763662248,'Chartoro FX Se?ales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4532
**⛔️ Stop Loss (SL): **4540

**🏆 TP1: **4529
**🏆 TP2:** 4524
**🏆 TP3:** 4516

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-21 03:30:48.000000');
INSERT INTO "raw_telegram_messages" VALUES(907,7908,-1002763662248,'Chartoro FX Se?ales Gratis','**EL PRECIO EMPIEZA A IMPULSAR ****👀**',0,'NONE',NULL,'2026-08-21 03:40:50.000000');
INSERT INTO "raw_telegram_messages" VALUES(908,7909,-1002763662248,'Chartoro FX Se?ales Gratis','**DIRECTO A LAS GANANCIAS **⚡️

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Sesión recién iniciada y el movimiento llegó rápido.__',0,'NONE',NULL,'2026-08-21 03:42:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(909,7910,-1002763662248,'Chartoro FX Se?ales Gratis','👀👀👀',0,'NONE',NULL,'2026-08-21 05:02:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(910,7911,-1002763662248,'Chartoro FX Se?ales Gratis','**BUENOS DÍAS TRADERS!**

Cada operación es una pieza de tu crecimiento:

✔ Sigue tu plan aunque no veas resultados inmediatos
✔ Celebra las pequeñas victorias — son la base de las grandes
✔ No compares tu progreso con otros, compáralo con tu “yo” de ayer

**Tu objetivo no es ser perfecto, es ser consistente.**

Únete al VIP y construyamos esa confianza juntos
👉 @SoporteChartoroFX',0,'NONE',NULL,'2026-08-21 10:36:57.000000');
INSERT INTO "raw_telegram_messages" VALUES(911,7912,-1002763662248,'Chartoro FX Se?ales Gratis','No necesitas operar más, **necesitas operar mejor** 🎯🎯🎯

Los miembros VIP se enfocan en setups de calidad, no en el ruido.
Por eso ganamos cuando otros entran en pánico.

➡️➡️ [GANA CON EL VIP](http://t.me/SoporteChartoroFX)',0,'NONE',NULL,'2026-08-21 12:22:59.000000');
INSERT INTO "raw_telegram_messages" VALUES(912,7913,-1002763662248,'Chartoro FX Se?ales Gratis','🔤🔤🔤   🔤🔤🔤🔤🔤🔤',0,'NONE',NULL,'2026-08-21 14:15:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(913,7914,-1002763662248,'Chartoro FX Se?ales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4590.47

🏆**TP1**: 4593.47
🏆**TP2**: 4600.47
🏆**TP3**: 4610.47

**⛔️ Stop Loss (SL)**: 4580.47

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Same as the original idea',1,'REGEX',NULL,'2026-08-21 14:53:40.000000');
INSERT INTO "raw_telegram_messages" VALUES(914,7915,-1002763662248,'Chartoro FX Se?ales Gratis','**🔥 LOS BENEFICIOS HAN LLEGADO OTRA VEZ!**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Estructura clara, ejecución limpia, resultados reales 💰__',0,'NONE',NULL,'2026-08-21 15:05:41.000000');
INSERT INTO "raw_telegram_messages" VALUES(915,7917,-1002763662248,'Chartoro FX Se?ales Gratis','**EL MOVIMIENTO SIGUE CRECIENDO 🚀

****#XAUUSD**** TP2 HIT, +100 Pips 🏆**

__El impulso ahora está entrando con mucha fuerza.__',0,'NONE',NULL,'2026-08-21 15:25:19.000000');
INSERT INTO "raw_telegram_messages" VALUES(916,7918,-1002763662248,'Chartoro FX Se?ales Gratis','**Y BOOM… OBJETIVO FINAL ALCANZADO ****🤯****

****#XAUUSD**** TP3 HIT, +200 Pips 🏆**

__La paciencia dio grandes resultados ____💰__',0,'NONE',NULL,'2026-08-21 15:46:09.000000');
INSERT INTO "raw_telegram_messages" VALUES(917,7920,-1002763662248,'Chartoro FX Se?ales Gratis','🔝 **VIP NO ES SOLO UNA SALA DE SEÑALES** 🔝

Es:
🔸 4–8 señales diarias de alta calidad
🔸 Un curso completo de trading
🔸 Rendimiento probado y transparente
🔸 Mentoría 24/7 cuando las decisiones realmente importan

Esa combinación es rara.
**POR ESO FUNCIONA ****✔️**',0,'NONE',NULL,'2026-08-21 18:20:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(918,7921,-1002763662248,'Chartoro FX Se?ales Gratis','❓ __Cuál ha sido tu mayor ganancia hasta ahora?__',0,'NONE',NULL,'2026-08-21 21:06:12.000000');
INSERT INTO "raw_telegram_messages" VALUES(919,7922,-1002763662248,'Chartoro FX Se?ales Gratis','Ningún trader logró ser consistente adivinando.
Por eso nos enfocamos en la estructura, el riesgo y la ejecución 💪🏼

Quieres resultados? **APRENDE CÓMO LO HACEMOS DENTRO DEL VIP** 🤑🤑🤑',0,'NONE',NULL,'2026-08-21 23:30:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(920,7924,-1002763662248,'Chartoro FX Se?ales Gratis','**2 NUEVOS MIEMBROS VIP ACABAN DE ELEGIR GANAR INGRESOS ADICIONALES MEDIANTE EL TRADING. VAMOS!** 🤑🤑🤑',0,'NONE',NULL,'2026-08-22 06:14:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(921,7926,-1002763662248,'Chartoro FX Se?ales Gratis','**CÓMO VA TU FIN DE SEMANA?**',0,'NONE',NULL,'2026-08-22 11:02:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(922,7927,-1002763662248,'Chartoro FX Se?ales Gratis','1️⃣ Copiar

2️⃣ Pegar

3️⃣ **GANAR DINERO** 💵💵💵',0,'NONE',NULL,'2026-08-22 13:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(923,7928,-1002763662248,'Chartoro FX Se?ales Gratis','🚀 **DENTRO DEL VIP, NO TIENES QUE ELEGIR ENTRE APRENDER O GANAR**

Copias de 4 a 8 señales diarias comprobadas mientras completas un curso de trading, y tienes acceso 24/7 a mentoría — para que cada operación construya habilidad, no solo ganancias.

**Si quieres progreso real, no victorias temporales, aquí es donde sucede** ✨

⬇️         ⬇️         ⬇️          ⬇️         ⬇️         ⬇️         ⬇️         ⬇️

[**HAZ CLIC AQUÍ PARA RECLAMAR TU ACCESO GRATIS AL VIP**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-22 15:01:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(924,7929,-1002763662248,'Chartoro FX Se?ales Gratis','💭 **REFLEXIÓN DE FIN DE SEMANA:**

Recuerdo cuando no tenía dirección y cada operación se sentía como una apuesta—__realmente no sabía lo que estaba haciendo.__ **No obtuve resultados de la noche a la mañana.** Tuve pérdidas, aprendí de la manera difícil __y seguí adelante.__

**Las cosas solo cambiaron cuando me lo tomé en serio y empecé a construir disciplina real, INCLUSO LOS FINES DE SEMANA.** 

**POR ESO SÉ EXACTAMENTE LO QUE SE NECESITA PARA GANAR AHORA** 🤑 🤑

Comparte tus experiencias [**AQUÍ **](https://t.me/m/q3-XLmhBNmY0)también!',0,'NONE',NULL,'2026-08-22 19:33:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(925,7930,-1002763662248,'Chartoro FX Se?ales Gratis','Así nos fue esta semana 🫡🫡🫡🫡',0,'NONE',NULL,'2026-08-22 21:45:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(926,7931,-1002763662248,'Chartoro FX Se?ales Gratis','**EL VIP TE DA:**

🟢 Señales VIP
🟢 Un curso de trading de 5 horas
🟢 Un sistema comprobado
🟢 Mentoría

💵 [**SUBE DE NIVEL CON VIP**](https://t.me/m/q3-XLmhBNmY0)  💵',0,'NONE',NULL,'2026-08-22 23:17:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(927,7932,-1002763662248,'Chartoro FX Se?ales Gratis','**QUIÉN AQUÍ AMA OPERAR ORO? ** **✨**',0,'NONE',NULL,'2026-08-23 01:10:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(928,7933,-1002763662248,'Chartoro FX Se?ales Gratis','👑 👑 👑',0,'NONE',NULL,'2026-08-23 03:11:01.000000');
INSERT INTO "raw_telegram_messages" VALUES(929,7934,-1002763662248,'Chartoro FX Se?ales Gratis','Sabías que existe un grupo VIP donde comparto todas mis operaciones para que las copies GRATIS? ✅💵

Puedes acceder a mi grupo TOTALMENTE GRATIS ‼️

Envíame un mensaje 👉🏼 @SoporteChartoroFX',0,'NONE',NULL,'2026-08-23 05:02:11.000000');
INSERT INTO "raw_telegram_messages" VALUES(930,7935,-1002763662248,'Chartoro FX Se?ales Gratis','[**⚠️**](https://t.me/m/q3-XLmhBNmY0) [**HAZ CLIC AQUÍ PARA RECIBIR DE 4 A 8 SEÑALES DIARIAS**](https://t.me/m/q3-XLmhBNmY0) [**⚠️**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-23 08:27:00.000000');
INSERT INTO "raw_telegram_messages" VALUES(931,7936,-1002763662248,'Chartoro FX Se?ales Gratis','☀️ **BUENOS DÍAS TRADERS!** ☀️

__El descanso también es parte del plan.__

✔ Usa el fin de semana para revisar tus operaciones
✔ Ajusta tu mentalidad, no solo tus gráficos
✔ La claridad mental genera mejores decisiones el lunes

Hoy no se opera, pero sí se crece. 🌱
__Ya hiciste tu revisión semanal?__',0,'NONE',NULL,'2026-08-23 10:43:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(932,7937,-1002763662248,'Chartoro FX Se?ales Gratis','❓ __Cuánto tiempo dedicas al trading cada semana?__',0,'NONE',NULL,'2026-08-23 12:01:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(933,7938,-1002763662248,'Chartoro FX Se?ales Gratis','Qué pasaría si tu teléfono pudiera hacerte ganar dinero?

✅ 4–8 señales diarias para copiar y pegar
✅ Educación y soporte sencillos
✅ 100% gratis para unirte

No solo veas cómo otros ganan, empieza hoy 🚀💰',0,'NONE',NULL,'2026-08-23 13:00:04.000000');
INSERT INTO "raw_telegram_messages" VALUES(934,7939,-1002763662248,'Chartoro FX Se?ales Gratis','**ESTÁS LISTO PARA VER LOS RESULTADOS DE LA SEMANA PASADA? **🔥📈',0,'NONE',NULL,'2026-08-23 16:14:23.000000');
INSERT INTO "raw_telegram_messages" VALUES(935,7940,-1002763662248,'Chartoro FX Se?ales Gratis','📈 **RESULTADOS SEMANALES DE SEÑALES **📈
__17 de Agosto – 21 de Agosto, 2026__

💰 TOTAL: **+732 PIPS GANADOS **💰

✔️ Win Ratio: 85% (16 ganadas / 3 perdidas)
✔️ Operaciones totales: 19 setups
✔️ Buy vs Sell: 10 compras / 9 ventas
✔️ XAUUSD volvió a destacar como uno de los instrumentos principales de la semana
✔️ Lunes (+321 pips), martes (+175 pips) y jueves (+160 pips) lideraron los resultados
✔️ Una semana más generando oportunidades en FOREX, GOLD y otros instrumentos

🤑 **QUÉ SIGNIFICA ESTO EN DINERO REAL?**

• 0.01 lote → el valor depende del instrumento y del tamaño del contrato
• 0.10 lote → el valor depende del instrumento y del tamaño del contrato
• 1.00 lote → el valor depende del instrumento y del tamaño del contrato

💰 **+732 PIPS EN SOLO UNA SEMANA**

__QUIERES RECIBIR LAS PRÓXIMAS SEÑALES Y SER PARTE DE LA COMUNIDAD?__',0,'NONE',NULL,'2026-08-23 18:32:23.000000');
INSERT INTO "raw_telegram_messages" VALUES(936,7942,-1002763662248,'Chartoro FX Se?ales Gratis','[**HAZ CLIC AQUÍ PARA GANAR COMO ELLOS**](https://t.me/m/q3-XLmhBNmY0)  🤑🤑🤑',0,'NONE',NULL,'2026-08-23 19:45:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(937,7943,-1002763662248,'Chartoro FX Se?ales Gratis','Pasas 20 minutos scrolleando? No ganas nada. 

Pasas 20 minutos operando? **GENERAS INGRESOS EXTRA.** 💰',0,'NONE',NULL,'2026-08-23 21:45:07.000000');
INSERT INTO "raw_telegram_messages" VALUES(938,7945,-1002763662248,'Chartoro FX Se?ales Gratis','⬇️         ⬇️         ⬇️         ⬇️         ⬇️

                   **   **[**VIP GRATIS**](https://t.me/m/q3-XLmhBNmY0)',0,'NONE',NULL,'2026-08-24 01:02:37.000000');
INSERT INTO "raw_telegram_messages" VALUES(939,7946,-1002763662248,'Chartoro FX Se?ales Gratis','XAUUSD SELL NOW 4637
Set TP1 +30 Pips',1,'REGEX',NULL,'2026-08-24 02:46:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(940,7947,-1002763662248,'Chartoro FX Se?ales Gratis','**🚨 SIGNAL ALERT🚨**

**📊 **#XAUUSD** **

**Direction: 📈 **#SELL** **

** Entry Point: **4637
**⛔️ Stop Loss (SL): **4645

**🏆 TP1: **4634
**🏆 TP2:** 4629
**🏆 TP3:** 4621

**⚠️ **__Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__',1,'REGEX',NULL,'2026-08-24 02:47:53.000000');
INSERT INTO "raw_telegram_messages" VALUES(941,7948,-1002763662248,'Chartoro FX Se?ales Gratis','**LA PRECISIÓN ENTREGA UNA VEZ MÁS ****⚡️**

**#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__La paciencia fue recompensada, beneficios asegurados temprano ____🔥__',0,'NONE',NULL,'2026-08-24 02:51:33.000000');
INSERT INTO "raw_telegram_messages" VALUES(942,7949,-1002763662248,'Chartoro FX Se?ales Gratis','**MOMENTUM A TODO RITMO ****💥**

**#XAUUSD**** TP2 HIT, +80 Pips 🏆**

__Sin ruido, solo ejecución limpia ____😎__',0,'NONE',NULL,'2026-08-24 02:54:05.000000');
INSERT INTO "raw_telegram_messages" VALUES(943,7950,-1002763662248,'Chartoro FX Se?ales Gratis','💵 [**HAZ CLIC AQUÍ PARA GANAR DINERO**](https://t.me/m/q3-XLmhBNmY0) 💵',0,'NONE',NULL,'2026-08-24 03:49:02.000000');
INSERT INTO "raw_telegram_messages" VALUES(944,7951,-1002763662248,'Chartoro FX Se?ales Gratis','Así nos fue esta semana 🫡🫡🫡🫡',0,'NONE',NULL,'2026-08-24 06:38:17.000000');
INSERT INTO "raw_telegram_messages" VALUES(945,7953,-1002763662248,'Chartoro FX Se?ales Gratis','**HAS VISTO CUÁNTO PODRÍAS HABER GANADO LA SEMANA PASADA?**',0,'NONE',NULL,'2026-08-24 12:04:34.000000');
INSERT INTO "raw_telegram_messages" VALUES(946,7954,-1002763662248,'Chartoro FX Se?ales Gratis','⚠️ __SEÑAL ENVIADA EN EL VIP__ ⚠️',0,'NONE',NULL,'2026-08-24 12:51:14.000000');
INSERT INTO "raw_telegram_messages" VALUES(947,7955,-1002763662248,'Chartoro FX Se?ales Gratis','**❗️SIGNAL ALERT❗️**

📊#XAUUSD📊

**Direction:📈** **#BUY**
**Entry Point**: 4664.35

🏆**TP1**: 4667.35
🏆**TP2**: 4674.35
🏆**TP3**: 4684.35

**⛔️ Stop Loss (SL)**: 4654.35

⚠️ __Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!__

Analysis:
Price breakout the resistance zone',1,'REGEX',NULL,'2026-08-24 12:53:13.000000');
INSERT INTO "raw_telegram_messages" VALUES(948,7956,-1002763662248,'Chartoro FX Se?ales Gratis','**PRIMER GOLPE… PAGO INMEDIATO ****💥****

****#XAUUSD**** TP1 HIT, +30 Pips 🏆**

__Sin esperar, reacción directa.__',0,'NONE',NULL,'2026-08-24 12:56:50.000000');
CREATE TABLE system_audit_logs (
	id INTEGER NOT NULL, 
	timestamp DATETIME NOT NULL, 
	event_type VARCHAR(60) NOT NULL, 
	severity VARCHAR(20) NOT NULL, 
	details_json TEXT NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "system_audit_logs" VALUES(1,'2026-08-21 09:03:12.717881','RECONCILIATION_COMPLETED','WARNING','{"total_trades_checked": 3, "reconciled_slots": 0, "emergency_closed_slots": 3, "timestamp": "2026-08-21T09:03:12.717250+00:00"}');
CREATE TABLE trades (
	id INTEGER NOT NULL, 
	ticket_id VARCHAR(64) NOT NULL, 
	slot_id INTEGER NOT NULL, 
	symbol VARCHAR(20) NOT NULL, 
	side VARCHAR(4) NOT NULL, 
	status VARCHAR(26) NOT NULL, 
	entry_price NUMERIC(18, 4) NOT NULL, 
	current_sl NUMERIC(18, 4) NOT NULL, 
	initial_sl NUMERIC(18, 4) NOT NULL, 
	tp1 NUMERIC(18, 4) NOT NULL, 
	tp2 NUMERIC(18, 4), 
	tp3 NUMERIC(18, 4), 
	lot_size NUMERIC(10, 2) NOT NULL, 
	pnl NUMERIC(18, 2) NOT NULL, 
	close_price NUMERIC(18, 4), 
	close_reason VARCHAR(255), 
	open_time DATETIME NOT NULL, 
	close_time DATETIME, 
	raw_signal_id INTEGER, realized_cash_pnl NUMERIC(18, 2) DEFAULT 0.00, peak_price NUMERIC(18, 4), 
	PRIMARY KEY (id)
);
INSERT INTO "trades" VALUES(1,'TKT-REC-01',1,'XAUUSD','BUY','CLOSED_REBOOT_NO_MILESTONE',2340,2330,2330,2350,2360,2370,0.5,0,0,'REBOOT_NO_MILESTONE_EMERGENCY_CLOSE','2026-08-21 09:03:12.708236','2026-08-21 09:03:12.717078',NULL,0,NULL);
INSERT INTO "trades" VALUES(2,'TKT-REC-02',2,'XAUUSD','BUY','CLOSED_REBOOT_NO_MILESTONE',2340,2330,2330,2350,2360,2370,0.5,0,0,'REBOOT_NO_MILESTONE_EMERGENCY_CLOSE','2026-08-21 09:03:12.710097','2026-08-21 09:03:12.717171',NULL,0,NULL);
INSERT INTO "trades" VALUES(3,'TKT-REC-03',3,'XAUUSD','BUY','CLOSED_REBOOT_NO_MILESTONE',2340,2330,2330,2350,2360,2370,0.5,0,0,'REBOOT_NO_MILESTONE_EMERGENCY_CLOSE','2026-08-21 09:03:12.710135','2026-08-21 09:03:12.717246',NULL,0,NULL);
INSERT INTO "trades" VALUES(4,'TKT-CB8B1B92',1,'XAUUSD','BUY','CLOSED_TP',2340,2360,2330,2350,2360,2370,0.5,1247.5,2370.5,'TP_FINAL_REACHED (2370.00)','2026-08-21 09:03:12.731351','2026-08-21 09:03:12.737910',NULL,0,NULL);
CREATE INDEX ix_raw_telegram_messages_message_id ON raw_telegram_messages (message_id);
CREATE INDEX ix_raw_telegram_messages_channel_id ON raw_telegram_messages (channel_id);
CREATE INDEX ix_raw_telegram_messages_received_at ON raw_telegram_messages (received_at);
CREATE INDEX ix_trades_slot_id ON trades (slot_id);
CREATE INDEX ix_trades_status ON trades (status);
CREATE UNIQUE INDEX ix_trades_ticket_id ON trades (ticket_id);
CREATE INDEX ix_system_audit_logs_timestamp ON system_audit_logs (timestamp);
CREATE INDEX ix_system_audit_logs_event_type ON system_audit_logs (event_type);
CREATE INDEX ix_news_interactions_created_at ON news_interactions (created_at);
CREATE INDEX ix_news_interactions_news_id ON news_interactions (news_id);
CREATE INDEX ix_news_interactions_action_type ON news_interactions (action_type);
COMMIT;
