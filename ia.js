const fetch = require("node-fetch");

async function chat() {
  try {
    const response = await fetch("http://localhost:11434/api/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "deepseek-coder",
        prompt: "Hola desde MiniAmigixV",
        stream: false
      }),
    });

    const data = await response.json();

    console.log("\n🤖 RESPUESTA IA:\n");
    console.log(data.response);

  } catch (error) {
    console.error("❌ Error:", error);
  }
prompt: "Hola desde MiniAmigixV",
prompt: "Crea un login en Django con Bootstrap rosa",
}

chat();