import os
from app import app

if __name__ == '__main__':
    # Configuração para Windows
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    print(f"""
    ╔════════════════════════════════════════╗
    ║         PsychAnalytica Platform        ║
    ╚════════════════════════════════════════╝
    """)
    print(f"💡 Servidor iniciado em: http://localhost:{port}")
    print(f"🔗 Interface de análise psicológica pronta!")
    print(f"*> Pressione Ctrl+C para parar")
    print("""")

    try:
        app.run(host=\"0.0.0.0\", port=port, debug=debug, use_reloader=False)
    except KeyboardInterrupt:
        print(f"\n🔴 Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no servidor: {e}")
        input("Pressione Enter para continuar...")


