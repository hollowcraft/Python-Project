chrome.action.onClicked.addListener(async (tab) => {
  if (tab.url) {
    fetch("http://127.0.0.1:5000/save_url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: tab.url })
    })
    .then(res => res.json())
    .then(data => console.log("Sauvegardé :", data))
    .catch(err => console.error("Erreur :", err));
  }
});
