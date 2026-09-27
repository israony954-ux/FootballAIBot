import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.prediction_runner import buscar_jogos_futuros, gerar_previsao
from app.multiple_runner import executar_multipla
from app.live_multiple import montar_multipla_jogos
from app.football_api import FootballAPI
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Football AI Bot\n\n"
        "Bot conectado com sucesso!\n"
        "Use /status para testar."
    )

async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Integração Telegram funcionando.")

async def multipla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ Buscando jogos e calculando a múltipla...")

    try:
        futuros = await asyncio.to_thread(buscar_jogos_futuros)

        analises = []
        for jogo in futuros[:4]:
            try:
                analise = await asyncio.to_thread(gerar_previsao, jogo)
                if analise:
                    analises.append(analise)
            except Exception:
                continue

        if not analises:
            await update.message.reply_text("Nenhuma análise disponível no momento.")
            return

        resultado = await asyncio.to_thread(executar_multipla, analises)

        selecoes = resultado.get("selecoes", [])

        if not selecoes:
            await update.message.reply_text(
                "Não foi encontrada uma múltipla dentro dos critérios atuais."
            )
            return

        linhas = ["🎯 MÚLTIPLA GERADA", ""]

        for selecao in selecoes:
            linhas.append(
                f"⚽ {selecao['jogo']}\n"
                f"📌 {selecao['mercado']}\n"
                f"📊 {selecao['probabilidade'] * 100:.1f}%\n"
            )

        linhas.append(
            f"🔥 Probabilidade aproximada: "
            f"{resultado['probabilidade'] * 100:.2f}%"
        )

        await update.message.reply_text("\n".join(linhas))

    except Exception as erro:
        await update.message.reply_text(
            f"❌ Erro ao gerar múltipla: {erro}"
        )

async def ao_vivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔴 Buscando jogos ao vivo e analisando...")

    try:
        api = FootballAPI()
        data = datetime.now().strftime("%Y-%m-%d")
        jogos = await asyncio.to_thread(api.buscar_jogos, data) or []

        status_live = {"1H", "2H", "HT", "ET", "BT", "P", "LIVE"}

        jogos_live = [
            jogo
            for jogo in jogos
            if jogo.get("fixture", {}).get("status", {}).get("short") in status_live
        ]

        if not jogos_live:
            await update.message.reply_text(
                "🔴 Nenhum jogo ao vivo encontrado no momento."
            )
            return

        resultado = await asyncio.to_thread(
            montar_multipla_jogos,
            jogos_live[:10],
            0.70,
            3
        )

        selecoes = resultado.get("selecoes", [])

        if not selecoes:
            await update.message.reply_text(
                f"🔴 {len(jogos_live)} jogo(s) ao vivo encontrado(s), "
                "mas nenhuma seleção atingiu o critério atual."
            )
            return

        linhas = [
            "🔴 MÚLTIPLA AO VIVO",
            f"📡 Jogos ao vivo encontrados: {len(jogos_live)}",
            ""
        ]

        for selecao in selecoes:
            linhas.append(
                f"⚽ {selecao['jogo']}\n"
                f"📌 {selecao['mercado']}\n"
                f"📊 {selecao['probabilidade'] * 100:.1f}%\n"
            )

        linhas.append(
            f"🔥 Probabilidade aproximada: "
            f"{resultado['probabilidade'] * 100:.2f}%"
        )

        await update.message.reply_text("\n".join(linhas))

    except Exception as erro:
        await update.message.reply_text(
            f"❌ Erro ao analisar jogos ao vivo: {erro}"
        )

async def jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Buscando jogos futuros...")

    try:
        futuros = await asyncio.to_thread(buscar_jogos_futuros)

        if not futuros:
            await update.message.reply_text(
                "📅 Nenhum jogo futuro encontrado no momento."
            )
            return

        linhas = [f"📅 JOGOS FUTUROS ({len(futuros)})", ""]

        for jogo in futuros[:10]:
            casa = jogo.get("teams", {}).get("home", {}).get(
                "name", "Casa"
            )
            fora = jogo.get("teams", {}).get("away", {}).get(
                "name", "Fora"
            )

            data_jogo = jogo.get("fixture", {}).get("date", "")
            horario = ""

            if data_jogo:
                try:
                    horario = data_jogo[11:16]
                except Exception:
                    horario = ""

            linhas.append(
                f"⚽ {casa} x {fora}"
                + (f" ⏰ {horario}" if horario else "")
            )

        if len(futuros) > 10:
            linhas.append("")
            linhas.append(f"... e mais {len(futuros) - 10} jogo(s).")

        await update.message.reply_text("\n".join(linhas))

    except Exception as erro:
        await update.message.reply_text(
            f"❌ Erro ao buscar jogos: {erro}"
        )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Football AI Bot está online.")

def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN não configurado.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("multipla", multipla))
    app.add_handler(CommandHandler("ao_vivo", ao_vivo))
    app.add_handler(CommandHandler("jogos", jogos))
    app.add_handler(CommandHandler("teste", teste))

    print("Football AI Bot Telegram iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()
